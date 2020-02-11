from bubble import BubbleObject, Bubble, BubblePriorityCalculator
from events import CollisionEvent
from register import EFFECTS
from utils.advBuiltins import AdvInteger, AdvFloat


class NormalBubble(Bubble):
    def __init__(self):
        super(NormalBubble, self).__init__()

        self.set_unlocalized_name("normal_bubble")
        self.speedMin: AdvInteger = AdvInteger(3)
        self.speedMax: AdvInteger = AdvInteger(16)

        self.health: AdvFloat = AdvFloat(1.5)
        self.maxHealth: AdvFloat = AdvFloat(1.0)
        self.scoreMultiplier: AdvFloat = AdvFloat(1.0)
        self.attackMultiplier: AdvFloat = AdvFloat(0.0)
        self.defenceMultiplier: AdvFloat = AdvFloat(1.0)
        BubblePriorityCalculator.add(self, 150000)

    def __call__(self, x, y, map, scene, size=None, speed=None):
        return BubbleObject(self, x, y, scene, size, speed)

    def on_collision(self, event: CollisionEvent):
        pass


class SpeedyBubble(Bubble):
    def __init__(self):
        super(SpeedyBubble, self).__init__()

        self.set_unlocalized_name("speedy_bubble")
        self.speedMin: AdvInteger = AdvInteger(16)
        self.speedMax: AdvInteger = AdvInteger(44)

        self.health: AdvFloat = AdvFloat(1.5)
        self.maxHealth: AdvFloat = AdvFloat(1.0)
        self.scoreMultiplier: AdvFloat = AdvFloat(1.0)
        self.attackMultiplier: AdvFloat = AdvFloat(0.0)
        self.defenceMultiplier: AdvFloat = AdvFloat(1.0)
        self.hideInPause = True

        BubblePriorityCalculator.add(self, 50000)

    def __call__(self, x, y, map, scene, size=None, speed=None):
        return BubbleObject(self, x, y, scene, size, speed)

    def on_collision(self, event: CollisionEvent):
        pass


class KeyBubble(Bubble):
    def __init__(self):
        super(KeyBubble, self).__init__()

        self.set_unlocalized_name("key_bubble")
        self.speedMin: AdvInteger = AdvInteger(10)
        self.speedMax: AdvInteger = AdvInteger(30)

        self.health: AdvFloat = AdvFloat(1.5)
        self.maxHealth: AdvFloat = AdvFloat(1.0)
        self.scoreMultiplier: AdvFloat = AdvFloat(1.0)
        self.attackMultiplier: AdvFloat = AdvFloat(0.0)
        self.defenceMultiplier: AdvFloat = AdvFloat(1.0)
        BubblePriorityCalculator.add(self, 300)

    def __call__(self, x, y, map, scene, size=None, speed=None):
        return BubbleObject(self, x, y, scene, 48, speed)

    def on_collision(self, event: CollisionEvent):
        event.player.level += 1


class DoubleBubble(Bubble):
    def __init__(self):
        super(DoubleBubble, self).__init__()

        self.set_unlocalized_name("double_bubble")
        self.speedMin: AdvInteger = AdvInteger(11)
        self.speedMax: AdvInteger = AdvInteger(32)

        self.health: AdvFloat = AdvFloat(3.0)
        self.maxHealth: AdvFloat = AdvFloat(1.0)
        self.scoreMultiplier: AdvFloat = AdvFloat(1.0)
        self.attackMultiplier: AdvFloat = AdvFloat(0.0)
        self.defenceMultiplier: AdvFloat = AdvFloat(1.0)
        BubblePriorityCalculator.add(self, 20000)

    def __call__(self, x, y, map, scene, size=None, speed=None):
        return BubbleObject(self, x, y, scene, size, speed)

    def on_collision(self, event: CollisionEvent):
        pass


