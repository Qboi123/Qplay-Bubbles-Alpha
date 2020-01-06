import resources
import bubble


class NormalBubble(bubble.Bubble):
    speed: int = 7
    randomMin: int = 0
    randomMax: int = 50000

    def __init__(self, x, y, batch, size=None):
        bubble_image = resources.bubbles["Normal"]
        super(NormalBubble, self).__init__(x, y, batch, size, bubble_image)

        print("Create NormalBubble")


class Bubble(bubble.Bubble):
    def __init__(self, x, y, batch, size=None):
        bubble_image = resources.bubbles["Normal"]

        super(Bubble, self).__init__(x, y, batch, size, bubble_image)
