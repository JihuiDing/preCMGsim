import numpy as np
import pandas as pd
from pathlib import Path
import re

def extract_coordinates_from_fgrid(fgrid_path):
    """
    Extract coordinates from a text FGRID file, handling multi-line value blocks.
    
    Args:
        fgrid_path (str): Path to the FGRID file
        
    Returns:
        tuple: (coords_df, corners_df) where:
            - coords_df: DataFrame with COORDS data
            - corners_df: DataFrame with CORNERS data
    """
    coords_data = []
    corners_data = []
    
    with open(fgrid_path, 'r') as f:
        lines = f.readlines()
        
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        if "'COORDS  '" in line or "'CORNERS '" in line:
            # Use regex to extract the number of values
            match = re.search(r"'(COORDS  |CORNERS )'\s+(\d+)", line)
            if match:
                keyword = match.group(1).strip()
                n_values = int(match.group(2))
            else:
                print(f"Warning: Could not parse header line: {line}")
                i += 1
                continue
            values = []
            i += 1
            while len(values) < n_values and i < len(lines):
                values += lines[i].strip().split()
                i += 1
            if keyword == 'COORDS':
                if len(values) == 7:
                    coords_data.append({
                        'i': int(values[0]),
                        'j': int(values[1]),
                        'k': int(values[2]),
                        'cell_id': int(values[3]),
                        'flag1': int(values[4]),
                        'flag2': int(values[5]),
                        'flag3': int(values[6])
                    })
                else:
                    print(f"Warning: COORDS block did not have 7 values: {values}")
            elif keyword == 'CORNERS':
                if len(values) == 24:
                    corners_data.append({
                        'x1': float(values[0]), 'y1': float(values[1]), 'z1': float(values[2]),
                        'x2': float(values[3]), 'y2': float(values[4]), 'z2': float(values[5]),
                        'x3': float(values[6]), 'y3': float(values[7]), 'z3': float(values[8]),
                        'x4': float(values[9]), 'y4': float(values[10]), 'z4': float(values[11]),
                        'x5': float(values[12]), 'y5': float(values[13]), 'z5': float(values[14]),
                        'x6': float(values[15]), 'y6': float(values[16]), 'z6': float(values[17]),
                        'x7': float(values[18]), 'y7': float(values[19]), 'z7': float(values[20]),
                        'x8': float(values[21]), 'y8': float(values[22]), 'z8': float(values[23])
                    })
                else:
                    print(f"Warning: CORNERS block did not have 24 values: {values}")
            continue
        i += 1
    
    # Create DataFrames
    coords_df = pd.DataFrame(coords_data)
    corners_df = pd.DataFrame(corners_data)
    
    return coords_df, corners_df

def main():
    # Path to the FGRID file
    fgrid_path = Path("data/demo_2zones.fgrid")
    
    # Extract coordinates
    coords_df, corners_df = extract_coordinates_from_fgrid(fgrid_path)
    
    # Save to CSV files
    coords_df.to_csv("data/coords.csv", index=False)
    corners_df.to_csv("data/corners.csv", index=False)
    
    # Print some statistics
    print(f"Number of coordinate sets: {len(coords_df)}")
    print(f"Number of corner sets: {len(corners_df)}")
    print("\nCoordinates DataFrame head:")
    print(coords_df.head())
    print("\nCorners DataFrame head:")
    print(corners_df.head())

if __name__ == "__main__":
    main() 