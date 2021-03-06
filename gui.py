from copy import copy

from typing import Dict, Tuple, Union

from pyglet import resource
from pyglet.sprite import Sprite
from pyglet.text import Label

import sprites
from effects import Effect
from events import EffectStartedEvent, EffectStoppedEvent, EffectUpdateEvent, DrawEvent, UpdateEvent, PauseEvent, \
    UnpauseEvent, AutoSaveEvent, ResizeEvent
from resources import Resources
from utils.advBuiltins import AdvInteger, AdvTuple


class EffectGUI(object):
    def __init__(self, scene):
        self.sprites: Dict[Effect, Tuple[Sprite, Sprite, Label]] = dict()

        self.startX = AdvInteger(128)
        self.endX = AdvInteger(1024)
        self.stepX = AdvInteger(64)

        self.startY = AdvInteger(scene.window.height - 40)
        self.endY = AdvInteger(scene.window.height - 40 - (self.stepX * (self.endX - self.startX)))
        self.stepY = AdvInteger(-32)

        self.currentX = self.startX
        self.currentY = self.startY

        self.fontPaddingX = AdvInteger(32)
        self.fontPaddingY = AdvInteger(8)

        EffectStartedEvent.bind(self.on_effect_started)
        EffectStoppedEvent.bind(self.on_effect_stopped)
        EffectUpdateEvent.bind(self.on_effect_update)
        DrawEvent.bind(self.on_draw)

    def on_effect_started(self, event: EffectStartedEvent):
        self.sprites[event.appliedEffect] = (Sprite(resource.image("textures/gui/effectBanner.png"),
                                                    self.currentX, self.currentY, batch=event.batch),
                                             Sprite(event.appliedEffect.icon,
                                                    self.currentX, self.currentY, batch=event.batch),
                                             Label(str(int(event.appliedEffect.timeRemaining)),
                                                   "Arial", 16, False, False, (255, 255, 255, 127),
                                                   self.currentX+self.fontPaddingX, self.currentY+self.fontPaddingY,
                                                   batch=event.batch))

        self.currentX += self.stepX
        if self.currentX >= self.endX:
            self.currentX = self.startX
            self.currentY += self.stepY

    def on_effect_stopped(self, event: EffectStoppedEvent):
        sprites = self.sprites.pop(event.appliedEffect)
        sprites[0].delete()
        sprites[1].delete()
        sprites[2].delete()
        for sprites in self.sprites.values():
            sprites[0].x -= self.stepX
            sprites[1].x -= self.stepX
            sprites[2].x -= self.stepX
            if sprites[0].x < self.startX:
                if not sprites[0].y == self.startY:
                    sprites[0].x = self.endX - self.stepX
                    sprites[0].y -= self.stepY

                    sprites[1].x = self.endX - self.stepX
                    sprites[1].y -= self.stepY

                    sprites[2].x = (self.endX - self.stepX) + self.fontPaddingX
                    sprites[2].y -= self.stepY
        self.currentX -= self.stepX
        if self.currentX < self.startX:
            if not self.currentY == self.startY:
                self.currentX = self.endX - self.stepX
                self.currentY -= self.stepY

    def on_effect_update(self, event: EffectUpdateEvent):
        try:
            self.sprites[event.appliedEffect][2].text = AdvInteger(int(event.appliedEffect.timeRemaining)).to_string()
            self.sprites[event.appliedEffect][2].draw()
        except KeyError:
            pass

    def on_draw(self, event: DrawEvent):
        for sprites in self.sprites.values():
            sprites[0].draw()
            sprites[1].draw()
            sprites[2].draw()


class GameGUI(object):
    def __init__(self, scene):
        self.sprites: Dict[str, Union[Sprite, Label]] = dict()

        self.sprites["BG"] = Sprite(Resources.get_resource("gui", "scoreboard_bg"), 0, scene.window.height-72, batch=scene.batch)
        self.sprites["BG"].scale_x = scene.window.width

        UpdateEvent.bind(self.on_update)
        DrawEvent.bind(self.on_draw)
        ResizeEvent.bind(self.on_resize)

    def on_resize(self, event: ResizeEvent):
        self.sprites["BG"].y = AdvInteger(event.height-72)

    def on_update(self, event: UpdateEvent):
        pass

    def on_draw(self, event: DrawEvent):
        self.sprites["BG"].draw()


