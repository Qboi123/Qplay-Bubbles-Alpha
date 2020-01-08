# noinspection PyUnusedFunction
class CollisionEvent(object):
    def __init__(self, event_object, other_object, window, batch, map, game_objects):
        self.gameObjects = game_objects
        self.eventObject = event_object
        self.otherObject = other_object
        self.window = window
        self.batch = batch
        self.map = map
