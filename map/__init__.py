import random
from typing import Dict, List

import pyglet
from opensimplex import OpenSimplex

import sprites
from bubble import BubbleObject, Bubble, BubblePriorityCalculator
from events import TickUpdateEvent, UpdateEvent, DrawEvent
from noise import SimplexNoiseGen
from sprites.objects import PhysicalObject
from utils import randint_lookup


class Map(object):
    def __init__(self):
        self.tick_updates = 0
        self.bubbles: List[BubbleObject] = []
        DrawEvent.bind(self.draw)
        UpdateEvent.bind(self.update)
        TickUpdateEvent.bind(self.tick_update)
        random.seed(4096)

    def create_random_bubble(self, x, y, batch, objects, random=random):
        # size_rand = random.random(self.tick_updates, 1)
        size_randint = random.randint(21, 80)  # size_rand * 50 + 10

        bubble = BubblePriorityCalculator.get(random)

        speed_randint = random.randint(bubble.speedMin, bubble.speedMax)  # size_rand * 50 + 10
        objects.append(self.create_bubble(x + size_randint / 2, y, bubble, batch, size_randint, speed_randint))

    def remove_bubble(self, obj: BubbleObject, objects: list):
        objects.remove(obj)
        obj.sprite.delete()
        obj.unbind_events()
        obj.dead = True
        self.bubbles.remove(obj)

    def create_bubble(self, x, y, bubble, batch, size, speed):
        bub = bubble(x, y, self, batch, size, speed)
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
                self.remove_bubble(bubble, event.gameObjects)
            elif bubble.dead:
                self.remove_bubble(bubble, event.gameObjects)

    def tick_update(self, event: TickUpdateEvent):
        # print("UPDATE")
        # y_rand = random.random(self.tick_updates, 2)
        size_randint = random.randint(0, event.window.height)
        self.create_random_bubble(event.window.width, size_randint, event.batch, event.gameObjects, event.scene.random)
        self.tick_updates += 1