class PauseGUI(object):
    def __init__(self, scene):
        self.sprites: Dict[str, Union[Sprite, Label]] = dict()

        self.startX = AdvInteger(64)
        self.startY = AdvInteger(scene.window.height - 128)

        self.endY = AdvInteger(40)

        self.currentX = self.startX
        self.currentY = self.startY

        PauseEvent.bind(self.on_pause)
        UnpauseEvent.bind(self.on_unpause)
        ResizeEvent.bind(self.on_resize)

    def on_pause(self, event: PauseEvent):
        self.oldBgColor = event.scene.backgroundColor
        event.scene.backgroundColor = AdvTuple((0.05, 0.25, 0.275, 1.0))

        bg = resource.image("textures/gui/pauseBG.png")
        self.sprites["BG"] = Sprite(bg, 0, 0, batch=event.scene.guiBatch)
        self.sprites["BG"].scale_x = AdvInteger(event.window.width)
        self.sprites["BG"].scale_y = AdvInteger(event.window.height-72)

        for bubble in sprites.BUBBLES:
            if not bubble.hideInPause:
                image = Resources.get_resource("bubbles", bubble.get_unlocalized_name(), 40)
                self.sprites[bubble.get_unlocalized_name()+".image"] = Sprite(
                    image, self.currentX, self.currentY, batch=event.scene.foregroundBatch)
                self.sprites[bubble.get_unlocalized_name()+".label"] = Label(
                    Resources.get_localized_name(f"bubble.{bubble.get_unlocalized_name()}.name"),
                    "Arial", 15, color=(255, 255, 255, 255), x=self.currentX + 30, y=self.currentY - 7.5, batch=event.scene.foregroundBatch)
                self.currentY -= 48
                if self.currentY <= self.endY:
                    self.currentY = self.startY
                    self.currentX += AdvInteger(256)
        AutoSaveEvent(1, event.scene)

    def on_resize(self, event: ResizeEvent):
        if not event.scene.pauseMode:
            return
        event.scene.backgroundColor = self.oldBgColor
        event.window.clear()

        for key, value in self.sprites.copy().items():
            value.delete()
            del self.sprites[key]

        self.currentX = self.startX
        self.currentY = self.startY

        self.startY = AdvInteger(event.height - 128)

        self.oldBgColor = event.scene.backgroundColor
        event.scene.backgroundColor = AdvTuple((0.05, 0.25, 0.275, 1.0))

        bg = resource.image("textures/gui/pauseBG.png")
        self.sprites["BG"] = Sprite(bg, 0, 0, batch=event.scene.guiBatch)
        self.sprites["BG"].scale_x = AdvInteger(event.width)
        self.sprites["BG"].scale_y = AdvInteger(event.height-72)

        for bubble in sprites.BUBBLES:
            if not bubble.hideInPause:
                image = Resources.get_resource("bubbles", bubble.get_unlocalized_name(), 40)
                self.sprites[bubble.get_unlocalized_name()+".image"] = Sprite(
                    image, self.currentX, self.currentY, batch=event.scene.foregroundBatch)
                self.sprites[bubble.get_unlocalized_name()+".label"] = Label(
                    Resources.get_localized_name(f"bubble.{bubble.get_unlocalized_name()}.name"),
                    "Arial", 15, color=(255, 255, 255, 255), x=self.currentX + 30, y=self.currentY - 7.5, batch=event.scene.foregroundBatch)
                self.currentY -= 48
                if self.currentY <= self.endY:
                    self.currentY = self.startY
                    self.currentX += AdvInteger(256)
        # AutoSaveEvent(1, event.scene)

    def on_unpause(self, event: UnpauseEvent):
        event.scene.backgroundColor = self.oldBgColor
        for key, value in self.sprites.copy().items():
            value.delete()
            del self.sprites[key]

        self.currentX = self.startX
        self.currentY = self.startY
