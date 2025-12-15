import numpy as np
from pathlib import Path

def generate_full_porosity(
        actid_file, 
        poro_file, 
        output_file,
        total_cells,
        show_summary = False
        ):
    """
    Generate a porosity data file for all cells, filling inactive cells with 0.
    
    Args:
        actid_file (str or Path): Path to the active cell ID file (actid.npy)
        poro_file (str or Path): Path to the porosity file (poro.npy)
        output_file (str or Path): Path to the output porosity data file
        total_cells (int): Total number of cells in the grid (default: 989001)
        use_compression (bool): Whether to use compressed CMG format (default: True)
    
    Returns:
        dict: Summary statistics of the generated data
    """
    # Convert to Path objects
    actid_file = Path(actid_file)
    poro_file = Path(poro_file)
    output_file = Path(output_file)
    
    # Check if input files exist
    if not actid_file.exists():
        raise FileNotFoundError(f"Active cell ID file not found: {actid_file}")
    if not poro_file.exists():
        raise FileNotFoundError(f"Porosity file not found: {poro_file}")
    
    active_cell_ids = np.load(actid_file)
    porosity_values = np.load(poro_file)
    
    # Convert active cell IDs to integers if needed
    if active_cell_ids.dtype != np.int64 and active_cell_ids.dtype != np.int32:
        active_cell_ids = active_cell_ids.astype(np.int64)
    
    # Verify that the number of active cells matches the number of porosity values
    if len(active_cell_ids) != len(porosity_values):
        raise ValueError(f"Mismatch: {len(active_cell_ids)} active cells but {len(porosity_values)} porosity values")
    
    # Check that cell IDs are within valid range
    min_id = np.min(active_cell_ids)
    max_id = np.max(active_cell_ids)
    
    if min_id < 1 or max_id > total_cells:
        raise ValueError(f"Cell IDs out of range: {min_id} to {max_id} (should be 1 to {total_cells})")
    
    # Create full porosity array initialized with zeros
    full_porosity = np.zeros(total_cells, dtype=np.float64)
    
    # Fill in porosity values for active cells
    full_porosity[active_cell_ids - 1] = porosity_values  # Subtract 1 because cell IDs are 1-based
    
    # Save the full porosity array
    np.save(output_file, full_porosity)
    
    # Print summary
    if show_summary:
        print("\n" + "="*60)
        print("FULL POROSITY SUMMARY")
        print("="*60)
        print(f"Total cells: {total_cells:,}")
        print(f"Active cells: {len(active_cell_ids):,}")
        print(f"Active cell IDs data type: {active_cell_ids.dtype}")
        print(f"Porosity values data type: {porosity_values.dtype}")
        print(f"Active porosity - Mean: {np.mean(porosity_values):.6f}")
        print(f"Active porosity - Min: {np.min(porosity_values):.6f}")
        print(f"Active porosity - Max: {np.max(porosity_values):.6f}")
        print(f"Full porosity - Mean: {np.mean(full_porosity):.6f}")
        print(f"Full porosity - Min: {np.min(full_porosity):.6f}")
        print(f"Full porosity - Max: {np.max(full_porosity):.6f}")
        print(f"Saved full porosity data to: {output_file}")
    
    return full_porosity