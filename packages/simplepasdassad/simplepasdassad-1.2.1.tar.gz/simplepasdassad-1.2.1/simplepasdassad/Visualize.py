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


# To open and add selected files to the dictionary
def add_files_to_dict(i):
    root = Tk()
    root.withdraw()
    file_paths = filedialog.askopenfilenames(
        filetypes=(("GeoTIFF files", "*.tif;*.tiff"), ("All files", "*.*"))
    )
    files = []
    if file_paths:
        for file_path in file_paths:
            file_name = os.path.basename(file_path).split(".")[0]
            files.append((file_name, file_path))
        for file_name, src in files:
            file_dict[file_name] = src
            print(f"File '{file_name}' added to the dictionary.")
        update_file_dropdown()
        update_files_select_multiple()
    else:
        print("No file selected.")


# To update dropdown widgets with file names
def update_file_dropdown():
    file_dropdown.options = list(file_dict.keys())


# To update the SelectMultiple widget with file names
def update_files_select_multiple():
    files_select_multiple.options = list(file_dict.keys())


# To select an output directory
def select_path(b):
    root = Tk()
    root.withdraw()
    directory = filedialog.askdirectory()
    if directory:
        output_directory_textbox.value = directory


# To normalize data (0,1)
def normalize_data(data):
    if np.isnan(np.nanmin(data)) or np.isnan(np.nanmax(data)):
        # Handle cases where all values are NaN
        normalized_data = np.zeros_like(data)
    else:
        normalized_data = (data - np.nanmin(data)) / (np.nanmax(data) - np.nanmin(data))
    return normalized_data


# Changing ticks format to dms
def decimal_degrees_to_dms(dd):
    degrees = int(dd)
    minutes = int((dd - degrees) * 60)
    seconds = ((dd - degrees) * 60 - minutes) * 60
    return degrees, minutes, seconds


# Function to plot an individual file with matplotlib
def plot_individual_file(b):
    clear_output(wait=True)
    display(header_widget, widget_box)
    file_name = file_dropdown.value
    file_path = file_dict.get(file_name, None)  # Get the file_path from the dict
    colormap = colormap_dropdown.value
    output_dir = output_directory_textbox.value
    output_file_name = output_filename_textbox.value
    dpi = dp_dropdown.value
    file_format = fmt_dropdown.value
    output_filename = os.path.join(
        output_dir, f"{file_name}_{output_file_name}.{file_format}"
    )  # For saving
    if file_path and colormap and output_dir and output_file_name:
        with rasterio.open(file_path) as src:
            data = src.read(1)
            transform = src.transform

            # Extract latitude and longitude from the georeferencing information
            lat, long = transform * (
                0,
                0,
            )  # Extract the coordinates from the top-left corner
            lat_deg, lat_min, lat_sec = decimal_degrees_to_dms(lat)
            long_deg, long_min, long_sec = decimal_degrees_to_dms(long)
        num_rows, num_cols = data.shape
        x = np.arange(0, num_cols) * transform.a + transform.c
        y = np.arange(0, num_rows) * transform.e + transform.f

        plt.figure(figsize=(8, 6))
        plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(nbins=1))
        plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(nbins=1))

        im = plt.imshow(
            normalize_data(data),
            cmap=colormap,
            extent=[x.min(), x.max(), y.min(), y.max()],
        )
        cbar = plt.colorbar(im, label="Value", pad=0.01)
        cbar.ax.get_yaxis().label.set_fontsize(
            12
        )  # Set font size for the colorbar label
        cbar.ax.get_yaxis().label.set_fontweight(
            "bold"
        )  # Set font weight for colorbar label
        plt.title(f"{file_name}\n", fontsize=14, fontweight="bold")
        x_ticks = np.linspace(x.min(), x.max(), num=len(plt.xticks()[0]))
        y_ticks = np.linspace(y.min(), y.max(), num=len(plt.yticks()[0]))

        # Set the x and y tick labels as DMS format with symbols
        plt.gca().set_xticklabels(
            [
                "%.0f° %.0f' %.0f\" %s"
                % (*decimal_degrees_to_dms(val), "W" if val < 0 else "E")
                for val in x_ticks
            ]
        )
        plt.gca().set_yticklabels(
            [
                "%.0f° %.0f' %.0f\" %s"
                % (*decimal_degrees_to_dms(val), "S" if val < 0 else "N")
                for val in y_ticks
            ]
        )
        plt.xticks(rotation=0, fontsize=10, ha=ha_widget.value, fontweight="bold")
        plt.yticks(rotation=90, fontsize=10, va=va_widget.value, fontweight="bold")
        plt.xlabel("Longitude", fontsize=12, fontweight="bold")
        plt.ylabel("Latitude", fontsize=12, fontweight="bold")
        plt.grid(False)
        if save_checkbox.value:
            plt.savefig(output_filename, dpi=dpi, bbox_inches="tight")
            print(f"Individual plot saved as '{output_filename}'.")
        plt.show()
    else:
        print(
            "Error: Please select a file, colormap, output directory, and output file name."
        )


