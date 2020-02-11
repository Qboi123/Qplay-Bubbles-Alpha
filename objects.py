from pyglet.graphics import Batch
from pyglet.window import Window

import utils
from events import CollisionEvent
from sprites.entity import Entity
from utils.advBuiltins import AdvFloat


class Collidable(object):
    def __init__(self, sprite):
        self.sprite: Entity = sprite
        self.dead = False

    def collides_with(self, other_object):
        """Determine if this object collides with another"""

        # # Ignore bullet collisions if we're supposed to
        # if not self.reacts_to_bullets and other_object.is_bullet:
        #     return False
        # if self.is_bullet and not other_object.reacts_to_bullets:
        #     return False

        # Calculate distance between object centers that would be a collision,
        # assuming square resources
        collision_distance = AdvFloat(self.sprite.image.width * 0.5 * self.sprite.scale + other_object.sprite.image.width * 0.5\
            * other_object.sprite.scale)

        # Get distance using position tuples
        actual_distance = utils.distance(self.sprite.position, other_object.sprite.position)

        return actual_distance <= collision_distance

    def on_collision(self, event: CollisionEvent):
        pass
