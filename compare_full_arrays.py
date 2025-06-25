import numpy as np
from pathlib import Path
import re

def compare_full_arrays(array1, 
                   array2, 
                   tolerance=1e-10, 
                   file1_name="File 1", 
                   file2_name="File 2",
                   ):
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
    print("\n" + "="*60)
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
