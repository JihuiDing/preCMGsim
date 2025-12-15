import numpy as np
from pathlib import Path
from compare_full_arrays import compare_files, debug_file_content

def debug_porosity_mapping(actid_file, poro_file, correct_file, index_to_check=5446):
    """
    Debug the porosity mapping to understand why specific indices have wrong values.
    
    Args:
        actid_file (str): Path to active cell ID file
        poro_file (str): Path to porosity file
        correct_file (str): Path to the correct porosity file
        index_to_check (int): Index that has wrong value
    """
    print("🔍 DEBUGGING POROSITY MAPPING")
    print("=" * 60)
    
    # Load the data
    print("Loading data files...")
    active_cell_ids = np.load(actid_file)
    porosity_values = np.load(poro_file)
    
    print(f"Active cell IDs shape: {active_cell_ids.shape}")
    print(f"Porosity values shape: {porosity_values.shape}")
    
    # Check if the problematic index is in active cell IDs
    cell_id_1_based = index_to_check + 1  # Convert to 1-based indexing
    is_active = cell_id_1_based in active_cell_ids
    
    print(f"\nIndex {index_to_check} analysis:")
    print(f"  1-based cell ID: {cell_id_1_based}")
    print(f"  Is this cell active? {is_active}")
    
    if is_active:
        # Find the position in the active cell array
        pos_in_active = np.where(active_cell_ids == cell_id_1_based)[0][0]
        porosity_value = porosity_values[pos_in_active]
        print(f"  Position in active array: {pos_in_active}")
        print(f"  Porosity value assigned: {porosity_value}")
    else:
        print(f"  This cell is NOT active, should be 0")
    
    # Load the correct file to see what it should be
    print(f"\nLoading correct file: {correct_file}")
    correct_value = None
    try:
        if correct_file.endswith('.dat'):
            from compare_full_arrays import read_cmg_format_file
            correct_array = read_cmg_format_file(correct_file)
        elif correct_file.endswith('.npy'):
            correct_array = np.load(correct_file)
        elif correct_file.endswith('.GRDECL') or correct_file.endswith('.gdecl'):
            from compare_full_arrays import read_gdecl_format_file
            correct_array = read_gdecl_format_file(correct_file)
        else:
            print(f"Unsupported file format: {correct_file}")
            return None
        
        correct_value = correct_array[index_to_check]
        print(f"Correct value at index {index_to_check}: {correct_value}")
        
        # Check if this should be an active cell
        if correct_value != 0:
            print(f"❌ PROBLEM: Index {index_to_check} should be active (value: {correct_value}) but is not in active cell list!")
            
            # Find the closest active cells
            print(f"\nLooking for nearby active cells...")
            nearby_active = []
            for i in range(max(0, index_to_check - 10), min(len(correct_array), index_to_check + 11)):
                if correct_array[i] != 0:
                    nearby_active.append((i, correct_array[i]))
            
            print(f"Nearby active cells (within ±10 indices):")
            for idx, val in nearby_active:
                print(f"  Index {idx}: {val}")
                
    except Exception as e:
        print(f"Error loading correct file: {e}")
        return None
    
    # Check for potential indexing issues
    print(f"\nChecking for indexing issues...")
    print(f"Active cell ID range: {np.min(active_cell_ids)} to {np.max(active_cell_ids)}")
    print(f"Total active cells: {len(active_cell_ids)}")
    
    # Check if there are any duplicate active cell IDs
    unique_ids = np.unique(active_cell_ids)
    if len(unique_ids) != len(active_cell_ids):
        print(f"⚠️  WARNING: Duplicate active cell IDs found!")
        print(f"   Unique IDs: {len(unique_ids)}, Total IDs: {len(active_cell_ids)}")
    
    # Check if active cell IDs are sorted
    if not np.all(np.diff(active_cell_ids) >= 0):
        print(f"⚠️  WARNING: Active cell IDs are not sorted!")
    
    # Generate a test array to see what we're producing
    print(f"\nGenerating test array...")
    total_cells = 989001
    test_array = np.zeros(total_cells, dtype=np.float64)
    test_array[active_cell_ids - 1] = porosity_values
    
    test_value = test_array[index_to_check]
    print(f"Our generated value at index {index_to_check}: {test_value}")
    
    return {
        'is_active': is_active,
        'correct_value': correct_value,
        'our_value': test_value,
        'active_cell_count': len(active_cell_ids),
        'unique_active_cells': len(unique_ids)
    }

def main():
    """Main function to run the debug analysis."""
    # File paths
    actid_file = "results/actid.npy"
    poro_file = "results/poro.npy"
    correct_file = "validation/fromPetrel_por.dat"  # Fixed filename
    
    try:
        result = debug_porosity_mapping(actid_file, poro_file, correct_file, index_to_check=5446)
        
        if result is None:
            print("❌ Debug analysis failed - could not load files")
            return
        
        print(f"\n" + "=" * 60)
        print("DEBUG SUMMARY")
        print("=" * 60)
        print(f"Index 5446 is active: {result['is_active']}")
        print(f"Correct value: {result['correct_value']}")
        print(f"Our value: {result['our_value']}")
        print(f"Active cells in our data: {result['active_cell_count']}")
        print(f"Unique active cells: {result['unique_active_cells']}")
        
        if result['correct_value'] != result['our_value']:
            print(f"\n❌ MISMATCH DETECTED!")
            if result['correct_value'] != 0 and result['our_value'] == 0:
                print(f"   This cell should be active but is missing from our active cell list")
            elif result['correct_value'] == 0 and result['our_value'] != 0:
                print(f"   This cell should be inactive but is in our active cell list")
            else:
                print(f"   Value mismatch: expected {result['correct_value']}, got {result['our_value']}")
        
    except Exception as e:
        print(f"❌ Error during debug: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 