class TripleBubble(Bubble):
    def __init__(self):
        super(TripleBubble, self).__init__()

        self.set_unlocalized_name("triple_bubble")
        self.speedMin: AdvInteger = AdvInteger(24)
        self.speedMax: AdvInteger = AdvInteger(38)

        self.health: AdvFloat = AdvFloat(4.0)
        self.maxHealth: AdvFloat = AdvFloat(1.0)
        self.scoreMultiplier: AdvFloat = AdvFloat(1.0)
        self.attackMultiplier: AdvFloat = AdvFloat(0.0)
        self.defenceMultiplier: AdvFloat = AdvFloat(1.0)
        BubblePriorityCalculator.add(self, 16667)

    def __call__(self, x, y, map, scene, size=None, speed=None):
        return BubbleObject(self, x, y, scene, size, speed)

    def on_collision(self, event: CollisionEvent):
        pass


class DecupleBubble(Bubble):
    def __init__(self):
        super(DecupleBubble, self).__init__()

        self.set_unlocalized_name("decuple_bubble")
        self.speedMin: AdvInteger = AdvInteger(32)
        self.speedMax: AdvInteger = AdvInteger(42)

        self.health: AdvFloat = AdvFloat(11.0)
        self.maxHealth: AdvFloat = AdvFloat(1.0)
        self.scoreMultiplier: AdvFloat = AdvFloat(1.0)
        self.attackMultiplier: AdvFloat = AdvFloat(0.0)
        self.defenceMultiplier: AdvFloat = AdvFloat(1.0)
        BubblePriorityCalculator.add(self, 2000)

    def __call__(self, x, y, map, scene, size=None, speed=None):
        return BubbleObject(self, x, y, scene, size, speed)

    def on_collision(self, event: CollisionEvent):
        pass


class DoubleScoreStatBubble(Bubble):
    def __init__(self):
        super(DoubleScoreStatBubble, self).__init__()

        self.set_unlocalized_name("double_state_bubble")
        self.speedMin: AdvInteger = AdvInteger(25)
        self.speedMax: AdvInteger = AdvInteger(33)
        self.scoreMultiplier: AdvInteger = AdvInteger(2)

        self.health: AdvFloat = AdvFloat(1.5)
        self.maxHealth: AdvFloat = AdvFloat(1.0)
        self.scoreMultiplier: AdvFloat = AdvFloat(2.0)
        self.attackMultiplier: AdvFloat = AdvFloat(0.0)
        self.defenceMultiplier: AdvFloat = AdvFloat(1.0)

        BubblePriorityCalculator.add(self, 2000)

    def __call__(self, x, y, map, scene, size=None, speed=None):
        return BubbleObject(self, x, y, scene, size, speed)

    def on_collision(self, event: CollisionEvent):
        event.player.add_effect(EFFECTS.ScoreStatusEffect(AdvFloat(event.eventObject.speed / 1.2), 2, event.scene))


class TripleScoreStatBubble(Bubble):
    def __init__(self):
        super(TripleScoreStatBubble, self).__init__()

        self.set_unlocalized_name("triple_state_bubble")
        self.speedMin: AdvInteger = AdvInteger(43)
        self.speedMax: AdvInteger = AdvInteger(54)
        self.scoreMultiplier: AdvInteger = AdvInteger(3)

        self.health: AdvFloat = AdvFloat(2.0)
        self.maxHealth: AdvFloat = AdvFloat(1.0)
        self.scoreMultiplier: AdvFloat = AdvFloat(3.0)
        self.attackMultiplier: AdvFloat = AdvFloat(0.0)
        self.defenceMultiplier: AdvFloat = AdvFloat(1.5)

        BubblePriorityCalculator.add(self, 1667)

    def __call__(self, x, y, map, scene, size=None, speed=None):
        return BubbleObject(self, x, y, scene, size, speed)

    def on_collision(self, event: CollisionEvent):
        event.player.add_effect(EFFECTS.ScoreStatusEffect(event.eventObject.speed / 3.6, 3, event.scene))


