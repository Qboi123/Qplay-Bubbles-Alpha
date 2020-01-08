from time import time

import pyglet
from typing import Tuple, Union, List, Dict

from pyglet.text import Label

from events import CollisionEvent
from objects import Collidable
from resources import Resources
from sprites.objects import PhysicalObject
from utils import PLAYER_SPEED
from utils.classes import Position2D


class Player(Collidable):
    def __init__(self, pos: Tuple[float, float], window, batch):
        # self.position = pos
        sprite = PhysicalObject(img=Resources.get_resource("player"), batch=batch, subpixel=True)

        super(Player, self).__init__(sprite)

        self.statsLabel = Label("Not loaded yet", "Helvetica", 16, anchor_x="left", anchor_y="top", batch=batch, x=0,
                                y=window.height, multiline=True, width=window.width, bold=True)

        self.gameOverText = Label("", "Helvetica", 36, anchor_x="center", anchor_y="baseline", align="center",
                                  batch=batch, x=window.width / 2, y=window.height / 2 - 50, multiline=True,
                                  width=window.width, color=(255, 0, 0, 255), bold=True)
        self.gameOverInfo = Label("", "Helvetica", 22, anchor_x="center", anchor_y="top", align="center",
                                  batch=batch, x=window.width / 2, y=window.height / 2 - 50, multiline=True,
                                  width=window.width, color=(255, 127, 127, 255), bold=True)

        self.rotation = 0
        # self.sprite2: pyglet.sprite.Sprite = pyglet.sprite.Sprite(resources.player, batch=batch)
        # self.sprite2.position = pos

        self._score: int = 0
        self._lives: int = 10

        self.activeEffects = list()

        self.__position: Position2D = Position2D(pos)

    def rotate(self, dt, degrees):
        # print(self.sprite.rotation)
        self.rotation += degrees * dt * 45
        if not self.dead:
            self.sprite.update(rotation=self.rotation)

    def draw(self):
        # super(PhysicalObject, self).update(self.position.x, self.position.y, self.rotation - 90, 1.2)
        if not self.dead:
            self.statsLabel.text = "Score: %s\nLives: %s" % (self._score, self._lives)
            self.statsLabel.draw()
        else:
            self.statsLabel.text = ""
            self.statsLabel.draw()

    def update(self, dt):
        if self._lives <= 0:
            if not self.dead:
                self.gameOverText.text = "GAME OVER"
                self.gameOverText.draw()
                self.gameOverInfo.text = "Score: %s" % self._score
                self.gameOverInfo.draw()
                self.gameOverTime = time() + 0.5
                self.sprite.delete()
                self.dead = True
            elif self.dead:
                if self.gameOverTime <= time():
                    if self.gameOverText.color == (255, 0, 0, 255):
                        self.gameOverText.color = (255, 127, 0, 255)
                        self.gameOverInfo.color = (255, 191, 127, 255)
                    elif self.gameOverText.color == (255, 127, 0, 255):
                        self.gameOverText.color = (255, 0, 0, 255)
                        self.gameOverInfo.color = (255, 127, 127, 255)

                    self.gameOverTime = time() + 0.5
                    self.gameOverText.draw()
                    self.gameOverInfo.draw()

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

    def handle_event(self, event):
        if isinstance(event, CollisionEvent):
            self.on_collision(event)

    def on_collision(self, event: CollisionEvent):
        self.handle_collision_with(event.otherObject)
        for effect in self.activeEffects:
            effect.on_effect_stopped()
