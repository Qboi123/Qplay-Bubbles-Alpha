import utils


class Collidable(object):
    def __init__(self, sprite):
        self.sprite = sprite
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
        collision_distance = self.sprite.image.width * 0.5 * self.sprite.scale + other_object.sprite.image.width * 0.5\
            * other_object.sprite.scale

        # Get distance using position tuples
        actual_distance = utils.distance(self.sprite.position, other_object.sprite.position)

        return actual_distance <= collision_distance

    def handle_collision_with(self, other_object):
        pass