_PaRaVis_ is a powerful GUI designed for extracting, visualizing, and analyzing Rao's Q based on VIs. The GUI comprises three main sections, each enhancing usability and functionality for different process aspects.

### installation
You can effortlessly install PaRaVis from PyPI using the following command:
```bash
pip install paravis
```
In Jupyter Notebook or Jupyter lab you can import different moduls of paravis as following:

|Module| Import Statement| Description|
|------------------------------|---------------------------------|-------------------------------------|
| Jupyter notebook Enviroment| ```from paravis import JupEnv```| Change theme and cell size within the Jupyter notebook.|
| Vegetation Index Analysis| ```from paravis import Indices```| Calculate and visually represent vegetation indices.|
| Rao's Q Index Computation| `from paravis import Raos`| Perform Rao's Q index computation with customizable options.|
| Visualization and Analysis| `from paravis import Visualize`| Visualize, analyze, and compare outputs using this module.|


### 1. Vegetation Index Analysis
provides a user-friendly interface for importing stacked raster datasets, selecting specific bands, and calculating multiple indices simultaneously. spatial visualizations with customization options enhance the exploration of vegetation indices. Users can also select and save calculated indices (based on their CV value) as GeoTIFF files for future analysis.

### 2. Rao's Q Index Computation
This section focuses on the computation of Rao's Q index from raster files in both unidimensional and multidimensional modes. offering  parameter customization options. parallelization using the Ray framework optimizes computational efficiency, reducing processing time significantly. The code employs the "tqdm" library to monitor processing time.

### 3. Visualization and Analysis
This part emphasizes visualizing and analyzing Rao's Q outputs through an intuitive interface. Various widgets facilitate seamless file selection, output path definition, and customization of plot settings. The tool generates insightful plots, histograms, difference heatmaps, and split plots, making complex operations accessible to users.



This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
