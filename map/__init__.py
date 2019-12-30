from typing import Dict

from bubble import Bubble


class World():
    bubbles: Dict[str, Bubble]
    def __init__(self, ):
        pass

    def create_bubble(self, x, y):
        new_asteroid = pyglet.sprite.Sprite(img=resources.asteroid_image,
                                            x=asteroid_x, y=asteroid_y)

    def show_bubble(self):
        pass