# To plot statistics in IQR range for selected files
def plot_selected_files(b):
    clear_output(wait=True)
    display(header_widget, widget_box)
    selected_files = files_select_multiple.value
    if selected_files:
        colormap = colormap_dropdown.value
        output_dir = output_directory_textbox.value
        output_file_name = output_filename_textbox.value
        dpi = dp_dropdown.value
        file_format = fmt_dropdown.value
        plot_type = plot_types_dropdown.value
        color_palette = color_palette_dropdown.value
        output_filename = os.path.join(
            output_dir, f"{plot_type}_{output_file_name}.{file_format}"
        )

        # setting the palette base on user selection and files number
        sns.set_palette(color_palette, len(selected_files))

        # Creating the figure
        plt.figure(figsize=(8, 6))
        data_dict = {"Files": [], "Pixel Values": []}
        for file_name in selected_files:
            file_path = file_dict.get(file_name, None)
            if file_path:
                with rasterio.open(file_path) as src:
                    data = normalize_data(src.read(1).flatten())

                # Define the lower and upper bounds to identify outliers and filter them
                IQR = pd.Series(data).quantile(0.75) - pd.Series(data).quantile(0.25)
                lower_bound = pd.Series(data).quantile(0.25) - 1.5 * IQR
                upper_bound = pd.Series(data).quantile(0.75) + 1.5 * IQR

                # Update data_dict with filtered datasets
                for value in data:
                    if lower_bound <= value <= upper_bound:
                        data_dict["Files"].append(file_name)
                        data_dict["Pixel Values"].append(value)

        # Create a pd for plots
        data_df = pd.DataFrame(data_dict)

        # Different statistic plots
        if plot_type == "Box Plot":
            sns.violinplot(
                data=data_df,
                x="Files",
                y="Pixel Values",
                inner="quartile",
                bw=0.02,
                flierprops=dict(marker=""),
                width=0.4,
                dodge=0.2,
            )
            sns.boxplot(
                data=data_df,
                x="Files",
                y="Pixel Values",
                flierprops=dict(marker=""),
                width=0.5,
                dodge=0.2,
            )
            sns.stripplot(
                data=data_df,
                x="Files",
                y="Pixel Values",
                palette=color_palette,
                alpha=0.002,
                jitter=0.35,
                size=0.7,
                marker="D",
                zorder=0,  # Places it behind other plots
            )

        elif plot_type == "Histogram":
            sns.histplot(
                data=data_df,
                x="Pixel Values",
                kde=False,
                stat="density",
                hue="Files",
                common_norm=False,
            )
        elif plot_type == "KDE Plot":
            sns.kdeplot(
                data=data_df,
                x="Pixel Values",
                hue="Files",
                color="black",
                lw=1,
                linestyle="--",
            )
        elif plot_type == "Violin Plot":
            sns.violinplot(
                data=data_df,
                x="Files",
                y="Pixel Values",
                inner="quartile",
                bw=0.02,
                palette=sns.color_palette(),
                flierprops=dict(marker=""),
                width=0.4,
                dodge=0.2,
            )
            sns.stripplot(
                data=data_df,
                x="Files",
                y="Pixel Values",
                palette=color_palette,
                alpha=0.002,
                jitter=0.35,
                size=0.7,
                marker="D",
                zorder=0,
            )

        # Customize the plot appearance
        plt.title(f"{plot_type}\n", fontsize=14, fontweight="bold")
        plt.xlabel(
            (
                "Rao's Value"
                if plot_type == "Histogram"
                else "Rao's Value" if plot_type == "KDE Plot" else "Files"
            ),
            fontsize=12,
            fontweight="bold",
        )
        plt.ylabel(
            (
                "Rao's Value"
                if plot_type == "Box Plot"
                else "Rao's Value" if plot_type == "Violin Plot" else "Density"
            ),
            fontsize=12,
            fontweight="bold",
        )
        plt.grid(True, alpha=0.5)
        sns.despine(trim=True, offset=5)
        plt.xticks(
            rotation=45, fontsize=10, fontweight="bold"
        )  # Rotate x-axis labels horizontally
        plt.yticks(
            rotation=45, fontsize=10, fontweight="bold"
        )  # Rotate x-axis labels horizontally

        # For saving figure
        if save_checkbox.value == True:
            plt.savefig(output_filename, dpi=dpi, bbox_inches="tight")
            print(f"selected files plot saved as '{output_filename}'.")
        plt.show()
    else:
        print("Error: Please select one or more files and a plot type.")


