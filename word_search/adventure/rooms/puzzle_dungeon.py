import pyfiglet

from colorama import Fore

from lib.word_crawler.inventory.object import Object

from lib.grid import Grid
from .space import Space
# ------------------------------------------------------------------------------
class PuzzleDungeon:
    def __init__(self, puzzle):
        self.__puzzle = puzzle

        self.__location = (0,0)
        self.__rooms = []

        self.__generate_rooms()

    def __generate_rooms(self):
        (rows, cols) = self.__puzzle.size()
        grid = Grid(rows, cols)

        for row in range(rows):
            self.__rooms.append([])
            for col in range(cols):
                letter = self.__puzzle.letter_at(row,col)
                letter_txt = pyfiglet.figlet_format(letter)

                button = Object(
                    "button",
                    "A large illuminated button.",
                    aliases=("illuminated button",),
                    state="OFF",
                    color=Fore.RED,
                    action=lambda: self.state="ON" if self.state == "OFF" else self.state="OFF"
                )

                letter_obj = Object(
                    F"Monolithic Letter '{letter.upper()}'",
                    letter_txt,
                    aliases=(
                        F'letter {letter.lower()}',
                        F'letter {letter.upper()}',
                        'letter',
                        F'{letter.lower()}',
                        F'{letter.upper()}'
                    ),
                    color=Fore.WHITE
                )
                letter_obj.parts.add(button)

                room = Space(
                    F"Puzzle Room - Location[{row},{col}]",
                    F"A large, mostly empty room. There's a {letter_obj} in the center.",
                    # items=[items.lantern],
                    objects=[letter_obj],
                )
                room.location = (row, col)
                self.__rooms[row].append(room)

        # Assign Exits
        for row in range(rows):
            for col in range(cols):
                room = self.__rooms[row][col]
                valid_dirs = grid.valid_directions(row, col)

                if valid_dirs['N']:
                    room.north = self.get_room(valid_dirs['N'][0], valid_dirs['N'][1])
                if valid_dirs['NE']:
                    room.northeast = self.get_room(valid_dirs['NE'][0], valid_dirs['NE'][1])
                if valid_dirs['E']:
                    room.east = self.get_room(valid_dirs['E'][0], valid_dirs['E'][1])
                if valid_dirs['SE']:
                    room.southeast = self.get_room(valid_dirs['SE'][0], valid_dirs['SE'][1])
                if valid_dirs['S']:
                    room.south = self.get_room(valid_dirs['S'][0], valid_dirs['S'][1])
                if valid_dirs['SW']:
                    room.southwest = self.get_room(valid_dirs['SW'][0], valid_dirs['SW'][1])
                if valid_dirs['W']:
                    room.west = self.get_room(valid_dirs['W'][0], valid_dirs['W'][1])
                if valid_dirs['NW']:
                    room.northwest = self.get_room(valid_dirs['NW'][0], valid_dirs['NW'][1])

    def get_room(self, row, col):
        return self.__rooms[row][col]
