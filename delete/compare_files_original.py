import numpy as np
from pathlib import Path
import re

def read_cmg_format_file(file_path):
    """
    Read a CMG format file and return the numerical values as a numpy array.
    
    Args:
        file_path (str or Path): Path to the CMG format file
        
    Returns:
        numpy.ndarray: Array of numerical values
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    values = []
    
    with open(file_path, 'r') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            
            # Skip empty lines and comments
            if not line or line.startswith('**'):
                continue
            
            # Split the line into tokens
            tokens = line.split()
            
            for token in tokens:
                # Check if token matches pattern N*value
                match = re.match(r'(\d+)\*([+-]?\d*\.?\d*)', token)
                if match:
                    count = int(match.group(1))
                    value = float(match.group(2))
                    values.extend([value] * count)
                else:
                    # If it's just a single number, add it once
                    try:
                        value = float(token)
                        values.append(value)
                    except ValueError:
                        # Skip non-numeric tokens
                        continue
    
    if not values:
        raise ValueError(f"No numerical values found in {file_path}. Check if the file format is correct.")
    
    return np.array(values, dtype=np.float64)

def read_gdecl_format_file(file_path):
    """
    Read a GRDECL format file and return the numerical values as a numpy array.
    
    Args:
        file_path (str or Path): Path to the GRDECL format file
        
    Returns:
        numpy.ndarray: Array of numerical values
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    values = []
    in_data_section = False
    
    with open(file_path, 'r') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
            
            # Check for data section start
            if line.upper().startswith('/'):
                in_data_section = True
                continue
            
            # If we're in data section, parse the line
            if in_data_section:
                # Split the line into tokens
                tokens = line.split()
                
                for token in tokens:
                    # Remove any trailing slashes
                    token = token.rstrip('/')
                    
                    # Check if token matches pattern N*value
                    match = re.match(r'(\d+)\*([+-]?\d*\.?\d*)', token)
                    if match:
                        count = int(match.group(1))
                        value = float(match.group(2))
                        values.extend([value] * count)
                    else:
                        # If it's just a single number, add it once
                        try:
                            value = float(token)
                            values.append(value)
                        except ValueError:
                            # Skip non-numeric tokens
                            continue
    
    if not values:
        raise ValueError(f"No numerical values found in {file_path}. Check if the file format is correct and contains data after the '/' marker.")
    
    return np.array(values, dtype=np.float64)

def read_numpy_file(file_path):
    """
    Read a numpy .npy file and return the array.
    
    Args:
        file_path (str or Path): Path to the numpy file
        
    Returns:
        numpy.ndarray: Array from the numpy file
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    array = np.load(file_path)
    
    if array.size == 0:
        raise ValueError(f"Empty array loaded from {file_path}")
    
    return array

def read_text_file(file_path):
    """
    Read a simple text file with one number per line.
    
    Args:
        file_path (str or Path): Path to the text file
        
    Returns:
        numpy.ndarray: Array of numerical values
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    values = []
    with open(file_path, 'r') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if line:  # Skip empty lines
                try:
                    value = float(line)
                    values.append(value)
                except ValueError:
                    print(f"Warning: Skipping non-numeric value on line {line_num}: {line}")
    
    if not values:
        raise ValueError(f"No numerical values found in {file_path}. Check if the file contains valid numbers.")
    
    return np.array(values, dtype=np.float64)

def read_file_by_extension(file_path):
    """
    Read a file based on its extension and return the numerical values.
    
    Args:
        file_path (str or Path): Path to the file
        
    Returns:
        numpy.ndarray: Array of numerical values
    """
    file_path = Path(file_path)
    extension = file_path.suffix.lower()
    
    if extension == '.npy':
        return read_numpy_file(file_path)
    elif extension == '.dat':
        return read_cmg_format_file(file_path)
    elif extension == '.gdecl' or extension == '.grdecl':
        return read_gdecl_format_file(file_path)
    elif extension == '.txt':
        return read_text_file(file_path)
    else:
        # Try to read as text file as fallback
        print(f"Unknown file extension {extension}, trying to read as text file...")
        return read_text_file(file_path)

