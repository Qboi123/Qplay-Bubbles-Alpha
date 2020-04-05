import sys

from pyglet.graphics import Batch
from pyglet.window import Window

from utils.classes import Position2D


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
        # print(f"Unbind: {func.__name__}")
        return func


# noinspection PyUnusedClass
class ResizeEvent(Event):
    _handlers = list()

    # noinspection PyMissingConstructor
    def __init__(self, width, height, old_width, old_height, scene):
        self.width = width
        self.height = height
        self.size = (width, height)

        self.oldWidth = old_width
        self.oldHeight = old_height
        self.oldSize = (old_width, old_height)

        self.window: Window = scene.window
        self.batch: Batch = scene.batch
        self.gameObjects = scene.game_objects
        self.map = scene.map
        self.player = scene.player
        self.scene = scene

        handler_ = None
        for handler in self._handlers:
            handler(self)

    @classmethod
    def bind(cls, func):
        cls._handlers.append(func)
        # # print(f"Bind: {func.__name__}")
        return func

    @classmethod
    def unbind(cls, func):
        cls._handlers.remove(func)
        # print(f"Unbind: {func.__name__}")
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
            pass
            # print(f"ERROR Handler not found", file=sys.stderr)

    @classmethod
    def bind(cls, func):
        cls._handlers.append(func)
        # # print(f"Bind: {func.__name__}")
        return func

    @classmethod
    def unbind(cls, func):
        cls._handlers.remove(func)
        # print(f"Unbind: {func.__name__}")
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
            pass
            # print(f"ERROR Handler not found", file=sys.stderr)

    @classmethod
    def bind(cls, func):
        cls._handlers.append(func)
        # print(f"Bind: {func.__name__}")
        return func

    @classmethod
    def unbind(cls, func):
        try:
            cls._handlers.remove(func)
        except ValueError as e:
            raise ValueError(f"Handler '{func.__name__ if type(func) == type and not hasattr(func,'__class__') else func.__class__.__name__ if func.__class__.__name__ != 'method' else func.__name__}' can't be unbinded: {e.args[0]}")
        # print(f"Unbind: {func.__name__}")
        return func


class BubbleUpdateEvent(Event):
    _handlers = list()

    def __init__(self, dt, bubble_object, scene):
        self.dt = dt
        self.bubbleObject = bubble_object
        super(BubbleUpdateEvent, self).__init__(scene)

    @classmethod
    def bind(cls, func):
        cls._handlers.append(func)
        # print(func)
        return func

    @classmethod
    def unbind(cls, func):
        cls._handlers.remove(func)
        # print(f"Unbind: {func.__name__}")
        return func


class BubbleCreateEvent(Event):
    _handlers = list()

    def __init__(self, bubble_object, scene):
        self.bubbleObject = bubble_object
        super(BubbleCreateEvent, self).__init__(scene)

    @classmethod
    def bind(cls, func):
        cls._handlers.append(func)
        # print(func)
        return func

    @classmethod
    def unbind(cls, func):
        cls._handlers.remove(func)
        # print(f"Unbind: {func.__name__}")
        return func


class BubbleRemoveEvent(Event):
    _handlers = list()

    def __init__(self, bubble_type, scene):
        self.bubbleType = bubble_type
        super(BubbleRemoveEvent, self).__init__(scene)

    @classmethod
    def bind(cls, func):
        cls._handlers.append(func)
        # print(func)
        return func

    @classmethod
    def unbind(cls, func):
        cls._handlers.remove(func)
        # print(f"Unbind: {func.__name__}")
        return func


class BubbleTickUpdateEvent(Event):
    _handlers = list()

    def __init__(self, dt, bubble_object, scene):
        self.dt = dt
        self.bubbleObject = bubble_object
        super(BubbleTickUpdateEvent, self).__init__(scene)

    @classmethod
    def bind(cls, func):
        cls._handlers.append(func)
        # print(func)
        return func

    @classmethod
    def unbind(cls, func):
        cls._handlers.remove(func)
        # print(f"Unbind: {func.__name__}")
        return func


class TickUpdateEvent(Event):
    _handlers = list()

    def __init__(self, dt, scene):
        self.dt = dt
        super(TickUpdateEvent, self).__init__(scene)

    @classmethod
    def bind(cls, func):
        cls._handlers.append(func)
        # print(func)
        return func

    @classmethod
    def unbind(cls, func):
        cls._handlers.remove(func)
        # print(f"Unbind: {func.__name__}")
        return func


class DrawEvent(Event):
    _handlers = list()

    def __init__(self, scene):
        super(DrawEvent, self).__init__(scene)

    @classmethod
    def bind(cls, func):
        cls._handlers.append(func)
        # print(f"Bind: {func.__name__}")
        return func

    @classmethod
    def unbind(cls, func):
        cls._handlers.remove(func)
        # print(f"Unbind: {func.__name__}")
        return func


class KeyEvent(Event):
    _handlers = list()

    def __init__(self, key, modifiers, type_, scene):
        self.key = key
        self.modifiers = modifiers
        self.eventType = type_
        super(KeyEvent, self).__init__(scene)

    @classmethod
    def bind(cls, func):
        cls._handlers.append(func)
        # print(f"Bind: {func.__name__}")
        return func

    @classmethod
    def unbind(cls, func):
        cls._handlers.remove(func)
        # print(f"Unbind: {func.__name__}")
        return func


