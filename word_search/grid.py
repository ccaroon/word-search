# Encapsulates some Grid logic

from word_search.direction import Direction
from word_search.position import Position

class Grid:
    def __init__(self, rows=2, cols=2):
        self.set_size(rows, cols)

    def get(self, row, col):
        return self._grid[row][col]

    def set(self, row, col, cell):
        self._grid[row][col] = cell

    def get_row(self, row):
        return self._grid[row]

    def set_row(self, row, cells):
        self._grid[row] = cells

    def fill(self, cell=' '):
        for row in range(self.__max_row):
            cols = []
            self._grid.append(cols)
            for col in range(self.__max_col):
                cols.append(cell)

    def size(self):
        return (self.__max_row, self.__max_col)

    def set_size(self, rows, cols):
        self.__max_row = rows
        self.__max_col = cols
        self._grid = []

    def location_to_vector(self, loc, length):
        vector = set()
        (row, col, dd) = loc

        for i in range(length):
            if self.in_bounds(row, col):
                vector.add((row, col))
                (row, col) = self.direction_to_col_row(dd, row, col)
            else:
                vector = None
                break

        return vector


    def valid_directions(self, pos:Position):
        valid = []
        directions = [Direction(code) for code in Direction.VALID_CODES]
        for direction in directions:
            start_pos = Position(pos.row, pos.col)

            start_pos.move(direction)
            if self.in_bounds(start_pos):
                valid.append(direction)

        return valid


    def in_bounds(self, pos):
        in_bounds = True
        if pos.row < 0 or pos.row >= self.__max_row:
            in_bounds = False

        if pos.col < 0 or pos.col >= self.__max_col:
            in_bounds = False

        return in_bounds


    def display(self, center=0, inc_ln=True):
        output = ""
        for row, line in enumerate(self._grid):
            if inc_ln:
                output += F"{row:2}: " + " ".join(line) + "\n"
            else:
                line = " ".join(line)
                output += line.center(center) + "\n"

        return(output)

    def __str__(self):
        return self.display(inc_ln=False)







#
