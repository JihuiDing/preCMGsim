#!/usr/bin/env python3
"""
Example usage of the porosity generation functions with compressed format.
"""

from delete.generate_full_porosity import (
    generate_full_porosity_data, 
    generate_full_porosity_data_simple,
    decompress_cmg_format_to_array
)
import numpy as np

def example_1_basic_usage():
    """Example 1: Basic usage with compression."""
    print("Example 1: Basic usage with compression")
    print("-" * 50)
    
    try:
        summary = generate_full_porosity_data(
            actid_file="results/actid.npy",
            poro_file="results/poro.npy", 
            output_file="results/full_porosity_example1.npy",
            use_compression=True
        )
        print(f"✅ Generated file with {summary['active_cells']:,} active cells")
        print(f"📦 Compression ratio: {summary['compression_ratio']:.1f}:1")
    except Exception as e:
        print(f"❌ Error: {e}")

def example_2_simple_function():
    """Example 2: Using the simple function with compression."""
    print("\nExample 2: Simple function with compression")
    print("-" * 50)
    
    try:
        full_porosity = generate_full_porosity_data_simple(
            actid_file="results/actid.npy",
            poro_file="results/poro.npy",
            output_file="results/full_porosity_example2.npy",
            use_compression=True
        )
        print(f"✅ Generated array with shape: {full_porosity.shape}")
        print(f"   Non-zero values: {np.count_nonzero(full_porosity):,}")
    except Exception as e:
        print(f"❌ Error: {e}")

def example_3_without_compression():
    """Example 3: Without compression for comparison."""
    print("\nExample 3: Without compression")
    print("-" * 50)
    
    try:
        summary = generate_full_porosity_data(
            actid_file="results/actid.npy",
            poro_file="results/poro.npy",
            output_file="results/full_porosity_example3.npy",
            use_compression=False
        )
        print(f"✅ Generated file without compression")
        print(f"📁 Files: {summary['output_file']}, {summary['text_file']}")
    except Exception as e:
        print(f"❌ Error: {e}")

def example_4_decompress_and_verify():
    """Example 4: Decompress and verify the compressed file."""
    print("\nExample 4: Decompress and verify")
    print("-" * 50)
    
    try:
        # Load the original numpy file
        original_array = np.load("results/full_porosity.npy")
        
        # Decompress the .dat file
        compressed_file = "results/full_porosity.dat"
        decompressed_array = decompress_cmg_format_to_array(compressed_file)
        
        print(f"Original array shape: {original_array.shape}")
        print(f"Decompressed array shape: {decompressed_array.shape}")
        
        # Verify they match
        if np.allclose(original_array, decompressed_array):
            print("✅ Decompressed data matches original exactly")
        else:
            print("❌ Decompressed data does not match original")
            
        # Show some statistics
        print(f"Original - Mean: {np.mean(original_array):.6f}, Non-zero: {np.count_nonzero(original_array):,}")
        print(f"Decompressed - Mean: {np.mean(decompressed_array):.6f}, Non-zero: {np.count_nonzero(decompressed_array):,}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def example_5_compression_efficiency():
    """Example 5: Compare file sizes and compression efficiency."""
    print("\nExample 5: Compression efficiency")
    print("-" * 50)
    
    try:
        from pathlib import Path
        
        # Check file sizes
        files_to_check = [
            "results/full_porosity.npy",
            "results/full_porosity.txt", 
            "results/full_porosity.dat"
        ]
        
        for file_path in files_to_check:
            path = Path(file_path)
            if path.exists():
                size_mb = path.stat().st_size / (1024 * 1024)
                print(f"📁 {path.name}: {size_mb:.2f} MB")
            else:
                print(f"❌ {path.name}: Not found")
        
        # Calculate compression ratios
        npy_size = Path("results/full_porosity.npy").stat().st_size
        dat_size = Path("results/full_porosity.dat").stat().st_size
        txt_size = Path("results/full_porosity.txt").stat().st_size
        
        print(f"\n📊 Compression ratios:")
        print(f"   .dat vs .npy: {npy_size/dat_size:.1f}:1")
        print(f"   .dat vs .txt: {txt_size/dat_size:.1f}:1")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def example_6_verify_results():
    """Example 6: Verify the generated results."""
    print("\nExample 6: Verify results")
    print("-" * 50)
    
    try:
        # Load the generated file
        full_porosity = np.load("results/full_porosity.npy")
        active_cell_ids = np.load("results/actid.npy").astype(np.int64)
        original_poro = np.load("results/poro.npy")
        
        print(f"Full porosity array shape: {full_porosity.shape}")
        print(f"Total cells: {len(full_porosity):,}")
        print(f"Active cells: {len(active_cell_ids):,}")
        print(f"Non-zero values: {np.count_nonzero(full_porosity):,}")
        
        # Verify that active cells have correct values
        active_values = full_porosity[active_cell_ids - 1]
        if np.allclose(active_values, original_poro):
            print("✅ Active cell values match original porosity data")
        else:
            print("❌ Active cell values do not match")
        
        # Verify that inactive cells are zero
        inactive_mask = np.ones(len(full_porosity), dtype=bool)
        inactive_mask[active_cell_ids - 1] = False
        inactive_values = full_porosity[inactive_mask]
        
        if np.all(inactive_values == 0):
            print("✅ Inactive cells are correctly set to zero")
        else:
            print("❌ Some inactive cells are not zero")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Run all examples."""
    print("Porosity Generation Function Examples (with Compression)")
    print("=" * 60)
    
    example_1_basic_usage()
    example_2_simple_function()
    example_3_without_compression()
    example_4_decompress_and_verify()
    example_5_compression_efficiency()
    example_6_verify_results()
    
    print("\n" + "=" * 60)
    print("All examples completed!")

if __name__ == "__main__":
    main() 