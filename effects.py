import random
from copy import copy
from time import time
from typing import Optional, Callable, List, Type

from pyglet import resource

import globals as g
from events import EffectUpdateEvent, UpdateEvent, TickUpdateEvent, EffectStoppedEvent, EffectStartedEvent, \
    PlayerCollisionEvent, EffectTickUpdateEvent, ScoreEvent, PauseEvent, UnpauseEvent
from exceptions import UnlocalizedNameError
# noinspection PyPep8Naming
from resources import Resources
from typinglib import Boolean, Object, Float
from utils import ROTATION_SPEED, MOTION_SPEED


# noinspection PyPep8Naming,PyUnusedLocal
class AppliedEffect(object):
    def __init__(self, base_class, time_length, scene, strength_multiply=1, dead=False):
        activeTypes: List[Type[Effect]] = [type(i.baseEffectClass) for i in scene.player.activeEffects]

        if base_class.isBadEffect:
            if ProtectionEffect not in base_class.incompatibles:
                base_class.incompatibles.append(ProtectionEffect)

        for incompatible in base_class.incompatibles:
            if incompatible in activeTypes:
                self.dead = True
                return

        self.dead: Boolean = dead

        if dead:
            return

        self._scene: Object = scene

        self.time: Float = time()

        self.stopTime: Float = time() + time_length
        self.strengthMultiply = strength_multiply

        self.baseEffectClass: Effect = base_class

        self.pauseTime: Optional[Float] = None
        self.pause: Boolean = False

        try:
            self.icon = Resources.get_effect_resource(self.baseEffectClass.get_unlocalized_name())
            # print(self.icon)
        except UnlocalizedNameError:
            self.icon = Resources.get_effect_resource("effect_none")

        # print(self.strengthMultiply)

        PlayerCollisionEvent.bind(self.player_collision)
        UpdateEvent.bind(self.update)
        TickUpdateEvent.bind(self.tick_update)

        PauseEvent.bind(self.on_pause)
        UnpauseEvent.bind(self.on_unpause)

        self.baseEffectClass.on_effect_started(self, scene)
        EffectStartedEvent(self, scene)

    def stop(self):
        self.timeRemaining = 0
        if not self.dead:
            self.baseEffectClass.on_effect_stopped(self, self._scene)
            EffectStoppedEvent(self, self._scene)
        self.dead = True

    def __repr__(self):
        return f'[{self.__class__.__name__}: {round(self.timeRemaining, 1)}]'

    def tick_update(self, event: TickUpdateEvent):
        self.baseEffectClass.on_tick_update(self, event)
        EffectTickUpdateEvent(event.dt, self, event.scene)

    def on_pause(self, event: PauseEvent):
        self.pauseTime = self.timeRemaining
        self.pause = True

    def on_unpause(self, event: UnpauseEvent):
        self.pause = False
        self.timeRemaining = self.pauseTime

    def update(self, event: UpdateEvent):
        # self.on_update(event.dt, event.window, event.batch, event.player)
        self.baseEffectClass.on_update(self, event)
        EffectUpdateEvent(event.dt, self, event.scene)
        if self.pause:
            self.timeRemaining = self.pauseTime
            return
        if self.timeRemaining <= 0:
            self.timeRemaining = 0
            if not self.dead:
                self.baseEffectClass.on_effect_stopped(self, event.scene)
                EffectStoppedEvent(self, event.scene)
            self.dead = True
        if self.dead:
            PlayerCollisionEvent.unbind(self.player_collision)
            UpdateEvent.unbind(self.update)
            TickUpdateEvent.unbind(self.tick_update)

    def player_collision(self, event: PlayerCollisionEvent):
        self.baseEffectClass.on_player_collision(self, event)

    @property
    def timeRemaining(self):
        return self._get_time_remaining()

    @timeRemaining.setter
    def timeRemaining(self, value):
        self._set_time_remaining(value)

    def _get_time_remaining(self):
        return self.stopTime - time()

    def _set_time_remaining(self, remaining):
        self.stopTime = time() + remaining


