#!/usr/bin/env python
import argparse

from word_search.generator import Generator

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Word Search Generator")

    parser.add_argument("word_file", help="File with words to include in the puzzle. One word per line.")
    parser.add_argument("--filler", default=Generator.FILLER_RANDOM_CHARS, help="What to fill the left over spaces with. Default: Random Letters")
    parser.add_argument("--title", default=None, help="Word Search's Title")
    parser.add_argument("--padding", type=int, default=10, help="Amount of extra room around the edges of the puzzle. Also filled with `filler`")

    args = parser.parse_args()

    generator = Generator(args.word_file, filler=args.filler, padding=args.padding, title=args.title)
    generator.generate()
    generator.display()

    generator.save("txt")
