"""
process_ecostress_tifs.py

Description:
    Batch-processes directory contents of ECOSTRESS Evapotranspiration (ET) 
    or SIF GeoTIFF files. Utilizes GDAL to iterate over raster files, extract 
    metadata (projections/geotransforms), and convert band data into NumPy 
    arrays for downstream statistical processing.

Author: [Your Name]
Date: [Current Date]
"""

import os
import glob
import numpy as np
try:
    from osgeo import gdal
except ImportError:
    import gdal

def load_rasters_to_arrays(input_dir):
    """
    Iterates through all GeoTIFF files in a directory, reads the raster data,
    and returns a dictionary mapping filenames to their NumPy arrays.
    
    Parameters:
        input_dir (str): Path to the directory containing .tif files.
        
    Returns:
        dict: A dictionary where Keys = filenames, Values = NumPy arrays of Band 1.
    """
    search_pattern = os.path.join(input_dir, "*.tif")
    tif_files = glob.glob(search_pattern)
    
    if not tif_files:
        print(f"No .tif files found in '{input_dir}'.")
        return {}

    print(f"Found {len(tif_files)} TIF files to load.")
    raster_dict = {}
    
    for file_path in tif_files:
        filename = os.path.basename(file_path)
        
        # Open the dataset using GDAL
        dataset = gdal.Open(file_path)
        
        if dataset is None:
            print(f"  -> [ERROR] Failed to open {filename}")
            continue
            
        try:
            # Extract spatial metadata (kept for reference in geospatial logic)
            geo_transform = dataset.GetGeoTransform()
            projection = dataset.GetProjection()
            
            # Read the first band (GDAL uses 1-based indexing)
            band = dataset.GetRasterBand(1)
            data_array = band.ReadAsArray()
            
            # Store the array in our dictionary
            raster_dict[filename] = {
                'array': data_array,
                'geotransform': geo_transform,
                'projection': projection
            }
            print(f"  -> Loaded {filename} | Shape: {data_array.shape}")
            
        except Exception as e:
            print(f"  -> [ERROR] Could not read band from {filename}: {e}")
            
        finally:
            # Explicitly clear the dataset from memory (equivalent to dataset.close)
            dataset = None
            band = None
            
    return raster_dict

if __name__ == "__main__":
    # Point these to the directories containing your specific variables
    ET_TIF_DIR = r"C:\path\to\your\ECOSTRESS_ET_Files"
    SIF_TIF_DIR = r"C:\path\to\your\ECOSTRESS_SIF_Files"
    
    # Load Evapotranspiration (ET) Rasters
    print("--- Loading ET Data ---")
    et_data = load_rasters_to_arrays(ET_TIF_DIR)
    
    # Example: How to access a specific array from the loop
    # If "ET_Image_1.tif" was processed, access it like this:
    # et_array_1 = et_data["ET_Image_1.tif"]['array']
    
    # Load SIF Rasters utilizing the exact same function (Code Reuse!)
    print("\n--- Loading SIF Data ---")
    sif_data = load_rasters_to_arrays(SIF_TIF_DIR)
