#!/usr/bin/python3

"""
Entry point for converting bin to png
"""

import bin_conversion
import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--directory', required=True, help="directory to ps2 collection, also the output directory")
    parser.add_argument('-p', '--processes', type=int, help="max spawnable processes used by multiprocessing", default=-1)


    args = parser.parse_args()
    return args

def main():
    args = parse_args()

    # converting all images in a dir from bin to png
    print("Converting bins to pngs")

    bin_conversion.convert_dirs(args.directory, processes=args.processes)


if __name__ == "__main__":
    main()
