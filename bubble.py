import random

from pyglet.graphics import Batch
from pyglet.sprite import Sprite
from pyglet.window import Window

import globals as g
import utils
from events import CollisionEvent, DrawEvent, UpdateEvent, TickUpdateEvent
from exceptions import UnlocalizedNameError
from objects import Collidable
from resources import Resources
from sprites.player import Player
from utils.classes import Position2D


class Bubble(object):
    def __init__(self):
        self.speedMin: float = 1
        self.speedMax: float = 1
        self.scoreMultiplier: float = 0

    def __call__(self, x, y, map, batch, size=None, speed=None):
        pass  # return BubbleObject(self, x, y, batch, size, speed)

    def set_unlocalized_name(self, name):
        if not hasattr(g, "NAME2BUBBLE"):
            g.NAME2BUBBLE = dict()
        if not hasattr(g, "BUBBLE2NAME"):
            g.BUBBLE2NAME = dict()
        g.NAME2BUBBLE[name] = self
        g.BUBBLE2NAME[self] = name

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


class BubbleObject(Collidable):
    def __init__(self, base_class, x, y, batch, size, speed):
        parent: BubbleObject

        self.scoreMultiplier = 0

        self.baseBubbleClass: Bubble = base_class
        self.name = self.baseBubbleClass.get_unlocalized_name()

        bub_resource = Resources.get_resource("bubbles", self.name)

        if speed is not None:
            pass
        else:
            slowest = self.baseBubbleClass.speedMin
            speed = slowest

        if size:
            pass
        else:
            smallest = min(list(bub_resource.keys()))
            size = smallest
        image = Resources.get_resource("bubbles", self.name, size)

        if self.name == "ultra_bubble":
            print(f"Size: {size}")

        # Properties
        self.speed = speed
        self.size = size

        self.position: Position2D = Position2D((x, y))

        sprite: Sprite = Sprite(img=image, x=x, y=y, batch=batch)
        super(BubbleObject, self).__init__(sprite)

        self.image = image

        DrawEvent.bind(self.draw)
        UpdateEvent.bind(self.update)
        CollisionEvent.bind(self.on_collision)

    def draw(self, event):
        pass
        # self.sprite.update(self.sprite.x, self.sprite.y, self.sprite.rotation, self.sprite.scale,
        #                    self.sprite.scale_x, self.sprite.scale_y)

    def update(self, event: UpdateEvent):
        if not self.dead:
            dx = -self.speed
            dy = 0

            speed_multiply = event.player._score / 10000
            if speed_multiply < 0.5:
                speed_multiply = 0.5

            dx *= speed_multiply

            # noinspection PyUnboundLocalVariable
            self.position += (dx * event.dt * utils.TICKS_PER_SEC, dy * event.dt * utils.TICKS_PER_SEC)
            self.sprite.update(x=self.position.x, y=self.position.y)

    def on_collision(self, event: CollisionEvent):
        if (not self.dead) and (not event.player.ghostMode):
            if type(event.otherObject) == Player:
                obj: Player = event.otherObject
                obj.add_score(((self.size / 2) + (self.speed / utils.TICKS_PER_SEC / 7))
                              * self.baseBubbleClass.scoreMultiplier)

                if hasattr(self.baseBubbleClass, "on_collision"):
                    self.baseBubbleClass.on_collision(event)

                self.dead = True

    def on_tick_update(self, event: TickUpdateEvent):
        if not self.dead:
            if hasattr(self.baseBubbleClass, "on_tick_update"):
                self.baseBubbleClass.on_tick_update(event)

    def unbind_events(self):
        DrawEvent.unbind(self.draw)
        UpdateEvent.unbind(self.update)
        CollisionEvent.unbind(self.on_collision)


class BubblePriorityCalculator(object):
    bubbles: dict = dict()
    totalPriority: int = 0

    @classmethod
    def add(cls, bubble, priority):
        cls.totalPriority += priority
        cls.bubbles[bubble] = (cls.totalPriority - priority, cls.totalPriority)

    @classmethod
    def get(cls, random=random):
        rand = random.randint(0, cls.totalPriority)

        for bubble, priority in cls.bubbles.items():
            priority_min, priority_max = priority
            if priority_min <= rand <= priority_max:
                return bubble