# Compute and plot the difference between two selected files
def difference_files(b):
    clear_output(wait=True)
    display(header_widget, widget_box)
    colormap = colormap_dropdown.value
    output_dir = output_directory_textbox.value
    output_file_name = output_filename_textbox.value
    dpi = dp_dropdown.value
    file_format = fmt_dropdown.value
    selected_files = files_select_multiple.value

    # Error for selecting more or less than 2 files
    if len(selected_files) != 2:
        print("Error: Please select exactly 2 files for differencing.")
        return
    file1_name, file1_path = selected_files[0], file_dict.get(selected_files[0], None)
    file2_name, file2_path = selected_files[1], file_dict.get(selected_files[1], None)
    output_filename = os.path.join(
        output_dir, f"{file1_name}_{file2_name}_{output_file_name}.{file_format}"
    )
    if file1_path and file2_path:
        with rasterio.open(file1_path) as src1, rasterio.open(file2_path) as src2:
            data1 = normalize_data(src1.read(1))
            data2 = normalize_data(src2.read(1))
            transform = src2.transform  # Get the transform object for one of 2 file

            # Extract latitude and longitude from the georeferencing information
            lat, long = transform * (
                0,
                0,
            )  # Extract the coordinates from the top-left corner
            lat_deg, lat_min, lat_sec = decimal_degrees_to_dms(lat)
            long_deg, long_min, long_sec = decimal_degrees_to_dms(long)
        global subtraction_data
        subtraction_data = normalize_data(abs(data1 - data2))
        # Create a meshgrid of coordinates
        num_rows, num_cols = data2.shape
        global x, y
        x = np.arange(0, num_cols) * transform.a + transform.c
        y = np.arange(0, num_rows) * transform.e + transform.f
        # Creating the figure
        plt.figure(figsize=(8, 6))
        plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(nbins=2))
        plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(nbins=2))
        im = plt.imshow(
            subtraction_data,
            cmap=colormap,
            extent=[x.min(), x.max(), y.min(), y.max()],
        )
        cbar = plt.colorbar(im, label="Value", pad=0.01)
        cbar.ax.get_yaxis().label.set_fontsize(
            12
        )  # Set font size for the colorbar label
        cbar.ax.get_yaxis().label.set_fontweight(
            "bold"
        )  # Set font weight for colorbar label
        plt.title(
            f"Difference plot\n{file1_name}----{file2_name}\n",
            fontsize=14,
            fontweight="bold",
        )
        x_ticks = np.linspace(x.min(), x.max(), num=len(plt.xticks()[0]))
        y_ticks = np.linspace(y.min(), y.max(), num=len(plt.yticks()[0]))

        # Set the x and y tick labels as DMS format with symbols
        plt.gca().set_xticklabels(
            [
                "%.0f° %.0f' %.0f\" %s"
                % (*decimal_degrees_to_dms(val), "W" if val < 0 else "E")
                for val in x_ticks
            ]
        )
        plt.gca().set_yticklabels(
            [
                "%.0f° %.0f' %.0f\" %s"
                % (*decimal_degrees_to_dms(val), "S" if val < 0 else "N")
                for val in y_ticks
            ]
        )
        plt.xticks(rotation=0, fontsize=10, ha=ha_widget.value, fontweight="bold")
        plt.yticks(rotation=90, fontsize=10, va=va_widget.value, fontweight="bold")
        plt.xlabel("Longitude", fontsize=12, fontweight="bold")
        plt.ylabel("Latitude", fontsize=12, fontweight="bold")
        plt.grid(False)
        if save_checkbox.value == True:
            plt.savefig(output_filename, dpi=dpi, bbox_inches="tight")
            print(f"Difference plot saved as '{output_filename}'.")
        plt.show()
    else:
        print("Error: Unable to subtract files. Please ensure both files are selected.")


