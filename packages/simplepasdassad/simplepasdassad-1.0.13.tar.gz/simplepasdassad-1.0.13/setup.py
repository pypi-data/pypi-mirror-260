from setuptools import setup, find_packages

libs_requires = [
    "jupyterthemes==0.20.0",
    "ipywidgets==7.7.2",
    "tk==0.1.0",
    "xarray==2022.12.0",
    "rioxarray==0.13.3",
    "rasterio==1.3.4",
    "numpy==1.26.2",
    "spyndex==0.2.0",
    "pandas==1.5.3",
    "matplotlib==3.5.1",
    "seaborn==0.12.2",
    "ray==2.7.0",
    "tqdm==4.64.1",
]

setup(
    name="simplepasdassad",
    version="1.0.13",
    description="parallel, efficient and ensemble analysis of Rao's Q spectral diversity using remote sensing datasets.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mmadrz/PaRaVis",
    author="Mohammad Reza Fathi",
    author_email="mmadrzfathi@gmail.com",
    license="MIT",
    packages=find_packages(),  # Automatically finds packages in the directory
    install_requires=libs_requires,
)
