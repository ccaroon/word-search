#!/usr/bin/env python
import argparse

from word_search.generator import Generator

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Word Search Generator")

    parser.add_argument("word_file", help="File with words to include in the puzzle. One word per line.")
    parser.add_argument("--filler", default=Generator.FILLER_RANDOM_CHARS, help="What to fill the left over spaces with. Default: Random Letters")
    parser.add_argument("--title", default=None, help="Word Search's Title")
    parser.add_argument("--padding", type=int, default=10, help="Amount of extra room around the edges of the puzzle. Also filled with `filler`")

    parser.add_argument("--bg-image", type=str, default=None, help="Image to use as background for PDF formatted saves.")
    parser.add_argument("--output", "-o", type=str, default=None, help="Write to named file")
    parser.add_argument("--nudge", type=float, default=0.0)


    args = parser.parse_args()

    generator = Generator(
        args.word_file,
        filler=args.filler,
        padding=args.padding,
        title=args.title,
        bg_image=args.bg_image
    )
    generator.generate()
    # generator.display()

    outfile = args.output
    if outfile is None:
        outfile = "/tmp/word-search.txt"

    generator.save(outfile, nudge=args.nudge)

    print(f"=> Word Search Saved Here: {outfile}")
