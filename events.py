import sys

from pyglet.graphics import Batch
from pyglet.window import Window


class Event(object):
    _handlers = list()

    def __init__(self, scene):
        self.window: Window = scene.window
        self.batch: Batch = scene.batch
        self.gameObjects = scene.game_objects
        self.map = scene.map
        self.player = scene.player
        self.scene = scene

        for handler in self._handlers:
            handler(self)

    @classmethod
    def bind(cls, func):
        cls._handlers.append(func)
        # print(func)

        def wrapper(self, *args, **kwargs):
            func(self, *args, **kwargs)
        return wrapper

    @classmethod
    def unbind(cls, func):
        cls._handlers.remove(func)
        print(f"Unbind: {func.__name__}")
        return func


# noinspection PyUnusedClass
class CollisionEvent(Event):
    _handlers = list()

    # noinspection PyMissingConstructor
    def __init__(self, event_obj, other_obj, scene):
        self.eventObject = event_obj
        self.otherObject = other_obj

        self.window: Window = scene.window
        self.batch: Batch = scene.batch
        self.gameObjects = scene.game_objects
        self.map = scene.map
        self.player = scene.player
        self.scene = scene

        handler_ = None
        for handler in self._handlers:
            if hasattr(self.eventObject, handler.__name__):
                if getattr(self.eventObject, handler.__name__) == handler:
                    handler_ = handler

        if handler_:
            handler_(self)
        else:
            print(f"ERROR Handler not found", file=sys.stderr)

    @classmethod
    def bind(cls, func):
        cls._handlers.append(func)
        # # print(f"Bind: {func.__name__}")
        return func

    @classmethod
    def unbind(cls, func):
        cls._handlers.remove(func)
        print(f"Unbind: {func.__name__}")
        return func


class PlayerCollisionEvent(CollisionEvent):
    _handlers = list()

    # noinspection PyMissingConstructor
    def __init__(self, event_obj, other_obj, scene):
        self.eventObject = event_obj
        self.otherObject = other_obj

        self.window: Window = scene.window
        self.batch: Batch = scene.batch
        self.gameObjects = scene.game_objects
        self.map = scene.map
        self.player = scene.player
        self.scene = scene

        handler_ = None
        if (self.eventObject.__name__ if type(self.eventObject) == type else self.eventObject.__class__.__name__) == \
                "Player":
            for handler in self._handlers:
                if hasattr(self.eventObject, handler.__name__):
                    if getattr(self.eventObject, handler.__name__) == handler:
                        handler_ = handler

        if handler_:
            handler_(self)
        else:
            print(f"ERROR Handler not found", file=sys.stderr)

    @classmethod
    def bind(cls, func):
        cls._handlers.append(func)
        # print(f"Bind: {func.__name__}")
        return func

    @classmethod
    def unbind(cls, func):
        cls._handlers.remove(func)
        print(f"Unbind: {func.__name__}")
        return func
    


class TickUpdateEvent(Event):
    _handlers = list()

    def __init__(self, dt, scene):
        self.dt = dt
        super(TickUpdateEvent, self).__init__(scene)

    @classmethod
    def bind(cls, func):
        cls._handlers.append(func)
        print(func)
        return func

    @classmethod
    def unbind(cls, func):
        cls._handlers.remove(func)
        print(f"Unbind: {func.__name__}")
        return func


class DrawEvent(Event):
    _handlers = list()

    def __init__(self, scene):
        super(DrawEvent, self).__init__(scene)

    @classmethod
    def bind(cls, func):
        cls._handlers.append(func)
        print(func)
        return func

    @classmethod
    def unbind(cls, func):
        cls._handlers.remove(func)
        print(f"Unbind: {func.__name__}")
        return func


class UpdateEvent(Event):
    _handlers = list()

    def __init__(self, dt, scene):
        self.dt = dt
        super(UpdateEvent, self).__init__(scene)

    @classmethod
    def bind(cls, func):
        cls._handlers.append(func)
        print(func)
        return func

    @classmethod
    def unbind(cls, func):
        cls._handlers.remove(func)
        print(f"Unbind: {func.__name__}")
        return func


class EffectEvent(Event):
    _handlers = list()

    def __init__(self, effect, scene):
        self.effect = effect
        super(EffectEvent, self).__init__(scene)

    @classmethod
    def bind(cls, func):
        cls._handlers.append(func)
        print(func)
        return func

    @classmethod
    def unbind(cls, func):
        cls._handlers.remove(func)
        print(f"Unbind: {func.__name__}")
        return func


class EffectStoppedEvent(EffectEvent):
    _handlers = list()

    def __init__(self, effect, scene):
        super(EffectStoppedEvent, self).__init__(effect, scene)

    @classmethod
    def bind(cls, func):
        cls._handlers.append(func)
        print(func)
        return func

    @classmethod
    def unbind(cls, func):
        cls._handlers.remove(func)
        print(f"Unbind: {func.__name__}")
        return func


class EffectStartedEvent(EffectEvent):
    _handlers = list()

    def __init__(self, effect, scene):
        super(EffectStartedEvent, self).__init__(effect, scene)

    @classmethod
    def bind(cls, func):
        cls._handlers.append(func)
        print(func)
        return func

    @classmethod
    def unbind(cls, func):
        cls._handlers.remove(func)
        print(f"Unbind: {func.__name__}")
        return func


class EffectUpdateEvent(EffectEvent):
    _handlers = list()

    def __init__(self, dt, effect, scene):
        self.dt = dt
        super(EffectUpdateEvent, self).__init__(effect, scene)

    @classmethod
    def bind(cls, func):
        cls._handlers.append(func)
        print(func)
        return func

    @classmethod
    def unbind(cls, func):
        cls._handlers.remove(func)
        print(f"Unbind: {func.__name__}")
        return func