class DecupleScoreStatBubble(Bubble):
    def __init__(self):
        super(DecupleScoreStatBubble, self).__init__()

        self.set_unlocalized_name("decuple_state_bubble")
        self.speedMin: AdvInteger = AdvInteger(50)
        self.speedMax: AdvInteger = AdvInteger(64)
        self.scoreMultiplier: AdvInteger = AdvInteger(2)

        self.health: AdvFloat = AdvFloat(2.0)
        self.maxHealth: AdvFloat = AdvFloat(1.0)
        self.scoreMultiplier: AdvFloat = AdvFloat(3.0)
        self.attackMultiplier: AdvFloat = AdvFloat(0.0)
        self.defenceMultiplier: AdvFloat = AdvFloat(1.5)

        BubblePriorityCalculator.add(self, 200)

    def __call__(self, x, y, map, scene, size=None, speed=None):
        return BubbleObject(self, x, y, scene, size, speed)

    def on_collision(self, event: CollisionEvent):
        event.player.add_effect(EFFECTS.ScoreStatusEffect(AdvFloat(event.eventObject.speed / 4.4), 3, event.scene))


class DeadlyBubble(Bubble):
    def __init__(self):
        super(DeadlyBubble, self).__init__()

        self.set_unlocalized_name("kill_bubble")
        self.speedMin: AdvInteger = AdvInteger(2)
        self.speedMax: AdvInteger = AdvInteger(8)

        self.health: AdvFloat = AdvFloat(2.0)
        self.maxHealth: AdvFloat = AdvFloat(3.0)
        self.scoreMultiplier: AdvFloat = AdvFloat(0.0)
        self.attackMultiplier: AdvFloat = AdvFloat(1.0)
        self.defenceMultiplier: AdvFloat = AdvFloat(1.0)
        BubblePriorityCalculator.add(self, 75000)

    def __call__(self, x, y, map, scene, size=None, speed=None):
        return BubbleObject(self, x, y, scene, size, speed, defen_mp=AdvFloat(size / 10))

    def on_collision(self, event: CollisionEvent):
        pass


class LifeBubble(Bubble):
    def __init__(self):
        super(LifeBubble, self).__init__()

        self.set_unlocalized_name("life_bubble")
        self.speedMin: AdvInteger = AdvInteger(24)
        self.speedMax: AdvInteger = AdvInteger(38)

        self.health: AdvFloat = AdvFloat(2.0)
        self.maxHealth: AdvFloat = AdvFloat(3.0)
        self.scoreMultiplier: AdvFloat = AdvFloat(0.0)
        self.attackMultiplier: AdvFloat = AdvFloat(0.0)
        self.defenceMultiplier: AdvFloat = AdvFloat(1.0)
        BubblePriorityCalculator.add(self, 10000)

    def __call__(self, x, y, map, scene, size=None, speed=None):
        return BubbleObject(self, x, y, scene, size, speed, defen_mp=AdvFloat(size / 10))

    def on_collision(self, event: CollisionEvent):
        event.player.regen(AdvInteger(1))


class TeleporterBubble(Bubble):
    def __init__(self):
        super(TeleporterBubble, self).__init__()

        self.set_unlocalized_name("teleporter_bubble")
        self.speedMin: AdvInteger = AdvInteger(32)
        self.speedMax: AdvInteger = AdvInteger(42)

        self.health: AdvFloat = AdvFloat(1.5)
        self.maxHealth: AdvFloat = AdvFloat(2.5)
        self.scoreMultiplier: AdvFloat = AdvFloat(0.0)
        self.attackMultiplier: AdvFloat = AdvFloat(0.1)
        self.defenceMultiplier: AdvFloat = AdvFloat(1.0)
        BubblePriorityCalculator.add(self, 1000)

    def __call__(self, x, y, map, scene, size=None, speed=None):
        return BubbleObject(self, x, y, scene, size, speed)

    def on_collision(self, event: CollisionEvent):
        event.player.add_effect(EFFECTS.TeleportingEffect(AdvFloat(5), AdvFloat(event.eventObject.size / 40),
                                                          event.scene))


