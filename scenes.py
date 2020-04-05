from random import Random
from collections import deque
from typing import List, Any, Union, Optional

import pyglet
from pyglet.gl import *
from pyglet.media import Player as MediaPlayer
from pyglet.text import Label
from pyglet.window import key

from bubble import BubbleObject
from events import CollisionEvent, UpdateEvent, DrawEvent, TickUpdateEvent, PlayerCollisionEvent, AutoSaveEvent, \
    PauseEvent, UnpauseEvent, ResizeEvent
from graphics.projection import WindowViewport, OrthographicProjection
from gui import EffectGUI, GameGUI, PauseGUI
from map import Map
from objects import Collidable
from resources import Resources
from sprites.entity import Entity
from sprites.player import Player
from utils import ROTATION_SPEED, MOTION_SPEED


class AudioEngine:
    """A high level audio engine for easily playing SFX and Music."""

    # noinspection PySameParameterValue
    def __init__(self, channels=16):
        self.sfx_players = deque([MediaPlayer() for _ in range(channels)], maxlen=channels)
        self.music_player = MediaPlayer()

    def set_volume(self, percentage):
        """Set the audio volume, as a percentage of 1 to 100.

        :param percentage: int: The volume, as a percentage.
        """
        volume = max(min(1, percentage / 100), 0)
        for player in self.sfx_players:
            player.volume = volume
        self.music_player.volume = volume

    # noinspection PyArgumentList
    def play(self, source, position=(0, 0, 0)):
        """Play a sound effect on the next available channel

        :param source: A pyglet audio Source
        :param position: Optional spacial position for the sound.
        """
        player = self.sfx_players[0]
        player.position = position
        player.queue(source=source)
        if not player.playing:
            player.play()
        else:
            player.next_source()
        self.sfx_players.rotate()

    def play_music(self, source):
        """Play a music track, or switch to a new one.

        :param source: A pyglet audio Source
        """
        self.music_player.queue(source=source)
        if not self.music_player.playing:
            self.music_player.play()
        else:
            self.music_player.next_source()


# noinspection PyUnusedName
class Scene:
    """A base class for all Scenes to inherit from.

    All Scenes must contain an `update` method. In addition,
    you can also define event handlers for any of the events
    dispatched by the `Window`. Any Scene methods that match
    the Window event names will be automatically set when
    changing to the Scene.
    """

    scene_manager = None  # This is assigned when adding the Scene
    audio = AudioEngine(32)  # All Scenes share the same AudioEngine

    def update(self, dt):
        raise NotImplementedError

    def init_scene(self):
        pass


