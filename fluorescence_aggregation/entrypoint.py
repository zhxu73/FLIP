#!/usr/bin/python3

"""
Entry point for generate fluorescence aggregation
"""

import fluorescence_aggregation
import argparse
import os
import json


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--directory', required=True, help="directory to ps2 collection")
    parser.add_argument('-o', '--output', required=True, help="directory for output files.")

    args = parser.parse_args()
    return args

def main():
    args = parse_args()

    this_dir = os.path.dirname(os.path.abspath(__file__))

    # getting offsets
    with open(os.path.join(this_dir, "static", "ps2", "sensor_fixed_metadata.json"), 'r') as f:
        ps2_dict = json.load(f)
        ps2_x = float(ps2_dict[0]['location_in_camera_box_m']['x'])
        ps2_y = float(ps2_dict[0]['location_in_camera_box_m']['y'])

    print("generating aggregates")
    fluorescence_aggregation.generate_aggregate(
        args.directory,
        args.output,
        os.path.join(this_dir, "static", 'Plot boundaries.xlsx'),
        os.path.join(this_dir, "static", 'multithresh.json'),
        ps2_x,
        ps2_y
    ) # generating aggregates
    fluorescence_aggregation.generate_fluorescence(args.directory, args.output, True) # generate fluorescence files

    print("Finished processing", args.directory)

if __name__ == "__main__":
    main()