def compare_arrays(array1, array2, tolerance=1e-10, file1_name="File 1", file2_name="File 2"):
    """
    Compare two numpy arrays and provide detailed comparison results.
    
    Args:
        array1 (numpy.ndarray): First array
        array2 (numpy.ndarray): Second array
        tolerance (float): Tolerance for floating point comparison
        file1_name (str): Name of first file for reporting
        file2_name (str): Name of second file for reporting
        
    Returns:
        dict: Comparison results
    """
    print(f"Comparing {file1_name} vs {file2_name}")
    print("=" * 60)
    
    # Check for empty arrays
    if len(array1) == 0:
        print(f"❌ ERROR: {file1_name} contains no numerical values!")
        return {
            'identical': False,
            'error': f'{file1_name} is empty',
            'size1': 0,
            'size2': len(array2)
        }
    
    if len(array2) == 0:
        print(f"❌ ERROR: {file2_name} contains no numerical values!")
        return {
            'identical': False,
            'error': f'{file2_name} is empty',
            'size1': len(array1),
            'size2': 0
        }
    
    # Basic array information
    print(f"{file1_name}:")
    print(f"  Shape: {array1.shape}")
    print(f"  Data type: {array1.dtype}")
    print(f"  Size: {len(array1):,} elements")
    print(f"  Min: {np.min(array1):.6f}")
    print(f"  Max: {np.max(array1):.6f}")
    print(f"  Mean: {np.mean(array1):.6f}")
    print(f"  Non-zero elements: {np.count_nonzero(array1):,}")
    
    print(f"\n{file2_name}:")
    print(f"  Shape: {array2.shape}")
    print(f"  Data type: {array2.dtype}")
    print(f"  Size: {len(array2):,} elements")
    print(f"  Min: {np.min(array2):.6f}")
    print(f"  Max: {np.max(array2):.6f}")
    print(f"  Mean: {np.mean(array2):.6f}")
    print(f"  Non-zero elements: {np.count_nonzero(array2):,}")
    
    # Check if arrays have the same size
    if len(array1) != len(array2):
        print(f"\n❌ ERROR: Arrays have different sizes!")
        print(f"   {file1_name}: {len(array1):,} elements")
        print(f"   {file2_name}: {len(array2):,} elements")
        return {
            'identical': False,
            'error': 'Different array sizes',
            'size1': len(array1),
            'size2': len(array2)
        }
    
    # Compare arrays
    print(f"\nComparing arrays with tolerance: {tolerance}")
    
    # Check for exact equality first
    if np.array_equal(array1, array2):
        print("✅ Arrays are exactly identical!")
        return {
            'identical': True,
            'exact_match': True,
            'tolerance_match': True,
            'max_difference': 0.0,
            'mean_difference': 0.0,
            'different_elements': 0
        }
    
    # Check for equality within tolerance
    differences = np.abs(array1 - array2)
    max_diff = np.max(differences)
    mean_diff = np.mean(differences)
    different_elements = np.sum(differences > tolerance)
    
    print(f"  Maximum difference: {max_diff:.2e}")
    print(f"  Mean difference: {mean_diff:.2e}")
    print(f"  Elements with difference > {tolerance}: {different_elements:,}")
    
    if different_elements == 0:
        print("✅ Arrays are identical within tolerance!")
        result = {
            'identical': True,
            'exact_match': False,
            'tolerance_match': True,
            'max_difference': max_diff,
            'mean_difference': mean_diff,
            'different_elements': 0
        }
    else:
        print("❌ Arrays are NOT identical!")
        
        # Find indices of different elements
        diff_indices = np.where(differences > tolerance)[0]
        print(f"  First 10 different elements:")
        for i in range(min(10, len(diff_indices))):
            idx = diff_indices[i]
            print(f"    Index {idx}: {array1[idx]:.6f} vs {array2[idx]:.6f} (diff: {differences[idx]:.2e})")
        
        if len(diff_indices) > 10:
            print(f"    ... and {len(diff_indices) - 10} more differences")
        
        result = {
            'identical': False,
            'exact_match': False,
            'tolerance_match': False,
            'max_difference': max_diff,
            'mean_difference': mean_diff,
            'different_elements': different_elements,
            'different_indices': diff_indices
        }
    
    return result