# noinspection PyMethodMayBeStatic
class Effect(object):
    def __init__(self, call_when=lambda time_, strength, scene: True):
        self.isBadEffect: Boolean = False
        self._call_when: Callable = call_when
        self.icon = resource.image("textures/effect/effect_none.png")
        # self.icon = Resources.get_effect_resource()
        self.incompatibles: List = []
    
    def __call__(self, time_length, strength_multiply, scene):
        if self._call_when(time_length, strength_multiply, scene):
            return AppliedEffect(self, time_length, scene, strength_multiply)
        else:
            appliedeffect = AppliedEffect(self, time_length, scene, strength_multiply, dead=True)
            return appliedeffect

    def set_unlocalized_name(self, name):
        if not hasattr(g, "NAME2EFFECT"):
            g.NAME2EFFECT = dict()
        if not hasattr(g, "EFFECT2NAME"):
            g.EFFECT2NAME = dict()
        g.NAME2EFFECT[name] = self
        g.EFFECT2NAME[self] = name

    def get_unlocalized_name(self):
        if hasattr(g, "BUBBLE2NAME"):
            if self in g.EFFECT2NAME.keys():
                return g.EFFECT2NAME[self]
            else:
                raise UnlocalizedNameError("There is not unlocalized name for object '%s'"
                                           % self if isinstance(self, type) else type(self))
        else:
            raise UnlocalizedNameError("There are no unlocalized names defined!")

    def on_update(self, appliedeffect: AppliedEffect, event: UpdateEvent):
        pass

    def on_tick_update(self, appliedeffect: AppliedEffect, event: TickUpdateEvent):
        pass  # self.baseEffectClass.on_tick_update(dt, window, batch, player)

    def on_effect_started(self, appliedeffect: AppliedEffect, scene):
        pass

    def on_effect_stopped(self, appliedeffect: AppliedEffect, scene):
        pass

    # noinspection PyUnusedLocal
    def on_player_collision(self, appliedeffect: AppliedEffect, event: PlayerCollisionEvent):
        print(
            f"Collision with "
            f"{event.otherObject.__class__.__name__ if type(event.otherObject) is not type else event.otherObject.__name__}"
        )
        # pass  # self.baseEffectClass.on_player_collision(window, batch, player, obj)

    def is_bad_effect(self):
        return self.isBadEffect


class TeleportingEffect(Effect):
    def __init__(self):
        super(TeleportingEffect, self).__init__()

        self.isBadEffect = True

        self.incompatibles = [TeleportingEffect, ParalyseEffect]
        self.set_unlocalized_name("teleporting")
        
    def on_effect_start(self, appliedeffect: AppliedEffect):
        pass

    def on_update(self, appliedeffect: AppliedEffect, event: UpdateEvent):
        if appliedeffect.time <= time():
            event.player.move_to(random.randint(0, event.window.width), random.randint(0, event.window.height - 72))
            appliedeffect.time = time() + appliedeffect.strengthMultiply
            # EffectUpdateEvent(self.teleportInterval, self, event.scene)


class SpeedBoostEffect(Effect):
    def __init__(self):
        super(SpeedBoostEffect, self).__init__(lambda time_, strength, scene: scene.player.motionSpeedMultiply < 2)

        self.isBadEffect = False

        self.incompatibles = [SlownessEffect, ParalyseEffect]
        self.set_unlocalized_name("speed_boost")

    def __call__(self, time_length, strength_multiply, scene):
        if scene.player.motionSpeedMultiply < 2:
            return AppliedEffect(self, time_length, scene, strength_multiply)
        else:
            appliedeffect = AppliedEffect(self, time_length, scene, strength_multiply)
            appliedeffect.dead = True
            return appliedeffect

    def on_effect_started(self, appliedeffect: AppliedEffect, scene):
        scene.player.motionSpeedMultiply += (0.5 * appliedeffect.strengthMultiply)

    def on_effect_stopped(self, appliedeffect: AppliedEffect, scene):
        scene.player.motionSpeedMultiply -= (0.5 * appliedeffect.strengthMultiply)


class SlownessEffect(Effect):
    def __init__(self):
        super(SlownessEffect, self).__init__(lambda time_, strength_multiply, scene:
                                             (scene.player.motionSpeedMultiply - (0.5 * strength_multiply) >= 0))

        self.isBadEffect = True

        self.incompatibles = [SpeedBoostEffect, ParalyseEffect]
        self.icon = resource.image("textures/effect/slowness.png")
        self.set_unlocalized_name("slowness")

    # def __call__(self, time_length, strength_multiply, scene):
    #     if :
    #         return AppliedEffect(self, time_length, scene, strength_multiply, self.incompatibles, self.icon)
    #     else:
    #         appliedeffect = AppliedEffect(self, time_length, scene, strength_multiply, self.incompatibles, self.icon)
    #         appliedeffect.dead = True
    #         return appliedeffect

    def on_effect_started(self, appliedeffect: AppliedEffect, scene):
        scene.player.motionSpeedMultiply -= (0.5 * appliedeffect.strengthMultiply)

    def on_effect_stopped(self, appliedeffect: AppliedEffect, scene):
        scene.player.motionSpeedMultiply += (0.5 * appliedeffect.strengthMultiply)