class SpeedBoostBubble(Bubble):
    def __init__(self):
        super(SpeedBoostBubble, self).__init__()

        self.set_unlocalized_name("speedboost_bubble")
        self.speedMin: AdvInteger = AdvInteger(32)
        self.speedMax: AdvInteger = AdvInteger(47)

        self.health: AdvFloat = AdvFloat(1.5)
        self.maxHealth: AdvFloat = AdvFloat(2.5)
        self.scoreMultiplier: AdvFloat = AdvFloat(0.1)
        self.attackMultiplier: AdvFloat = AdvFloat(0.0)
        self.defenceMultiplier: AdvFloat = AdvFloat(1.375)
        BubblePriorityCalculator.add(self, 2000)

    def __call__(self, x, y, map, scene, size=None, speed=None):
        return BubbleObject(self, x, y, scene, size, speed)

    def on_collision(self, event: CollisionEvent):
        event.player.add_effect(EFFECTS.SpeedBoostEffect(AdvFloat(7), AdvFloat(event.eventObject.size / 40),
                                                         event.scene))


class SlownessBubble(Bubble):
    def __init__(self):
        super(SlownessBubble, self).__init__()

        self.set_unlocalized_name("slowness_bubble")
        self.speedMin: AdvInteger = AdvInteger(1)
        self.speedMax: AdvInteger = AdvInteger(8)

        self.health: AdvFloat = AdvFloat(1.5)
        self.maxHealth: AdvFloat = AdvFloat(2.5)
        self.scoreMultiplier: AdvFloat = AdvFloat(0.0)
        self.attackMultiplier: AdvFloat = AdvFloat(0.0)
        self.defenceMultiplier: AdvFloat = AdvFloat(1.0)
        BubblePriorityCalculator.add(self, 8000)

    def __call__(self, x, y, map, scene, size=None, speed=None):
        return BubbleObject(self, x, y, scene, size, speed)

    def on_collision(self, event: CollisionEvent):
        event.player.add_effect(EFFECTS.SlownessEffect(AdvFloat(8), AdvFloat(event.eventObject.size / 60),
                                                       event.scene))


class UltraBubble(Bubble):
    def __init__(self):
        super(UltraBubble, self).__init__()

        self.set_unlocalized_name("ultra_bubble")
        self.speedMin: AdvInteger = AdvInteger(47)
        self.speedMax: AdvInteger = AdvInteger(59)

        self.health: AdvFloat = AdvFloat(2.0)
        self.maxHealth: AdvFloat = AdvFloat(3.0)
        self.scoreMultiplier: AdvFloat = AdvFloat(10.0)
        self.attackMultiplier: AdvFloat = AdvFloat(0.0)
        self.defenceMultiplier: AdvFloat = AdvFloat(2.0)
        BubblePriorityCalculator.add(self, 10)

    # noinspection PyUnusedLocal
    def __call__(self, x, y, map, scene, size=None, speed=None):
        return BubbleObject(self, x, y, scene, 48, speed)

    def on_collision(self, event: CollisionEvent):
        event.player.add_effect(EFFECTS.ScoreStatusEffect(AdvFloat(20), AdvFloat(10), event.scene))
        event.player.add_effect(EFFECTS.ProtectionEffect(AdvFloat(12.5), AdvFloat(1), event.scene))


