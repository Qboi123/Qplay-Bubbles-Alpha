from copy import copy

from typing import Dict, Tuple, Union

from pyglet import resource
from pyglet.sprite import Sprite
from pyglet.text import Label

import sprites
from effects import Effect
from events import EffectStartedEvent, EffectStoppedEvent, EffectUpdateEvent, DrawEvent, UpdateEvent, PauseEvent, \
    UnpauseEvent, AutoSaveEvent
from resources import Resources


class EffectGUI(object):
    def __init__(self, scene):
        self.sprites: Dict[Effect, Tuple[Sprite, Sprite, Label]] = dict()

        self.startX = 128
        self.endX = 1024
        self.stepX = 64

        self.startY = scene.window.height - 40
        self.endY = scene.window.height - 40 - (self.stepX * (self.endX - self.startX))
        self.stepY = -32

        self.currentX = self.startX
        self.currentY = self.startY

        self.fontPaddingX = 32
        self.fontPaddingY = 8

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
        self.sprites[event.appliedEffect][2].text = str(int(event.appliedEffect.timeRemaining))
        self.sprites[event.appliedEffect][2].draw()

    def on_draw(self, event: DrawEvent):
        for sprites in self.sprites.values():
            sprites[0].draw()
            sprites[1].draw()
            sprites[2].draw()


class GameGUI(object):
    def __init__(self, scene):
        self.sprites: Dict[str, Union[Sprite, Label]] = dict()

        self.sprites["BG"] = Sprite(Resources.get_resource("gui", "scoreboard_bg"), 0, scene.window.height-72, batch=scene.batch)

        UpdateEvent.bind(self.on_update)
        DrawEvent.bind(self.on_draw)

    def on_update(self, event: UpdateEvent):
        pass

    def on_draw(self, event: DrawEvent):
        self.sprites["BG"].draw()


class PauseGUI(object):
    def __init__(self, scene):
        self.sprites: Dict[str, Union[Sprite, Label]] = dict()

        self.startX = 64
        self.startY = scene.window.height - 128

        self.endY = 40

        self.currentX = self.startX
        self.currentY = self.startY

        PauseEvent.bind(self.on_pause)
        DrawEvent.bind(self.on_draw)
        UnpauseEvent.bind(self.on_unpause)

    def on_pause(self, event: PauseEvent):
        bg = resource.image("textures/gui/pauseBG.png")
        self.sprites["BG"] = Sprite(bg, 0, 0, batch=event.batch)

        for bubble in sprites.BUBBLES:
            image = Resources.get_resource("bubbles", bubble.get_unlocalized_name(), 40)
            self.sprites[bubble.get_unlocalized_name()+".image"] = Sprite(
                image, self.currentX, self.currentY, batch=event.batch)
            self.sprites[bubble.get_unlocalized_name()+".label"] = Label(
                Resources.get_localized_name(f"bubble.{bubble.get_unlocalized_name()}.name"),
                "Arial", 15, color=(255, 255, 255, 255), x=self.currentX + 30, y=self.currentY - 7.5)
            self.currentY -= 48
            if self.currentY <= self.endY:
                self.currentY = self.startY
                self.currentX += 256
        AutoSaveEvent(1, event.scene)

    def on_draw(self, event: DrawEvent):
        for sprite in self.sprites.values():
            sprite.draw()

    def on_unpause(self, event: UnpauseEvent):
        for key, value in self.sprites.copy().items():
            value.delete()
            del self.sprites[key]

        self.currentX = self.startX
        self.currentY = self.startY