class ParalyseEffect(Effect):
    def __init__(self):
        super(ParalyseEffect, self).__init__(lambda time_, strength_multiply, scene:
                                             (scene.player.motionSpeedMultiply - (0.5 * strength_multiply) >= 0))

        self.isBadEffect = True

        self.incompatibles = [SpeedBoostEffect, SlownessEffect, ParalyseEffect, TeleportingEffect]
        self.icon = resource.image("textures/effect/paralyse.png")
        self.set_unlocalized_name("paralyse")

        self.oldMotion: Optional[float] = None
        self.oldRotation: Optional[float] = None

    def on_effect_started(self, appliedeffect: AppliedEffect, scene):
        self.oldMotion = scene.player.motionSpeedMultiply
        self.oldRotation = scene.player.rotationSpeedMultiply

        scene.player.motionSpeedMultiply = 0
        scene.player.rotationSpeedMultiply = 0

    def on_effect_stopped(self, appliedeffect: AppliedEffect, scene):
        scene.player.motionSpeedMultiply = self.oldMotion
        scene.player.rotationSpeedMultiply = self.oldRotation


# noinspection PyMethodMayBeStatic
class ScoreStatusEffect(Effect):
    def __init__(self):
        super(ScoreStatusEffect, self).__init__()

        self.isBadEffect = False

        self.incompatibles = [ScoreStatusEffect]
        self.icon = resource.image("textures/effect/score_status.png")
        self.set_unlocalized_name("score_status")

        self.bindings = dict()

    def on_effect_started(self, appliedeffect: AppliedEffect, scene):
        self.bindings[appliedeffect] = lambda event, appliedeffect_=appliedeffect: self.onscore(appliedeffect_, event)
        ScoreEvent.bind(self.bindings[appliedeffect], True)

    def onscore(self, appliedeffect: AppliedEffect, event: ScoreEvent):
        event.addscore(event.score * appliedeffect.strengthMultiply)

    def on_effect_stopped(self, appliedeffect: AppliedEffect, scene):
        ScoreEvent.unbind(self.bindings[appliedeffect])


class GhostEffect(Effect):
    def __init__(self):
        super(GhostEffect, self).__init__()

        self.isBadEffect = False

        self.incompatibles = [GhostEffect]
        self.icon = resource.image("textures/effect/ghost_mode.png")
        self.set_unlocalized_name("ghost_mode")

    def on_effect_started(self, appliedeffect: AppliedEffect, scene):
        scene.player.ghostMode = True

    def on_effect_stopped(self, appliedeffect: AppliedEffect, scene):
        scene.player.ghostMode = False


class ProtectionEffect(Effect):
    def __init__(self):
        super(ProtectionEffect, self).__init__()

        self.isBadEffect = False

        self.incompatibles = [ProtectionEffect]
        self.set_unlocalized_name("protection")

    def on_effect_started(self, appliedeffect: AppliedEffect, scene):
        for effect in scene.player.activeEffects:
            effect: AppliedEffect
            if effect.baseEffectClass.is_bad_effect():
                effect.stop()
        scene.player.damageHook = lambda atk: None

    def on_effect_stopped(self, appliedeffect: AppliedEffect, scene):
        scene.player.damageHook = None


