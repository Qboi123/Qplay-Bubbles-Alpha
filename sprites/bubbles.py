from bubble import BubbleObject, Bubble, BubblePriorityCalculator
from effects import TeleportingEffect, SpeedBoostEffect, SlownessEffect, ScoreStatusEffect, GhostEffect, ParalyseEffect
from events import CollisionEvent
from register import EFFECTS


class NormalBubble(Bubble):
    def __init__(self):
        super(NormalBubble, self).__init__()

        self.set_unlocalized_name("normal_bubble")
        self.speedMultiplier = 12
        self.speedMin = 7
        self.speedMax = 16
        self.scoreMultiplier = 1
        
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
        self.speedMin = 22
        self.speedMax = 28
        self.scoreMultiplier = 1

        BubblePriorityCalculator.add(self, 50000)

    def __call__(self, x, y, map, batch, size=None, speed=None):
        return BubbleObject(self, x, y, batch, size, speed)

    def on_collision(self, event: CollisionEvent):
        pass


class DoubleBubble(Bubble):
    def __init__(self):
        super(DoubleBubble, self).__init__()

        self.set_unlocalized_name("double_bubble")
        self.randomMin = 25000
        self.randomMax = 35000
        self.speedMin = 22
        self.speedMax = 32
        self.scoreMultiplier = 2

        BubblePriorityCalculator.add(self, 20000)

    def __call__(self, x, y, map, batch, size=None, speed=None):
        return BubbleObject(self, x, y, batch, size, speed)

    def on_collision(self, event: CollisionEvent):
        pass


class TripleBubble(Bubble):
    def __init__(self):
        super(TripleBubble, self).__init__()

        self.set_unlocalized_name("triple_bubble")
        self.randomMin = 35000
        self.randomMax = 42000
        self.speedMin = 32
        self.speedMax = 42
        self.scoreMultiplier = 3

        BubblePriorityCalculator.add(self, 10000)

    def __call__(self, x, y, map, batch, size=None, speed=None):
        return BubbleObject(self, x, y, batch, size, speed)

    def on_collision(self, event: CollisionEvent):
        pass


class DeadlyBubble(Bubble):
    def __init__(self):
        super(DeadlyBubble, self).__init__()

        self.set_unlocalized_name("kill_bubble")
        self.randomMin = 42000
        self.randomMax = 60000
        self.speedMin = 5
        self.speedMax = 19
        self.scoreMultiplier = 3

        BubblePriorityCalculator.add(self, 75000)

    def __call__(self, x, y, map, batch, size=None, speed=None):
        return BubbleObject(self, x, y, batch, size, speed)

    def on_collision(self, event: CollisionEvent):
        event.player.damage(1)


class LifeBubble(Bubble):
    def __init__(self):
        super(LifeBubble, self).__init__()

        self.set_unlocalized_name("life_bubble")
        self.randomMin = 60000
        self.randomMax = 65000
        self.speedMin = 32
        self.speedMax = 42
        self.scoreMultiplier = 0

        BubblePriorityCalculator.add(self, 15000)

    def __call__(self, x, y, map, batch, size=None, speed=None):
        return BubbleObject(self, x, y, batch, size, speed)

    def on_collision(self, event: CollisionEvent):
        event.player.gainlives(1)


class TeleporterBubble(Bubble):
    def __init__(self):
        super(TeleporterBubble, self).__init__()

        self.set_unlocalized_name("teleporter_bubble")
        self.speedMin = 32
        self.speedMax = 42
        self.scoreMultiplier = 0

        BubblePriorityCalculator.add(self, 1000)

    def __call__(self, x, y, map, batch, size=None, speed=None):
        return BubbleObject(self, x, y, batch, size, speed)

    def on_collision(self, event: CollisionEvent):
        event.player.add_effect(EFFECTS.TeleportingEffect(5, event.eventObject.size / 40, event.scene))


class SpeedBoostBubble(Bubble):
    def __init__(self):
        super(SpeedBoostBubble, self).__init__()

        self.set_unlocalized_name("speedboost_bubble")
        self.speedMin = 32
        self.speedMax = 47
        self.scoreMultiplier = 1.75

        BubblePriorityCalculator.add(self, 2000)

    def __call__(self, x, y, map, batch, size=None, speed=None):
        return BubbleObject(self, x, y, batch, size, speed)

    def on_collision(self, event: CollisionEvent):
        event.player.add_effect(EFFECTS.SpeedBoostEffect(7, event.eventObject.size / 40, event.scene))


class SlownessBubble(Bubble):
    def __init__(self):
        super(SlownessBubble, self).__init__()

        self.set_unlocalized_name("slowness_bubble")
        self.speedMin = 3
        self.speedMax = 12
        self.scoreMultiplier = 0.875

        BubblePriorityCalculator.add(self, 8000)

    def __call__(self, x, y, map, batch, size=None, speed=None):
        return BubbleObject(self, x, y, batch, size, speed)

    def on_collision(self, event: CollisionEvent):
        event.player.add_effect(EFFECTS.SlownessEffect(8, event.eventObject.size / 60, event.scene))


class UltraBubble(Bubble):
    def __init__(self):
        super(UltraBubble, self).__init__()

        self.set_unlocalized_name("ultra_bubble")
        self.speedMin = 47
        self.speedMax = 59
        self.scoreMultiplier = 10

        BubblePriorityCalculator.add(self, 100)

    # noinspection PyUnusedLocal
    def __call__(self, x, y, map, batch, size=None, speed=None):
        return BubbleObject(self, x, y, batch, 48, speed)

    def on_collision(self, event: CollisionEvent):
        event.player.add_effect(EFFECTS.ScoreStatusEffect(10, 10, event.scene))


class GhostBubble(Bubble):
    def __init__(self):
        super(GhostBubble, self).__init__()

        self.set_unlocalized_name("ghost_bubble")
        self.speedMin = 47
        self.speedMax = 59
        self.scoreMultiplier = 10

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

        BubblePriorityCalculator.add(self, 30303)

    # noinspection PyUnusedLocal
    def __call__(self, x, y, map, batch, size=None, speed=None):
        return BubbleObject(self, x, y, batch, size, speed)

    def on_collision(self, event: CollisionEvent):
        # pass
        event.player.add_effect(EFFECTS.ConfusionEffect(6, 1, event.scene))


class DoubleScoreStatBubble(Bubble):
    def __init__(self):
        super(DoubleScoreStatBubble, self).__init__()

        self.set_unlocalized_name("double_state_bubble")
        self.speedMin = 25
        self.speedMax = 33
        self.scoreMultiplier = 2

        BubblePriorityCalculator.add(self, 875)

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

        BubblePriorityCalculator.add(self, 450)

    def __call__(self, x, y, map, batch, size=None, speed=None):
        return BubbleObject(self, x, y, batch, size, speed)

    def on_collision(self, event: CollisionEvent):
        event.player.add_effect(EFFECTS.ScoreStatusEffect(event.eventObject.speed / 2.4, 3, event.scene))
