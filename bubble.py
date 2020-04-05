import random

from pyglet.sprite import Sprite

import globals as g
import utils
from events import CollisionEvent, DrawEvent, UpdateEvent, TickUpdateEvent, BubbleUpdateEvent, BubbleTickUpdateEvent, \
    PauseEvent, UnpauseEvent, ResizeEvent
from exceptions import UnlocalizedNameError
from objects import Collidable
from resources import Resources
from sprites.entity import Entity
from sprites.player import Player
from typinglib import Boolean, Float, String, Integer, Union
from utils.classes import Position2D


class Bubble(object):
    def __init__(self):
        self.speedMin: Float = 1
        self.speedMax: Float = 1

        self.health: Float = 0.5
        self.maxHealth: Float = 1.0
        self.scoreMultiplier: Float = 0.0
        self.attackMultiplier: Float = 0.0
        self.defenceMultiplier: Float = 1.0

        self.hideInPause: Boolean = False

    def check_unlocalized_name(self):
        if hasattr(g, "BUBBLE2NAME"):
            if self in g.BUBBLE2NAME.keys():
                return g.BUBBLE2NAME[self]
            else:
                raise UnlocalizedNameError(
                    f"There is no unlocalized name for object "
                    f"'{self.__name__ if isinstance(self, type) else self.__class__.__name__}'")
        else:
            raise UnlocalizedNameError("There are no unlocalized names defined!")

    def __call__(self, x, y, map, scene, size=None, speed=None):
        pass  # return BubbleObject(self, x, y, batch, size, speed)

    def set_unlocalized_name(self, name):
        if not hasattr(g, "NAME2BUBBLE"):
            g.NAME2BUBBLE = dict()
        if not hasattr(g, "BUBBLE2NAME"):
            g.BUBBLE2NAME = dict()
        g.NAME2BUBBLE[name]: Bubble = self
        g.BUBBLE2NAME[self]: String = name

    def get_unlocalized_name(self):
        if hasattr(g, "BUBBLE2NAME"):
            if self in g.BUBBLE2NAME.keys():
                return g.BUBBLE2NAME[self]
            else:
                raise UnlocalizedNameError("There is not unlocalized name for object '%s'"
                                           % self if isinstance(self, type) else type(self))
        else:
            raise UnlocalizedNameError("There are no unlocalized names defined!")

    def on_collision(self, event: CollisionEvent):
        pass

    def on_tick_update(self, event: TickUpdateEvent):
        pass


