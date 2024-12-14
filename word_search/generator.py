import os
import random
import re
import yaml

from word_search.grid import Grid
from word_search.position import Position
from word_search.vector import Vector

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
# from reportlab.lib.colors import black, white, lightgrey


class Generator():
    DEFAULT_PADDING = 15
    TEXT_WIDTH = 80

    INSERT_TRIES = 3000

    EMPTY = " "
    FILLER_RANDOM_CHARS = "__random-chars__"
    HIDDEN_WORD_MARKER = "@"

    # PDF
    FONT_NORMAL = "Times-Roman"
    FONT_BOLD = "Times-Bold"
    FONT_FIXED = "Courier"
    FONT_FIXED_BOLD = "Courier-Bold"

    def __init__(self,
        word_file:str,
        rows:int=None, cols:int=None,
        **kwargs
    ):
        self.__word_file = word_file
        self.__filler = kwargs.get("filler", self.FILLER_RANDOM_CHARS)
        self.__padding = kwargs.get("padding", self.DEFAULT_PADDING)
        self.__bg_image = kwargs.get("bg_image", None)

        self.__title = kwargs.get("title")
        if self.__title is None:
            self.__title = self.__default_title()

        self.__word_list = None
        self.__read_word_list()

        self.__longest_word = self.find_longest_word()
        if rows is None or cols is None:
            rows = len(self.__longest_word) + self.__padding
            cols = len(self.__longest_word) + self.__padding

        self.__diagram = Grid(rows, cols)
        self.__diagram.fill(self.EMPTY)


    def __read_word_list(self):
        self.__word_list = []

        with open(self.__word_file, "r") as file:
            while line := file.readline():
                word = line.strip()
                if word.startswith("#"):
                    continue

                self.__word_list.append(word)

        self.__word_list.sort()


    def __default_title(self, ):
        basename = os.path.basename(self.__word_file)
        (title, _) = os.path.splitext(basename)
        return title


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
        ltr_list = list(re.sub(r"\s", "", word))
        if ltr_list[0] == self.HIDDEN_WORD_MARKER:
            ltr_list = ltr_list[1:]

        return ltr_list


    def __insert_word(self, word:str, vector:Vector):
        for ltr in self.__letter_list(word):
            self.__diagram.set(vector.position, ltr.upper())
            vector.move()


    def __save_yml(self, file_path, **kwargs):
        (num_rows, _) = self.__diagram.size
        rows = []
        for i in range(num_rows):
            row_str = ''.join(self.__diagram.get_row(i))
            rows.append(row_str)

        # Don't include words that are marked as hidden
        word_list = list(filter(
            lambda word: word[0] != self.HIDDEN_WORD_MARKER,
            self.__word_list
        ))

        output = {
            'title': self.__title,
            'author': "Craig N. Caroon",
            'difficulty': "easy",
            'diagram': rows,
            'words': word_list
        }

        with open(file_path, "w") as file:
            yaml.safe_dump(output, file)


    def __save_txt(self, file_path, **kwargs):
        divider = ("-" * self.TEXT_WIDTH) + "\n"

        with open(file_path, "w") as file:
            file.write(f"{self.__title.center(self.TEXT_WIDTH)}\n")
            file.write(divider)
            file.write(
                self.__diagram.display(center=self.TEXT_WIDTH, inc_ln=False)
            )

            file.write("\n")

            # Don't include words that are marked as hidden
            word_list = list(filter(
                lambda word: word[0] != self.HIDDEN_WORD_MARKER,
                self.__word_list
            ))

            per_col = 3
            max_word_length = len(self.__longest_word)
            word_count = len(word_list)
            for i in range(0, word_count, per_col):
                output = ""
                for idx in range(per_col):
                    if i + idx < word_count:
                        word = word_list[i + idx]
                        output += f"* {word:{max_word_length+3}}"

                file.write(f"{output.center(self.TEXT_WIDTH)}\n")
            file.write(divider)


    def __save_pdf(self, file_path, **kwargs):
        pdf = Canvas(
            file_path,
            pagesize=letter,
            pageCompression=0
        )

        # Border - Shaded / Rounded
        # pdf.setStrokeColorRGB(0,0,0)
        # pdf.setFillColor(lightgrey)
        # pdf.roundRect(3.0 * inch, 7.4 * inch, 5 * inch, 1 * inch, 10, fill=1)

        # Title @ top
        pdf.setFillColorRGB(0,0,0)
        pdf.setFont(self.FONT_NORMAL, 64)
        pdf.drawCentredString(4.25*inch, 10*inch, self.__title)

        # Clip Art Background Image
        if self.__bg_image:
            pdf.drawImage(self.__bg_image,
                1.50*inch, 2.75*inch,
                width=400, height=500
            )

        # The Word Search Puzzle
        pdf.setFont(self.FONT_FIXED_BOLD, 16)
        puzzle = self.__diagram.display(center=self.TEXT_WIDTH, inc_ln=False)
        nudge = kwargs.get("nudge", 0.0)
        x_pos = (2.0 * inch) + (nudge * inch)
        text_obj = pdf.beginText(x_pos, 7.75*inch)
        text_obj.textLines(puzzle)
        pdf.drawText(text_obj)


        # Word List
        # Don't include words that are marked as hidden
        text_obj = pdf.beginText(1.5*inch, 2.5*inch)
        word_list = list(filter(
            lambda word: word[0] != self.HIDDEN_WORD_MARKER,
            self.__word_list
        ))
        word_len = len(self.__longest_word)
        for idx in range(0, len(word_list), 3):
            text_obj.textLine(f"{word_list[idx]:{word_len}} {word_list[idx+1]:{word_len}} {word_list[idx+2]:{word_len}}")
        pdf.drawText(text_obj)

        pdf.showPage()
        pdf.save()


    def save(self, path:str, **kwargs):
        (_, file_format) = os.path.splitext(path)

        outfile = path
        if path is None:
            path = "/tmp" if path is None else path
            basename = re.sub(r"\W", "-", self.__title.lower())
            outfile = f"{path}/{basename}.{file_format}"

        if file_format in (".yaml",".yml"):
            self.__save_yml(outfile, **kwargs)
        elif file_format in (".text", ".txt"):
            self.__save_txt(outfile, **kwargs)
        elif file_format in (".pdf"):
            self.__save_pdf(outfile, **kwargs)


    def display(self):
        print(self.__diagram.display())


    def generate(self):
        size = self.__diagram.size
        # Fill empty diagram with words
        for word in self.__word_list:
            word_inserted = False

            counter = 0
            while not word_inserted and counter < self.INSERT_TRIES:
                counter += 1
                vector = Vector.random(
                    size[0], size[1]
                )
                if self.__check_fit(word, vector.copy()):
                    self.__insert_word(word, vector)
                    word_inserted = True

            if not word_inserted:
                print(F"FAIL: '{word}' not inserted.")

        # Fill left-over empty spaces with **something**
        if self.__filler is not None:
            for row in range(size[0]):
                for col in range(size[1]):
                    pos = Position(row, col)
                    if self.__diagram.get(pos) == self.EMPTY:
                        if self.__filler == self.FILLER_RANDOM_CHARS:
                            self.__diagram.set(pos, chr(random.randint(65,90)))
                        else:
                            self.__diagram.set(
                                pos,
                                random.choice(self.__filler).upper()
                            )
