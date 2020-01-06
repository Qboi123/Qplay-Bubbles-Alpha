import pyglet
from typing import Tuple, Union, List, Dict

import resources
from objects import Collidable
from sprites.objects import PhysicalObject
from utils import PLAYER_SPEED
from utils.classes import Position2D


class Player(Collidable):
    def __init__(self, pos: Tuple[float, float], batch):
        # self.position = pos
        sprite = PhysicalObject(img=resources.player, batch=batch, subpixel=True)

        super(Player, self).__init__(sprite)

        self.rotation = 0
        # self.sprite: pyglet.sprite.Sprite = pyglet.sprite.Sprite(resources.player, batch=batch)
        # self.sprite.position = pos

        self.__position: Position2D = Position2D(pos)

    def rotate(self, degrees):
        # print(self.sprite.rotation)
        self.rotation += degrees
        self.sprite.update(rotation=self.rotation)

    def draw(self):
        # super(PhysicalObject, self).update(self.position.x, self.position.y, self.rotation - 90, 1.2)
        pass

    @property
    def player_position(self):
        return self.__position

    @player_position.setter
    def player_position(self, value: Union[
            Tuple[Union[float, int], Union[float, int]], List[Union[float, int]], Dict[str, Union[float, int]]]):
        self.__position = self.__position.__init__(value)
        self.sprite.update(x=self.__position.x, y=self.__position.y)

    # def set_position(self, pos):
    #     self.__position.__init__(pos)
    #     super(PhysicalObject, self).update(x=self.__position.x, y=self.__position.y)

    def move_pixels(self, dt, pixels):
        rot_x = self.rotation
        import math

        d = dt * pixels  # distance covered this tick.
        # strafe = math.degrees(math.atan(pixels))
        angle_radians = -math.radians(-self.rotation)
        dx = -math.cos(angle_radians)
        dy = math.sin(angle_radians)
        # dx = math.sin(x_angle)
        # dy = math.cos(x_angle)

        dx, dy = dx * d * 10, dy * d * 10

        self.__position += (dx, dy)
        self.sprite.update(x=self.__position.x, y=self.__position.y)
