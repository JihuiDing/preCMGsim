import numpy as np
import os
import re

def extract_sorted_filenames(
        folder_dir=None,
        is_save=False,
        save_dir=None,
        save_name='filenames.csv'
):
    """
    Extract file names from a folder and sort them numerically.
    Returns a list of sorted file names (excluding hidden files like .DS_Store).
    """

    # Check if the directory exists
    if not os.path.exists(folder_dir):
        print(f"Error: Directory '{folder_dir}' does not exist.")
        return []

    # Get all files, excluding hidden files
    filenames = [
        file_path.name for file_path in folder_dir.iterdir()
        if file_path.is_file() and not file_path.name.startswith('.')
    ]

    # Function to extract number inside filename
    def extract_number(filename):
        match = re.search(r'(\d+)', filename)
        return int(match.group(1)) if match else float('inf')

    # Sort numerically
    filenames = sorted(filenames, key=extract_number)
    
    if is_save:
        np.savetxt(save_dir/f'{save_name}', np.array(filenames), delimiter=',', fmt='%s')

    return filenames

