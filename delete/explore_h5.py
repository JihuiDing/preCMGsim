import h5py
import json
import numpy as np

def print_h5_structure(group, indent=0):
    """
    Recursively print the structure of an HDF5 file
    
    Args:
        group: h5py.Group or h5py.File object
        indent: Current indentation level for pretty printing
    """
    # Print group name and attributes
    print(' ' * indent + f"Group: {group.name}")
    if len(group.attrs) > 0:
        print(' ' * (indent + 2) + "Attributes:")
        for attr_name, attr_value in group.attrs.items():
            print(' ' * (indent + 4) + f"{attr_name}: {attr_value}")
    
    # Print datasets in this group
    for name, obj in group.items():
        if isinstance(obj, h5py.Dataset):
            print(' ' * (indent + 2) + f"Dataset: {name}")
            print(' ' * (indent + 4) + f"Shape: {obj.shape}")
            print(' ' * (indent + 4) + f"Type: {obj.dtype}")
            
            # If it's a string dataset that might contain JSON, try to parse it
            if obj.dtype.kind == 'O':
                try:
                    data = obj[()]
                    if isinstance(data, str):
                        parsed = json.loads(data)
                        print(' ' * (indent + 4) + f"Content (JSON parsed): {parsed}")
                    else:
                        print(' ' * (indent + 4) + f"Content: {data}")
                except:
                    print(' ' * (indent + 4) + f"Content: {obj[()]}")
            else:
                # Show first few elements for numeric datasets
                if len(obj.shape) > 0:
                    print(' ' * (indent + 4) + f"First few values: {obj[:min(5, obj.shape[0])]}")
                else:
                    print(' ' * (indent + 4) + f"Value: {obj[()]}")
        else:
            # Recursively print subgroups
            print_h5_structure(obj, indent + 2)

def extract_h5_structure(file_path):
    """
    Extract and print the complete structure of an HDF5 file
    
    Args:
        file_path: Path to the HDF5 file
    """
    try:
        with h5py.File(file_path, 'r') as f:
            print("=== HDF5 File Structure ===")
            print_h5_structure(f)
    except Exception as e:
        print(f"Error opening file: {e}")

if __name__ == "__main__":
    # Example usage:
    # Replace 'your_file.h5' with your actual HDF5 file path
    file_path = 'your_file.h5'
    extract_h5_structure(file_path)
    
    # You can also call it with a specific file path
    # extract_h5_structure('path/to/your/file.h5')
