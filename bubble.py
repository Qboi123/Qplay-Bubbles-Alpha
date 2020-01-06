import pyglet

from utils import EAST, WEST, NORTH, SOUTH
from utils.classes import Position2D


class Bubble(object):
    speed: int = 0
    direction: str = WEST

    def __init__(self, x, y, batch, size, bub_resource):
        parent: Bubble

        if size:
            pass
        else:
            smallest = min(list(bub_resource.keys()))
            size = smallest
        image = bub_resource[size]
        print(image, x, y, batch)
        self.direction = WEST
        self.__position: Position2D = Position2D((x, y))
        self.sprite: pyglet.sprite.Sprite = pyglet.sprite.Sprite(img=image,
                                            x=x, y=y, batch=batch)

    def draw(self):
        self.sprite.update(self.sprite.x, self.sprite.y, self.sprite.rotation, self.sprite.scale,
                           self.sprite.scale_x, self.sprite.scale_y)
        print("Draw")

    def update(self, dt):
        # dx, dy = self.sprite.position

        if self.direction == WEST:
            dx = self.speed
        if self.direction == EAST:
            dx = self.speed
        if self.direction == NORTH:
            dy = self.speed
        if self.direction == SOUTH:
            dy = self.speed

        dx = -self.speed
        dy = 0

        print(self.direction)

        # self.sprite.position = (x * dt, y * dt)
        # noinspection PyUnboundLocalVariable
        self.__position += (dx * dt, dy * dt)
        self.sprite.update(x=self.__position.x, y=self.__position.y)
        print("Update")
