import resources
import bubble
from sprites.objects import PhysicalObject
from sprites.player import Player


class NormalBubble(bubble.Bubble):
    # noinspection PyMissingConstructor
    def __init__(self):
        super(NormalBubble, self).__init__()

        self.set_unlocalized_name("normal_bubble")
        self.randomMin = 0
        self.randomMax = 50000
        self.speed = 7
        self.score_multiplier = 1

    def __call__(self, x, y, map, batch, size=None):
        return bubble.BubbleObject(self, x, y, batch, size)


class Bubble(bubble.Bubble):
    def __init__(self, x, y, batch, size=None):
        bubble_image = resources.bubbles["Normal"]

        super(Bubble, self).__init__(x, y, batch, size, bubble_image)
