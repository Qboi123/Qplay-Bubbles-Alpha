from typing import Tuple


class Player():
    position: Tuple[float, float] = (0.0, 0.0)

    def __init__(self, pos: Tuple[float, float, float]):
        self.position = pos

    @classmethod
    def move(cls, relative_pos: Tuple[float, float]):
        x, y = cls.position
        cls.position = (x+relative_pos[0], y+relative_pos[1])

    @classmethod
    def move_to(cls, pos: Tuple[float, float]):
        cls.position = pos
