import random
from time import time

from events import EffectUpdateEvent, UpdateEvent, TickUpdateEvent, EffectStoppedEvent, EffectStartedEvent, \
    PlayerCollisionEvent, EffectTickUpdateEvent, ScoreEvent


# noinspection PyUnusedFunction


# noinspection PyUnusedClass,PyUnusedFunction,PyPep8Naming
class AppliedEffect(object):
    def __init__(self, time_length, scene, strength_multiply=1, incompatibles=[]):
        activeTypes = [type(i) for i in scene.player.activeEffects]

        for incompatible in incompatibles:
            if incompatible in activeTypes:
                self.dead = True
                return

        self.stopTime = time() + time_length
        self.strengthMultiply = strength_multiply
        self.dead = False

        print(self.strengthMultiply)

        PlayerCollisionEvent.bind(self.player_collision)
        UpdateEvent.bind(self.update)
        TickUpdateEvent.bind(self.tick_update)

        self.on_effect_started(scene)
        EffectStartedEvent(self, scene)

    def __repr__(self):
        return f'[{self.__class__.__name__}: {round(self.timeRemaining, 1)}]'

    def tick_update(self, event: TickUpdateEvent):
        self.on_tick_update(event)
        EffectTickUpdateEvent(event.dt, self, event.scene)

    def update(self, event: UpdateEvent):
        # self.on_update(event.dt, event.window, event.batch, event.player)
        self.on_update(event)
        EffectUpdateEvent(event.dt, self, event.scene)
        if self.timeRemaining <= 0:
            self.timeRemaining = 0
            if not self.dead:
                self.on_effect_stopped(event.scene)
                EffectStoppedEvent(self, event.scene)
            self.dead = True
        if self.dead:
            PlayerCollisionEvent.unbind(self.player_collision)
            UpdateEvent.unbind(self.update)
            TickUpdateEvent.unbind(self.tick_update)

    def player_collision(self, event: PlayerCollisionEvent):
        self.on_player_collision(event)

    @property
    def timeRemaining(self):
        return self._get_time_remaining()

    @timeRemaining.setter
    def timeRemaining(self, value):
        self._set_time_remaining(value)

    def on_update(self, event: UpdateEvent):
        pass

    def on_tick_update(self, event: TickUpdateEvent):
        pass  # self.baseEffectClass.on_tick_update(dt, window, batch, player)

    def on_effect_started(self, scene):
        pass

    def on_effect_stopped(self, scene):
        pass

    def on_player_collision(self, event: PlayerCollisionEvent):
        print(f"Collision with {event.otherObject.__class__.__name__ if type(event.otherObject) is not type else event.otherObject.__name__}")
        # pass  # self.baseEffectClass.on_player_collision(window, batch, player, obj)

    def _get_time_remaining(self):
        return self.stopTime - time()

    def _set_time_remaining(self, remaining):
        self.stopTime = time() + remaining


class TeleportingEffect(AppliedEffect):
    def __init__(self, time_length, scene, strength_multiply=1):
        super(TeleportingEffect, self).__init__(time_length, scene, strength_multiply, incompatibles=[TeleportingEffect, ParalisEffect])
        if not self.dead:
            self.teleportInterval = 1 / self.strengthMultiply
            self._time = time()
            # UpdateEvent.bind(self.on_update)

    def on_update(self, event: UpdateEvent):
        if self._time <= time():
            event.player.move_to(random.randint(0, event.window.width), random.randint(0, event.window.height))
            self._time = time() + self.teleportInterval
            EffectUpdateEvent(self.teleportInterval, self, event.scene)


class SpeedBoostEffect(AppliedEffect):
    def __init__(self, time_length, scene, strength_multiply=1):
        if scene.player.motionSpeedMultiply < 2:
            super(SpeedBoostEffect, self).__init__(time_length, scene, strength_multiply, incompatibles=[SlownessEffect, ParalisEffect])
        else:
            self.dead = True

    def on_effect_started(self, scene):
        scene.player.motionSpeedMultiply += (0.5 * self.strengthMultiply)

    def on_effect_stopped(self, scene):
        scene.player.motionSpeedMultiply -= (0.5 * self.strengthMultiply)


class SlownessEffect(AppliedEffect):
    def __init__(self, time_length, scene, strength_multiply=1):
        if scene.player.motionSpeedMultiply - (0.5 * strength_multiply) >= 0:
            super(SlownessEffect, self).__init__(time_length, scene, strength_multiply, incompatibles=[SpeedBoostEffect, ParalisEffect])
        else:
            self.dead = True

    def on_effect_started(self, scene):
        scene.player.motionSpeedMultiply -= (0.5 * self.strengthMultiply)

    def on_effect_stopped(self, scene):
        scene.player.motionSpeedMultiply += (0.5 * self.strengthMultiply)


class ParalisEffect(AppliedEffect):
    def __init__(self, time_length, scene, strength_multiply=1):
        if scene.player.motionSpeedMultiply - (0.5 * strength_multiply) >= 0:
            self.oldMotion = scene.player.motionSpeedMultiply
            self.oldRotation = scene.player.rotationSpeedMultiply
            super(ParalisEffect, self).__init__(time_length, scene, strength_multiply,
                                                incompatibles=[SpeedBoostEffect, SlownessEffect, ParalisEffect, TeleportingEffect])
        else:
            self.dead = True

    def on_effect_started(self, scene):
        scene.player.motionSpeedMultiply = 0
        scene.player.rotationSpeedMultiply = 0

    def on_effect_stopped(self, scene):
        scene.player.motionSpeedMultiply = self.oldMotion
        scene.player.rotationSpeedMultiply = self.oldRotation


class ScoreStatusEffect(AppliedEffect):
    def __init__(self, time_length, scene, strength_multiply=1):
        if scene.player.motionSpeedMultiply - (0.5 * strength_multiply) >= 0:
            super(ScoreStatusEffect, self).__init__(time_length, scene, strength_multiply)
            ScoreEvent.bind(self.on_score, True)
        else:
            self.dead = True

    def on_score(self, event: ScoreEvent):
        event.add_score(event.score * self.strengthMultiply)

    def on_effect_stopped(self, scene):
        ScoreEvent.unbind(self.on_score)


class GhostEffect(AppliedEffect):
    def __init__(self, time_length, scene, strength_multiply=1):
        if scene.player.motionSpeedMultiply - (0.5 * strength_multiply) >= 0:
            super(GhostEffect, self).__init__(time_length, scene, strength_multiply)
        else:
            self.dead = True

    def on_effect_started(self, scene):
        scene.player.ghostMode = True

    def on_effect_stopped(self, scene):
        scene.player.ghostMode = False


class ConfusionEffect(AppliedEffect):
    def __init__(self, time_length, scene, strength_multiply=1):
        self.old = scene.motionKeys.copy()
        if scene.player.motionSpeedMultiply - (0.5 * strength_multiply) >= 0:
            super(ConfusionEffect, self).__init__(time_length, scene, strength_multiply)
        else:
            self.dead = True

    def on_effect_started(self, scene):
        random.shuffle(scene.motionKeys)

    def on_effect_stopped(self, scene):
        scene.motionKeys = self.old