def debug_file_content(file_path, max_lines=10):
    """
    Debug function to show the content of a file for troubleshooting.
    
    Args:
        file_path (str or Path): Path to the file
        max_lines (int): Maximum number of lines to show
    """
    file_path = Path(file_path)
    if not file_path.exists():
        print(f"❌ File not found: {file_path}")
        return
    
    print(f"\n🔍 Debug: Content of {file_path.name} (first {max_lines} lines):")
    print("-" * 50)
    
    try:
        with open(file_path, 'r') as f:
            for i, line in enumerate(f, 1):
                if i > max_lines:
                    print(f"... and {file_path.stat().st_size:,} more bytes")
                    break
                print(f"{i:3d}: {repr(line.rstrip())}")
    except UnicodeDecodeError:
        print(f"❌ File appears to be binary or has encoding issues")
        print(f"   File size: {file_path.stat().st_size:,} bytes")
    except Exception as e:
        print(f"❌ Error reading file: {e}")

def compare_files(file1_path, file2_path, tolerance=1e-10, debug=False):
    """
    Compare numerical values in two files and provide detailed comparison results.
    
    Args:
        file1_path (str or Path): Path to the first file
        file2_path (str or Path): Path to the second file
        tolerance (float): Tolerance for floating point comparison
        debug (bool): Whether to show debug information about file contents
        
    Returns:
        dict: Comparison results
    """
    file1_path = Path(file1_path)
    file2_path = Path(file2_path)
    
    # Check if files exist
    if not file1_path.exists():
        raise FileNotFoundError(f"File not found: {file1_path}")
    if not file2_path.exists():
        raise FileNotFoundError(f"File not found: {file2_path}")
    
    print(f"Comparing files:")
    print(f"  File 1: {file1_path.name} ({file1_path.stat().st_size:,} bytes)")
    print(f"  File 2: {file2_path.name} ({file2_path.stat().st_size:,} bytes)")
    
    # Show debug information if requested
    if debug:
        debug_file_content(file1_path)
        debug_file_content(file2_path)
    
    try:
        # Read both files
        print(f"\nReading {file1_path.name}...")
        array1 = read_file_by_extension(file1_path)
        
        print(f"Reading {file2_path.name}...")
        array2 = read_file_by_extension(file2_path)
        
        # Compare arrays
        result = compare_arrays(array1, array2, tolerance=tolerance, 
                              file1_name=file1_path.name, file2_name=file2_path.name)
        
        # Print summary
        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)
        if result['identical']:
            print("✅ FILES ARE IDENTICAL")
            if result.get('exact_match', False):
                print("   (Exact match)")
            else:
                print("   (Match within tolerance)")
        else:
            print("❌ FILES ARE DIFFERENT")
            if 'different_elements' in result:
                print(f"   {result['different_elements']:,} elements differ")
                print(f"   Max difference: {result['max_difference']:.2e}")
            else:
                print(f"   Error: {result.get('error', 'Unknown error')}")
        
        return result
        
    except Exception as e:
        print(f"❌ Error during comparison: {e}")
        if not debug:
            print(f"💡 Try running with debug=True to see file contents")
        import traceback
        traceback.print_exc()
        raise

def main():
    """Main function to compare files in the validation folder."""
    validation_dir = Path("validation")
    
    if not validation_dir.exists():
        print(f"❌ Validation directory not found: {validation_dir}")
        return
    
    # List files in validation directory
    files = list(validation_dir.glob("*"))
    print(f"Files found in validation directory:")
    for i, file in enumerate(files, 1):
        print(f"  {i}. {file.name} ({file.stat().st_size:,} bytes)")
    
    if len(files) < 2:
        print(f"❌ Need at least 2 files to compare, found {len(files)}")
        return
    
    # Use the first two files for comparison
    file1 = files[0]
    file2 = files[1]
    
    # Call the comparison function
    try:
        result = compare_files(file1, file2)
        print(f"\n✅ Comparison completed successfully!")
    except Exception as e:
        print(f"❌ Comparison failed: {e}")

if __name__ == "__main__":
    main() 