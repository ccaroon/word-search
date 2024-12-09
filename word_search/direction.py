class Direction:
    __OFFSET = {
        "N":  (-1, 0),
        "NE": (-1, 1),
        "E":  (0, 1),
        "SE": (1, 1),
        "S":  (1, 0),
        "SW": (1, -1),
        "W":  (0, -1),
        "NW": (-1,-1)
    }

    VALID_CODES = tuple(__OFFSET.keys())

    def __init__(self, code:str):
        if code not in self.__OFFSET:
            raise ValueError(f"Invalid Direction Code '{code}'")

        self.__code = code
        self.__delta = self.__OFFSET.get(code)


    @property
    def code(self):
        return self.__code

    @property
    def row_delta(self):
        return self.__delta[0]


    @property
    def col_delta(self):
        return self.__delta[1]


    def __str__(self):
        return f"{self.__code} ({self.row_delta},{self.col_delta})"