class MouseEvent(Event):
    _handlers = list()

    def __init__(self, x, y, type_, scene, button=None):
        self.x = x
        self.y = y
        self.pos = Position2D((x, y))

        self.button = button
        self.eventType = type_
        super(MouseEvent, self).__init__(scene)

    @classmethod
    def bind(cls, func):
        cls._handlers.append(func)
        # print(f"Bind: {func.__name__}")
        return func

    @classmethod
    def unbind(cls, func):
        cls._handlers.remove(func)
        # print(f"Unbind: {func.__name__}")
        return func


class UpdateEvent(Event):
    _handlers = list()

    def __init__(self, dt, scene):
        self.dt = dt
        super(UpdateEvent, self).__init__(scene)

    @classmethod
    def bind(cls, func):
        cls._handlers.append(func)
        # print(f"Bind: {func.__name__}")
        return func

    @classmethod
    def unbind(cls, func):
        cls._handlers.remove(func)
        # print(f"Unbind: {func.__name__}")
        return func


class AutoSaveEvent(Event):
    _handlers = list()

    def __init__(self, dt, scene):
        self.dt = dt
        super(AutoSaveEvent, self).__init__(scene)

    @classmethod
    def bind(cls, func):
        cls._handlers.append(func)
        # print(f"Bind: {func.__name__}")
        return func

    @classmethod
    def unbind(cls, func):
        cls._handlers.remove(func)
        # print(f"Unbind: {func.__name__}")
        return func


class PauseEvent(Event):
    _handlers = list()

    def __init__(self, scene):
        self.pause = True
        super(PauseEvent, self).__init__(scene)

    @classmethod
    def bind(cls, func):
        cls._handlers.append(func)
        # print(f"Bind: {func.__name__}")
        return func

    @classmethod
    def unbind(cls, func):
        cls._handlers.remove(func)
        # print(f"Unbind: {func.__name__}")
        return func


class UnpauseEvent(Event):
    _handlers = list()

    def __init__(self, scene):
        self.pause = False
        super(UnpauseEvent, self).__init__(scene)

    @classmethod
    def bind(cls, func):
        cls._handlers.append(func)
        # print(f"Bind: {func.__name__}")
        return func

    @classmethod
    def unbind(cls, func):
        cls._handlers.remove(func)
        # print(f"Unbind: {func.__name__}")
        return func


class EffectEvent(Event):
    _handlers = list()

    def __init__(self, effect, scene):
        self.appliedEffect = effect
        super(EffectEvent, self).__init__(scene)

    @classmethod
    def bind(cls, func):
        cls._handlers.append(func)
        # print(func)
        return func

    @classmethod
    def unbind(cls, func):
        cls._handlers.remove(func)
        # print(f"Unbind: {func.__name__}")
        return func


class EffectStoppedEvent(EffectEvent):
    _handlers = list()

    def __init__(self, effect, scene):
        super(EffectStoppedEvent, self).__init__(effect, scene)

    @classmethod
    def bind(cls, func):
        cls._handlers.append(func)
        # print(func)
        return func

    @classmethod
    def unbind(cls, func):
        cls._handlers.remove(func)
        # print(f"Unbind: {func.__name__}")
        return func


class EffectStartedEvent(EffectEvent):
    _handlers = list()

    def __init__(self, effect, scene):
        super(EffectStartedEvent, self).__init__(effect, scene)

    @classmethod
    def bind(cls, func):
        cls._handlers.append(func)
        # print(func)
        return func

    @classmethod
    def unbind(cls, func):
        cls._handlers.remove(func)
        # print(f"Unbind: {func.__name__}")
        return func


class EffectUpdateEvent(EffectEvent):
    _handlers = list()

    def __init__(self, dt, effect, scene):
        self.dt = dt
        super(EffectUpdateEvent, self).__init__(effect, scene)

    @classmethod
    def bind(cls, func):
        cls._handlers.append(func)
        # print(func)
        return func

    @classmethod
    def unbind(cls, func):
        cls._handlers.remove(func)
        # print(f"Unbind: {func.__name__}")
        return func


class EffectTickUpdateEvent(EffectEvent):
    _handlers = list()

    def __init__(self, dt, effect, scene):
        self.dt = dt
        super(EffectTickUpdateEvent, self).__init__(effect, scene)

    @classmethod
    def bind(cls, func):
        cls._handlers.append(func)
        # print(func)
        return func

    @classmethod
    def unbind(cls, func):
        cls._handlers.remove(func)
        # print(f"Unbind: {func.__name__}")
        return func


class ScoreEvent(Event):
    _handlers = list()
    _handlers_params = {"cancelscore": []}
    cancelscore = False

    def __init__(self, score, scene):
        self.score = score
        super(ScoreEvent, self).__init__(scene)

    @classmethod
    def bind(cls, func, cancelscore=False):
        cls._handlers.append(func)
        if cancelscore:
            cls._handlers_params["cancelscore"].append(func)
            cls.cancelscore = True
        # print(func)
        return func

    @classmethod
    def unbind(cls, func):
        cls._handlers.remove(func)
        if func in cls._handlers_params["cancelscore"]:
            if len(cls._handlers_params["cancelscore"]) == 1:
                cls.cancelscore = False
            cls._handlers_params["cancelscore"].remove(func)
        # print(f"Unbind: {func.__name__}")
        return func

    # noinspection PyProtectedMember
    def addscore(self, score):
        self.player._addscore(score)

    # noinspection PyProtectedMember
    def removescore(self, score):
        self.player._removescore(score)
