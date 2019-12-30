import json
import math
import random
import time
import pyglet

from collections import deque

from pyglet.gl import *
from pyglet.media import Player as MediaPlayer
from pyglet.window import key, mouse, Window
from pyglet.sprite import Sprite
from pyglet.graphics import OrderedGroup


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


class GameScene(Scene):
    def __init__(self, window):
        Scene.__init__(self)
        self.window = window

    def on_draw(self):
        self.window.clear()

    def update(self, dt):
        pass

    def tick_update(self, dt):
        pass
