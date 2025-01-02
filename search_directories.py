from pathlib import Path
import csv
from datetime import datetime

def search_files(main_folder, search_folder):
    """
    Search for files that exist in search_folder throughout all directories in main_folder
    and export results to two CSV files: matches and missing files.
    
    Args:
        main_folder (str): Path to the main directory to search in
        search_folder (str): Path to the folder containing reference files
    """
    # Convert string paths to Path objects
    main_path = Path(main_folder)
    search_path = Path(search_folder)
    
    # Get list of file names from search folder with their original paths
    search_files = {file.name: str(file) for file in search_path.rglob('*') if file.is_file()}
    
    # Store results for matches and missing files
    matches = []
    missing = []
    
    # Keep track of which search files were found
    found_files = set()

    # Search through all directories in main folder
    for file_path in main_path.rglob('*'):
        if file_path.is_file():
            if file_path.name in search_files:
                # Get last modified time and convert to readable format
                mod_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                mod_time_str = mod_time.strftime('%Y-%m-%d %H:%M:%S')
                
                matches.append([
                    file_path.name,
                    search_files[file_path.name],  # Reference path
                    str(file_path),                # Found path
                    mod_time_str                   # Last modified date
                ])
                found_files.add(file_path.name)
    
    # Find files that exist in search_folder but weren't found in main_folder
    for filename, ref_path in search_files.items():
        if filename not in found_files:
            missing.append([
                filename,
                ref_path,
                "Not found in main folder"
            ])

    # Export matches to CSV
    output_file = main_path / 'search_results.csv'
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['File Name', 'Reference Path', 'Found Path', 'Last Modified'])
        sorted_matches = sorted(matches, key=lambda x: (x[1], x[2]))
        writer.writerows(sorted_matches)

    # Export missing files to CSV
    missing_file = main_path / 'missing_files.csv'
    with open(missing_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['File Name', 'Reference Path', 'Status'])
        sorted_missing = sorted(missing, key=lambda x: x[1])
        writer.writerows(sorted_missing)
    
    print(f"Found {len(matches)} matches. Results exported to {output_file}")
    print(f"Found {len(missing)} missing files. Results exported to {missing_file}")

if __name__ == "__main__":
    # Example usage
    main_folder = r"C:\Your\Main\Folder\Path"  
    search_folder = r"C:\Your\Main\Folder\Path\Subfolder" 

    main_folder = r"/Users/tvlcek/Documents/code-experiments/test_main_folder"
    search_folder = r"/Users/tvlcek/Documents/code-experiments/test_main_folder/search_folder"
    
    search_files(main_folder, search_folder)
