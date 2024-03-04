# Import libraries
import math
import os
import platform
import subprocess
import tkinter as tk
import warnings
from itertools import combinations
from tkinter import Tk, filedialog

import matplotlib
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
import rasterio
import ray
import rioxarray
import seaborn as sns
import spyndex
import xarray as xr
from IPython.display import clear_output, display
from ipywidgets import interactive, widgets
from mpl_toolkits.axes_grid1 import make_axes_locatable
from rasterio.io import MemoryFile
from tqdm import tqdm

# Disable all warnings
warnings.filterwarnings("ignore")

plt.rcParams["font.family"] = (
    "DejaVu Sans"  # Use a font that supports Unicode characters
)

# Check if running in an interactive session
if "CI" not in os.environ:
    root = tk.Tk()  # Create the main Tkinter
    root.wm_attributes("-topmost", 1)  # display on top
    root.eval("tk::PlaceWindow . center")
    root.withdraw()
else:
    root = None  # Set root to None in non-interactive mode/testing


# For updating widgets base on uni or multidimensional mode
def update_input(mode_value):
    if mode_value == "unidimensional":
        input_text.description = "Input File:"
        input_button.description = "Input"
    else:
        input_text.description = "Input Files:"
        input_button.description = "Inputs"


# For selecting the input(s)
def select_input(btn):
    root = tk.Tk()
    root.withdraw()
    if mode.value == "unidimensional":
        file_path = filedialog.askopenfilename(
            filetypes=[("TIFF Files", "*.tif" or "*.ttif")]
        )
        if file_path:
            input_text.options = [file_path]
            input_text.value = os.path.basename(
                file_path
            )  # Assign the file name without the path
            global input_indice
            input_indice = [rasterio.open(file_path)]
    else:
        file_paths = filedialog.askopenfilenames(
            filetypes=[("TIFF Files", "*.tif" or "*.ttif")]
        )
        if file_paths:
            input_text.options = list(file_paths)
            input_text.value = "\n".join(
                [os.path.basename(fp) for fp in file_paths]
            )  # Display file names only
            input_indices.clear()
            input_indices.extend([rasterio.open(fp) for fp in file_paths])


# For selecting output path
def select_path(button):
    root = tk.Tk()
    root.withdraw()
    save_path = filedialog.askdirectory()
    output_text.value = save_path


# for getting available Memory
def get_memory_usage():
    system_platform = platform.system()

    # Linux-specific memory monitoring
    if system_platform == "Linux":
        try:
            output = subprocess.check_output(["free", "-b"])
            lines = output.decode("utf-8").split("\n")
            data = lines[1].split()
            available_memory = int(data[6])
            return available_memory / (1024**3)  # Convert to GB
        except Exception as e:
            print("Error:", str(e))
            return None

    # Windows-specific memory monitoring
    elif system_platform == "Windows":
        try:
            response = os.popen('systeminfo | find "Available Physical Memory"').read()
            available_memory = int(
                response.split(":")[1].strip().split(" ")[0].replace(",", "")
            ) / (
                1024
            )  # Convert to GB
            return available_memory
        except Exception as e:
            print("Error:", str(e))
            return None
    else:
        print("Unsupported operating system:", system_platform)
        return None


# Check if the platform is Linux
if platform.system() == "Linux":
    # Check if running in interactive mode
    if "CI" not in os.environ:
        sudo_password = input("Enter your sudo password: ")
        clear_output(wait=True)  # Clear the output area
    else:
        # in case of non-interactive mode/tests
        sudo_password = "sudopass"


