from typing import Dict

import pyglet
from opensimplex import OpenSimplex

import sprites
from bubble import Bubble
from utils import randint_lookup


class Map(object):
    def __init__(self):
        self.tick_updates = 0
        self.bubbles: Dict[int, Bubble] = {}

    def create_bubble(self, x, y, bubbles_list, batch):
        bubble_rand = OpenSimplex(4096).noise2d(self.tick_updates, 0)
        bubble_randint = randint_lookup(bubble_rand, 0, 65535)

        size_rand = OpenSimplex(4096).noise2d(self.tick_updates, 1)
        size_randint = randint_lookup(size_rand, 10, 60)  # size_rand * 50 + 10

        for bubble in bubbles_list:
            if bubble.randomMin <= bubble_randint <= bubble.randomMax:
                bub = bubble(x, y, batch, size_randint)
                self.bubbles[self.tick_updates] = bub
                bub.draw()
                break

    def draw(self):
        for bubble in list(self.bubbles.values()):
            bubble.draw()

    def update(self, dt):
        # print(self.bubbles)
        for bubble in list(self.bubbles.values()):
            bubble.update(dt)

    def tick_update(self, dt, window: pyglet.window.Window, batch: pyglet.graphics.Batch):
        print("UPDATE")
        y_rand = OpenSimplex(4096).noise2d(self.tick_updates, 2)
        size_randint = randint_lookup(y_rand, 0, window.height)
        self.create_bubble(window.width, size_randint, sprites.BUBBLES, batch)
        self.tick_updates += 1
