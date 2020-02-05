from bubble import BubbleObject, Bubble, BubblePriorityCalculator
from effects import TeleportingEffect, SpeedBoostEffect, SlownessEffect, ScoreStatusEffect, GhostEffect, ParalyseEffect
from events import CollisionEvent
from register import EFFECTS
from typinglib import Float, Integer


class NormalBubble(Bubble):
    def __init__(self):
        super(NormalBubble, self).__init__()

        self.set_unlocalized_name("normal_bubble")
        self.speedMultiplier = 12
        self.speedMin = 7
        self.speedMax = 16

        self.health: Float = 1.5
        self.maxHealth: Float = 1.0
        self.scoreMultiplier: Float = 1.0
        self.attackMultiplier: Float = 0.0
        self.defenceMultiplier: Float = 1.0

        BubblePriorityCalculator.add(self, 150000)

    def __call__(self, x, y, map, batch, size=None, speed=None):
        return BubbleObject(self, x, y, batch, size, speed)

    def on_collision(self, event: CollisionEvent):
        pass


class SpeedyBubble(Bubble):
    def __init__(self):
        super(SpeedyBubble, self).__init__()

        self.set_unlocalized_name("speedy_bubble")
        self.randomMin = 15000
        self.randomMax = 25000
        self.speedMin = 32
        self.speedMax = 44

        self.health: Float = 1.5
        self.maxHealth: Float = 1.0
        self.scoreMultiplier: Float = 1.0
        self.attackMultiplier: Float = 0.0
        self.defenceMultiplier: Float = 1.0

        self.hideInPause = True

        BubblePriorityCalculator.add(self, 50000)

    def __call__(self, x, y, map, batch, size=None, speed=None):
        return BubbleObject(self, x, y, batch, size, speed)

    def on_collision(self, event: CollisionEvent):
        pass


class DoubleBubble(Bubble):
    def __init__(self):
        super(DoubleBubble, self).__init__()

        self.set_unlocalized_name("double_bubble")
        self.speedMin = 22
        self.speedMax = 32

        self.health: Float = 3.0
        self.maxHealth: Float = 1.0
        self.scoreMultiplier: Float = 1.0
        self.attackMultiplier: Float = 0.0
        self.defenceMultiplier: Float = 1.0

        BubblePriorityCalculator.add(self, 20000)

    def __call__(self, x, y, map, batch, size=None, speed=None):
        return BubbleObject(self, x, y, batch, size, speed)

    def on_collision(self, event: CollisionEvent):
        pass


class TripleBubble(Bubble):
    def __init__(self):
        super(TripleBubble, self).__init__()

        self.set_unlocalized_name("triple_bubble")
        self.speedMin = 32
        self.speedMax = 42

        self.health: Float = 4.0
        self.maxHealth: Float = 1.0
        self.scoreMultiplier: Float = 1.0
        self.attackMultiplier: Float = 0.0
        self.defenceMultiplier: Float = 1.0

        BubblePriorityCalculator.add(self, 16667)

    def __call__(self, x, y, map, batch, size=None, speed=None):
        return BubbleObject(self, x, y, batch, size, speed)

    def on_collision(self, event: CollisionEvent):
        pass


class DecupleBubble(Bubble):
    def __init__(self):
        super(DecupleBubble, self).__init__()

        self.set_unlocalized_name("decuple_bubble")
        self.speedMin = 32
        self.speedMax = 42

        self.health: Float = 11.0
        self.maxHealth: Float = 1.0
        self.scoreMultiplier: Float = 1.0
        self.attackMultiplier: Float = 0.0
        self.defenceMultiplier: Float = 1.0

        BubblePriorityCalculator.add(self, 2000)

    def __call__(self, x, y, map, batch, size=None, speed=None):
        return BubbleObject(self, x, y, batch, size, speed)

    def on_collision(self, event: CollisionEvent):
        pass


class DoubleScoreStatBubble(Bubble):
    def __init__(self):
        super(DoubleScoreStatBubble, self).__init__()

        self.set_unlocalized_name("double_state_bubble")
        self.speedMin = 25
        self.speedMax = 33
        self.scoreMultiplier = 2

        self.health: Float = 1.5
        self.maxHealth: Float = 1.0
        self.scoreMultiplier: Float = 2.0
        self.attackMultiplier: Float = 0.0
        self.defenceMultiplier: Float = 1.0

        BubblePriorityCalculator.add(self, 2000)

    def __call__(self, x, y, map, batch, size=None, speed=None):
        return BubbleObject(self, x, y, batch, size, speed)

    def on_collision(self, event: CollisionEvent):
        event.player.add_effect(EFFECTS.ScoreStatusEffect(event.eventObject.speed / 1.2, 2, event.scene))