# Call rao function when a button is clicked
def click(btn):
    ray.shutdown()  # for running again
    p_minkowski = p_minkowskii.value  # Get the degree param for minkowski

    # Compute Euclidean distance between two vectors
    def euclidean_dist(pair_list):
        return math.sqrt(sum([(x[0] - x[1]) ** 2 for x in pair_list]))

    # Compute Manhattan distance between two vectors
    def manhattan_dist(pair_list):
        return sum([abs(x[0] - x[1]) for x in pair_list])

    # Compute Chebyshev distance between two vectors
    def chebyshev_dist(pair_list):
        return max([abs(x[0] - x[1]) for x in pair_list])

    # Compute Jaccard distance between two vectors
    def jaccard_dist(pair_list):
        dists = []
        for x in pair_list:
            numerator = min(x[0], x[1])
            denominator = max(x[0], x[1])
            dists.append(1 - (numerator / denominator))
        return sum(dists)

    # Compute canberra distance between two vectors
    def canberra_dist(pair_list):
        dists = []
        for x in pair_list:
            numerator = abs(x[0] - x[1])
            denominator = abs(x[0]) + abs(x[1])
            dists.append(numerator / denominator)
        return sum(dists)

    # Compute Minkowski distance between two vectors with parameter p
    def minkowski_dist(pair_list, p_minkowski):
        return sum(
            [(abs(x[0] - x[1]) ** p_minkowski) ** (1 / p_minkowski) for x in pair_list]
        )

    # Convert TIFF input(s) to NumPy array
    def tiff_to_np(tiff_input):
        matrix1 = tiff_input.read()
        matrix1 = matrix1.reshape((matrix1.shape[1]), matrix1.shape[2])
        minNum = -999
        matrix1[matrix1 == minNum] = np.nan
        return matrix1

    # Write the computation output to a GeoTIFF file
    def export_geotiff(naip_meta, output_rao, output_path):
        naip_meta["count"] = 1
        naip_meta["dtype"] = "float64"
        with rasterio.open(output_path, "w", **naip_meta) as dst:
            dst.write(output_rao, 1)

    # Computes Rao's Q index for a specified range of rows and columns
    @ray.remote
    def compute_raoq_range(
        row_start,
        row_end,
        col_start,
        col_end,
        trastersm_list,
        window,
        distance_m,
        na_tolerance,
    ):
        w = int(
            (window - 1) / 2
        )  # Number of neighbors from the central pixel to the edge of the window
        raoq_values = []  # Initialize a list to store computed Rao's Q values

        # iterate through rows and columns
        for rw in range(row_start, row_end):
            for cl in range(col_start, col_end):

                # Create a list of border condition results for all input arrays
                borderCondition = [
                    np.sum(
                        np.invert(np.isnan(x[rw - w : rw + w + 1, cl - w : cl + w + 1]))
                    )
                    < np.power(window, 2) - ((np.power(window, 2)) * na_tolerance)
                    for x in trastersm_list
                ]

                # Check if any array satisfies the border condition
                if True in borderCondition:
                    raoq_values.append(np.nan)
                else:

                    # Extract sub-windows for all input arrays
                    tw = [
                        x[rw - w : rw + w + 1, cl - w : cl + w + 1]
                        for x in trastersm_list
                    ]
                    lv = [x.ravel() for x in tw]  # Flatten the sub-windows

                    # Generate combinations of sub-window pairs
                    vcomb = combinations(range(lv[0].shape[0]), 2)
                    vcomb = list(vcomb)
                    vout = []

                    # Calculate  selected distances for all sub-window pairs
                    for comb in vcomb:
                        lpair = [[x[comb[0]], x[comb[1]]] for x in lv]
                        if distance_m == "euclidean":
                            out = euclidean_dist(lpair)
                        elif distance_m == "manhattan":
                            out = manhattan_dist(lpair)
                        elif distance_m == "chebyshev":
                            out = chebyshev_dist(lpair)
                        elif distance_m == "canberra":
                            out = canberra_dist(lpair)
                        elif distance_m == "minkowski":
                            out = minkowski_dist(lpair, p_minkowski)
                        elif distance_m == "Jaccard":
                            out = jaccard_dist(lpair)
                        vout.append(out)

                    # Rescale the computed distances and calculate Rao's Q value
                    vout_rescaled = [x * 2 for x in vout]
                    vout_rescaled[:] = [x / window**4 for x in vout_rescaled]
                    raoq_value = np.nansum(vout_rescaled)
                    raoq_values.append(raoq_value)

        # Return the results for the specified row and column range
        return row_start, row_end, col_start, col_end, raoq_values

    # Parallelizes the computation of Rao's Q
    def parallel_raoq(
        data_input,
        output_path,
        distance_m="euclidean",
        window=9,
        na_tolerance=0.0,
        batch_size=100,
    ):
        if window % 2 == 1:
            w = int((window - 1) / 2)
        else:
            raise Exception(
                "The size of the moving window must be an odd number. Exiting..."
            )

        # Convert input data to NumPy arrays
        numpy_data = [tiff_to_np(data) for data in data_input]

        # Initialize raoq array with NaN values
        raoq = np.zeros(shape=numpy_data[0].shape)
        raoq[:] = np.nan

        # Create a list of transformed arrays for each input
        trastersm_list = []
        for mat in numpy_data:
            trasterm = np.zeros(shape=(mat.shape[0] + 2 * w, mat.shape[1] + 2 * w))
            trasterm[:] = np.nan
            trasterm[w : w + mat.shape[0], w : w + mat.shape[1]] = mat
            trastersm_list.append(trasterm)

        # Adjust batch size to fit all pixels
        max_rows = numpy_data[0].shape[0] - 2 * w + 1
        max_cols = numpy_data[0].shape[1] - 2 * w + 1
        batch_size = min(batch_size, max_rows, max_cols)

        # Adjust row and column batches
        rows = numpy_data[0].shape[0]
        cols = numpy_data[0].shape[1]
        row_batches = range(w, rows + w, batch_size)
        col_batches = range(w, cols + w, batch_size)

        # Adjust the last batch
        row_batches = list(row_batches)
        col_batches = list(col_batches)
        if row_batches[-1] != rows + w:
            row_batches.append(rows + w)
        if col_batches[-1] != cols + w:
            col_batches.append(cols + w)

        # Use Ray to parallelize the computation
        ray_results = []
        for row_start, row_end in zip(row_batches[:-1], row_batches[1:]):
            for col_start, col_end in zip(col_batches[:-1], col_batches[1:]):
                pixel_data = (
                    row_start,
                    row_end,
                    col_start,
                    col_end,
                    trastersm_list,
                    window,
                    distance_m,
                    na_tolerance,
                )
                ray_results.append(compute_raoq_range.remote(*pixel_data))

        # Update raoq array with the computed values
        with tqdm(total=len(ray_results)) as pbar:
            for result in ray_results:
                row_start, row_end, col_start, col_end, raoq_values = ray.get(result)
                raoq[row_start - w : row_end - w, col_start - w : col_end - w] = (
                    np.array(raoq_values).reshape(
                        row_end - row_start, col_end - col_start
                    )
                )
                pbar.update(1)

        # Export the computed Rao's Q index as a TIFF file
        info = data_input[0].profile
        export_geotiff(info, raoq, output_path)

    # Use the obtained password with the sudo command for linux platform
    if platform.system() == "Linux":
        command = f'echo "{sudo_password}" | sudo -S mount -o remount,size={memory_slider.value}G /dev/shm'
        os.system(command)

    # Initialize Ray
    ray.init(
        num_cpus=num_cpu_cores.value,
        object_store_memory=memory_slider.value * 10**9,
    )
    output = parallel_raoq(
        data_input=(input_indice if mode.value == "unidimensional" else input_indices),
        output_path=(
            r"{}/{}.tif".format(output_text.value, output_filename_text.value)
        ),
        distance_m=distance_options.value,
        window=window.value,
        na_tolerance=na_tolerance.value,
        batch_size=batch_size.value,
    )
    # Shutdown Ray
    ray.shutdown()


