import re
import sys
import argparse
from pathlib import Path

def count_cmg_data_points_accurate(file_path):
    """
    Count the total number of data points in a CMG data file with compressed format.
    Handles patterns like '48*0 3*1' which means 48 zeros followed by 3 ones.
    
    Args:
        file_path (str): Path to the CMG data file
        
    Returns:
        int: Total number of data points
    """
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
                if line_num % 50 == 0:
                    print(f"Processed {line_num} lines, found {data_points:,} data points so far...")
    
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return 0
    except Exception as e:
        print(f"Error reading file: {e}")
        return 0
    
    return data_points

def analyze_cmg_format(file_path):
    """
    Analyze the CMG file format in detail.
    
    Args:
        file_path (str): Path to the CMG data file
    """
    print(f"Analyzing CMG format of: {file_path}")
    print("-" * 60)
    
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
            
        print(f"Total lines in file: {len(lines)}")
        
        # Show header
        if lines:
            print(f"\nHeader: {lines[0].strip()}")
        
        # Analyze first few data lines
        print("\nFirst 5 data lines analysis:")
        data_lines = [line.strip() for line in lines[1:] if line.strip() and not line.strip().startswith('**')]
        
        for i, line in enumerate(data_lines[:5]):
            print(f"\nLine {i+1}: {line}")
            
            # Parse the line
            tokens = line.split()
            total_count = 0
            
            for token in tokens:
                match = re.match(r'(\d+)\*([+-]?\d*\.?\d*)', token)
                if match:
                    count = int(match.group(1))
                    value = match.group(2)
                    total_count += count
                    print(f"  {token} -> {count} times value {value}")
                else:
                    try:
                        float(token)
                        total_count += 1
                        print(f"  {token} -> single value")
                    except ValueError:
                        print(f"  {token} -> non-numeric (skipped)")
            
            print(f"  Total data points in this line: {total_count}")
        
        # Count total compressed patterns
        compressed_patterns = 0
        single_values = 0
        
        for line in data_lines:
            tokens = line.split()
            for token in tokens:
                if re.match(r'\d+\*[+-]?\d*\.?\d*', token):
                    compressed_patterns += 1
                else:
                    try:
                        float(token)
                        single_values += 1
                    except ValueError:
                        pass
        
        print(f"\nFormat Summary:")
        print(f"Compressed patterns (N*value): {compressed_patterns}")
        print(f"Single values: {single_values}")
        
    except Exception as e:
        print(f"Error analyzing file: {e}")

def main():
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='Count data points in CMG files with compressed format')
    parser.add_argument('file_path', nargs='?', default="data/JD_Sula_2025_flow_nontg_pinchoutarray_all.dat",
                       help='Path to the CMG data file (default: data/JD_Sula_2025_flow_nontg_pinchoutarray_all.dat)')
    parser.add_argument('--no-analysis', action='store_true',
                       help='Skip the detailed file analysis')
    parser.add_argument('--quiet', action='store_true',
                       help='Suppress progress messages')
    
    args = parser.parse_args()
    
    # Convert to Path object
    cmg_file = Path(args.file_path)
    
    # Check if file exists
    if not cmg_file.exists():
        print(f"Error: File '{cmg_file}' not found.")
        return
    
    print(f"Counting data points in CMG file: {cmg_file}")
    print("=" * 70)
    
    # Analyze file format first (unless --no-analysis is specified)
    if not args.no_analysis:
        analyze_cmg_format(cmg_file)
        print("\n" + "=" * 70)
    
    print("Counting data points with compressed format handling...")
    
    # Count data points
    total_points = count_cmg_data_points_accurate(cmg_file)
    
    print("\n" + "=" * 70)
    print(f"RESULT: Total number of data points = {total_points:,}")
    print("=" * 70)

if __name__ == "__main__":
    main() 