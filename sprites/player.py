import pyglet
from typing import Tuple, Union, List, Dict

from pyglet.text import Label

import resources
from objects import Collidable
from sprites.objects import PhysicalObject
from utils import PLAYER_SPEED
from utils.classes import Position2D


class Player(Collidable):
    def __init__(self, pos: Tuple[float, float], window, batch):
        # self.position = pos
        sprite = PhysicalObject(img=resources.player, batch=batch, subpixel=True)

        super(Player, self).__init__(sprite)

        self.label = Label("Not loaded yet", "Helvetica", 16, anchor_x="left", anchor_y="top", batch=batch, x=0, y=window.height, multiline=True, width=window.width, bold=True)

        self.gameover_lbl1 = Label("", "Helvetica", 28, anchor_x="center", anchor_y="baseline", align="center", batch=batch, x=window.width/2, y=window.height/2 - 50, multiline=True, width=window.width, color=(255, 0, 0, 255), bold=True)

        self.rotation = 0
        # self.sprite2: pyglet.sprite.Sprite = pyglet.sprite.Sprite(resources.player, batch=batch)
        # self.sprite2.position = pos

        self._score: int = 0
        self._lives: int = 7

        self.__position: Position2D = Position2D(pos)

    def rotate(self, degrees):
        # print(self.sprite.rotation)
        self.rotation += degrees
        if not self.dead:
            self.sprite.update(rotation=self.rotation)

    def draw(self):
        # super(PhysicalObject, self).update(self.position.x, self.position.y, self.rotation - 90, 1.2)
        self.label.text = "Score: %s\nLives: %s" % (self._score, self._lives)
        self.label.draw()

    def update(self, dt):
        if self._lives <= 0:
            if not self.dead:
                self.gameover_lbl1.text = "GAME OVER"
                self.gameover_lbl1.draw()
                self.sprite.delete()
                self.dead = True

    def damage(self, lives):
        self._lives -= lives

    def gain_lives(self, lives):
        self._lives += lives

    @property
    def player_position(self):
        return self.__position

    @player_position.setter
    def player_position(self, value: Union[
            Tuple[Union[float, int], Union[float, int]], List[Union[float, int]], Dict[str, Union[float, int]]]):
        self.__position = self.__position.__init__(value)
        if not self.dead:
            self.sprite.update(x=self.__position.x, y=self.__position.y)

    # def set_position(self, pos):
    #     self.__position.__init__(pos)
    #     super(PhysicalObject, self).update(x=self.__position.x, y=self.__position.y)

    def remove_score(self, value):
        self._score -= int(value)

    def add_score(self, value):
        self._score += int(value)

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
        if not self.dead:
            self.sprite.update(x=self.__position.x, y=self.__position.y)
