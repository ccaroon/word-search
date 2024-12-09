import random

from word_search.position import Position
from word_search.direction import Direction

class Vector:
    def __init__(self, pos:Position, direction:Direction):
        self.__position = pos
        self.__direction = direction


    @property
    def position(self):
        return self.__position


    @property
    def direction(self):
        return self.__direction


    @classmethod
    def random(cls, max_row:int, max_col:int):
        row = random.randint(0, max_row)
        col = random.randint(0, max_col)

        return Vector(
            Position(row,col),
            Direction.random()
        )

    def copy(self):
        return Vector(
            self.position.copy(),
            self.direction.copy()
        )

    def move(self):
        self.__position.move(self.__direction)


    def __eq__(self, other):
        return self.position == other.position and self.direction == other.direction
