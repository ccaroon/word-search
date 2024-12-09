from word_search.direction import Direction

class Position:
    def __init__(self, row, col):
        self.row = row
        self.col = col


    def move(self, direction:Direction):
        """
        Move in the given `direction`

        >>> pos = Position(0,0)
        >>> dir = Direction("SE")
        >>> pos.move(dir)
        >>> pos
        (1, 1)
        """
        self.row += direction.row_delta
        self.col += direction.col_delta


    def __add__(self, other:any):
        """
        >>> pos = Position(0,0)
        >>> dir = Direction("SE")
        >>> pos = pos + dir
        >>> pos
        (1, 1)
        """
        if isinstance(other, Direction):
            self.move(other)
            return self
        else:
            raise TypeError(f"Cannot Add {type(other)} to a Position")


    def __repr__(self):
        return f"({self.row}, {self.col})"
