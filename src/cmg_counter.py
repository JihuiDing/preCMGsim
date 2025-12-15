import re
from pathlib import Path

def count_cmg_data_points(file_path, show_progress=True):
    """
    Count the total number of data points in a CMG data file with compressed format.
    
    Args:
        file_path (str or Path): Path to the CMG data file
        show_progress (bool): Whether to show progress messages
        
    Returns:
        int: Total number of data points
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"File '{file_path}' not found.")
    
    data_points = 0
    
    try:
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
                        data_points += count
                    else:
                        # If it's just a single number, count it as 1
                        try:
                            float(token)
                            data_points += 1
                        except ValueError:
                            # Skip non-numeric tokens
                            continue
                
                # Print progress every 50 lines
                if show_progress and line_num % 50 == 0:
                    print(f"Processed {line_num} lines, found {data_points:,} data points so far...")
    
    except Exception as e:
        raise Exception(f"Error reading file: {e}")
    
    return data_points

def quick_count(file_path):
    """
    Quick count without progress messages.
    
    Args:
        file_path (str or Path): Path to the CMG data file
        
    Returns:
        int: Total number of data points
    """
    return count_cmg_data_points(file_path, show_progress=False)

# Example usage functions
def example_usage():
    """Show examples of how to use the functions."""
    print("Example usage:")
    print("=" * 50)
    
    # Example 1: Count with progress
    print("1. Count with progress messages:")
    print("   count = count_cmg_data_points('data/your_file.dat')")
    
    # Example 2: Quick count without progress
    print("\n2. Quick count without progress:")
    print("   count = quick_count('data/your_file.dat')")
    
    # Example 3: Using Path object
    print("\n3. Using Path object:")
    print("   from pathlib import Path")
    print("   file_path = Path('data/your_file.dat')")
    print("   count = count_cmg_data_points(file_path)")
    
    # Example 4: Error handling
    print("\n4. With error handling:")
    print("   try:")
    print("       count = count_cmg_data_points('data/your_file.dat')")
    print("       print(f'Total data points: {count:,}')")
    print("   except FileNotFoundError as e:")
    print("       print(f'File not found: {e}')")
    print("   except Exception as e:")
    print("       print(f'Error: {e}')")

if __name__ == "__main__":
    example_usage() 