# To generate a generative heatmap plot for the difference between two selected files with an slidebar
def heatmap_files(b):
    clear_output(wait=True)
    display(header_widget, widget_box)
    colormap = colormap_dropdown.value
    output_dir = output_directory_textbox.value
    output_file_name = output_filename_textbox.value
    dpi = dp_dropdown.value
    file_format = fmt_dropdown.value
    selected_files = files_select_multiple.value
    if len(selected_files) != 2:
        print("Error: Please select exactly 2 files for differencing.")
        return
    if "subtraction_data" not in globals():
        print("Please generate Difference Plot first.")
        return
    file1_name, file1_path = selected_files[0], file_dict.get(selected_files[0], None)
    file2_name, file2_path = selected_files[1], file_dict.get(selected_files[1], None)

    file_path = file_dict.get(selected_files, None)
    window_size = window_size_slider.value

    output_filename = os.path.join(
        output_dir,
        f"Difference_heatmap_{file1_name}_{file2_name}_window{window_size}_{output_file_name}.{file_format}",
    )
    if file1_path and file2_path:
        with rasterio.open(file1_path) as src:
            transform = src.transform  # Get the transform object for one of the files
            data = normalize_data(subtraction_data)
            nrows, ncols = data.shape
            # Get the pixel size in the X (same as Y as we Reproject inputs)
            pixel_size_x = transform.a

            # Extract latitude and longitude from the georeferencing information
            lat, long = transform * (
                0,
                0,
            )  # Extract the coordinates from the top-left corner
            lat_deg, lat_min, lat_sec = decimal_degrees_to_dms(lat)
            long_deg, long_min, long_sec = decimal_degrees_to_dms(long)

            # Calculate the grid cell size based on the selected window size
            grid_size_rows = max(1, nrows // window_size)
            grid_size_cols = max(1, ncols // window_size)
            grid_means = np.zeros((grid_size_rows, grid_size_cols))
            for i in range(grid_size_rows):
                for j in range(grid_size_cols):
                    row_start = i * window_size
                    row_end = min((i + 1) * window_size, nrows)
                    col_start = j * window_size
                    col_end = min((j + 1) * window_size, ncols)
                    grid = data[row_start:row_end, col_start:col_end]
                    valid_pixels = np.isfinite(grid)  # Find non-NaN values
                    grid_mean = np.nanmean(
                        grid[valid_pixels]
                    )  # Calculate mean for valid pixels
                    grid_means[i, j] = grid_mean

            # Create x and y arrays based on the transform
            x = np.arange(0, ncols) * transform.a + transform.c
            y = np.arange(0, nrows) * transform.e + transform.f
            plt.figure(figsize=(8, 6))
            plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(nbins=2))
            plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(nbins=2))
            im = plt.imshow(
                data, cmap=colormap, extent=[x.min(), x.max(), y.min(), y.max()]
            )

            # Grid lines
            for i in range(grid_size_rows):
                plt.axhline(y[i * window_size], color="white", linewidth=0.5)
            for j in range(grid_size_cols):
                plt.axvline(x[j * window_size], color="white", linewidth=0.5)

            # Calculate the number of grid lines in x and y directions
            num_x_lines = grid_size_cols + 1
            num_y_lines = grid_size_rows + 1

            # Calculate the difference between adjacent grid lines
            grid_cell_width = x[1] - x[0]
            grid_cell_height = y[1] - y[0]

            # Calculate font size based on the number of grid lines and resolution
            min_grid_line_count = min(num_x_lines, num_y_lines)
            font_size = (
                np.mean([abs(grid_cell_width), abs(grid_cell_height)])
                * 80
                / (min_grid_line_count * pixel_size_x)
            )  # Adjust 80

            # Display grid means as text with adjusted font size
            for i in range(grid_size_rows):
                for j in range(grid_size_cols):
                    plt.text(
                        x[j * window_size] + (window_size / 2) * transform.a,
                        y[i * window_size] + (window_size / 2) * transform.e,
                        f"{round(grid_means[i, j], 2)}",
                        color="white",
                        ha="center",
                        va="center",
                        fontsize=font_size,  # Adjusted font size
                        fontweight="bold",
                    )
            cbar = plt.colorbar(im, label="Value", pad=0.01)
            cbar.ax.get_yaxis().label.set_fontsize(
                12
            )  # Set font size for the colorbar label
            cbar.ax.get_yaxis().label.set_fontweight(
                "bold"
            )  # Set font weight for colorbar label
            plt.title(
                f"Difference Heatmap Plot\nFiles: {file1_name}-{file2_name}   Grid Size: {window_size}\n",
                fontsize=14,
                fontweight="bold",
            )
            x_ticks = np.linspace(x.min(), x.max(), num=len(plt.xticks()[0]))
            y_ticks = np.linspace(y.min(), y.max(), num=len(plt.yticks()[0]))

            # Set the x and y tick labels as DMS format with symbols
            plt.gca().set_xticklabels(
                [
                    "%.0f° %.0f' %.0f\" %s"
                    % (*decimal_degrees_to_dms(val), "W" if val < 0 else "E")
                    for val in x_ticks
                ]
            )
            plt.gca().set_yticklabels(
                [
                    "%.0f° %.0f' %.0f\" %s"
                    % (*decimal_degrees_to_dms(val), "S" if val < 0 else "N")
                    for val in y_ticks
                ]
            )
            plt.xticks(rotation=0, fontsize=10, ha=ha_widget.value, fontweight="bold")
            plt.yticks(rotation=90, fontsize=10, va=va_widget.value, fontweight="bold")
            plt.xlabel("Longitude", fontsize=12, fontweight="bold")
            plt.ylabel("Latitude", fontsize=12, fontweight="bold")
            if save_checkbox.value:
                plt.savefig(output_filename, dpi=dpi, bbox_inches="tight")
                print(f"Difference heatmap plot saved as '{output_filename}'.")
            plt.show()
    else:
        print("Error: Please select a file to generate the heatmap plot.")


