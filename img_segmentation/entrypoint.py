#!/usr/bin/python3

"""
Entry point for segmenting image
"""

import image_segmentation
import argparse

# getting the directory that this file is running from
this_dir = os.path.dirname(os.path.abspath(__file__))

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--directory', required=True, help="directory to ps2 collection")
    parser.add_argument('-o', '--output', required=True, help="directory for output files.")
    parser.add_argument('-p', '--processes', help="max spawnable processes used by multiprocessing", default=-1)

    args = parser.parse_args()
    return args

def main():
    args = parse_args()

    # segmenting images using new python macro
    print("segmenting images")
    image_segmentation.process_collection(args.directory)

if __name__ == "__main__":
    main()
