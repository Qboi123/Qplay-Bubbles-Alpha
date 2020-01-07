import resources
import bubble
from sprites.objects import PhysicalObject
from sprites.player import Player


class NormalBubble(bubble.Bubble):
    def __init__(self):
        super(NormalBubble, self).__init__()

        self.set_unlocalized_name("normal_bubble")
        self.randomMin = 0
        self.randomMax = 15000
        self.speedMultiplier = 12
        self.speedMin = 7
        self.speedMax = 16
        self.scoreMultiplier = 1

    def __call__(self, x, y, map, batch, size=None, speed=None):
        return bubble.BubbleObject(self, x, y, batch, size, speed)

    def on_collision(self, player: Player):
        pass


class SpeedyBubble(bubble.Bubble):
    def __init__(self):
        super(SpeedyBubble, self).__init__()

        self.set_unlocalized_name("speedy_bubble")
        self.randomMin = 15000
        self.randomMax = 25000
        self.speedMin = 22
        self.speedMax = 28
        self.scoreMultiplier = 1

    def __call__(self, x, y, map, batch, size=None, speed=None):
        return bubble.BubbleObject(self, x, y, batch, size, speed)

    def on_collision(self, player: Player):
        pass


class DoubleBubble(bubble.Bubble):
    def __init__(self):
        super(DoubleBubble, self).__init__()

        self.set_unlocalized_name("double_bubble")
        self.randomMin = 25000
        self.randomMax = 35000
        self.speedMin = 22
        self.speedMax = 32
        self.scoreMultiplier = 2

    def __call__(self, x, y, map, batch, size=None, speed=None):
        return bubble.BubbleObject(self, x, y, batch, size, speed)

    def on_collision(self, player: Player):
        pass


class TripleBubble(bubble.Bubble):
    def __init__(self):
        super(TripleBubble, self).__init__()

        self.set_unlocalized_name("triple_bubble")
        self.randomMin = 35000
        self.randomMax = 42000
        self.speedMin = 32
        self.speedMax = 42
        self.scoreMultiplier = 3

    def __call__(self, x, y, map, batch, size=None, speed=None):
        return bubble.BubbleObject(self, x, y, batch, size, speed)

    def on_collision(self, player: Player):
        pass


class DeadlyBubble(bubble.Bubble):
    def __init__(self):
        super(DeadlyBubble, self).__init__()

        self.set_unlocalized_name("kill_bubble")
        self.randomMin = 42000
        self.randomMax = 60000
        self.speedMin = 5
        self.speedMax = 19
        self.scoreMultiplier = 3

    def __call__(self, x, y, map, batch, size=None, speed=None):
        return bubble.BubbleObject(self, x, y, batch, size, speed)

    def on_collision(self, player: Player):
        player.damage(1)


class LifeBubble(bubble.Bubble):
    def __init__(self):
        super(LifeBubble, self).__init__()

        self.set_unlocalized_name("life_bubble")
        self.randomMin = 60000
        self.randomMax = 65000
        self.speedMin = 32
        self.speedMax = 42
        self.scoreMultiplier = 0

    def __call__(self, x, y, map, batch, size=None, speed=None):
        return bubble.BubbleObject(self, x, y, batch, size, speed)

    def on_collision(self, player: Player):
        player.gain_lives(1)