class TripleScoreStatBubble(Bubble):
    def __init__(self):
        super(TripleScoreStatBubble, self).__init__()

        self.set_unlocalized_name("triple_state_bubble")
        self.speedMin = 46
        self.speedMax = 63
        self.scoreMultiplier = 2

        self.health: Float = 2.0
        self.maxHealth: Float = 1.0
        self.scoreMultiplier: Float = 3.0
        self.attackMultiplier: Float = 0.0
        self.defenceMultiplier: Float = 1.5

        BubblePriorityCalculator.add(self, 1667)

    def __call__(self, x, y, map, batch, size=None, speed=None):
        return BubbleObject(self, x, y, batch, size, speed)

    def on_collision(self, event: CollisionEvent):
        event.player.add_effect(EFFECTS.ScoreStatusEffect(event.eventObject.speed / 2.4, 3, event.scene))


class DecupleScoreStatBubble(Bubble):
    def __init__(self):
        super(DecupleScoreStatBubble, self).__init__()

        self.set_unlocalized_name("decuple_state_bubble")
        self.speedMin = 46
        self.speedMax = 63
        self.scoreMultiplier = 2

        self.health: Float = 2.0
        self.maxHealth: Float = 1.0
        self.scoreMultiplier: Float = 3.0
        self.attackMultiplier: Float = 0.0
        self.defenceMultiplier: Float = 1.5

        BubblePriorityCalculator.add(self, 200)

    def __call__(self, x, y, map, batch, size=None, speed=None):
        return BubbleObject(self, x, y, batch, size, speed)

    def on_collision(self, event: CollisionEvent):
        event.player.add_effect(EFFECTS.ScoreStatusEffect(event.eventObject.speed / 2.4, 3, event.scene))


class DeadlyBubble(Bubble):
    def __init__(self):
        super(DeadlyBubble, self).__init__()

        self.set_unlocalized_name("kill_bubble")
        self.speedMin: Integer = 5
        self.speedMax: Integer = 19

        self.health: Float = 2.0
        self.maxHealth: Float = 3.0
        self.scoreMultiplier: Float = 0.0
        self.attackMultiplier: Float = 1.0
        self.defenceMultiplier: Float = 1.0

        BubblePriorityCalculator.add(self, 75000)

    def __call__(self, x, y, map, batch, size=None, speed=None):
        # print(Integer(size / 10))
        return BubbleObject(self, x, y, batch, size, speed, defen_mp=Float(size / 10))

    def on_collision(self, event: CollisionEvent):
        pass


class LifeBubble(Bubble):
    def __init__(self):
        super(LifeBubble, self).__init__()

        self.set_unlocalized_name("life_bubble")
        self.speedMin: Integer = 32
        self.speedMax: Integer = 42

        self.health: Float = 2.0
        self.maxHealth: Float = 1
        self.scoreMultiplier: Float = 0.0
        self.attackMultiplier: Float = 0.0
        self.defenceMultiplier: Float = 1.0

        BubblePriorityCalculator.add(self, 10000)

    def __call__(self, x, y, map, batch, size=None, speed=None):
        return BubbleObject(self, x, y, batch, size, speed, defen_mp=Integer(size / 10))

    def on_collision(self, event: CollisionEvent):
        event.player.regen(1)


class TeleporterBubble(Bubble):
    def __init__(self):
        super(TeleporterBubble, self).__init__()

        self.set_unlocalized_name("teleporter_bubble")
        self.speedMin: Integer = 32
        self.speedMax: Integer = 42

        self.health: Float = 1.5
        self.maxHealth: Float = 0.5
        self.scoreMultiplier: Float = 0.0
        self.attackMultiplier: Float = 0.1
        self.defenceMultiplier: Float = 1.0

        BubblePriorityCalculator.add(self, 1000)

    def __call__(self, x, y, map, batch, size=None, speed=None):
        return BubbleObject(self, x, y, batch, size, speed)

    def on_collision(self, event: CollisionEvent):
        event.player.add_effect(EFFECTS.TeleportingEffect(5, event.eventObject.size / 40, event.scene))


class SpeedBoostBubble(Bubble):
    def __init__(self):
        super(SpeedBoostBubble, self).__init__()

        self.set_unlocalized_name("speedboost_bubble")
        self.speedMin: Integer = 32
        self.speedMax: Integer = 47

        self.health: Float = 1.5
        self.maxHealth: Float = 1.0
        self.scoreMultiplier: Float = 0.1
        self.attackMultiplier: Float = 0.0
        self.defenceMultiplier: Float = 1.375

        BubblePriorityCalculator.add(self, 2000)

    def __call__(self, x, y, map, batch, size=None, speed=None):
        return BubbleObject(self, x, y, batch, size, speed)

    def on_collision(self, event: CollisionEvent):
        event.player.add_effect(EFFECTS.SpeedBoostEffect(7, event.eventObject.size / 40, event.scene))


