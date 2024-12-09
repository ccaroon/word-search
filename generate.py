#!/usr/bin/env python
import os
import sys

from word_search.generator import Generator

# used_vectors = []
# def check_intersection(vector):
#     valid = True
#     for used_vector in used_vectors:
#         i = vector.intersection(used_vector)
#         if i:
#             valid = False
#             break

#     return valid

def read_word_list(filename:str):
    words = []
    with open(filename, "r") as file:
        while word := file.readline():
            words.append(word.strip())

    return words

if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        basename = os.path.basename(filename)
        (title, _) = os.path.splitext(basename)
        words = read_word_list(filename)

        generator = Generator(title, words)
        generator.generate()
        generator.display()

        generator.save("txt")
    else:
        print(f"Usage: {sys.argv[0]} <word-list-file-name>")