# To create an split_plot as an attractive plot for comparing to selected files
def split_plot(_):
    clear_output(wait=True)
    display(header_widget, widget_box)
    colormap = colormap_dropdown.value
    output_dir = output_directory_textbox.value
    output_file_name = output_filename_textbox.value
    dpi = dp_dropdown.value
    file_format = fmt_dropdown.value
    selected_files = files_select_multiple.value
    if len(selected_files) != 2:
        print("Error: Please select exactly 2 files to compare.")
        return
    file1_name, file1_path = selected_files[0], file_dict.get(selected_files[0], None)
    file2_name, file2_path = selected_files[1], file_dict.get(selected_files[1], None)
    if file1_path and file2_path:
        with rasterio.open(file1_path) as src1, rasterio.open(file2_path) as src2:
            left_data = normalize_data(src1.read(1))
            right_data = normalize_data(src2.read(1))
            right_crs = src2.crs
            right_transform = (
                src2.transform
            )  # Get the transform object for one of 2 file

    # To create the combined raster from to selected files
    def create_combined_raster(split_size):
        combined_data = np.copy(left_data)
        # Calculate the split column index
        split_position = int(split_size * left_data.shape[1])
        # Combine the left and right rasters
        combined_data[:, split_position:] = right_data[:, split_position:]
        return combined_data

    # To display and save the split plot
    def display_split_view(split_size):
        combined_data = create_combined_raster(split_size)

        # Create a new rasterio dataset for the combined data
        with MemoryFile() as memfile:
            with memfile.open(
                driver="GTiff",
                height=combined_data.shape[0],
                width=combined_data.shape[1],
                count=1,
                dtype=combined_data.dtype,
                crs=right_crs,
                transform=right_transform,
            ) as dataset:
                dataset.write(combined_data, 1)

            # Plot the combined image with the split line
            with memfile.open() as combined_ds:
                combined_data = combined_ds.read(1)
                combined_transform = (
                    combined_ds.transform
                )  # Get the transform object for one of 2 file

                # Extract latitude and longitude from the georeferencing information
                lat, long = combined_transform * (
                    0,
                    0,
                )  # Extract the coordinates from the top-left corner
                lat_deg, lat_min, lat_sec = decimal_degrees_to_dms(lat)
                long_deg, long_min, long_sec = decimal_degrees_to_dms(long)

                # Create a meshgrid of coordinates
                num_rows, num_cols = combined_data.shape
                global x, y  # Define x and y as global variables
                x = np.arange(0, num_cols) * combined_transform.a + combined_transform.c
                y = np.arange(0, num_rows) * combined_transform.e + combined_transform.f
                plt.figure(figsize=(8, 6))
                plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(nbins=2))
                plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(nbins=2))
                im = plt.imshow(combined_data, cmap=colormap, origin="upper")
                cbar = plt.colorbar(im, label="Value", pad=0.01)
                cbar.ax.get_yaxis().label.set_fontsize(
                    12
                )  # Set font size for the colorbar label
                cbar.ax.get_yaxis().label.set_fontweight(
                    "bold"
                )  # Set font weight for colorbar label
                plt.title(
                    f"Split Plot\nLeft: {file1_name} ------------ Right: {file2_name}\n",
                    fontsize=14,
                    fontweight="bold",
                )
                x_ticks = np.linspace(x.min(), x.max(), num=len(plt.xticks()[0]))
                y_ticks = np.linspace(y.min(), y.max(), num=len(plt.yticks()[0]))
                y_ticks = y_ticks[::-1]

                # Set the x and y tick labels as DMS format with symbols
                plt.gca().set_xticklabels(
                    [
                        "%.0f° %.0f' %.0f\" %s"
                        % (*decimal_degrees_to_dms(val), "W" if val < 0 else "E")
                        for val in x_ticks
                    ]
                )
                plt.gca().set_yticklabels(
                    [
                        "%.0f° %.0f' %.0f\" %s"
                        % (*decimal_degrees_to_dms(val), "S" if val < 0 else "N")
                        for val in y_ticks
                    ]
                )
                plt.xticks(
                    rotation=0, fontsize=10, ha=ha_widget.value, fontweight="bold"
                )
                plt.yticks(
                    rotation=90, fontsize=10, va=va_widget.value, fontweight="bold"
                )

                # Set the axis labels as latitude and longitude
                plt.xlabel("Longitude", fontsize=12, fontweight="bold")
                plt.ylabel("Latitude", fontsize=12, fontweight="bold")
                plt.grid(False)

                # Add the split line
                split_position = int(split_size * left_data.shape[1])
                plt.axvline(x=split_position, color="red", linestyle="--", linewidth=1)
                if save_checkbox.value == True:
                    output_filename = os.path.join(
                        output_dir,
                        f"SplitPlot_{file1_name}_{file2_name}_{output_file_name}.{file_format}",
                    )
                    plt.savefig(output_filename, dpi=dpi, bbox_inches="tight")
                    print(f"Split plot saved as '{output_filename}'.")
                plt.show()

    # To save the split plot with slider changes
    def save_plot(split_size):
        combined_data = create_combined_raster(split_size)
        colormap = colormap_dropdown.value
        output_dir = output_directory_textbox.value
        output_file_name = output_filename_textbox.value
        dpi = dp_dropdown.value
        file_format = fmt_dropdown.value

        # Create a new rasterio dataset for the combined data
        with MemoryFile() as memfile:
            with memfile.open(
                driver="GTiff",
                height=combined_data.shape[0],
                width=combined_data.shape[1],
                count=1,
                dtype=combined_data.dtype,
                crs=right_crs,
                transform=right_transform,
            ) as dataset:
                dataset.write(combined_data, 1)

            # Plot the combined image with the split line
            with memfile.open() as combined_ds:
                combined_data = combined_ds.read(1)
                combined_transform = combined_ds.transform

                # Extract latitude and longitude from the georeferencing information
                lat, long = combined_transform * (
                    0,
                    0,
                )  # Extract the coordinates from the top-left corner
                lat_deg, lat_min, lat_sec = decimal_degrees_to_dms(lat)
                long_deg, long_min, long_sec = decimal_degrees_to_dms(long)

                # Create a meshgrid of coordinates
                num_rows, num_cols = combined_data.shape
                x = np.arange(0, num_cols) * combined_transform.a + combined_transform.c
                y = np.arange(0, num_rows) * combined_transform.e + combined_transform.f
                y = y[::-1]
                plt.figure(figsize=(8, 6))
                plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(nbins=2))
                plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(nbins=2))
                im = plt.imshow(combined_data, cmap=colormap, origin="upper")
                cbar = plt.colorbar(im, label="Value", pad=0.01)
                cbar.ax.get_yaxis().label.set_fontsize(
                    12
                )  # Set font size for the colorbar label
                cbar.ax.get_yaxis().label.set_fontweight(
                    "bold"
                )  # Set font weight for colorbar label
                plt.title(
                    f"Split Plot\nLeft: {file1_name} ------------ Right: {file2_name}\n",
                    fontsize=14,
                    fontweight="bold",
                )
                x_ticks = np.linspace(x.min(), x.max(), num=len(plt.xticks()[0]))
                y_ticks = np.linspace(y.min(), y.max(), num=len(plt.yticks()[0]))
                y_ticks = y_ticks[::-1]
                # Set the x and y tick labels as DMS format with symbols
                plt.gca().set_xticklabels(
                    [
                        "%.0f° %.0f' %.0f\" %s"
                        % (*decimal_degrees_to_dms(val), "W" if val < 0 else "E")
                        for val in x_ticks
                    ]
                )
                plt.gca().set_yticklabels(
                    [
                        "%.0f° %.0f' %.0f\" %s"
                        % (*decimal_degrees_to_dms(val), "S" if val < 0 else "N")
                        for val in y_ticks
                    ]
                )
                plt.xticks(
                    rotation=0, fontsize=10, ha=ha_widget.value, fontweight="bold"
                )
                plt.yticks(
                    rotation=90, fontsize=10, va=va_widget.value, fontweight="bold"
                )
                plt.xlabel("Longitude", fontsize=12, fontweight="bold")
                plt.ylabel("Latitude", fontsize=12, fontweight="bold")
                plt.grid(False)

                # Add the split line
                split_position = int(split_size * left_data.shape[1])
                plt.axvline(x=split_position, color="red", linestyle="--", linewidth=1)

                # Save the plot
                output_filename = os.path.join(
                    output_dir,
                    f"SplitPlot_{file1_name}_{file2_name}_{output_file_name}.{file_format}",
                )
                plt.savefig(output_filename, dpi=dpi, bbox_inches="tight")
                print(f"Split plot saved as '{output_filename}'.")
                plt.show()
                clear_output(wait=True)
                display(header_widget, widget_box)
                # Display the interactive plot
                display(widgets.HBox([interactive_plot, save_gif_button]))

    # Function to generate and save a GIF with a moving split line using Matplotlib
    def save_gif():
        file_format = fmt_dropdown.value
        global x, y
        images = []
        fig, ax = plt.subplots(figsize=(8, 6))
        split_line = ax.axvline(
            x=0, color="red", linestyle="--", linewidth=1
        )  # Initialize the line for the split
        cbar = plt.colorbar(
            ax.imshow(left_data, cmap=colormap, origin="upper"),
            label="Value",
            pad=0.01,
        )
        cbar.ax.get_yaxis().label.set_fontsize(
            12
        )  # Set font size for the colorbar label
        cbar.ax.get_yaxis().label.set_fontweight(
            "bold"
        )  # Set font weight for colorbar label

        def animate(split_position):
            ax.clear()
            combined_data = create_combined_raster(split_position)
            im = ax.imshow(combined_data, cmap=colormap, origin="upper")
            ax.set_title(
                f"Left: {file1_name} ------------ Right: {file2_name}\n",
                fontsize=14,
                fontweight="bold",
            )
            plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(nbins=2))
            plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(nbins=2))
            x_ticks = np.linspace(x.min(), x.max(), num=len(plt.xticks()[0]))
            y_ticks = np.linspace(y.min(), y.max(), num=len(plt.yticks()[0]))
            y_ticks = y_ticks[::-1]
            # Set the x and y tick labels as DMS format with symbols
            plt.gca().set_xticklabels(
                [
                    "%.0f° %.0f' %.0f\" %s"
                    % (*decimal_degrees_to_dms(val), "W" if val < 0 else "E")
                    for val in x_ticks
                ]
            )
            plt.gca().set_yticklabels(
                [
                    "%.0f° %.0f' %.0f\" %s"
                    % (*decimal_degrees_to_dms(val), "S" if val < 0 else "N")
                    for val in y_ticks
                ]
            )
            plt.xticks(rotation=0, fontsize=10, ha=ha_widget.value, fontweight="bold")
            plt.yticks(rotation=90, fontsize=10, va=va_widget.value, fontweight="bold")
            ax.set_xlabel("Longitude", fontsize=12, fontweight="bold")
            ax.set_ylabel("Latitude", fontsize=12, fontweight="bold")
            ax.grid(False)
            # Add the split line
            split_position_pixel = int(split_position * left_data.shape[1])
            ax.axvline(x=split_position_pixel, color="red", linestyle="--", linewidth=1)
            # Update the split line position
            split_position_pixel = int(split_position * left_data.shape[1])
            split_line.set_xdata([split_position_pixel, split_position_pixel])
            # Append the current frame to the list of images
            images.append([split_line])

        # Create the animation
        anim = animation.FuncAnimation(
            fig, animate, frames=np.arange(0, 1.01, 0.01), interval=100
        )

        # Save the animation as a GIF
        gif_filename = os.path.join(
            output_dir,
            f"SplitPlotAnimation_{file1_name}_{file2_name}_{output_file_name}.gif",
        )
        anim.save(
            gif_filename,
            writer="pillow",
            dpi=dpi,
            fps=10,
            savefig_kwargs={"format": file_format},
        )  # Specify the frame format)  # Adjust fps as needed
        clear_output(wait=True)
        display(header_widget, widget_box)

        # Display the interactive plot
        display(widgets.HBox([interactive_plot, save_gif_button]))
        print(f"Split plot animation saved as '{gif_filename}'.")

    # Create an interactive widget to adjust the split size
    split_slider = widgets.FloatSlider(
        value=0.5,
        min=0,
        max=1.0,
        step=0.01,
        description="Split Size:",
        continuous_update=False,
    )

    # Callback function to handle slider value changes
    def on_slider_value_change(change):
        split_size = change["new"]
        if save_checkbox.value:
            save_plot(split_size)

    # Attach the callback function to the slider's value attribute
    split_slider.observe(on_slider_value_change, names="value")

    # Create the interactive plot
    interactive_plot = interactive(display_split_view, split_size=split_slider)

    # Button to save the plot as a GIF
    save_gif_button = widgets.Button(description="Generate GIF")
    save_gif_button.on_click(lambda x: save_gif())

    # Display the button
    display(widgets.HBox([interactive_plot, save_gif_button]))