input_indices = []  # List to store input rasterio.DatasetReader instances

# Create widgets for input parameters
mode = widgets.ToggleButtons(
    options=["unidimensional", "multidimensional"],
    description="Mode:",
    value="unidimensional",
)

# Define the toggle buttons
distance_options = widgets.ToggleButtons(
    options=[
        "euclidean",
        "manhattan",
        "chebyshev",
        "Jaccard",
        "canberra",
        "minkowski",
    ],
    description="Distance:",
    value="euclidean",
)

# Create the layout using GridBox
buttons_layout = widgets.GridBox(
    children=[distance_options],
    layout=widgets.Layout(grid_template_columns="repeat(1, 1fr)"),
)

# Create widgets for input parameters
output_text = widgets.Text(
    description="Output Path:", placeholder="Enter output path here"
)
output_button = widgets.Button(description="Output Path")
output_filename_text = widgets.Text(description="Output name:", value="Rao")
p_minkowskii = widgets.BoundedIntText(description="degree:", value=2, min=2, max=5000)
window = widgets.BoundedIntText(description="Window:", min=1, max=333, step=2, value=3)
na_tolerance = widgets.BoundedFloatText(
    description="NA Tolerance:", min=0, max=1, step=0.1, value=0.0
)
batch_size = widgets.BoundedIntText(
    description="Batch size:", min=10, max=10000, step=10, value=100
)
input_text = widgets.Textarea(
    value="", description="Input File:", placeholder="Input file(s) name"
)

# Create a Dropdown for workers
import multiprocessing

num_cpu_cores = widgets.Dropdown(
    options=list(range(1, multiprocessing.cpu_count() + 1)),
    description="CPU workers:",
)

# Get available memory
available_memory = get_memory_usage()
if available_memory is not None:
    # Calculate the maximum value for the slider (85% of available memory)
    max_slider_value = int(available_memory * 0.85)
else:
    print("Unable to retrieve available memory information.")
    max_slider_value = 10

# Create a slider for available memory
memory_slider = widgets.IntSlider(
    value=0, min=1, max=max_slider_value, step=1, description=f"Memory (GB):"
)

# Buttons
input_button = widgets.Button(description="Input")
run_button = widgets.Button(description="Run")

# adjustment
input_button.layout.margin = "0px 0px 0px 50px"
p_minkowskii.layout.margin = "0px 0px 0px 50px"
run_button.layout.margin = "0px 0px 0px 170px"
input_text.layout.height = "90px"
input_text.layout.width = "350px"

# Update data input widget when mode is changed
mode.observe(lambda change: update_input(change["new"]), names="value")

# Header
header_widget = widgets.HTML(
    "<h3 style='font-family: Arial, sans-serif; color: white; font-weight: semibold;background-color: blue; text-align: center;'>Extract Rao’s-Q diversity</h3>"
)
header_widget.layout.width = "300px"
header_widget.layout.height = "25px"
display(header_widget)

# Create box layouts for widgets
vbox_margin = "10px"
input_widgets = widgets.VBox(
    [
        widgets.HBox(
            [
                mode,
                input_button,
                output_text,
                output_button,
                output_filename_text,
                input_text,
            ]
        ),
        widgets.HBox([window, na_tolerance, batch_size, num_cpu_cores, memory_slider]),
        widgets.HBox([buttons_layout, p_minkowskii, run_button]),
    ],
    layout=widgets.Layout(justify_content="space-between", margin=f"0px {vbox_margin}"),
)

# Attach functions to buttons
input_button.on_click(select_input)
output_button.on_click(select_path)
run_button.on_click(click)

# Display the input widgets
display(input_widgets)
