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

# Define a dic for datasets
indices_dict = {}


# Function to open and reproject GeoTIFF datasets
def open_gd(bt):
    clear_output(wait=True)  # Clear the output area

    # Select GeoTIFF datasets using Tkinter
    root = Tk()
    root.withdraw()
    file_paths = filedialog.askopenfilenames(
        filetypes=(("GeoTIFF files", "*.tif;*.tiff"), ("All files", "*.*"))
    )
    global dataset_dict
    dataset_dict = {}  # For saving selected datasets
    for file_path in file_paths:
        global file_name
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        dataset = xr.open_rasterio(file_path).astype("float64")

        # Reprojection datasets
        dst_crs = "EPSG:4326"  # Define the target CRS (WGS 84, EPSG:4326)
        dataset = dataset.rio.reproject(dst_crs)  # Reproject the dataset to EPSG:4326
        dataset = dataset.where(dataset != 0, np.nan)  # Replace 0 values with NaN
        bounds = dataset.rio.transform()
        dataset_dict[file_name] = {"dataset": dataset, "bounds": bounds}

    print("GeoTIFF datasets loaded:", dataset_dict.keys())
    display(widgets_row)  # Display the main container


# Normalize the bands to the range [0, 1]
def normalize(band):
    band_min, band_max = (band.min(), band.max())
    return (band - band_min) / ((band_max - band_min))


# For calculating desire indices
def calculate_indices(b):

    # Check if user selected any VI ro not
    if len(index_selection.value) == 0:
        print("Error: Please select one or more indices to campute.")
        return
    selected_bands = [selection_widget.value for selection_widget in band_selection]
    selected_indices = (
        list(index_selection.value)
        if len(index_selection.value) > 1
        else list(index_selection.value)[0]
    )
    global indices_dict
    indices_dict = {}
    for file_name, data in dataset_dict.items():
        dataset = data["dataset"]
        bounds = data["bounds"]
        snt = dataset / 10000
        index = index_names

        # Specify parameters for indices calculation
        params = {
            "B": snt.sel(band=selected_bands[0]),
            "G": snt.sel(band=selected_bands[1]),
            "R": snt.sel(band=selected_bands[2]),
            "RE1": snt.sel(band=selected_bands[3]),
            "N": snt.sel(band=selected_bands[4]),
            "N2": snt.sel(band=selected_bands[5]),
            "L": 0.5,
            "g": 2.5,
            "C1": 6,
            "C2": 7.5,
            "kNN": 0.5,
            "kNR": spyndex.computeKernel(
                kernel="RBF",
                params={
                    "a": snt.sel(band=selected_bands[4]),
                    "b": snt.sel(band=selected_bands[2]),
                    "sigma": snt.sel(band=[selected_bands[4], selected_bands[2]]).mean(
                        "band"
                    ),
                },
            ),
        }

        # Calculate the indices and place them in the defined dictionary
        idx = spyndex.computeIndex(index=selected_indices, params=params)
        indices_dict[file_name] = {}

        # Add bands to dictionary as seperate Gtiff
        for band in snt.band:
            selected_band_data = snt.sel(band=band)
            bands_data = normalize(selected_band_data)
            indices_dict[file_name][f"Band{band.item()}"] = bands_data
        if len(index_selection.value) > 1:
            for i in selected_indices:
                indices_data = idx.sel(index=f"{i}")
                normalized_data = normalize(indices_data)
                indices_dict[file_name][i] = normalized_data
        else:
            indices_data = idx
            normalized_data = normalize(indices_data)
            indices_dict[file_name][selected_indices] = normalized_data

    # Calculate and add CV values
    for dataset, indices in indices_dict.items():
        for index_name, index_data in indices.items():
            mean_value = np.mean(index_data)
            std_deviation = np.std(index_data)
            cv_percentage = (std_deviation / mean_value) * 100  # CV in percentage

            # Add to existing dictionary
            indices[index_name]["cv_percentage"] = cv_percentage
    print("Indices calculation finished!")
    dataset_up_dr()


