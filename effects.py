import random
from time import time


# noinspection PyUnusedFunction
from typing import Optional

from pyglet.graphics import Batch
from pyglet.window import Window

from events import EffectUpdateEvent, UpdateEvent, TickUpdateEvent, EffectStoppedEvent, EffectStartedEvent, \
    CollisionEvent, PlayerCollisionEvent
from sprites.player import Player


# noinspection PyUnusedClass,PyUnusedFunction,PyPep8Naming
class AppliedEffect(object):
    def __init__(self, time_length, scene, strength_multiply=1):
        self.stopTime = time() + time_length
        self.strengthMultiply = strength_multiply
        self.dead = False

        PlayerCollisionEvent.bind(self.on_player_collision)
        UpdateEvent.bind(self.on_update)
        TickUpdateEvent.bind(self.on_tick_update)

        self.on_effect_started(scene)

    def __repr__(self):
        return f'[{self.__class__.__name__}: {round(self.timeRemaining, 1)}]'

    def update(self, event: UpdateEvent):
        # self.on_update(event.dt, event.window, event.batch, event.player)
        if self.timeRemaining <= 0:
            self.timeRemaining = 0
            self.dead = True
            self.on_effect_stopped(event.scene)

    @property
    def timeRemaining(self):
        return self._get_time_remaining()

    @timeRemaining.setter
    def timeRemaining(self, value):
        self._set_time_remaining(value)

    def on_update(self, event: UpdateEvent):
        self.update(event)
        EffectUpdateEvent(event.dt, self, event.scene)

    def on_tick_update(self, event: TickUpdateEvent):
        pass  # self.baseEffectClass.on_tick_update(dt, window, batch, player)

    def on_effect_started(self, scene):
        EffectStartedEvent(self, scene)

    def on_effect_stopped(self, scene):
        EffectStoppedEvent(self, scene)

    def on_player_collision(self, window: Window, batch: Batch, player: Player, obj):
        print(f"Collision with {obj.__class__.__name__ if type(obj) is not type else obj.__name__}")
        # pass  # self.baseEffectClass.on_player_collision(window, batch, player, obj)

    def _get_time_remaining(self):
        return self.stopTime - time()

    def _set_time_remaining(self, remaining):
        self.stopTime = time() + remaining


class TeleportingEffect(AppliedEffect):
    def __init__(self, time_length, scene, strength_multiply=1):
        super(TeleportingEffect, self).__init__(time_length, scene, strength_multiply)
        self.teleportInterval = 1 / self.strengthMultiply
        self._time = time()
        UpdateEvent.bind(self.on_update)

    def on_update(self, event: UpdateEvent):
        if self._time <= time():
            event.player.move_to(random.randint(0, event.window.width), random.randint(0, event.window.height))
            self._time = time() + self.teleportInterval
            EffectUpdateEvent(self.teleportInterval, self, event.scene)


class SpeedBoostEffect(AppliedEffect):
    def __init__(self, time_length, scene, strength_multiply=1):
        if scene.player.motionSpeedMultiply < 2:
            super(SpeedBoostEffect, self).__init__(time_length, scene, strength_multiply)
        else:
            self.dead = True

    def on_effect_started(self, scene):
        super(SpeedBoostEffect, self).on_effect_started(scene)
        scene.player.motionSpeedMultiply += (0.5 * self.strengthMultiply)

    def on_effect_stopped(self, scene):
        super(SpeedBoostEffect, self).on_effect_stopped(scene)
        scene.player.motionSpeedMultiply -= (0.5 * self.strengthMultiply)