# noinspection PyPep8Naming,PyUnusedLocal,PyShadowingNames,PyAttributeOutsideInit
class ConfusionEffect(Effect):
    def __init__(self):
        super(ConfusionEffect, self).__init__()
        self.incompatibles = [ConfusionEffect]

        self.isBadEffect = True

        self.set_unlocalized_name("confusion")
        self.old: Optional[list] = None

    def on_effect_started(self, appliedeffect: AppliedEffect, scene):
        self.old = scene.motionKeys.copy()
        self.new = scene.motionKeys.copy()
        random.shuffle(self.new)
        LEFT = 0
        RIGHT = 1
        UP = 3
        DOWN = 2

        from pyglet.window import key

        LEFT2 = self.new[LEFT]
        RIGHT2 = self.new[RIGHT]
        UP2 = self.new[UP]
        DOWN2 = self.new[DOWN]

        keys = {key.LEFT: "<KEY LEFT>",
                key.RIGHT: "<KEY RIGHT>",
                key.UP: "<KEY UP>",
                key.DOWN: "<KEY DOWN>"}

        news = {key.LEFT: "<NEW LEFT>",
                key.RIGHT: "<NEW RIGHT>",
                key.UP: "<NEW UP>",
                key.DOWN: "<NEW DOWN>"}

        print(f"OLD: {self.old}")
        print(f"NEW: {self.new}")

        print()

        print(f"<NEW LEFT>={LEFT2}")
        print(f"<NEW RIGHT>={RIGHT2}")
        print(f"<NEW UP>={UP2}")
        print(f"<NEW DOWN>={DOWN2}")

        print()

        print(f"<KEY LEFT>={key.LEFT}")
        print(f"<KEY RIGHT>={key.RIGHT}")
        print(f"<KEY UP>={key.UP}")
        print(f"<KEY DOWN>={key.DOWN}")

        print()

        print(f"LEFT={keys[LEFT2]}")
        print(f"RIGHT={keys[RIGHT2]}")
        print(f"UP={keys[UP2]}")
        print(f"DOWN={keys[DOWN2]}")

        old_mpx_strafe = copy(scene.player_mpx_strafe)
        old_rot_strafe = copy(scene.player_rot_strafe)

        rot_strafe = {-ROTATION_SPEED: keys[key.LEFT],
                      ROTATION_SPEED: keys[key.RIGHT],
                      0: ""}

        mot_strafe = {-MOTION_SPEED: keys[key.UP],
                      MOTION_SPEED: keys[key.DOWN],
                      0: ""}

        print()

        print(f"Rotation Strafe: {old_rot_strafe}")
        print(f"Motion Strafe: {old_mpx_strafe}")
        print(f"Rota- / Motion Keys: {[keys[key] for key in self.old]}")

        a = [rot_strafe[old_rot_strafe], mot_strafe[old_mpx_strafe]]

        print(f"Keys: {a}")

        scene.motionKeys = self.new

        scene.safe_change_key(key.LEFT, LEFT2, old_rot_strafe, old_mpx_strafe)
        scene.safe_change_key(key.RIGHT, RIGHT2, old_rot_strafe, old_mpx_strafe)
        scene.safe_change_key(key.UP, UP2, old_rot_strafe, old_mpx_strafe)
        scene.safe_change_key(key.DOWN, DOWN2, old_rot_strafe, old_mpx_strafe)

        print()

        print(f"Rotation Strafe: {scene.player_rot_strafe}")
        print(f"Motion Strafe: {scene.player_mpx_strafe}")
        print(f"Rota- / Motion Keys: {[keys[key] for key in self.new]}")

        b = [rot_strafe[scene.player_rot_strafe], mot_strafe[scene.player_mpx_strafe]]

        print(f"Keys: {b}")

        # if old_rot_strafe < 0:
        #     print(f"<NEW LEFT> == <KEY LEFT>: {LEFT2 == key.LEFT}")
        #     print(f"<NEW LEFT> == <KEY RIGHT>: {LEFT2 == key.RIGHT}")
        #     print(f"<NEW LEFT> == <KEY UP>: {LEFT2 == key.UP}")
        #     print(f"<NEW LEFT> == <KEY DOWN>: {LEFT2 == key.DOWN}")
        #     if LEFT2 == key.LEFT:
        #         pass
        #     elif LEFT2 == key.RIGHT:
        #         scene.player_rot_strafe += ROTATION_SPEED * 2
        #     elif LEFT2 == key.UP:
        #         scene.player_rot_strafe += ROTATION_SPEED
        #         scene.player_mpx_strafe -= MOTION_SPEED
        #     elif LEFT2 == key.DOWN:
        #         scene.player_rot_strafe += ROTATION_SPEED
        #         scene.player_mpx_strafe += MOTION_SPEED
        # elif old_rot_strafe > 0:
        #     if RIGHT2 == key.LEFT:
        #         scene.player_rot_strafe -= ROTATION_SPEED * 2
        #     elif RIGHT2 == key.RIGHT:
        #         pass
        #     elif RIGHT2 == key.UP:
        #         scene.player_rot_strafe -= ROTATION_SPEED
        #         scene.player_mpx_strafe -= MOTION_SPEED
        #     elif RIGHT2 == key.DOWN:
        #         scene.player_rot_strafe -= ROTATION_SPEED
        #         scene.player_mpx_strafe += MOTION_SPEED
        # if old_mpx_strafe < 0:
        #     if UP2 == key.LEFT:  # UP to LEFT
        #         scene.player_mpx_strafe += MOTION_SPEED
        #         scene.player_rot_strafe -= ROTATION_SPEED
        #     elif UP2 == key.RIGHT:  # UP to RIGHT
        #         scene.player_mpx_strafe += MOTION_SPEED
        #         scene.player_rot_strafe += ROTATION_SPEED
        #     elif UP2 == key.UP:
        #         pass
        #     elif UP2 == key.DOWN:
        #         scene.player_mpx_strafe += ROTATION_SPEED * 2
        # elif old_mpx_strafe > 0:
        #     if DOWN2 == key.LEFT:
        #         scene.player_mpx_strafe -= MOTION_SPEED
        #         scene.player_rot_strafe -= ROTATION_SPEED
        #     elif DOWN2 == key.RIGHT:
        #         scene.player_mpx_strafe -= MOTION_SPEED
        #         scene.player_rot_strafe += ROTATION_SPEED
        #     elif DOWN2 == key.UP:
        #         scene.player_mpx_strafe -= ROTATION_SPEED * 2
        #     elif DOWN2 == key.DOWN:
        #         pass
        scene.player_rot_strafe = 0
        scene.player_mpx_strafe = 0

    def on_effect_stopped(self, appliedeffect: AppliedEffect, scene):
        scene.motionKeys = self.old