class SlownessBubble(Bubble):
    def __init__(self):
        super(SlownessBubble, self).__init__()

        self.set_unlocalized_name("slowness_bubble")
        self.speedMin: Integer = 3
        self.speedMax: Integer = 12

        self.health: Float = 1.5
        self.maxHealth: Float = 1.0
        self.scoreMultiplier: Float = 0.0
        self.attackMultiplier: Float = 0.0
        self.defenceMultiplier: Float = 1.0

        BubblePriorityCalculator.add(self, 8000)

    def __call__(self, x, y, map, batch, size=None, speed=None):
        return BubbleObject(self, x, y, batch, size, speed)

    def on_collision(self, event: CollisionEvent):
        event.player.add_effect(EFFECTS.SlownessEffect(8, event.eventObject.size / 60, event.scene))


class UltraBubble(Bubble):
    def __init__(self):
        super(UltraBubble, self).__init__()

        self.set_unlocalized_name("ultra_bubble")
        self.speedMin: Integer = 47
        self.speedMax: Integer = 59

        self.health: Float = 2.0
        self.maxHealth: Float = 1.0
        self.scoreMultiplier: Float = 10.0
        self.attackMultiplier: Float = 0.0
        self.defenceMultiplier: Float = 2.0

        BubblePriorityCalculator.add(self, 10)

    # noinspection PyUnusedLocal
    def __call__(self, x, y, map, batch, size=None, speed=None):
        return BubbleObject(self, x, y, batch, 48, speed)

    def on_collision(self, event: CollisionEvent):
        event.player.add_effect(EFFECTS.ScoreStatusEffect(20, 10, event.scene))
        event.player.add_effect(EFFECTS.ProtectionEffect(12.5, 1, event.scene))


class GhostBubble(Bubble):
    def __init__(self):
        super(GhostBubble, self).__init__()

        self.set_unlocalized_name("ghost_bubble")
        self.speedMin = 47
        self.speedMax = 59

        self.health: Float = 1.5
        self.maxHealth: Float = 1.0
        self.scoreMultiplier: Float = 0.5
        self.attackMultiplier: Float = 0.0
        self.defenceMultiplier: Float = 1.5

        BubblePriorityCalculator.add(self, 2500)

    # noinspection PyUnusedLocal
    def __call__(self, x, y, map, batch, size=None, speed=None):
        return BubbleObject(self, x, y, batch, size, speed)

    def on_collision(self, event: CollisionEvent):
        # pass
        event.player.add_effect(EFFECTS.GhostEffect(6, 1, event.scene))


class ParalyseBubble(Bubble):
    def __init__(self):
        super(ParalyseBubble, self).__init__()

        self.set_unlocalized_name("paralyse_bubble")
        self.speedMin = 24
        self.speedMax = 37
        self.scoreMultiplier = 10

        self.health: Float = 1.5
        self.maxHealth: Float = 1.0
        self.scoreMultiplier: Float = 0.0
        self.attackMultiplier: Float = 0.2
        self.defenceMultiplier: Float = 4.0

        BubblePriorityCalculator.add(self, 7500)

    # noinspection PyUnusedLocal
    def __call__(self, x, y, map, batch, size=None, speed=None):
        return BubbleObject(self, x, y, batch, size, speed)

    def on_collision(self, event: CollisionEvent):
        # pass
        event.player.add_effect(EFFECTS.ParalisEffect(6, 1, event.scene))


class ConfusionBubble(Bubble):
    def __init__(self):
        super(ConfusionBubble, self).__init__()

        self.set_unlocalized_name("confusion_bubble")
        self.speedMin = 24
        self.speedMax = 37
        self.scoreMultiplier = 10

        self.health: Float = 1.5
        self.maxHealth: Float = 1.0
        self.scoreMultiplier: Float = 0.0
        self.attackMultiplier: Float = 0.1
        self.defenceMultiplier: Float = 1.0

        BubblePriorityCalculator.add(self, 30303)

    # noinspection PyUnusedLocal
    def __call__(self, x, y, map, batch, size=None, speed=None):
        return BubbleObject(self, x, y, batch, size, speed)

    def on_collision(self, event: CollisionEvent):
        # pass
        event.player.add_effect(EFFECTS.ConfusionEffect(6, 1, event.scene))


class ProtectionBubble(Bubble):
    def __init__(self):
        super(ProtectionBubble, self).__init__()

        self.set_unlocalized_name("protection_bubble")
        self.speedMin = 46
        self.speedMax = 63
        self.scoreMultiplier = 2

        self.health: Float = 2.0
        self.maxHealth: Float = 1.0
        self.scoreMultiplier: Float = 0.1
        self.attackMultiplier: Float = 0.0
        self.defenceMultiplier: Float = 3.0

        BubblePriorityCalculator.add(self, 2000)

    def __call__(self, x, y, map, batch, size=None, speed=None):
        return BubbleObject(self, x, y, batch, size, speed)

    def on_collision(self, event: CollisionEvent):
        event.player.add_effect(EFFECTS.ProtectionEffect(event.eventObject.speed / 8, 1, event.scene))
        event.player.regen(event.eventObject.size / 20)