# noinspection PyUnusedLocal
class BubbleObject(Collidable):
    # noinspection SpellCheckingInspection
    def __init__(self, base_class, x, y, scene, size, speed,
                 attac_mp: Float = None, defen_mp: Float = None, regen_mp: Float = None, score_mp: Integer = 0):
        base_class: Bubble

        # Bubble resource
        bub_resource = Resources.get_resource("bubbles", base_class.get_unlocalized_name())

        # Calculate speed
        if speed is not None:
            pass
        else:
            slowest: Union[Integer, Float] = self.baseBubbleClass.speedMin
            speed: Float = float(slowest)

        # Calculate size
        if size:
            pass
        else:
            smallest: Integer = min(list(bub_resource.keys()))
            size: Integer = smallest

        # Get image from resource
        image = Resources.get_resource("bubbles", base_class.get_unlocalized_name(), size)

        # Properties
        self.health: Float = base_class.health
        self.maxHealth: Float = base_class.maxHealth
        self.speed: Float = speed
        self.size: Integer = size

        # Multipliers
        self.regenMultiplier: Float = 0.0
        self.scoreMultiplier: Integer = base_class.scoreMultiplier if score_mp is None else Integer(score_mp)
        self.attackMultiplier: Float = base_class.attackMultiplier if attac_mp is None else Float(attac_mp)
        self.defenceMultiplier: Float = base_class.defenceMultiplier if defen_mp is None else Float(defen_mp)

        # Baseclass object and name
        self.baseBubbleClass: Bubble = base_class
        self.name: String = self.baseBubbleClass.get_unlocalized_name()

        # States
        self.position: Position2D = Position2D((x, y))
        self.pause: Boolean = False

        # Sprite
        sprite: Entity = Entity(defence_mp=self.defenceMultiplier, attack_mp=self.attackMultiplier,
                                regen_mp=self.regenMultiplier, health=self.health, max_health=self.maxHealth,
                                image=image, x=x, y=y, batch=scene.batch)
        super(BubbleObject, self).__init__(sprite)

        # (Bubble) Image
        self.image = image

        # Event bindings
        DrawEvent.bind(self.draw)
        UpdateEvent.bind(self.update)
        CollisionEvent.bind(self.on_collision)
        PauseEvent.bind(self.on_pause)
        UnpauseEvent.bind(self.on_unpause)
        ResizeEvent.bind(self.on_resize)

    def on_resize(self, event: ResizeEvent):
        y_new = event.height * (self.position.y / event.oldHeight)
        x_new = event.width - (event.oldWidth - self.position.x)

        # print(f"RESIZE: {x_new, y_new}")
        self.position.y = y_new
        self.position.x = x_new

    def draw(self, event):
        self.sprite.draw()

    def on_unpause(self, event: PauseEvent):
        self.pause = False

    def on_pause(self, event: PauseEvent):
        self.pause = True

    def update(self, event: UpdateEvent):
        if not self.pause:
            if self.baseBubbleClass.get_unlocalized_name() == "kill_bubble":
                pass
                # print(self.sprite.dead)
                # print(self.sprite.health)
            if self.sprite.dead:
                self.dead = True
            if not self.dead:
                dx = -self.speed
                dy = 0

                speed_div = 10

                speed_multiply = (event.player.level / speed_div) + 0.4

                dx *= speed_multiply
                # noinspection PyUnboundLocalVariable
                self.position += ((dx * event.dt * (1 / utils.TICKS_PER_SEC)), dy * event.dt * (1 / utils.TICKS_PER_SEC))
                self.sprite.update(x=self.position.x, y=self.position.y)
            BubbleUpdateEvent(event.dt, self, event.scene)

    def on_collision(self, event: CollisionEvent):
        if not self.dead:
            if type(event.otherObject) == Player:
                if not event.otherObject.ghostMode:
                    obj: Player = event.otherObject
                    obj.addscore(((self.size / 2) + (self.speed / utils.TICKS_PER_SEC / 7))
                                  * self.baseBubbleClass.scoreMultiplier)

                    if hasattr(self.baseBubbleClass, "on_collision"):
                        self.baseBubbleClass.on_collision(event)

    def on_tick_update(self, event: TickUpdateEvent):
        if not self.dead:
            if hasattr(self.baseBubbleClass, "on_tick_update"):
                self.baseBubbleClass.on_tick_update(event)
        BubbleTickUpdateEvent(event.dt, self, event.scene)

    def unbind_events(self):
        DrawEvent.unbind(self.draw)
        UpdateEvent.unbind(self.update)
        CollisionEvent.unbind(self.on_collision)
        PauseEvent.unbind(self.on_pause)
        UnpauseEvent.unbind(self.on_unpause)
        ResizeEvent.unbind(self.on_resize)


class BubblePriorityCalculator(object):
    bubbles: dict = dict()
    totalPriority: int = 0

    @classmethod
    def add(cls, bubble, priority):
        cls.totalPriority += priority
        cls.bubbles[bubble] = (cls.totalPriority - priority, cls.totalPriority)

    @classmethod
    def get(cls, rand=random):
        rand = rand.randint(0, cls.totalPriority)

        for bubble, priority in cls.bubbles.items():
            priority_min, priority_max = priority
            if priority_min <= rand <= priority_max:
                return bubble
