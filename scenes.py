from collections import deque
from typing import List, Any, Union

import pyglet
from pyglet.gl import *
from pyglet.media import Player as MediaPlayer
from pyglet.window import key

from map import Map
from sprites.objects import PhysicalObject
from sprites.player import Player


class AudioEngine:
    """A high level audio engine for easily playing SFX and Music."""

    def __init__(self, channels=5):
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


class Scene:
    """A base class for all Scenes to inherit from.

    All Scenes must contain an `update` method. In addition,
    you can also define event handlers for any of the events
    dispatched by the `Window`. Any Scene methods that match
    the Window event names will be automatically set when
    changing to the Scene.
    """

    scene_manager = None  # This is assigned when adding the Scene
    audio = AudioEngine()  # All Scenes share the same AudioEngine

    def update(self, dt):
        raise NotImplementedError


# noinspection PyUnusedFunction
class GameScene(Scene):
    def __init__(self, window):
        Scene.__init__(self)
        self.window: pyglet.window.Window = window
        self.batch: pyglet.graphics.Batch = pyglet.graphics.Batch()
        self.game_objects: Union[Any, PhysicalObject] = list()
        self.player: Player = Player((self.window.height / 2, self.window.width / 2), self.window, self.batch)
        self.game_objects.append(self.player)
        self.map: Map = Map()

        # Define local player variables
        self.player_rot_strafe = 0
        self.player_mpx_strafe = 0

    def on_draw(self):
        try:
            self.window.clear()
            self.batch.draw()
            self.player.draw()
            self.map.draw()
        except Exception as e:
            print("%s: %s" % (str(e.__repr__()), str(e.args[0])))

    def on_key_press(self, symbol, modifiers):
        if symbol == key.LEFT:
            self.player_rot_strafe -= 5
        if symbol == key.RIGHT:
            self.player_rot_strafe += 5

        if symbol == key.DOWN:
            self.player_mpx_strafe += 10
        if symbol == key.UP:
            self.player_mpx_strafe -= 10

    def on_key_release(self, symbol, modifiers):
        if symbol == key.LEFT:
            self.player_rot_strafe += 5
        if symbol == key.RIGHT:
            self.player_rot_strafe -= 5

        if symbol == key.DOWN:
            self.player_mpx_strafe -= 10
        if symbol == key.UP:
            self.player_mpx_strafe += 10

    def update(self, dt):
        # To avoid handling collisions twice, we employ nested loops of ranges.
        # This method also avoids the problem of colliding an object with itself.
        for i in range(len(self.game_objects)):
            for j in range(i + 1, len(self.game_objects)):

                obj_1 = self.game_objects[i]
                obj_2 = self.game_objects[j]

                # Make sure the objects haven't already been killed
                if not obj_1.dead and not obj_2.dead:
                    if obj_1.collides_with(obj_2):
                        obj_1.handle_collision_with(obj_2)
                        obj_2.handle_collision_with(obj_1)

        if self.player_rot_strafe:
            self.player.rotate(self.player_rot_strafe)
            # self.player_rot_strafe = 0

        if self.player_mpx_strafe:
            self.player.move_pixels(dt, self.player_mpx_strafe)
            # self.player_mpx_strafe = 0
        self.player.update(dt)
        self.map.update(dt, self.window, self.batch, self.game_objects)

    def tick_update(self, dt):
        self.map.tick_update(dt, self.window, self.batch, self.game_objects)

    def auto_save_update(self, dt):
        self.save.save_save(self.map, self.player)
