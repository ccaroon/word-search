import random

class Direction:
    __CODE_MAP = {
        "N":  (-1, 0),
        "NE": (-1, 1),
        "E":  (0, 1),
        "SE": (1, 1),
        "S":  (1, 0),
        "SW": (1, -1),
        "W":  (0, -1),
        "NW": (-1,-1)
    }

    VALID_CODES = tuple(__CODE_MAP.keys())

    def __init__(self, code:str):
        if code not in self.__CODE_MAP:
            raise ValueError(f"Invalid Direction Code '{code}'")

        self.__code = code
        self.__delta = self.__CODE_MAP.get(code)


    @property
    def code(self):
        return self.__code

    @property
    def row_delta(self):
        return self.__delta[0]


    @property
    def col_delta(self):
        return self.__delta[1]


    @classmethod
    def random(self):
        """
        Pick a random direction

        >>> d = Direction.random()
        >>> isinstance(d, Direction)
        True
        >>> d.code in Direction.VALID_CODES
        True
        """
        rand_code = random.choice(self.VALID_CODES)
        return Direction(rand_code)


    def copy(self):
        return Direction(self.code)


    def __eq__(self, other):
        return self.code == other.code


    def __str__(self):
        return f"{self.__code} ({self.row_delta},{self.col_delta})"