# For imported datasets
file_dict = {}

# GUI components
select_files_button = widgets.Button(description="Select Raster Files")
select_files_button.on_click(add_files_to_dict)
output_directory_textbox = widgets.Text(
    description="Output Path:", placeholder="Enter output path here"
)
output_directory_button = widgets.Button(description="Output Path")
output_directory_button.on_click(select_path)
output_filename_textbox = widgets.Text(description="Output Name:", value="RaoVis")
file_dropdown = widgets.Dropdown(
    options=list(file_dict.keys()), description="Select File:"
)
files_select_multiple = widgets.SelectMultiple(
    options=list(file_dict.keys()), description="Select Files:"
)
files_select_multiple.layout.height = "90px"
files_select_multiple.layout.width = "350px"
plot_types_dropdown = widgets.Dropdown(
    options=["Box Plot", "Histogram", "KDE Plot", "Violin Plot"],
    description="Plot Type:",
)
color_palette_dropdown = widgets.Dropdown(
    options=list(plt.colormaps()),
    value="rainbow",
    description="Color Palette:",
)
dp_dropdown = widgets.Dropdown(
    description="DPI:",
    options=[100, 200, 300, 400, 500, 600, 700, 800, 900, 1000],
    value=500,
)
fmt_dropdown = widgets.Dropdown(
    description="Format:", options=["png", "jpg", "svg", "tiff", "tif"], value="jpg"
)
colormap_dropdown = widgets.Dropdown(
    options=plt.colormaps(), description="Colormap:", value="nipy_spectral"
)
save_checkbox = widgets.Checkbox(description="save plot")
plot_individual_button = widgets.Button(description="Plot")
plot_individual_button.on_click(plot_individual_file)
plot_selected_button = widgets.Button(description="Plot")
plot_selected_button.on_click(plot_selected_files)
difference_files_button = widgets.Button(description="Difference Plot")
difference_files_button.on_click(difference_files)
window_size_slider = widgets.IntSlider(
    value=30, min=1, max=150, step=1, description="Grid Size:"
)
from ipywidgets import Layout, interact, widgets

