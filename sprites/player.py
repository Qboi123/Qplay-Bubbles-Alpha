import pyglet
from typing import Tuple

import resources
from sprites.objects import PhysicalObject
from utils import PLAYER_SPEED
from utils.classes import Position2D


class Player(PhysicalObject):
    def __init__(self, pos: Tuple[float, float], batch):
        # self.position = pos
        super(Player, self).__init__(img=resources.player, batch=batch)

        self.rotation = 0
        self.sprite: pyglet.sprite.Sprite = pyglet.sprite.Sprite(resources.player, batch=batch)
        self.sprite.position = pos

        self.__position: Position2D = Position2D(pos)

    def rotate(self, degrees):
        # print(self.sprite.rotation)
        super(PhysicalObject, self).update(rotation = self.rotation - 90)

    def draw(self):
        # super(PhysicalObject, self).update(self.position.x, self.position.y, self.rotation - 90, 1.2)
        pass

    def move_pixels(self, dt, pixels):
        rot_x = self.rotation
        import math

        d = dt * pixels  # distance covered this tick.
        # strafe = math.degrees(math.atan(pixels))
        angle_radians = -math.radians(-(self.rotation - 90))
        dx = -math.cos(angle_radians)
        dy = math.sin(angle_radians)
        # dx = math.sin(x_angle)
        # dy = math.cos(x_angle)

        dx, dy = dx * d * 10, dy * d * 10

        self.__position += (dx, dy)
