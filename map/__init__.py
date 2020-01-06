from typing import Dict, List

import pyglet
from opensimplex import OpenSimplex

import sprites
from bubble import BubbleObject, Bubble
from sprites.objects import PhysicalObject
from utils import randint_lookup


class Map(object):
    def __init__(self):
        self.tick_updates = 0
        self.bubbles: List[BubbleObject] = []

    def create_random_bubble(self, x, y, bubbles_list, batch, objects):
        bubble_rand = OpenSimplex(4096).noise2d(self.tick_updates, 0)
        bubble_randint = randint_lookup(bubble_rand, 0, 65535)

        size_rand = OpenSimplex(4096).noise2d(self.tick_updates, 1)
        size_randint = randint_lookup(size_rand, 21, 80)  # size_rand * 50 + 10

        for bubble in bubbles_list:
            if bubble.randomMin <= bubble_randint <= bubble.randomMax:
                objects.append(self.create_bubble(x + size_randint / 2, y, bubble, batch, size_randint))
                break

    def remove_bubble(self, obj: BubbleObject, objects: list):
        objects.remove(obj)
        obj.sprite.delete()
        self.bubbles.remove(obj)

    def create_bubble(self, x, y, bubble, batch, size):
        bub = bubble(x, y, self, batch, size)
        self.bubbles.append(bub)
        bub.draw()
        return bub

    def draw(self):
        for bubble in self.bubbles:
            bubble.draw()

    def update(self, dt, window: pyglet.window.Window, batch: pyglet.graphics.Batch, objects):
        # print(self.bubbles)
        for bubble in self.bubbles:
            bubble.update(dt)
            if bubble.position.x < (0 - bubble.size / 2):
                self.remove_bubble(bubble, objects)
            if bubble.dead == True:
                self.remove_bubble(bubble, objects)

    def tick_update(self, dt, window: pyglet.window.Window, batch: pyglet.graphics.Batch, objects):
        # print("UPDATE")
        y_rand = OpenSimplex(4096).noise2d(self.tick_updates, 2)
        size_randint = randint_lookup(y_rand, 0, window.height)
        self.create_random_bubble(window.width, size_randint, sprites.BUBBLES, batch, objects)
        self.tick_updates += 1
