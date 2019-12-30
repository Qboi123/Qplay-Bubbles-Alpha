import pyglet

import resources


class Bubble(object):
    def __init__(self, parent, x, y, batch, image):
        self.sprite, parent.sprite = pyglet.sprite.Sprite(img=image,
                                            x=x, y=y, batch=batch)
