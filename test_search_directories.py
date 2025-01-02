from pathlib import Path

def create_test_structure(base_path):
    """
    Creates a test folder structure with sample files
    
    Structure:
    main_folder/
    ├── documents/
    │   ├── work/
    │   │   ├── report.txt
    │   │   └── presentation.pdf
    │   └── personal/
    │       ├── notes.txt
    │       └── budget.xlsx
    ├── search_folder/
    │   ├── report.txt
    │   └── notes.txt
    └── media/
        ├── images/
        │   ├── photo.jpg
        │   └── report.txt
        └── videos/
            └── video.mp4
    """
    
    # Convert to Path object
    base = Path(base_path)
    
    # Create folder structure
    folders = [
        'documents/work',
        'documents/personal',
        'search_folder',
        'media/images',
        'media/videos'
    ]
    
    # Create folders
    for folder in folders:
        (base / folder).mkdir(parents=True, exist_ok=True)
    
    # Create sample files
    files = [
        'documents/work/report.txt',
        'documents/work/presentation.pdf',
        'documents/personal/notes.txt',
        'documents/personal/budget.xlsx',
        'search_folder/report.txt',
        'search_folder/notes.txt',
        'media/images/photo.jpg',
        'media/images/report.txt',
        'media/videos/video.mp4'
    ]
    
    # Create files
    for file in files:
        file_path = base / file
        file_path.touch()
        # Add some content to txt files
        if file_path.suffix == '.txt':
            file_path.write_text(f"This is a sample content for {file_path.name}")

import unittest
import csv
from search_directories import search_files
import tempfile
import shutil

class TestSearchDirectories(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = Path(tempfile.mkdtemp())
        create_test_structure(self.test_dir)
        
    def tearDown(self):
        # Clean up the temporary directory after tests
        shutil.rmtree(self.test_dir)
        
    def test_search_files(self):
        # Define paths for testing
        main_folder = self.test_dir
        search_folder = main_folder / "search_folder"
        
        # Run the search
        search_files(main_folder, search_folder)
        
        # Check if results file was created
        results_file = main_folder / "search_results.csv"
        self.assertTrue(results_file.exists())
        
        # Read and verify results
        with open(results_file, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            results = list(reader)
            
            # Should find 5 matches
            self.assertEqual(len(results), 5)
            
            # Verify all expected files are found
            found_files = {(row['File Name'], row['Found Path']) for row in results}
            expected_files = {
                ('report.txt', str(main_folder / 'documents/work/report.txt')),
                ('report.txt', str(main_folder / 'media/images/report.txt')),
                ('notes.txt', str(main_folder / 'documents/personal/notes.txt'))
            }
            
            # Check that all expected files are in the results
            for expected in expected_files:
                self.assertIn(expected[0], [f[0] for f in found_files])
            
            # Verify CSV headers
            expected_headers = {'File Name', 'Reference Path', 'Found Path', 'Last Modified'}
            self.assertEqual(set(results[0].keys()), expected_headers)
            
            # Verify all entries have non-empty values
            for row in results:
                for value in row.values():
                    self.assertTrue(value, "Found empty value in results")

if __name__ == '__main__':
    unittest.main()