import random
import re

from grid import Grid, Position

class Generator():
    ROW_PADDING = 15
    COL_PADDING = 15

    def __init__(self, word_list:list[str], rows:int=None, cols:int=None):
        self.__word_list = word_list
        self.__rows = rows
        self.__cols = cols

        if self.__rows is None or self.__cols is None:
            longest_word = self.find_longest_word()
            self.__rows = len(longest_word) + self.ROW_PADDING
            self.__cols = len(longest_word) + self.COL_PADDING

        self.__diagram = None
        self.__init_diagram()


    def find_longest_word(self):
        longest_word = max(self.__word_list, key=lambda w: len(x))
        return longest_word


    def __init_diagram(self):
        self.__diagram = Grid(self.__rows, self.__cols)
        self.__diagram.fill()

        for row in range(self.__rows):
            for col in range(self.__cols):
                self.__diagram.set(row, col, chr(random.randint(65,90)))


    def __insert_word(self, word:str, pos:Position, direction:str):
        letters = list(re.sub(r"\s", "", word))

        for ltr in letters:
            self.__diagram.set(pos.row, pos.col, ltr.upper())
            (row, col) = self.__diagram.direction_to_col_row(
                direction, pos.row, pos.col)


    def random_loc():
        row = random.randint(0, max_rows)
        col = random.randint(0, max_cols)
        didx = random.randint(0, len(Grid.DIRECTIONS)-1)
        dd = Grid.DIRECTIONS[didx]

        return (row, col, dd)

    def generate(self):
        pass
