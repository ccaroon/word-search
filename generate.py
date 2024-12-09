#!/bin/env python
import random
import sys
import os.path
import re
import yaml

from word_search.grid import Grid
# ------------------------------------------------------------------------------



def read_word_list(filename:str):
    words = []
    with open(filename, "r") as file:
        while word := file.readline():
            words.append(word.strip())

    return words





# loc = random_loc()
# print(loc)
# v = diagram.location_to_vector(loc, 5)
# print(v)

# Insert Words
# RR-CC-DD

# loc = random_loc()
# vector = diagram.location_to_vector(loc)

used_vectors = []
def check_intersection(vector):
    valid = True
    for used_vector in used_vectors:
        i = vector.intersection(used_vector)
        if i:
            valid = False
            break

    return valid


for word in words:
    word_inserted = False

    counter = 0
    # print(F"Working on '{word}'...")
    while not word_inserted and counter < 1000:
        counter += 1
        loc = random_loc()
        vector = diagram.location_to_vector(loc, len(word))
        loc_str = F"{loc[0]:02}-{loc[1]:02}-{loc[2]}"

        if vector and vector not in used_vectors and check_intersection(vector):
            insert_word(word, loc)
            used_vectors.append(vector)
            word_inserted = True

    if not word_inserted:
        print(F"FAIL: '{word}' not inserted.")
    # else:
    #     print(F"'{word}' inserted at {loc_str}.")

# ------------------------------------------------------------------------------
# Print to Screen
# ------------------------------------------------------------------------------
with open(F"./puzzles/{puzzle_name}.txt", "w") as file:
    # file.write(F"{puzzle_name.capitalize():>40}\n")
    file.write(F"{puzzle_name.capitalize().center(80)}\n")
    file.write("--------------------------------------------------------------------------------\n")
    file.write(diagram.display(center=80, inc_ln=False))

    file.write(F"\n")

    per_col = 3
    for i in range(0, len(words), per_col):
        output = ""
        for idx in range(per_col):
            if i+idx < len(words):
                output = output + F"* {words[i+idx]:{max_word_length+3}}"

        file.write(F"{output.center(80)}\n")
    file.write("--------------------------------------------------------------------------------\n")
# ------------------------------------------------------------------------------
# Print to YAML file
# ------------------------------------------------------------------------------
(num_rows, _) = diagram.size()
rows = []
for i in range(num_rows):
    row_str = ''.join(diagram.get_row(i))
    rows.append(row_str)

output = {
    'title': puzzle_name.capitalize(),
    'author': "Craig N. Caroon",
    'difficulty': "easy",
    'diagram': rows,
    'words': words
}

with open(F"./puzzles/{puzzle_name}.yml", "w") as file:
    yaml.safe_dump(output, file)



if __name__ == "__main__":






# ------------------------------------------------------------------------------
