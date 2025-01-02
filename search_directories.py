from pathlib import Path
import csv
from datetime import datetime

def search_files(main_folder, search_folder):
    """
    Search for files that exist in search_folder throughout all directories in main_folder
    and export results to a CSV file.
    
    Args:
        main_folder (str): Path to the main directory to search in
        search_folder (str): Path to the folder containing reference files
    """
    # Convert string paths to Path objects
    main_path = Path(main_folder)
    search_path = Path(search_folder)
    
    # Get list of file names from search folder with their original paths
    search_files = {file.name: str(file) for file in search_path.rglob('*') if file.is_file()}
    
    # Store results: [filename, reference_path, found_path, last_modified]
    results = []
    
    # Search through all directories in main folder
    for file_path in main_path.rglob('*'):
        if file_path.is_file() and file_path.name in search_files:
            # Get last modified time and convert to readable format
            mod_time = datetime.fromtimestamp(file_path.stat().st_mtime)
            mod_time_str = mod_time.strftime('%Y-%m-%d %H:%M:%S')
            
            results.append([
                file_path.name,
                search_files[file_path.name],  # Reference path
                str(file_path),                # Found path
                mod_time_str                   # Last modified date
            ])
    
    # Export results to CSV
    output_file = main_path / 'search_results.csv'
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['File Name', 'Reference Path', 'Found Path', 'Last Modified'])
        
        # Sort results by reference path (primary) and found path (secondary)
        sorted_results = sorted(results, key=lambda x: (x[1], x[2]))
        writer.writerows(sorted_results)
    
    print(f"Found {len(results)} matches. Results exported to {output_file}")

if __name__ == "__main__":
    # Example usage
    main_folder = r"C:\Your\Main\Folder\Path"  
    search_folder = r"C:\Your\Main\Folder\Path\Subfolder" 

    main_folder = r"/Users/tvlcek/Documents/code-experiments/test_main_folder"
    search_folder = r"/Users/tvlcek/Documents/code-experiments/test_main_folder/search_folder"
    
    search_files(main_folder, search_folder)
