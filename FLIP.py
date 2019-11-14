"""
Fluorescence Imaging Pipeline main file

Jacob Long
2019-11-7
"""

import argparse
import json
import os
import subprocess
import sys
import tkinter
import tkinter.filedialog as fd
import tkinter.ttk

import bin_conversion
import fluorescence_aggregation
import image_segmentation

# getting the directory that this file is running from
this_dir = os.path.dirname(os.path.abspath(__file__))

def headless(directory):
    """run the full pipeline on a directory without a gui"""

    bin_conversion.convert_dirs(directory) # converting all images in a dir from bin to png
    # imagej_macro(args.macro, args.directory) # old fiji macro
    image_segmentation.process_collection(directory) # new python macro

    # getting offsets
    with open(os.path.join(this_dir, "static", "ps2", "sensor_fixed_metadata.json"), 'r') as f:
        ps2_dict = json.load(f)
        ps2_x = float(ps2_dict[0]['location_in_camera_box_m']['x'])
        ps2_y = float(ps2_dict[0]['location_in_camera_box_m']['y'])

    fluorescence_aggregation.generate_aggregate(
        directory, 
        os.path.join(this_dir, "static", 'Plot boundaries.xlsx'),
        os.path.join(this_dir, "static", 'multithresh.json'),
        ps2_x, 
        ps2_y
    ) # generating aggregates
    fluorescence_aggregation.generate_fluorescence(directory, True) # generate fluorescence files

    print("Finished processing", directory)

def run_imagej_macro():
    """
    runs a command that will call imagej with a specified macro
    """

    # trying to find a local imagej installation, but if one is not found, ask the user where it is
    imagej_path = os.path.join(this_dir, 'Fiji.app/ImageJ-win64.exe')
    if not os.path.exists(imagej_path):
        imagej_path = fd.askopenfilename(title="Could not find imagej, please select your imagej.exe")

    # asking the user where their imagej macro is.
    macro_path = fd.askopenfilename(title="Please select an imagej macro")

    # if the user cancels either of the selections, return
    if not macro_path or not imagej_path:
        return

    subprocess.call([
        imagej_path,
        "-macro",
        macro_path
    ])

def gui():
    # setting up tkinter window
    root = tkinter.Tk()
    root.title("Generate Fluorescence Aggregates")
    # root.geometry("300x125")
    # root.configure(background='white')
    root.resizable(False, False)

    # configuring grid for resizable buttons
    tkinter.Grid.columnconfigure(root, 0, weight=1)
    for y in range(3):
        tkinter.Grid.rowconfigure(root, y, weight=1)

    # creating a button for each main function
    bin_to_binary_btn = tkinter.ttk.Button(
        root, 
        text="Binary To PNG", 
        command=lambda: bin_conversion.convert_dirs(fd.askdirectory(title="Please select a ps2 collection"))
    )
    bin_to_binary_btn.grid(column=0, row=0, sticky="nsew", padx=2, pady=2, ipadx=10, ipady=7, columnspan=2)

    imagej_macro_btn = tkinter.ttk.Button(
        root, 
        text="ImageJ Macro", 
        command=run_imagej_macro
    )
    imagej_macro_btn.grid(column=0, row=1, sticky="nsew", padx=2, pady=2, ipadx=10, ipady=7)

    image_segmentation_btn = tkinter.ttk.Button(
        root, 
        text="Python Macro", 
        command=lambda: image_segmentation.process_collection(fd.askdirectory(title="Please select a ps2 collection"))
    )
    image_segmentation_btn.grid(column=1, row=1, sticky="nsew", padx=2, pady=2, ipadx=10, ipady=7)

    # getting offsets
    with open(os.path.join(this_dir, "static", "ps2", "sensor_fixed_metadata.json"), 'r') as f:
        ps2_dict = json.load(f)
        ps2_x = float(ps2_dict[0]['location_in_camera_box_m']['x'])
        ps2_y = float(ps2_dict[0]['location_in_camera_box_m']['y'])

    # calling single process
    # using a file dialog, ask the user for a collection path
    # use the Plot boundaries.xlsx and multithresh json next to this file
    # use offsets from sensor_fixed_metadata.json
    generate_aggregate_btn = tkinter.ttk.Button(
        root, 
        text="Generate Aggregate and Fluorescence", 
        command=lambda: fluorescence_aggregation.single_process(
            filepath=fd.askdirectory(title="Please select a ps2 collection"),
            plot_boundaries=os.path.join(this_dir, 'static', 'Plot boundaries.xlsx'),
            multithresh_json=os.path.join(this_dir, 'static', 'multithresh.json'),
            offset_x=ps2_x,
            offset_y=ps2_y
        ),
    )
    generate_aggregate_btn.grid(column=0, row=2, sticky="nsew", padx=2, pady=2, ipadx=10, ipady=7, columnspan=2)

    # starting gui
    root.mainloop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--directory', help="directory to ps2 collection")
    # parser.add_argument('-m', '--macro', help="filepath to an imagej macro", required=True)

    args = parser.parse_args()

    # if the user gave command line arguments, then use the cli, else open a gui
    if args.directory:
        headless(args.directory)
    else:
        gui()
