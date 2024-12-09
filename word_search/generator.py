import random
import re
import yaml

from word_search.grid import Grid
from word_search.position import Position
from word_search.direction import Direction
from word_search.vector import Vector

class Generator():
    ROW_PADDING = 15
    COL_PADDING = 15
    TEXT_WIDTH = 80
    EMPTY = " "

    def __init__(self,
        title:str,
        word_list:list[str],
        rows:int=None, cols:int=None
    ):
        self.__title = title
        self.__word_list = word_list
        # self.__rows = rows
        # self.__cols = cols
        self.__longest_word = self.find_longest_word()

        if rows is None or cols is None:
            rows = len(self.__longest_word) + self.ROW_PADDING
            cols = len(self.__longest_word) + self.COL_PADDING

        self.__diagram = Grid(rows, cols)
        self.__diagram.fill(self.EMPTY)


    def find_longest_word(self):
        longest_word = max(self.__word_list, key=lambda w: len(w))
        return longest_word


    def __check_fit(self, word:str, vector:Vector) -> bool:
        fits = True

        # for each letter in word
        for ltr in self.__letter_list(word):
            # ...cell(r,c) in bounds
            if not self.__diagram.in_bounds(vector.position):
                fits = False
                break

            cell = self.__diagram.get(vector.position)
            # ...cell(r,c) empty or same letter as in diagram
            if cell != self.EMPTY and cell.upper() != ltr.upper():
                fits = False
                break

            vector.move()

        return fits


    def __letter_list(self, word:str) -> list:
        return list(re.sub(r"\s", "", word))


    def __insert_word(self, word:str, vector:Vector):
        for ltr in self.__letter_list(word):
            self.__diagram.set(vector.position, ltr.upper())
            vector.move()


    def __save_yml(self, file_path):
        (num_rows, _) = self.__diagram.size()
        rows = []
        for i in range(num_rows):
            row_str = ''.join(self.__diagram.get_row(i))
            rows.append(row_str)

        output = {
            'title': self.__title.capitalize(),
            'author': "Craig N. Caroon",
            'difficulty': "easy",
            'diagram': rows,
            'words': self.__word_list
        }

        with open(f"{file_path}.yml", "w") as file:
            yaml.safe_dump(output, file)


    def __save_txt(self, file_path):
        divider = ("-" * self.TEXT_WIDTH) + "\n"

        with open(f"{file_path}.txt", "w") as file:
            file.write(f"{self.__title.capitalize().center(self.TEXT_WIDTH)}\n")
            file.write(divider)
            file.write(
                self.__diagram.display(center=self.TEXT_WIDTH, inc_ln=False)
            )

            file.write("\n")

            per_col = 3
            max_word_length = len(self.__longest_word)
            word_count = len(self.__word_list)
            for i in range(0, word_count, per_col):
                output = ""
                for idx in range(per_col):
                    if i + idx < word_count:
                        word = self.__word_list[i + idx]
                        output += f"* {word:{max_word_length+3}}"

                file.write(f"{output.center(self.TEXT_WIDTH)}\n")
            file.write(divider)


    def save(self, file_format:str, path:str=None):
        path = "/tmp" if path is None else path
        basename = re.sub(r"\W", "-", self.__title.lower())

        if file_format in ("yaml","yml"):
            self.__save_yml(f"{path}/{basename}")
        elif file_format in ("text", "txt"):
            self.__save_txt(f"{path}/{basename}")


    def display(self):
        print(self.__diagram.display())


    def generate(self):
        size = self.__diagram.size
        # Fill empty diagram with words
        for word in self.__word_list:
            word_inserted = False

            counter = 0
            while not word_inserted and counter < 1000:
                counter += 1
                # loc = random_loc()
                # vector = self.__diagram.location_to_vector(loc, len(word))
                # loc_str = f"{loc[0]:02}-{loc[1]:02}-{loc[2]}"


                vector = Vector.random(
                    size[0], size[1]
                )
                if self.__check_fit(word, vector.copy()):
                    self.__insert_word(word, vector)
                    word_inserted = True

                # if vector and vector not in used_vectors and check_intersection(vector):
                #     insert_word(word, loc)
                #     used_vectors.append(vector)
                #     word_inserted = True

            if not word_inserted:
                print(F"FAIL: '{word}' not inserted.")

        # Fill left-over empty spaces with random letters
        # TODO: ^^^ this ^^^
        for row in range(size[0]):
            for col in range(size[1]):
                pos = Position(row, col)
                if self.__diagram.get(pos) == self.EMPTY:
                    self.__diagram.set(pos, chr(random.randint(65,90)))







#
