import os
import glob
from pathlib import Path

def extract_filenames_from_properties():
    """
    Extract file names from the results/properties folder.
    Returns a list of file names (excluding hidden files like .DS_Store).
    """
    # Define the path to the properties folder
    properties_path = "results/properties"
    
    # Check if the directory exists
    if not os.path.exists(properties_path):
        print(f"Error: Directory '{properties_path}' does not exist.")
        return []
    
    # Get all files in the directory
    files = []
    try:
        # Use pathlib for better cross-platform compatibility
        properties_dir = Path(properties_path)
        
        # Get all files, excluding hidden files
        for file_path in properties_dir.iterdir():
            if file_path.is_file() and not file_path.name.startswith('.'):
                files.append(file_path.name)
        
        # Alternative method using glob (uncomment if preferred)
        # files = [os.path.basename(f) for f in glob.glob(os.path.join(properties_path, "*")) 
        #         if os.path.isfile(f) and not os.path.basename(f).startswith('.')]
        
    except Exception as e:
        print(f"Error reading directory: {e}")
        return []
    
    return files

def main():
    """Main function to extract and display file names."""
    print("Extracting file names from results/properties folder...")
    print("-" * 50)
    
    # Extract file names
    filenames = extract_filenames_from_properties()
    
    if filenames:
        print(f"Found {len(filenames)} files:")
        print()
        for i, filename in enumerate(filenames, 1):
            print(f"{i:2d}. {filename}")
        
        print()
        print("File details:")
        print("-" * 30)
        
        # Get additional file information
        properties_path = "results/properties"
        for filename in filenames:
            file_path = os.path.join(properties_path, filename)
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                # Convert to MB for readability
                size_mb = file_size / (1024 * 1024)
                print(f"{filename}: {size_mb:.1f} MB")
    else:
        print("No files found in the properties folder.")

if __name__ == "__main__":
    main() 