import random
from time import time
from typing import Dict, List

import pyglet
from opensimplex import OpenSimplex

import sprites
from bubble import BubbleObject, Bubble, BubblePriorityCalculator
from events import TickUpdateEvent, UpdateEvent, DrawEvent, BubbleRemoveEvent
from noise import SimplexNoiseGen
from sprites.objects import PhysicalObject
from utils import randint_lookup, MIN_BUBBLE_SIZE, MAX_BUBBLE_SIZE


class Map(object):
    def __init__(self):
        self._bubCreateInterval = 0.1
        self._bubCreateTime = time() + self._bubCreateInterval
        self.tick_updates = 0
        self.bubbles: List[BubbleObject] = []
        DrawEvent.bind(self.draw)
        UpdateEvent.bind(self.update)
        TickUpdateEvent.bind(self.tick_update)
        random.seed(4096)

    def create_random_bubble(self, x, batch, objects, scene, random=random):
        # size_rand = random.random(self.tick_updates, 1)
        size_randint = random.randint(MIN_BUBBLE_SIZE, MAX_BUBBLE_SIZE)  # size_rand * 50 + 10

        y_randint = random.randint(int(size_randint / 2), scene.window.height - 72 - int(size_randint / 2))

        bubble = BubblePriorityCalculator.get(random)

        speed_randint = random.randint(bubble.speedMin, bubble.speedMax)  # size_rand * 50 + 10
        objects.append(self.create_bubble(x + size_randint / 2, y_randint, bubble, batch, size_randint, speed_randint, scene))

    def remove_bubble(self, obj: BubbleObject, objects: list, scene):
        objects.remove(obj)
        obj.unbind_events()
        obj.sprite.delete()
        obj.dead = True
        BubbleRemoveEvent(obj.baseBubbleClass, scene)
        self.bubbles.remove(obj)

    def create_bubble(self, x, y, bubble, batch, size, speed, scene):
        bub = bubble(x, y, self, batch, size, speed)
        BubbleRemoveEvent(bub, scene)
        self.bubbles.append(bub)
        # bub.draw()
        return bub

    def draw(self, event):
        pass
        # for bubble in self.bubbles:
        #     bubble.draw()

    def update(self, event: UpdateEvent):
        for bubble in self.bubbles:
            if bubble.position.x < (0 - bubble.size / 2):
                self.remove_bubble(bubble, event.gameObjects, event.scene)
            elif bubble.dead:
                self.remove_bubble(bubble, event.gameObjects, event.scene)
        if len(self.bubbles) < 100:
            self.create_random_bubble(event.window.width, event.batch, event.gameObjects, event.scene, event.scene.random)
            self.tick_updates += 1
            self._bubCreateTime = time() + self._bubCreateInterval

    def tick_update(self, event: TickUpdateEvent):
        pass
        # print("UPDATE")
        # y_rand = random.random(self.tick_updates, 2)
        # size_randint = random.randint(0, event.window.height)
        # self.create_random_bubble(event.window.width, size_randint, event.batch, event.gameObjects, event.scene.random)
        # self.tick_updates += 1
