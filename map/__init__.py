import random as random_
from time import time
from typing import List, Optional

from bubble import BubbleObject, BubblePriorityCalculator
from events import TickUpdateEvent, UpdateEvent, DrawEvent, BubbleRemoveEvent, BubbleCreateEvent
from utils import MIN_BUBBLE_SIZE, MAX_BUBBLE_SIZE


class Map(object):
    def __init__(self):
        self._bubCreateInterval: float = 0.1
        self._bubCreateTime: float = time() + self._bubCreateInterval
        self.tick_updates: float = 0
        self.bubbles: List[BubbleObject] = []
        self.bubbleCreationHook: Optional[type] = None
        self.bubbleRemoveHook: Optional[type] = None

        DrawEvent.bind(self.draw)
        UpdateEvent.bind(self.update)
        TickUpdateEvent.bind(self.tick_update)
        random_.seed(4096)

    def create_random_bubble(self, x, batch, objects, scene, random=random_):
        if self.bubbleCreationHook:
            return self.bubbleCreationHook(x, batch, objects, scene, random)

        # size_rand = random.random(self.tick_updates, 1)
        size_randint = random.randint(MIN_BUBBLE_SIZE, MAX_BUBBLE_SIZE)  # size_rand * 50 + 10
        y_randint = random.randint(int(size_randint / 2), scene.window.height - 72 - int(size_randint / 2))

        bubble = BubblePriorityCalculator.get(random)
        speed_randint = random.randint(bubble.speedMin, bubble.speedMax)  # size_rand * 50 + 10

        objects.append(self.create_bubble(x + size_randint / 2, y_randint, bubble, batch, size_randint, speed_randint, scene))

    def remove_bubble(self, obj: BubbleObject, objects: list, scene):
        if self.bubbleRemoveHook:
            return self.bubbleRemoveHook(obj, objects, scene)

        objects.remove(obj)
        obj.unbind_events()
        obj.sprite.delete()
        obj.dead = True
        BubbleRemoveEvent(obj.baseBubbleClass, scene)

        self.bubbles.remove(obj)

    def create_bubble(self, x, y, bubble, batch, size, speed, scene):
        bub = bubble(x, y, self, batch, size, speed)
        BubbleCreateEvent(bub, scene)

        self.bubbles.append(bub)
        return bub

    def draw(self, event):
        pass

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
