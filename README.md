# JPL Earth Data Processing Pipelines

## Overview
This repository contains Python pipelines developed to automate the processing of Earth observation data, specifically **OCO-3 (Orbiting Carbon Observatory-3)** and **ECOSTRESS** datasets. Originally drafted during an internship at NASA's Jet Propulsion Laboratory (JPL), these scripts have been refactored for performance, scalability, and readability.

## Features
* **OCO-3 SIF Extraction:** Batch processes `.nc4` (NetCDF4) files to extract Spatial Data (Latitude/Longitude), Sounding IDs, and Solar-Induced Fluorescence (SIF) data into consolidated, analysis-ready CSVs.
* **ECOSTRESS Raster Processing:** Dynamically loads large batches of `.tif` (GeoTIFF) Evapotranspiration arrays using `gdal`, completely automating what would otherwise be a tedious manual data-entry process.

## Prerequisites
Ensure you have Python 3.8+ installed. You can install the required dependencies using:
`pip install -r requirements.txt`
*(Note: `gdal` can sometimes be tricky to install via pip on Windows; using `conda install -c conda-forge gdal` is recommended).*

## Usage
1. Place your raw `.nc4` or `.tif` files in the respective input directories.
2. Update the `INPUT_DIR` and `OUTPUT_DIR` paths in the `if __name__ == "__main__":` block of the scripts.
3. Run the scripts from your terminal:
   `python src/extract_oco3_sif.py`
