***
<div align="center">
  <img src="https://github.com/mmadrz/PaRaVis/blob/main/LOGO.png"><br>
</div>

***

## Overview
_PaRaVis_ is a powerful Graphical package designed for extracting, visualizing, and analyzing Rao's Q based on VIs and raster datasets. It comprises three main sections, each enhancing usability and functionality for different process aspects.

### 1. Vegetation Index Analysis
provides a user-friendly interface for importing stacked raster datasets, selecting specific bands, and calculating multiple indices simultaneously. spatial visualizations with customization options enhance the exploration of vegetation indices. Users can also select and save calculated indices (based on their CV value) as GeoTIFF files for future analysis.

### 2. Rao's Q Index Computation
Focuses on the computation of Rao's Q index from raster files in both unidimensional and multidimensional modes. offering  parameter customization options. parallelization using the Ray framework optimizes computational efficiency, reducing processing time significantly. The code employs the "tqdm" library to monitor processing time.

### 3. Visualization and Analysis
Emphasizes visualizing and analyzing Rao's Q outputs through an intuitive interface. Various widgets facilitate seamless file selection, output path definition, and customization of plot settings. The tool generates insightful plots, histograms, difference heatmaps, and split plots, making complex operations accessible to users.

## Installation and Usage
You can effortlessly install _PaRaVis_ from PyPI using the following command:
```bash
pip install paravis
```
<br/>

If you are using _PaRaVis_ on Debian-based Linux distributions like Ubuntu operating system, you should also install the following package for tkinter support befor using _PaRaVis_ :
```bash
sudo apt-get install python3-tk
```
<br/>

**Note:** To customize theme and cell size for a better experience within Jupyter Notebook, use the following magic command from your jupyter notebook, and remember to refresh for changes to take effect (use F5):
```bash
!jt -t grade3 -cellw 100% -N -T -kl
```
<br/>

In Jupyter Notebook or Jupyter Lab you can import different modules of _PaRaVis_ as follows:

|Module| Import Statement| Description|
|------------------------------|---------------------------------|-------------------------------------|
| Vegetation Index Analysis| ```from paravis import Indices```| Calculate and visually represent vegetation indices.|
| Rao's Q Index Computation| `from paravis import Raos`| Perform Rao's Q index computation with customizable options.|
| Visualization and Analysis| `from paravis import Visualize`| Visualize, analyze, and compare outputs using this module.|