from pyglet.sprite import Sprite

import globals as g
import resources
import utils
from assets.exceptions import UnlocalizedNameError
from objects import Collidable
from sprites.objects import PhysicalObject
from sprites.player import Player
from utils.classes import Position2D


class Bubble(object):
    def __init__(self):
        pass

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


class BubbleObject(Collidable):
    def __init__(self, base_class, x, y, batch, size):
        parent: BubbleObject

        self.scoreMultiplier = 0

        self.baseBubbleClass = base_class
        self.name = self.baseBubbleClass.get_unlocalized_name()

        bub_resource = resources.bubbles[self.name]

        if size:
            pass
        else:
            smallest = min(list(bub_resource.keys()))
            size = smallest
        image = bub_resource[size]

        self.size = size

        # print(image, x, y, batch)
        self.position: Position2D = Position2D((x, y))

        sprite: Sprite = Sprite(img=image, x=x, y=y, batch=batch)
        super(BubbleObject, self).__init__(sprite)

        self.image = image

    def draw(self):
        self.sprite.update(self.sprite.x, self.sprite.y, self.sprite.rotation, self.sprite.scale,
                           self.sprite.scale_x, self.sprite.scale_y)
        # print("Draw")

    def update(self, dt):
        # dx, dy = self.sprite.position

        # if self.baseBubbleClass.direction == WEST:
        #     dx = self.baseBubbleClass.speed
        # if self.baseBubbleClass.direction == EAST:
        #     dx = self.baseBubbleClass.speed
        # if self.baseBubbleClass.direction == NORTH:
        #     dy = self.baseBubbleClass.speed
        # if self.baseBubbleClass.direction == SOUTH:
        #     dy = self.baseBubbleClass.speed

        dx = -self.baseBubbleClass.speed
        dy = 0

        # print(self.direction)

        # self.sprite.position = (x * dt, y * dt)
        # noinspection PyUnboundLocalVariable
        self.position += (dx * dt * utils.TICKS_PER_SEC, dy * dt * utils.TICKS_PER_SEC)
        self.sprite.update(x=self.position.x, y=self.position.y)
        # print("Update")

    def handle_collision_with(self, other_object):
        if type(other_object) == Player:
            other_object: Player

            print("%s has collision with %s" % (repr(self), repr(other_object)))
            # other_object.add_score(((self.size / 2) + (self.speed / 5 / 7)) * self.scoreMultiplier)

            self.dead = True
