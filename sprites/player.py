from time import time
from typing import Tuple, Union, List, Dict, Callable, Optional

from pyglet.text import Label

from effects import AppliedEffect
from events import CollisionEvent, UpdateEvent, TickUpdateEvent, DrawEvent, ScoreEvent, PauseEvent, \
    PlayerCollisionEvent, UnpauseEvent, ResizeEvent
from objects import Collidable
from resources import Resources
from sprites.entity import Entity
from typinglib import Bool, Float, Integer, Boolean, Property
from utils.advBuiltins import AdvFloat, AdvInteger
from utils.classes import Position2D


# noinspection PySameParameterValue,PyUnusedClass,PyUnusedLocal
class Player(Collidable):
    def __init__(self, pos: Tuple[float, float], scene, health: Float = 50.0):
        """
        The player, is the main character in the game. You can control him with the arrows.
        :param pos:
        :param scene.window:
        """

        # Scene
        self.scene = scene

        # Sprite
        sprite: Entity = Entity(1.0, 1.0, 1.0, health, 50.0, image=Resources.get_resource("player"),
                                batch=scene.playerBatch, subpixel=True)

        super(Player, self).__init__(sprite)

        # Labels and texts
        self.statsLabel: Label = Label("Not loaded yet", "Helvetica", 14, anchor_x="left", anchor_y="top",
                                       batch=scene.foregroundBatch, x=0, y=scene.window.height, multiline=True,
                                       width=scene.window.width, bold=True, color=(255, 255, 255, 127))
        self.gameOverText: Label = Label("", "Helvetica", 36, anchor_x="center", anchor_y="baseline", align="center",
                                         batch=scene.foregroundBatch, x=scene.window.width / 2,
                                         y=scene.window.height / 2 - 50, multiline=True,
                                         width=scene.window.width, color=(255, 0, 0, 255), bold=True)
        self.gameOverInfo: Label = Label("", "Helvetica", 22, anchor_x="center", anchor_y="top", align="center",
                                         batch=scene.foregroundBatch, x=scene.window.width / 2,
                                         y=scene.window.height / 2 - 50, multiline=True,
                                         width=scene.window.width, color=(255, 127, 127, 255), bold=True)

        # Multipliers
        self.motionSpeedMultiply: AdvFloat = AdvFloat(1.0)
        self.rotationSpeedMultiply: AdvFloat = AdvFloat(1.0)
        self.scoreMultiply: AdvInteger = AdvInteger(1)
        self.defenceMultiplier: Property = Property(self.get_defence, self.set_defence)
        self.attackMultiplier: Property = Property(self.get_attack, self.set_attack)
        self.regenMultiplier: Property = Property(self.get_regen, self.set_regen)

        # Stats
        self.score: AdvInteger = AdvInteger(0)
        self.level: AdvInteger = AdvInteger(1)
        self.health: Property = Property(self.get_health, self.set_health)

        # Active effects
        self.activeEffects: List[AppliedEffect] = list()

        # Abilities
        self.ghostMode: Bool = False

        # Position and rotation
        self.rotation: AdvFloat = AdvFloat(0.0)
        self.position: Position2D = Position2D(pos)

        # Pause variable
        self.pause: Boolean = False

        # Hooks
        self.damageHook: Optional[Callable] = None
        self.gainLivesHook: Optional[Callable] = None
        self.removeScoreHook: Optional[Callable] = None
        self.addScoreHook: Optional[Callable] = None

        # Normal Events
        DrawEvent.bind(self.draw)
        UpdateEvent.bind(self.update)
        CollisionEvent.bind(self.on_collision)
        TickUpdateEvent.bind(self.tick_update)
        ResizeEvent.bind(self.on_resize)

        # Pause Events
        PauseEvent.bind(self.on_pause)
        UnpauseEvent.bind(self.on_unpause)

    def get_regen(self):
        return self.sprite.regenMultiplier

    def set_regen(self, value):
        self.sprite.regenMultiplier = value

    def get_attack(self):
        return self.sprite.attackMultiplier

    def set_attack(self, value):
        self.sprite.attackMultiplier = value

    def get_defence(self):
        return self.sprite.defenceMultiplier

    def set_defence(self, value):
        self.sprite.defenceMultiplier = value

    def get_health(self):
        return self.sprite.health

    def set_health(self, value):
        self.sprite.health = value

    def get_max_health(self):
        return self.sprite.maxHealth

    def set_max_health(self, value):
        self.sprite.maxHealth = value

    def regen(self, value):
        self.sprite.regen(value)

    def damage(self, atk: Union[Float, Integer]):
        if self.damageHook is not None:
            return self.damageHook(atk)
        self.sprite.damage(atk)

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
                self.sprite.update(rotation=self.rotation)\

    def on_resize(self, event: ResizeEvent):
        y_new = event.height * (self.position.y / event.oldHeight)
        x_new = event.width - (event.oldWidth - self.position.x)

        # print(f"RESIZE: {x_new, y_new}")
        self.position.y = y_new
        self.position.x = x_new

    def draw(self, event):
        """
        Draw event
        :return:
        """
        if not self.dead:
            self.statsLabel.text = f"Score: {self.score}\nLevel: {self.level}\nHP: {int(self.get_health())} / {int(self.sprite.maxHealth)}"
            self.statsLabel.draw()
        else:
            self.statsLabel.text = f"\nLevel: {self.level}\nHP: {self.get_health()} / {self.sprite.maxHealth}"
            self.statsLabel.draw()

    def update(self, event: UpdateEvent):
        """
        Update event
        :return:
        """
        # print(self.sprite.dead)
        if self.sprite.dead:  # Game over
            # print(f"GAME OVER CHECK FOR DEAD={not self.dead}")
            if not self.dead:  # Game over screen not active
                # Texts and labels
                self.gameOverText.text = "GAME OVER"
                self.gameOverText.draw()
                self.gameOverInfo.text = f"Score: {self.score}"
                self.gameOverInfo.draw()
                self.gameOverTime = time() + 0.5

                # print("PLAYER DEAD")
                self.sprite.delete()

                # Player is dead
                self.dead = True

                # print(f"PLAYER DEAD={self.dead}")
                event.scene.scene_manager.save.delete_save()
            elif self.dead:
                # Change colors
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
                    # noinspection PyAttributeOutsideInit
                    self.gameOverTime = time() + 0.5
                    self.gameOverText.draw()
                    self.gameOverInfo.draw()
        else:
            if not self.pause:
                # print(f"ActiveEffects: {[i.dead for i in self.activeEffects]}")
                for effect in self.activeEffects:
                    if effect.dead:
                        self.activeEffects.remove(effect)
            self.sprite.update(x=self.position.x, y=self.position.y)

    def tick_update(self, event):
        pass

    @property
    def player_position(self):
        """
        Get player position

        :return:
        """
        return self.position

    @player_position.setter
    def player_position(self, value: Union[Tuple[Union[float, int], Union[float, int]],
                                           List[Union[float, int]], Dict[str, Union[float, int]]]):
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
        if self.removeScoreHook:
            return self.removeScoreHook(self, value)

        self.score -= int(value)

    def _addscore(self, value):
        """
        Adding score to the player

        :param value:
        :return:
        """
        if self.addScoreHook:
            return self.addScoreHook(self, value)

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
        # if hasattr(event.otherObject, "sprite"):
        #     if isinstance(event.otherObject.sprite, Entity):
        #         event.otherObject.sprite.damage(self.attackMultiplier)
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
