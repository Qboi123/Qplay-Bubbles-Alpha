from typing import List, Union, Dict, Tuple, Any


class Position2D(object):
    # noinspection PyProtectedMember
    def __init__(self, pos: Union[
            Tuple[Union[float, int], Union[float, int]], List[Union[float, int]], Dict[str, Union[float, int]]]):
        if type(pos) == list or type(pos) == tuple:
            self.x: Union[float, int] = pos[0]
            self.y: Union[float, int] = pos[1]
        elif type(pos) == dict:
            self.x: Union[float, int] = pos["x"]
            self.y: Union[float, int] = pos["y"]
        else:
            raise TypeError("Invalid type: %s, supported types: %s, %s, %s, %s" % (type(pos), tuple, list, dict,
                                                                               Position2D))

    # noinspection PyProtectedMember
    @staticmethod
    def __other(other: Union[tuple, list, dict, Any]):
        other_x: Union[float, int] = 0.0
        other_y: Union[float, int] = 0.0
        if type(other) == tuple:
            other_x = other[0]
            other_y = other[1]
        elif type(other) == list:
            other_x = other[0]
            other_y = other[1]
        elif type(other) == dict:
            other_x = other["x"]
            other_y = other["y"]
        elif type(other) == Position2D:
            other_x = other.x
            other_y = other.y
        else:
            raise TypeError("Invalid type: %s, supported types: %s, %s, %s, %s" % (type(other), tuple, list, dict,
                                                                               type(Position2D)))
        return other_x, other_y

    def __int__(self):
        return int(self.x * self.y)

    def __float__(self):
        return self.x * self.y

    def __str__(self):
        return "Position2D=(x:%s,y:%s)" % (self.x, self.y)

    def __bool__(self):
        return bool(self.x * self.y)

    # noinspection PyProtectedMember
    def __eq__(self, other: Union[
            Tuple[Union[float, int], Union[float, int]], List[Union[float, int]], Dict[str, Union[float, int]]]):
        other_x, other_y = self.__other(other)
        return self.x == other_x and self.y == other_y

    def __gt__(self, other: Union[
            Tuple[Union[float, int], Union[float, int]], List[Union[float, int]], Dict[str, Union[float, int]]]):
        other_x, other_y = self.__other(other)
        return self.x > other_x and self.y > other_y

    def __lt__(self, other: Union[
            Tuple[Union[float, int], Union[float, int]], List[Union[float, int]], Dict[str, Union[float, int]]]):
        other_x, other_y = self.__other(other)
        return self.x < other_x and self.y < other_y

    def __add__(self, other: Union[
            Tuple[Union[float, int], Union[float, int]], List[Union[float, int]], Dict[str, Union[float, int]]]):
        other_x, other_y = self.__other(other)
        return Position2D([self.x + other_x, self.y + other_y])

    def __sub__(self, other: Union[
            Tuple[Union[float, int], Union[float, int]], List[Union[float, int]], Dict[str, Union[float, int]]]):
        other_x, other_y = self.__other(other)
        return Position2D([self.x - other_x, self.y - other_y])

    def __mod__(self, other: Union[
            Tuple[Union[float, int], Union[float, int]], List[Union[float, int]], Dict[str, Union[float, int]]]):
        other_x, other_y = self.__other(other)
        return Position2D([self.x % other_x, self.y % other_y])

    def __mul__(self, other: Union[
            Tuple[Union[float, int], Union[float, int]], List[Union[float, int]], Dict[str, Union[float, int]]]):
        other_x, other_y = self.__other(other)
        return Position2D([self.x * other_x, self.y * other_y])

    def __rmod__(self, other: Union[
            Tuple[Union[float, int], Union[float, int]], List[Union[float, int]], Dict[str, Union[float, int]]]):
        other_x, other_y = self.__other(other)
        return Position2D([other_x % self.x, other_y % self.y])

    def __rmul__(self, other: Union[
            Tuple[Union[float, int], Union[float, int]], List[Union[float, int]], Dict[str, Union[float, int]]]):
        other_x, other_y = self.__other(other)
        return Position2D([other_x * self.x, other_y * self.y])

    def __truediv__(self, other):
        other_x, other_y = self.__other(other)
        return Position2D([self.x / other_x, self.y / other_y])

    def __rtruediv__(self, other):
        other_x, other_y = self.__other(other)
        return Position2D([other_x / self.x, other_y / self.y])

    def __floordiv__(self, other):
        other_x, other_y = self.__other(other)
        return Position2D([self.x // other_x, self.y // other_y])

    def __rfloordiv__(self, other):
        other_x, other_y = self.__other(other)
        return Position2D([other_x // self.x, other_y // self.y])

    def __invert__(self):
        return Position2D([-self.x, -self.y])

    def __neg__(self):
        return Position2D([-self.x, -self.y])

    def __pos__(self):
        return Position2D([+self.x, +self.y])

    def __radd__(self, other):
        other_x, other_y = self.__other(other)
        return Position2D([other_x + self.x, other_y + self.y])

    def __rsub__(self, other):
        other_x, other_y = self.__other(other)
        return Position2D([other_x - self.x, other_y - self.y])