class GhostBubble(Bubble):
    def __init__(self):
        super(GhostBubble, self).__init__()

        self.set_unlocalized_name("ghost_bubble")
        self.speedMin: AdvInteger = AdvInteger(47)
        self.speedMax: AdvInteger = AdvInteger(59)

        self.health: AdvFloat = AdvFloat(1.5)
        self.maxHealth: AdvFloat = AdvFloat(2.5)
        self.scoreMultiplier: AdvFloat = AdvFloat(0.5)
        self.attackMultiplier: AdvFloat = AdvFloat(0.0)
        self.defenceMultiplier: AdvFloat = AdvFloat(1.5)
        BubblePriorityCalculator.add(self, 2500)

    # noinspection PyUnusedLocal
    def __call__(self, x, y, map, scene, size=None, speed=None):
        return BubbleObject(self, x, y, scene, size, speed)

    def on_collision(self, event: CollisionEvent):
        # pass
        event.player.add_effect(EFFECTS.GhostEffect(6, 1, event.scene))


class ParalyseBubble(Bubble):
    def __init__(self):
        super(ParalyseBubble, self).__init__()

        self.set_unlocalized_name("paralyse_bubble")
        self.speedMin: AdvInteger = AdvInteger(24)
        self.speedMax: AdvInteger = AdvInteger(37)

        self.health: AdvFloat = AdvFloat(1.5)
        self.maxHealth: AdvFloat = AdvFloat(1.0)
        self.scoreMultiplier: AdvFloat = AdvFloat(0.0)
        self.attackMultiplier: AdvFloat = AdvFloat(0.2)
        self.defenceMultiplier: AdvFloat = AdvFloat(4.0)

        BubblePriorityCalculator.add(self, 7500)

    # noinspection PyUnusedLocal
    def __call__(self, x, y, map, scene, size=None, speed=None):
        return BubbleObject(self, x, y, scene, size, speed)

    def on_collision(self, event: CollisionEvent):
        # pass
        event.player.add_effect(EFFECTS.ParalisEffect(6, 1, event.scene))


class ConfusionBubble(Bubble):
    def __init__(self):
        super(ConfusionBubble, self).__init__()

        self.set_unlocalized_name("confusion_bubble")
        self.speedMin: AdvInteger = AdvInteger(24)
        self.speedMax: AdvInteger = AdvInteger(37)

        self.health: AdvFloat = AdvFloat(1.5)
        self.maxHealth: AdvFloat = AdvFloat(1.0)
        self.scoreMultiplier: AdvFloat = AdvFloat(0.0)
        self.attackMultiplier: AdvFloat = AdvFloat(0.1)
        self.defenceMultiplier: AdvFloat = AdvFloat(1.0)

        BubblePriorityCalculator.add(self, 30303)

    # noinspection PyUnusedLocal
    def __call__(self, x, y, map, scene, size=None, speed=None):
        return BubbleObject(self, x, y, scene, size, speed)

    def on_collision(self, event: CollisionEvent):
        # pass
        event.player.add_effect(EFFECTS.ConfusionEffect(6, 1, event.scene))


class ProtectionBubble(Bubble):
    def __init__(self):
        super(ProtectionBubble, self).__init__()

        self.set_unlocalized_name("protection_bubble")
        self.speedMin: AdvInteger = AdvInteger(32)
        self.speedMax: AdvInteger = AdvInteger(42)

        self.health: AdvFloat = AdvFloat(2.0)
        self.maxHealth: AdvFloat = AdvFloat(1.0)
        self.scoreMultiplier: AdvFloat = AdvFloat(0.1)
        self.attackMultiplier: AdvFloat = AdvFloat(0.0)
        self.defenceMultiplier: AdvFloat = AdvFloat(3.0)

        BubblePriorityCalculator.add(self, 2000)

    def __call__(self, x, y, map, scene, size=None, speed=None):
        return BubbleObject(self, x, y, scene, size, speed)

    def on_collision(self, event: CollisionEvent):
        event.player.add_effect(EFFECTS.ProtectionEffect(event.eventObject.speed / 8, 1, event.scene))
        event.player.regen(event.eventObject.size / 20)
