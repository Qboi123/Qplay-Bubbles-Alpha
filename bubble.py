import pyglet

from utils import EAST, WEST, NORTH, SOUTH


class Bubble(object):
    speed: int = 0
    direction: str = WEST

    def __init__(self, parent, x, y, batch, size, bub_resource):
        parent: Bubble

        if size:
            pass
        else:
            smallest = min(list(bub_resource.keys()))
            size = smallest
        image = bub_resource[size]
        self.parent = parent
        self.sprite: pyglet.sprite.Sprite = pyglet.sprite.Sprite(img=image,
                                            x=x, y=y, batch=batch)
        self.parent.sprite = self.sprite
        if hasattr(parent, "parent"):
            del self.parent.parent

    def update(self, dt):
        x, y = self.parent.sprite.position

        if self.parent.direction == WEST:
            x -= self.parent.speed
        if self.parent.direction == EAST:
            x += self.parent.speed
        if self.parent.direction == NORTH:
            y += self.parent.speed
        if self.parent.direction == SOUTH:
            y -= self.parent.speed

        self.parent.sprite.position = (x, y)
