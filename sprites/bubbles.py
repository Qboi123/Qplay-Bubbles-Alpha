import resources
from bubble import Bubble


class NormalBubble(Bubble):
    speed: int = 1
    def __init__(self, x, y, batch, size=None):
        bubble = resources.bubbles["Normal"]

        super(Bubble).__init__(self, x, y, batch, size, bubble)
        self.image = image
