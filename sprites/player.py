from time import time
from typing import Tuple, Union, List, Dict

from pyglet.text import Label

from events import CollisionEvent, UpdateEvent, TickUpdateEvent, DrawEvent, ScoreEvent
from objects import Collidable
from resources import Resources
from sprites.objects import PhysicalObject
from utils.classes import Position2D


# noinspection PySameParameterValue,PyUnusedClass
class Player(Collidable):
    def __init__(self, pos: Tuple[float, float], scene):
        """
        The player, is the main character in the game. You can control him with the arrows.
        :param pos:
        :param scene.window:
        :param batch:
        """
        
        self.scene = scene
        # self.position = pos
        sprite = PhysicalObject(img=Resources.get_resource("player"), batch=scene.batch, subpixel=True)

        super(Player, self).__init__(sprite)

        self.statsLabel = Label("Not loaded yet", "Helvetica", 16, anchor_x="left", anchor_y="top", batch=scene.batch, x=0,
                                y=scene.window.height, multiline=True, width=scene.window.width, bold=True)

        self.gameOverText = Label("", "Helvetica", 36, anchor_x="center", anchor_y="baseline", align="center",
                                  batch=scene.batch, x=scene.window.width / 2, y=scene.window.height / 2 - 50, multiline=True,
                                  width=scene.window.width, color=(255, 0, 0, 255), bold=True)
        self.gameOverInfo = Label("", "Helvetica", 22, anchor_x="center", anchor_y="top", align="center",
                                  batch=scene.batch, x=scene.window.width / 2, y=scene.window.height / 2 - 50, multiline=True,
                                  width=scene.window.width, color=(255, 127, 127, 255), bold=True)

        self.motionSpeedMultiply: int = 1
        self.rotationSpeedMultiply: int = 1
        self.rotation = 0

        self._score: int = 0
        self._lives: int = 10

        self.activeEffects = list()

        self.ghostMode = False

        self.__position: Position2D = Position2D(pos)

        DrawEvent.bind(self.draw)
        UpdateEvent.bind(self.update)
        TickUpdateEvent.bind(self.tick_update)
        CollisionEvent.bind(self.on_collision)

    def refresh(self):
        self.sprite.update(rotation=self.rotation, x=self.__position.x, y=self.__position.y)

    def add_effect(self, effect):
        if not effect.dead:
            self.activeEffects.append(effect)

    def rotate(self, dt, degrees):
        """
        Rotating the player
        :param dt:
        :param degrees:
        :return:
        """
        self.rotation += (degrees * dt * 45) * self.rotationSpeedMultiply
        if not self.dead:
            self.sprite.update(rotation=self.rotation)

    def draw(self, event):
        """
        Draw event
        :return:
        """
        if not self.dead:
            self.statsLabel.text = "Score: %s\nLives: %s\nEffects: %s" % (self._score, self._lives, self.activeEffects)
            self.statsLabel.draw()
        else:
            self.statsLabel.text = ""
            self.statsLabel.draw()

    def update(self, event: UpdateEvent):
        """
        Update event
        :return:
        """
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
        else:
            # print(f"ActiveEffects: {[i.dead for i in self.activeEffects]}")
            for effect in self.activeEffects:
                if effect.dead:
                    self.activeEffects.remove(effect)

    def tick_update(self, event):
        pass
        # if self._lives <= 0:
        #     pass
        # else:
        #     for effect in self.activeEffects:
        #         effect.tick_update(dt, scene.window, batch, self)

    def damage(self, lives):
        """
        Removes lives from the player
        :param lives:
        :return:
        """
        self._lives -= lives

    def gain_lives(self, lives):
        """
        Adds lives to the player
        :param lives:
        :return:
        """
        self._lives += lives

    @property
    def player_position(self):
        """
        Get player position

        :return:
        """
        return self.__position

    @player_position.setter
    def player_position(self, value: Union[
        Tuple[Union[float, int], Union[float, int]], List[Union[float, int]], Dict[str, Union[float, int]]]):
        """
        Set player position

        :param value:
        :return:
        """
        self.__position = self.__position.__init__(value)
        if not self.dead:
            self.sprite.update(x=self.__position.x, y=self.__position.y)

    def _remove_score(self, value):
        """
        Removes score, from the player

        :param value:
        :return:
        """
        self._score -= int(value)

    def _add_score(self, value):
        """
        Adding score to the player

        :param value:
        :return:
        """
        self._score += int(value)

    def remove_score(self, value):
        if not ScoreEvent.cancel_score:
            self._remove_score(value)
        ScoreEvent(-value, self.scene)
        
    def add_score(self, value):
        if not ScoreEvent.cancel_score:
            self._add_score(value)
        ScoreEvent(value, self.scene)

    def move_pixels(self, dt, pixels):
        """
        Move pixels, based on rotation

        :param dt:
        :param pixels:
        :return:
        """
        if not self.dead:
            import math

            d = dt * pixels  # distance covered this tick.
            angle_radians = -math.radians(-self.rotation)
            dx = -math.cos(angle_radians)
            dy = math.sin(angle_radians)

            dx, dy = dx * d * 10, dy * d * 10

            position = self.__position + (dx * self.motionSpeedMultiply, dy * self.motionSpeedMultiply)

            if self.sprite.width / 2 < position.x < self.scene.window.width - self.sprite.width / 2:
                self.__position.x = position.x
            elif not self.sprite.width / 2 < position.x:
                self.__position.x = self.sprite.width / 2
            elif not position.x < self.scene.window.width - self.sprite.width / 2:
                self.__position.x = self.scene.window.width - self.sprite.width / 2
            if self.sprite.height / 2 < position.y < self.scene.window.height - self.sprite.height / 2:
                self.__position.y = position.y
            elif not self.sprite.height / 2 < position.y:
                self.__position.y = self.sprite.height / 2
            elif not position.y < self.scene.window.height - self.sprite.height / 2:
                self.__position.y = self.scene.window.height - self.sprite.height / 2
            self.sprite.update(x=self.__position.x, y=self.__position.y)

    def handle_event(self, event):
        """
        Event handler

        :param event:
        :return:
        """
        if isinstance(event, CollisionEvent):
            self.on_collision(event)

    def on_collision(self, event: CollisionEvent):
        """
        Collision event handler

        :param event:
        :return:
        """
        # self.on_collision(event.scene.window, event.batch, event.otherObject)
        # for effect in self.activeEffects:
        #     effect.on_player_collision(event.scene.window, event.batch, self, event.otherObject)

    def move_to(self, x, y):
        """
        Teleportation effect, moves the player directly to the given position (x, y)

        :param x:
        :param y:
        :return:
        """
        self.__position.x = x
        self.__position.y = y
        if not self.dead:
            self.sprite.update(x=self.__position.x, y=self.__position.y)