# For Ploting figures
def plot_figure(button):
    clear_output(wait=True)  # Clear the output for multiple attempts

    # Get values from widgets
    selected_dataset = dataset_dropdown.value
    selected_indices = indices_dropdown.value
    selected_cmap = cmap_dropdown.value
    cv_value = float(indices_dict[selected_dataset][selected_indices]["cv_percentage"])
    bounds = dataset_dict[selected_dataset]["bounds"]
    selected_indices_data = indices_dict[selected_dataset][selected_indices]
    normalized_indices_data = normalize(selected_indices_data)

    # Figure options
    plt.figure(figsize=(20, 5))
    plt.imshow(normalized_indices_data, cmap=selected_cmap, vmin=0, vmax=1)
    cbar = plt.colorbar(pad=0.01, label="Value")
    cbar.ax.get_yaxis().label.set_fontsize(12)  # Set font size for the colorbar label
    cbar.ax.get_yaxis().label.set_fontweight(
        "bold"
    )  # Set font weight for colorbar label
    plt.title(
        f"{selected_indices} - {selected_dataset} - CV: {cv_value:.2f}%\n",
        size=14,
        fontweight="semibold",
    )
    x_ticks = np.linspace(
        bounds[2], (bounds[2] + selected_indices_data.shape[1] * bounds[0]), num=5
    )
    y_ticks = np.linspace(
        bounds[5], (bounds[5] + selected_indices_data.shape[0] * bounds[4]), num=5
    )
    plt.xticks(
        np.linspace(0, selected_indices_data.shape[1], num=5),
        ["{:.2f}\u00b0 {}".format(tick, "W" if tick < 0 else "E") for tick in x_ticks],
        size=10,
        fontweight="semibold",
        ha="left",
    )
    plt.yticks(
        np.linspace(0, selected_indices_data.shape[0], num=5),
        ["{:.2f}\u00b0 {}".format(tick, "S" if tick < 0 else "N") for tick in y_ticks],
        size=10,
        fontweight="semibold",
    )
    plt.gca().xaxis.get_major_ticks()[4].label1.set_visible(False)
    plt.gca().xaxis.get_major_ticks()[4].tick1line.set_visible(False)
    plt.gca().yaxis.get_major_ticks()[4].label1.set_visible(False)
    plt.gca().yaxis.get_major_ticks()[4].tick1line.set_visible(False)

    plt.xlabel("Longitude", size=12, fontweight="semibold")
    plt.ylabel("Latitude", size=12, fontweight="semibold")
    plt.xticks(rotation=0)  # Rotate the x-axis ticks
    plt.yticks(rotation=90)  # Rotate the y-axis ticks
    display(widgets_row)
    plt.show()


# For selecting the Path
def select_path(button):
    root = tk.Tk()
    root.withdraw()
    save_path = filedialog.askdirectory()
    save_path_text.value = save_path
    save_path_text_2.value = save_path


# For saving the figure
def save_figure(button):

    # Get values from widgets
    selected_dataset = dataset_dropdown.value
    selected_indices = indices_dropdown.value
    selected_cmap = cmap_dropdown.value
    save_path = save_path_text.value
    save_name = save_name_text.value
    dpi = dpi_dropdown.value
    file_format = format_dropdown.value
    cv_value = float(indices_dict[selected_dataset][selected_indices]["cv_percentage"])
    bounds = dataset_dict[selected_dataset]["bounds"]
    selected_indices_data = indices_dict[selected_dataset][selected_indices]
    normalized_indices_data = normalize(selected_indices_data)

    # Figure options
    plt.figure(figsize=(20, 5))
    plt.imshow(normalized_indices_data, cmap=selected_cmap, vmin=0, vmax=1)
    cbar = plt.colorbar(pad=0.01, label="Value")
    cbar.ax.get_yaxis().label.set_fontsize(12)
    cbar.ax.get_yaxis().label.set_fontweight("bold")
    plt.title(
        f"{selected_indices} - {selected_dataset} - CV: {cv_value:.2f}%\n",
        size=14,
        fontweight="semibold",
    )
    x_ticks = np.linspace(
        bounds[2], (bounds[2] + selected_indices_data.shape[1] * bounds[0]), num=5
    )
    y_ticks = np.linspace(
        bounds[5], (bounds[5] + selected_indices_data.shape[0] * bounds[4]), num=5
    )
    plt.xticks(
        np.linspace(0, selected_indices_data.shape[1], num=5),
        ["{:.2f}\u00b0 {}".format(tick, "W" if tick < 0 else "E") for tick in x_ticks],
        size=10,
        fontweight="semibold",
        ha="left",
    )
    plt.yticks(
        np.linspace(0, selected_indices_data.shape[0], num=5),
        ["{:.2f}\u00b0 {}".format(tick, "S" if tick < 0 else "N") for tick in y_ticks],
        size=10,
        fontweight="semibold",
    )
    plt.gca().xaxis.get_major_ticks()[4].label1.set_visible(False)
    plt.gca().xaxis.get_major_ticks()[4].tick1line.set_visible(False)
    plt.gca().yaxis.get_major_ticks()[4].label1.set_visible(False)
    plt.gca().yaxis.get_major_ticks()[4].tick1line.set_visible(False)
    plt.xlabel("Longitude", size=12, fontweight="semibold")
    plt.ylabel("Latitude", size=12, fontweight="semibold")
    plt.yticks(rotation=90)  # Rotate the y-axis ticks
    save_figure_path = f"{save_path}/{save_name}.{file_format}"
    plt.savefig(save_figure_path, dpi=dpi, bbox_inches="tight")
    plt.close()
    print(f"Figure saved as {save_figure_path}")


