from pyglet.graphics import Batch
from pyglet.window import Window

import resources
from bubble import BubbleObject, Bubble, BubblePriorityCalculator
from effects import TeleportingEffect, SpeedBoostEffect
from events import CollisionEvent
from init import Effects
from sprites.objects import PhysicalObject
from sprites.player import Player


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

        BubblePriorityCalculator.add(self, 50000)

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
        event.player.gain_lives(1)


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
        event.player.add_effect(TeleportingEffect(5, event.scene, event.eventObject.size - 80))


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
        event.player.add_effect(SpeedBoostEffect(7.5, event.scene, event.eventObject.size - 80))
