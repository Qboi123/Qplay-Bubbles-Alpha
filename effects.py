from time import time


# noinspection PyUnusedFunction
from pyglet.graphics import Batch
from pyglet.window import Window

from sprites.player import Player


# noinspection PyUnusedClass,PyUnusedFunction
class Effect(object):
    def __init__(self, base_class, time_length):
        self.baseEffectClass = base_class
        self.stopTime = time() + time_length
        self.timeRemaining = property(self._get_time_remaining, self._set_time_remaining)
        self.dead = False

    def update(self, dt, window: Window, batch: Batch, player: Player):
        self.on_update(dt, window, batch, player)
        if self.timeRemaining <= 0:
            self.timeRemaining = 0
            self.dead = True
            self.on_effect_stopped(window, batch, player)

    def tick_update(self, dt, window: Window, batch: Batch, player: Player):
        self.on_tick_update(dt, window, batch, player)

    def on_update(self, dt, window: Window, batch: Batch, player: Player):
        pass

    def on_tick_update(self, dt, window: Window, batch: Batch, player: Player):
        pass

    def on_effect_stopped(self, window: Window, batch: Batch, player: Player):
        pass

    def on_player_collision(self, window: Window, batch: Batch, player: Player, obj):
        pass

    def _get_time_remaining(self):
        return self.stopTime - time()

    def _set_time_remaining(self, remaining):
        self.stopTime = time() + remaining