# For saving Gtiff of selected VI files
def save_indices(button):

    # Get user-selected inputs
    selected_dataset = dataset_dropdown_2.value
    selected_indices_with_cv = index_tosave.value
    save_path = save_path_text.value
    dataset_info = dataset_dict[selected_dataset]

    # Iterate over selected indices and save selected indices GeoTIFFs
    for index_with_cv in selected_indices_with_cv:
        index_name = index_with_cv.split(" ---------- ")[0]
        index_data = indices_dict[selected_dataset][f"{index_name}"]
        output_path = f"{save_path}/{selected_dataset}_{index_name}.tif"
        original_dataset = dataset_info["dataset"]
        index_data.rio.write_crs(original_dataset.rio.crs, inplace=True)
        index_data.rio.to_raster(output_path, compress="lzw")
        print(f"Index '{index_name}' saved as {output_path}")


# For updating the dataset dropdowns
def dataset_up_dr():

    # First dataset dropdown
    dataset_dropdown.options = list(indices_dict.keys())
    dataset_dropdown.value = list(dataset_dict.keys())[0]
    indices_dropdown.options = list(indices_dict[file_name].keys())

    # Second dataset dropdown
    dataset_dropdown_2.options = list(dataset_dict.keys())
    dataset_dropdown_2.value = list(dataset_dict.keys())[0]


# For updating the index_tosave widget with indices sorted by CV value
def indices_up_dr(change):
    selected_location = change.new
    selected_indices = indices_dict.get(selected_location, {})
    sorted_indices = sorted(
        selected_indices.items(), key=lambda x: x[1]["cv_percentage"], reverse=True
    )  # Sort indices based on CV value
    index_tosave.options = [
        f"{index_name} ---------- CV value: {index_info['cv_percentage']:.2f}%"
        for index_name, index_info in sorted_indices
    ]


# Create header widgets
header_widget1 = widgets.HTML(
    "<h3 style='font-family: Arial, sans-serif; color: white; font-weight:semibold; background-color: blue; text-align: center;'>Bands Order</h3>"
)
header_widget2 = widgets.HTML(
    "<h3 style='font-family: Arial, sans-serif; color: white; font-weight: semibold; background-color: blue; text-align: center;'>Indices Selection</h3>"
)
header_widget3 = widgets.HTML(
    "<h3 style='font-family: Arial, sans-serif; color: white; font-weight: semibold; background-color: blue; text-align: center;'>Indices Visualization</h3>"
)
header_widget4 = widgets.HTML(
    "<h3 style='font-family: Arial, sans-serif; color: white; font-weight: semibold; background-color: blue; text-align: center;'>Saving Indices</h3>"
)

# Create a button widget for loading
load_button = widgets.Button(description="Load Datasets")

# Create GUI for band selection
band_names = [
    "Blue",
    "Green",
    "Red",
    "Red Edge",
    "Near Infrared 1",
    "Near Infrared 2",
]
default_band_numbers = [2, 3, 5, 6, 7, 8]  # Default band numbers (for WV-2 dataset)
band_selection = []
for i in range(len(band_names)):
    selection_widget = widgets.Dropdown(
        options=list(range(1, 10)),
        value=default_band_numbers[i],  # Set default value
        description=band_names[i] + ":",
    )
    band_selection.append(selection_widget)

