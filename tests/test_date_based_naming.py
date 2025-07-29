"""
Unit tests for date-based file naming functionality.
Tests the new _yyyy_mm_dd suffix feature for output file names.
"""
import unittest
import tempfile
import os
from datetime import datetime
from unittest.mock import patch
import sys

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.models.file_processor import FileProcessor


class TestDateBasedNaming(unittest.TestCase):
    """Test cases for date-based file naming functionality."""
    
    def setUp(self) -> None:
        """Set up test fixtures before each test method."""
        self.processor = FileProcessor()
        
    def test_get_default_output_name_with_current_date(self) -> None:
        """Test that default output name includes current date."""
        # Create temporary test file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp_file:
            temp_file.write('test content')
            temp_file_path = temp_file.name
            
        try:
            # Set source file
            self.processor.set_source_file(temp_file_path)
            
            # Get default output name
            output_name = self.processor.get_default_output_name()
            
            # Get expected date suffix
            expected_date = datetime.now().strftime("%Y_%m_%d")
            
            # Verify date suffix is included
            self.assertIn(expected_date, output_name)
            self.assertTrue(output_name.endswith('.txt'))
            
        finally:
            os.unlink(temp_file_path)
            
    def test_get_default_output_name_different_extensions(self) -> None:
        """Test date-based naming with different file extensions."""
        test_cases = [
            ('sample.txt', '.txt'),
            ('database.sql', '.sql'),
            ('config.json', '.json'),
            ('script.py', '.py')
        ]
        
        for filename, extension in test_cases:
            with self.subTest(filename=filename):
                # Create temporary test file
                with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=extension) as temp_file:
                    temp_file.write('test content')
                    temp_file_path = temp_file.name
                    
                try:
                    # Set source file
                    self.processor.set_source_file(temp_file_path)
                    
                    # Get default output name
                    output_name = self.processor.get_default_output_name()
                    
                    # Get expected date suffix
                    expected_date = datetime.now().strftime("%Y_%m_%d")
                    
                    # Verify format
                    self.assertIn(expected_date, output_name)
                    self.assertTrue(output_name.endswith(extension))
                    
                finally:
                    os.unlink(temp_file_path)
                    
    def test_get_default_output_name_specific_example(self) -> None:
        """Test the specific example: sample_00.txt -> sample_00_2025_07_28.txt"""
        # Create temporary file with specific name pattern
        temp_dir = tempfile.mkdtemp()
        test_file_path = os.path.join(temp_dir, 'sample_00.txt')
        
        try:
            # Create the test file
            with open(test_file_path, 'w', encoding='utf-8') as f:
                f.write('test content')
                
            # Set source file
            self.processor.set_source_file(test_file_path)
            
            # Get default output name
            output_name = self.processor.get_default_output_name()
            
            # Get expected date suffix
            expected_date = datetime.now().strftime("%Y_%m_%d")
            expected_output = f"sample_00_{expected_date}.txt"
            
            # Verify exact format
            self.assertEqual(output_name, expected_output)
            
        finally:
            os.unlink(test_file_path)
            os.rmdir(temp_dir)
            
    @patch('src.models.file_processor.datetime')
    def test_get_default_output_name_mocked_date(self, mock_datetime) -> None:
        """Test date-based naming with mocked date for consistency."""
        # Mock datetime to return specific date
        mock_now = mock_datetime.now.return_value
        mock_now.strftime.return_value = "2025_07_28"
        
        # Create temporary test file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp_file:
            temp_file.write('test content')
            temp_file_path = temp_file.name
            
        try:
            # Set source file
            self.processor.set_source_file(temp_file_path)
            
            # Get default output name
            output_name = self.processor.get_default_output_name()
            
            # Verify mocked date is used
            self.assertIn("2025_07_28", output_name)
            mock_datetime.now.assert_called_once()
            mock_now.strftime.assert_called_once_with("%Y_%m_%d")
            
        finally:
            os.unlink(temp_file_path)
            
    def test_get_default_output_name_no_source_file(self) -> None:
        """Test default output name when no source file is set."""
        # Don't set any source file
        output_name = self.processor.get_default_output_name()
        
        # Should return empty string
        self.assertEqual(output_name, "")
        
    def test_get_default_output_name_complex_filename(self) -> None:
        """Test date-based naming with complex filenames."""
        test_cases = [
            'my_file_with_underscores.txt',
            'file-with-dashes.sql',
            'file.with.dots.json',
            'file with spaces.txt',
            'UPPERCASE_FILE.TXT'
        ]
        
        for filename in test_cases:
            with self.subTest(filename=filename):
                # Create temporary directory and file
                temp_dir = tempfile.mkdtemp()
                test_file_path = os.path.join(temp_dir, filename)
                
                try:
                    # Create the test file
                    with open(test_file_path, 'w', encoding='utf-8') as f:
                        f.write('test content')
                        
                    # Set source file
                    self.processor.set_source_file(test_file_path)
                    
                    # Get default output name
                    output_name = self.processor.get_default_output_name()
                    
                    # Get expected components
                    expected_date = datetime.now().strftime("%Y_%m_%d")
                    name, ext = os.path.splitext(filename)
                    expected_output = f"{name}_{expected_date}{ext}"
                    
                    # Verify format
                    self.assertEqual(output_name, expected_output)
                    
                finally:
                    os.unlink(test_file_path)
                    os.rmdir(temp_dir)
                    
    def test_date_format_consistency(self) -> None:
        """Test that date format is consistently YYYY_MM_DD."""
        # Create temporary test file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp_file:
            temp_file.write('test content')
            temp_file_path = temp_file.name
            
        try:
            # Set source file
            self.processor.set_source_file(temp_file_path)
            
            # Get multiple output names (should be consistent)
            output_name_1 = self.processor.get_default_output_name()
            output_name_2 = self.processor.get_default_output_name()
            
            # Should be identical (same date)
            self.assertEqual(output_name_1, output_name_2)
            
            # Verify date format pattern (YYYY_MM_DD)
            import re
            date_pattern = r'_\d{4}_\d{2}_\d{2}'
            self.assertTrue(re.search(date_pattern, output_name_1))
            
        finally:
            os.unlink(temp_file_path)
            
    def test_edge_case_no_extension(self) -> None:
        """Test date-based naming for files without extensions."""
        # Create temporary file without extension
        temp_dir = tempfile.mkdtemp()
        test_file_path = os.path.join(temp_dir, 'README')
        
        try:
            # Create the test file
            with open(test_file_path, 'w', encoding='utf-8') as f:
                f.write('test content')
                
            # Set source file
            self.processor.set_source_file(test_file_path)
            
            # Get default output name
            output_name = self.processor.get_default_output_name()
            
            # Get expected date suffix
            expected_date = datetime.now().strftime("%Y_%m_%d")
            expected_output = f"README_{expected_date}"
            
            # Verify format (no extension)
            self.assertEqual(output_name, expected_output)
            
        finally:
            os.unlink(test_file_path)
            os.rmdir(temp_dir)


if __name__ == '__main__':
    unittest.main()
