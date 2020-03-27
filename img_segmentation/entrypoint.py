#!/usr/bin/python3

"""
Entry point for segmenting image
"""

import image_segmentation
import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--directory', required=True, help="directory to ps2 collection, also the output directory")
    parser.add_argument('-p', '--processes', type=int, help="max spawnable processes used by multiprocessing", default=-1)

    args = parser.parse_args()
    return args

def main():
    args = parse_args()

    # segmenting images using new python macro
    print("segmenting images")
    image_segmentation.process_collection(args.directory, args.processes)

if __name__ == "__main__":
    main()