# noinspection PyUnusedFunction
class GameScene(Scene):
    def __init__(self, window):
        Scene.__init__(self)

        self.pauseMode = False
        self.window: pyglet.window.Window = window
        self.backgroundBatch: pyglet.graphics.Batch = pyglet.graphics.Batch()
        self.batch: pyglet.graphics.Batch = pyglet.graphics.Batch()
        self.playerBatch: pyglet.graphics.Batch = pyglet.graphics.Batch()
        self.guiBatch: pyglet.graphics.Batch = pyglet.graphics.Batch()
        self.foregroundBatch: pyglet.graphics.Batch = pyglet.graphics.Batch()

        self.viewport: WindowViewport = WindowViewport(self.window)
        self.projection: OrthographicProjection = OrthographicProjection(self.viewport)

        self.player: Optional[Player] = None
        self.game_objects: List[Union[Any, Collidable]] = list()
        self.map: Optional[Map] = None
        self.fps: Optional[Label] = None

        self.gameGUI: Optional[GameGUI] = None
        self.effectGUI: Optional[EffectGUI] = None
        self.pauseGUI: Optional[PauseGUI] = None

        self.random = Random(4096)

        self.motionKeys = [key.LEFT, key.RIGHT, key.DOWN, key.UP]

        self.fps_text: Optional[str] = None

        # Define local player variables
        self.player_rot_strafe = 0
        self.player_mpx_strafe = 0

        self.backgroundColor = (0.1, 0.5, 0.55, 1)

        self.oldWidth = window.width
        self.oldHeight = window.height

        self.windowSize = self.window.get_size()

    def on_resize(self, width, height):
        self.windowSize = (width, height)
        self.projection.apply()
        ResizeEvent(width, height, self.oldWidth, self.oldHeight, self)
        self.oldWidth = width
        self.oldHeight = height
        # print('The window was resized to %dx%d' % (width, height))

    def reset_strafe(self):
        # Define local player variables
        self.player_rot_strafe = 0
        self.player_mpx_strafe = 0

    def init_scene(self):
        self.gameGUI = GameGUI(self)
        self.effectGUI = EffectGUI(self)
        self.pauseGUI = PauseGUI(self)

        self.player: Player = Player((self.window.height / 2, self.window.width / 2), self)
        self.game_objects.append(self.player)
        self.map: Map = Map()
        self.fps: Label = Label("0 FPS", "helverica", 14, False, True, x=self.window.width, y=self.window.height,
                                width=self.window.width, anchor_x="right", anchor_y="top", align="right",
                                multiline=False, batch=self.batch, color=(255, 255, 255, 127))

        if not self.scene_manager.save.load_save(self):
            self.random = Random(4096)
            self.map.init_bubbles(self)
        self.player.refresh()
        self.fps_text = "FPS: 0"

    def pause(self):
        PauseEvent(self)
        self.pauseMode = True

    def unpause(self):
        UnpauseEvent(self)
        self.pauseMode = False

    def on_draw(self):
        try:
            glClearColor(*self.backgroundColor)
            # glClearColor(0.25, 0.25, 0.25, 1)
            self.window.clear()
            self.backgroundBatch.draw()
            DrawEvent(self)
            self.batch.draw()
            self.playerBatch.draw()
            self.guiBatch.draw()
            self.foregroundBatch.draw()
            self.fps.draw()
        except Exception as e:
            tb = e.__traceback__
            if tb.tb_next:
                new_tb = tb.tb_next
                while new_tb:
                    tb = new_tb
                    new_tb = tb.tb_next
            print("Line %s | File %s - %s: %s" % (
                tb.tb_lineno, tb.tb_frame.f_code.co_filename, str(e.__class__.__name__), str(e.args[0])))

    # noinspection PyUnusedLocal
    def safe_change_key(self, old, new, rot_strafe, mot_strafe):
        self.on_key_release(old, [])
        self.on_key_press(new, [])
        # if old == key.LEFT and rot_strafe == -ROTATION_SPEED:
        #     self.on_key_release(old, [])
        #     self.on_key_press(new, [])
        #     # if old == key.LEFT:
        #     #     pass
        #     # elif old == key.RIGHT:
        #     #     self.player_rot_strafe += ROTATION_SPEED * 2
        #     # elif old == key.UP:
        #     #     self.player_rot_strafe += ROTATION_SPEED
        #     #     self.player_mpx_strafe -= MOTION_SPEED
        #     # elif old == key.DOWN:
        #     #     self.player_rot_strafe += ROTATION_SPEED
        #     #     self.player_mpx_strafe += MOTION_SPEED
        # elif old == key.RIGHT and rot_strafe == ROTATION_SPEED:
        #     self.on_key_release(old, [])
        #     self.on_key_press(new, [])
        #
        #     # if old == key.LEFT:
        #     #     self.player_rot_strafe -= ROTATION_SPEED * 2
        #     # elif old == key.RIGHT:
        #     #     pass
        #     # elif old == key.UP:
        #     #     self.player_rot_strafe -= ROTATION_SPEED
        #     #     self.player_mpx_strafe -= MOTION_SPEED
        #     # elif old == key.DOWN:
        #     #     self.player_rot_strafe -= ROTATION_SPEED
        #     #     self.player_mpx_strafe += MOTION_SPEED
        # elif old == key.UP and mot_strafe == -MOTION_SPEED:
        #     self.on_key_release(old, [])
        #     self.on_key_press(new, [])
        #     # if old == key.LEFT:
        #     #     self.player_mpx_strafe += MOTION_SPEED
        #     #     self.player_rot_strafe -= ROTATION_SPEED
        #     # elif old == key.RIGHT:
        #     #     self.player_mpx_strafe += MOTION_SPEED
        #     #     self.player_rot_strafe += ROTATION_SPEED
        #     # elif old == key.UP:
        #     #     pass
        #     # elif old == key.DOWN:
        #     #     self.player_mpx_strafe += MOTION_SPEED * 2
        # elif old == key.DOWN and mot_strafe == MOTION_SPEED:
        #     self.on_key_release(old, [])
        #     self.on_key_press(new, [])
        #     # if old == key.LEFT:
        #     #     self.player_mpx_strafe -= MOTION_SPEED
        #     #     self.player_rot_strafe -= ROTATION_SPEED
        #     # elif old == key.RIGHT:
        #     #     self.player_mpx_strafe -= MOTION_SPEED
        #     #     self.player_rot_strafe += ROTATION_SPEED
        #     # elif old == key.UP:
        #     #     self.player_mpx_strafe -= MOTION_SPEED * 2
        #     # elif old == key.DOWN:
        #     #     pass

    # noinspection PyUnusedLocal
    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            if self.pauseMode:
                self.unpause()
            else:
                self.pause()
            return pyglet.event.EVENT_HANDLED
        if not self.pauseMode:
            if symbol == self.motionKeys[0]:
                self.player_rot_strafe -= ROTATION_SPEED
            if symbol == self.motionKeys[1]:
                self.player_rot_strafe += ROTATION_SPEED
            if symbol == self.motionKeys[2]:
                self.player_mpx_strafe += MOTION_SPEED
            if symbol == self.motionKeys[3]:
                self.player_mpx_strafe -= MOTION_SPEED

    # noinspection PyUnusedLocal
    def on_key_release(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            return pyglet.event.EVENT_HANDLED
        if not self.pauseMode:
            if symbol == self.motionKeys[0]:
                self.player_rot_strafe += ROTATION_SPEED
            if symbol == self.motionKeys[1]:
                self.player_rot_strafe -= ROTATION_SPEED

            if symbol == self.motionKeys[2]:
                self.player_mpx_strafe -= MOTION_SPEED
            if symbol == self.motionKeys[3]:
                self.player_mpx_strafe += MOTION_SPEED

    def update(self, dt):
        # To avoid handling collisions twice, we employ nested loops of ranges.
        # This method also avoids the problem of colliding an object with itself.
        # print("Update")
        if self.pauseMode:
            return
        for i in range(len(self.game_objects)):
            for j in range(i + 1, len(self.game_objects)):

                obj_1 = self.game_objects[i]
                obj_2 = self.game_objects[j]

                # Make sure the objects haven't already been killed
                if (not obj_1.dead) and (not obj_2.dead):
                    if obj_1.collides_with(obj_2):
                        CollisionEvent(obj_1, obj_2, self)
                        if isinstance(obj_1, Player):
                            PlayerCollisionEvent(obj_1, obj_2, self)
                        CollisionEvent(obj_2, obj_1, self)
                        self.fps_text = "FPS: %s" % round(1 / dt, 1)
                        if hasattr(obj_1, "sprite") and hasattr(obj_2, "sprite"):
                            if isinstance(obj_1.sprite, Entity) and isinstance(obj_2.sprite, Entity):
                                if isinstance(obj_1, BubbleObject) and isinstance(obj_2, BubbleObject):
                                    continue
                                obj_2.sprite.damage(obj_1.sprite.attackMultiplier)
                                obj_1.sprite.damage(obj_2.sprite.attackMultiplier)

        if self.player_rot_strafe:
            self.player.rotate(dt, self.player_rot_strafe)

        if self.player_mpx_strafe:
            self.player.move_pixels(dt, self.player_mpx_strafe)

        UpdateEvent(dt, self)

    def tick_update(self, dt):
        # self.map.tick_update(dt, self.window, self.batch, self.game_objects)
        self.fps.text = self.fps_text
        if self.pauseMode:
            return
        TickUpdateEvent(dt, self)

    # noinspection PyUnusedLocal
    def auto_save_update(self, dt):
        if self.pauseMode or self.player.dead:
            return
        AutoSaveEvent(dt, self)


# noinspection PyUnusedClass,PySameParameterValue
class LoadingScene(Scene, Resources):
    # event = Event()
    def __init__(self, window):
        self.window = window
        super(LoadingScene, self).__init__()

    def update(self, dt):
        if self.loaded:
            self.scene_manager.change_scene("GameScene")


class MapSelectionScene(Scene):
    def __init__(self, window):
        from glooey.scrolling import ScrollPane
        self.window = window
        super(MapSelectionScene, self).__init__()

        self.scrollregion = ScrollPane()
        self.scrollregion.set_horz_scrolling(True)
        self.scrollregion.set_view()

    def on_draw(self):
        self.scrollregion.do_draw()

    def update(self, dt):
        pass