# Indices list
index_names = [
    "ARI",
    "ARI2",
    "BAI",
    "BCC",
    "BNDVI",
    "CIG",
    "CIRE",
    "CVI",
    "DVI",
    "EVI",
    "EVI2",
    "ExG",
    "ExGR",
    "ExR",
    "FCVI",
    "GARI",
    "GBNDVI",
    "GCC",
    "GLI",
    "GNDVI",
    "GOSAVI",
    "GRNDVI",
    "GRVI",
    "GSAVI",
    "IKAW",
    "IPVI",
    "MCARI",
    "MCARI1",
    "MCARI2",
    "MCARIOSAVI",
    "MGRVI",
    "MNLI",
    "MRBVI",
    "MSAVI",
    "MSR",
    "MTVI1",
    "MTVI2",
    "NDREI",
    "NDTI",
    "NDVI",
    "NDWI",
    "NDYI",
    "NGRDI",
    "NIRv",
    "NLI",
    "NormG",
    "NormNIR",
    "NormR",
    "OSAVI",
    "RCC",
    "RDVI",
    "RGBVI",
    "RGRI",
    "RI",
    "SARVI",
    "SAVI",
    "SI",
    "SR",
    "SR2",
    "SR3",
    "SeLI",
    "TCARI",
    "TCARIOSAVI",
    "TCI",
    "TDVI",
    "TGI",
    "TVI",
    "TriVI",
    "VARI",
    "VARI700",
    "VI700",
    "VIG",
    "kIPVI",
    "kNDVI",
    "kRVI",
]

# Create multiselection for selecting indices to calculate
index_selection = widgets.SelectMultiple(
    options=index_names, layout=widgets.Layout(width="300px", height="190px")
)

# Create multiselection box for indices we want to save
index_tosave = widgets.SelectMultiple(
    layout=widgets.Layout(width="300px", height="90px")
)

# For indices calculation button
calculate_button = widgets.Button(description="Calculate Indices")
calculate_button.layout.margin = "0px 0px 0px 140px"  # Adjust the margins
calculate_button.layout.width = "150px"

# For plotting and saving the figure
plot_button = widgets.Button(description="Plot Figure")
save_button = widgets.Button(description="Save Figure")
path_button = widgets.Button(description="Output Path")

# For entering the save path and plot name
save_path_text = widgets.Text(
    description="Output Path:", placeholder="Enter output path here"
)
save_name_text = widgets.Text(
    description="Output Name:",
    placeholder="Enter plot name here",
    value="index_fig",
)

# For DPI, Format and Colormap
dpi_dropdown = widgets.Dropdown(
    description="DPI:", options=[100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
)
format_dropdown = widgets.Dropdown(
    description="Format:", options=["png", "jpg", "svg", "tiff", "tif"]
)
cmap_dropdown = widgets.Dropdown(
    description="Colormap:", options=plt.colormaps(), value="nipy_spectral"
)

# Dataset and Indices dropdowns
indices_dropdown = widgets.Dropdown(options=[], description="Indices:")
dataset_dropdown = widgets.Dropdown(
    options=list(indices_dict.keys()), description="Dataset:"
)

# For dataset selection
dataset_dropdown_2 = widgets.Dropdown(
    options=list(indices_dict.keys()), description="Dataset:"
)

# For save path
save_path_text_2 = widgets.Text(
    description="Output Path:", placeholder="Enter output path here"
)
path_button_2 = widgets.Button(description="Output Path")
save_button_2 = widgets.Button(description="Save Indices")
path_button_2.layout.margin = "4px 4px 0px 155px"
save_button_2.layout.margin = "6px 6px 0px 155px"

# ordering Containers for widgets
plot_container = widgets.HBox([cmap_dropdown, plot_button])
path_container = widgets.HBox([save_path_text, path_button])
dropdowns_container = widgets.VBox([dpi_dropdown, format_dropdown])
save_container = widgets.HBox([save_name_text, save_button])
main_container = widgets.VBox(
    [
        dataset_dropdown,
        indices_dropdown,
        plot_container,
        dropdowns_container,
        path_container,
        save_container,
    ]
)
widgets_container = widgets.VBox(
    [
        dataset_dropdown_2,
        index_tosave,
        save_path_text_2,
        path_button_2,
        save_button_2,
    ]
)
index_widget = widgets.VBox([index_selection, calculate_button])
vbox_margin = "10px"
widgets_row = widgets.HBox(
    [
        load_button,
        widgets.VBox([header_widget1] + band_selection),
        widgets.VBox([header_widget2, index_widget]),
        widgets.VBox([header_widget3, main_container]),
        widgets.VBox([header_widget4, widgets_container]),
    ],
    layout=widgets.Layout(justify_content="space-between", margin=f"0px {vbox_margin}"),
)
display(widgets_row)

# Attach the update function to the dropdown's value change event
dataset_dropdown_2.observe(indices_up_dr, names="value")

# Attach functions to buttons
load_button.on_click(open_gd)
calculate_button.on_click(calculate_indices)
plot_button.on_click(plot_figure)
save_button.on_click(save_figure)
path_button.on_click(select_path)
path_button_2.on_click(select_path)
save_button_2.on_click(save_indices)