# Create widget sliders for HA and VA
ha_widget = widgets.Dropdown(
    options=["center", "right", "left"],
    value="center",
    description="H-Alignment:",
    layout=Layout(width="140px"),  # Adjust the width to make it smaller
)

va_widget = widgets.Dropdown(
    options=["center", "top", "bottom", "baseline"],
    value="center",
    description="V-Alignment:",
    layout=Layout(width="140px"),
)
heatmap_button = widgets.Button(description="Difference Heatmap")
heatmap_button.on_click(heatmap_files)
split_button = widgets.Button(description="Split Plot")
split_button.on_click(split_plot)

# Arrange the widgets in a VBox for display
widget_box = widgets.HBox(
    [
        widgets.HBox(
            [
                widgets.VBox(
                    [
                        widgets.HBox([select_files_button, save_checkbox]),
                        widgets.HBox(
                            [output_directory_textbox, output_directory_button]
                        ),
                        output_filename_textbox,
                        widgets.HBox([ha_widget, va_widget]),
                    ]
                ),
                widgets.HBox(
                    [
                        widgets.VBox(
                            [
                                file_dropdown,
                                colormap_dropdown,
                                dp_dropdown,
                                widgets.HBox([fmt_dropdown, plot_individual_button]),
                            ]
                        )
                    ]
                ),
                widgets.HBox(
                    [
                        files_select_multiple,
                        widgets.VBox(
                            [
                                color_palette_dropdown,
                                plot_types_dropdown,
                                window_size_slider,
                            ]
                        ),
                        widgets.VBox(
                            [
                                plot_selected_button,
                                difference_files_button,
                                heatmap_button,
                                split_button,
                            ]
                        ),
                    ]
                ),
            ]
        )
    ]
)

header_widget = widgets.HTML(
    "<h3 style='font-family: Arial, sans-serif; color: white; font-weight: semibold; background-color: blue; text-align: center;'>Rao’s-Q Visualization</h3>"
)
header_widget.layout.width = "300px"
header_widget.layout.height = "25px"
display(header_widget, widget_box)
