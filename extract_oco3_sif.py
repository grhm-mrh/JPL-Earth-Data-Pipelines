"""
extract_oco3_sif.py

Description:
    Automates the extraction of Solar-Induced Fluorescence (SIF) data from 
    OCO-3 (Orbiting Carbon Observatory-3) NetCDF4 files. Extracts spatial coordinates 
    and SIF values, converting them from multi-dimensional arrays into flat, 
    consolidated tabular formats (CSV) for easier geospatial analysis.

Author: [M.Graham]
Date: [06/24/2026]
"""

import os
import glob
import numpy as np
import pandas as pd
import netCDF4 as nc

def process_oco3_files(input_dir, output_dir):
    """
    Iterates through all .nc4 files in the input directory, extracts relevant 
    SIF variables, and outputs them as combined DataFrames to CSV.
    """
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Find all .nc4 files in the input directory dynamically
    search_pattern = os.path.join(input_dir, "*.nc4")
    file_list = glob.glob(search_pattern)
    
    if not file_list:
        print(f"No .nc4 files found in '{input_dir}'.")
        return

    print(f"Found {len(file_list)} files. Starting processing...")
    
    for file_path in file_list:
        filename = os.path.basename(file_path)
        print(f"Processing: {filename}...")
        
        try:
            # Open dataset safely using context manager
            with nc.Dataset(file_path, 'r') as dataset:
                # Extract arrays
                sif_757nm = np.asarray(dataset['Daily_SIF_757nm'])
                sounding_id = np.asarray(dataset['Metadata/SoundingId'])
                latitude = np.asarray(dataset['Latitude'])
                longitude = np.asarray(dataset['Longitude'])
                
            # Flatten arrays and consolidate into a single Pandas DataFrame
            # This is vastly superior to saving variables in separate files
            df = pd.DataFrame({
                'SoundingID': sounding_id.flatten(),
                'Latitude': latitude.flatten(),
                'Longitude': longitude.flatten(),
                'Daily_SIF_757nm': sif_757nm.flatten()
            })
            
            # Generate output filename (e.g., File1.nc4 -> File1_processed.csv)
            out_filename = filename.replace('.nc4', '_processed.csv')
            out_path = os.path.join(output_dir, out_filename)
            
            # Save the consolidated table
            df.to_csv(out_path, index=False)
            print(f"  -> Successfully saved to {out_filename}")
            
        except KeyError as ke:
            print(f"  -> Missing expected variable in {filename}: {ke}")
        except Exception as e:
            print(f"  -> Unexpected error processing {filename}: {e}")

if __name__ == "__main__":
    # Define local data paths here
    INPUT_DIRECTORY = r"C:\path\to\your\OCO3_Files"
    OUTPUT_DIRECTORY = r"C:\path\to\your\Processed_CSVs"
    
    process_oco3_files(INPUT_DIRECTORY, OUTPUT_DIRECTORY)
