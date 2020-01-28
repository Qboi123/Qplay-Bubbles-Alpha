from time import time
from typing import Tuple, Union, List, Dict

from pyglet.text import Label

from events import CollisionEvent, UpdateEvent, TickUpdateEvent, DrawEvent, ScoreEvent, PauseEvent, \
    PlayerCollisionEvent, UnpauseEvent
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
        # Scene
        self.scene = scene

        # Sprite
        sprite = PhysicalObject(img=Resources.get_resource("player"), batch=scene.batch, subpixel=True)

        super(Player, self).__init__(sprite)

        # Labels and texts
        self.statsLabel = Label("Not loaded yet", "Helvetica", 14, anchor_x="left", anchor_y="baseline", batch=scene.batch, x=0,
                                y=scene.window.height-32, multiline=True, width=scene.window.width, bold=True,
                                color=(255, 255, 255, 127))

        self.gameOverText = Label("", "Helvetica", 36, anchor_x="center", anchor_y="baseline", align="center",
                                  batch=scene.batch, x=scene.window.width / 2, y=scene.window.height / 2 - 50, multiline=True,
                                  width=scene.window.width, color=(255, 0, 0, 255), bold=True)
        self.gameOverInfo = Label("", "Helvetica", 22, anchor_x="center", anchor_y="top", align="center",
                                  batch=scene.batch, x=scene.window.width / 2, y=scene.window.height / 2 - 50, multiline=True,
                                  width=scene.window.width, color=(255, 127, 127, 255), bold=True)

        # Multipliers
        self.motionSpeedMultiply: int = 1
        self.rotationSpeedMultiply: int = 1

        # Stats
        self.score: int = 0
        self.lives: int = 10

        # Active effects
        self.activeEffects = list()

        # Modes
        self.ghostMode = False

        # Position and rotation
        self.rotation = 0
        self.position: Position2D = Position2D(pos)

        # Pause variable
        self.pause = False

        # Normal Events
        DrawEvent.bind(self.draw)
        UpdateEvent.bind(self.update)
        TickUpdateEvent.bind(self.tick_update)
        CollisionEvent.bind(self.on_collision)

        # Pause Events
        PauseEvent.bind(self.on_pause)
        UnpauseEvent.bind(self.on_unpause)

    def on_pause(self, event: PauseEvent):
        self.pause = True

    def on_unpause(self, event: UnpauseEvent):
        self.pause = False

    def refresh(self):
        self.sprite.update(rotation=self.rotation, x=self.position.x, y=self.position.y)

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
        if not self.pause:
            self.rotation += (degrees * dt * 45) * self.rotationSpeedMultiply
            if not self.dead:
                self.sprite.update(rotation=self.rotation)

    def draw(self, event):
        """
        Draw event
        :return:
        """
        if not self.dead:
            self.statsLabel.text = "Score: %s\nLives: %s" % (self.score, self.lives)
            self.statsLabel.draw()
        else:
            self.statsLabel.text = ""
            self.statsLabel.draw()

    def update(self, event: UpdateEvent):
        """
        Update event
        :return:
        """
        if self.lives <= 0:  # Game over
            if not self.dead:  # Game over screen not active
                # Texts and labels
                self.gameOverText.text = "GAME OVER"
                self.gameOverText.draw()
                self.gameOverInfo.text = "Score: %s" % self.score
                self.gameOverInfo.draw()
                self.gameOverTime = time() + 0.5

                # Delete sprite
                self.sprite.delete()

                # Player is dead
                self.dead = True
            elif self.dead:
                # Change colros
                if self.gameOverTime <= time():
                    if self.gameOverText.color == (255, 0, 0, 255):  # If it's red
                        # Set to orange
                        self.gameOverText.color = (255, 127, 0, 255)
                        self.gameOverInfo.color = (255, 191, 127, 255)
                    elif self.gameOverText.color == (255, 127, 0, 255):  # If it's orange
                        # Set to red
                        self.gameOverText.color = (255, 0, 0, 255)
                        self.gameOverInfo.color = (255, 127, 127, 255)

                    # Interval
                    self.gameOverTime = time() + 0.5
                    self.gameOverText.draw()
                    self.gameOverInfo.draw()
        else:
            if not self.pause:
                # print(f"ActiveEffects: {[i.dead for i in self.activeEffects]}")
                for effect in self.activeEffects:
                    if effect.dead:
                        self.activeEffects.remove(effect)

    def tick_update(self, event):
        pass
        # if self.lives <= 0:
        #     pass
        # else:
        #     for appliedEffect in self.activeEffects:
        #         appliedEffect.tick_update(dt, scene.window, batch, self)

    def damage(self, lives):
        """
        Removes lives from the player
        :param lives:
        :return:
        """
        self.lives -= lives

    def gainlives(self, lives):
        """
        Adds lives to the player
        :param lives:
        :return:
        """
        self.lives += lives

    @property
    def player_position(self):
        """
        Get player position

        :return:
        """
        return self.position

    @player_position.setter
    def player_position(self, value: Union[
        Tuple[Union[float, int], Union[float, int]], List[Union[float, int]], Dict[str, Union[float, int]]]):
        """
        Set player position

        :param value:
        :return:
        """
        self.position = self.position.__init__(value)
        if not self.dead:
            self.sprite.update(x=self.position.x, y=self.position.y)

    def _removescore(self, value):
        """
        Removes score, from the player

        :param value:
        :return:
        """
        self.score -= int(value)

    def _addscore(self, value):
        """
        Adding score to the player

        :param value:
        :return:
        """
        self.score += int(value)

    def removescore(self, value):
        if not ScoreEvent.cancelscore:
            self._removescore(value)
        ScoreEvent(-value, self.scene)

    def addscore(self, value):
        if not ScoreEvent.cancelscore:
            self._addscore(value)
        ScoreEvent(value, self.scene)

    def move_pixels(self, dt, pixels):
        """
        Move pixels, based on rotation

        :param dt:
        :param pixels:
        :return:
        """
        if not self.pause:
            if not self.dead:
                import math

                d = dt * pixels  # distance covered this tick.
                angle_radians = -math.radians(-self.rotation)
                dx = -math.cos(angle_radians)
                dy = math.sin(angle_radians)

                dx, dy = dx * d * 10, dy * d * 10

                position = self.position + (dx * self.motionSpeedMultiply, dy * self.motionSpeedMultiply)

                if self.sprite.width / 2 < position.x < self.scene.window.width - self.sprite.width / 2:
                    self.position.x = position.x
                elif not self.sprite.width / 2 < position.x:
                    self.position.x = self.sprite.width / 2
                elif not position.x < self.scene.window.width - self.sprite.width / 2:
                    self.position.x = self.scene.window.width - self.sprite.width / 2
                if self.sprite.height / 2 < position.y < self.scene.window.height - self.sprite.height / 2 - 72:
                    self.position.y = position.y
                elif not self.sprite.height / 2 < position.y:
                    self.position.y = self.sprite.height / 2
                elif not position.y < self.scene.window.height - self.sprite.height / 2 - 72:
                    self.position.y = self.scene.window.height - self.sprite.height / 2 - 72
                self.sprite.update(x=self.position.x, y=self.position.y)

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
        PlayerCollisionEvent(self, event.otherObject, event.scene)
        # self.on_collision(event.scene.window, event.batch, event.otherObject)
        # for appliedEffect in self.activeEffects:
        #     appliedEffect.on_player_collision(event.scene.window, event.batch, self, event.otherObject)

    def move_to(self, x, y):
        """
        Teleportation appliedEffect, moves the player directly to the given position (x, y)

        :param x:
        :param y:
        :return:
        """
        if not self.pause:
            self.position.x = x
            self.position.y = y
            if not self.dead:
                self.sprite.update(x=self.position.x, y=self.position.y)
