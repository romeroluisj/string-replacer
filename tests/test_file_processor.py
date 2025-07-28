"""
Unit tests for the FileProcessor model class.
Tests all business logic and file operations.
"""
import unittest
import tempfile
import os
import sys

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.models.file_processor import FileProcessor


class TestFileProcessor(unittest.TestCase):
    """Test cases for FileProcessor class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.processor = FileProcessor()
        
        # Create temporary test files
        self.temp_dir = tempfile.mkdtemp()
        self.test_file_path = os.path.join(self.temp_dir, "test_file.txt")
        self.test_content = "Hello foo world!\nThis is a foo test.\nNo bar here yet."
        
        with open(self.test_file_path, 'w', encoding='utf-8') as f:
            f.write(self.test_content)
    
    def tearDown(self):
        """Clean up after each test method."""
        # Clean up temporary files
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)
        
        # Clean up any output files
        output_path = os.path.join(self.temp_dir, "test_output.txt")
        if os.path.exists(output_path):
            os.remove(output_path)
            
        os.rmdir(self.temp_dir)
    
    def test_init(self):
        """Test FileProcessor initialization."""
        self.assertEqual(self.processor.source_file_path, "")
        self.assertEqual(self.processor.find_text, "")
        self.assertEqual(self.processor.replace_text, "")
        self.assertEqual(self.processor.output_file_name, "")
        self.assertEqual(self.processor.max_random_length, 10)
    
    def test_set_source_file_valid(self):
        """Test setting a valid source file."""
        self.processor.set_source_file(self.test_file_path)
        self.assertEqual(self.processor.source_file_path, self.test_file_path)
    
    def test_set_source_file_invalid(self):
        """Test setting an invalid source file."""
        with self.assertRaises(FileNotFoundError):
            self.processor.set_source_file("/nonexistent/file.txt")
    
    def test_set_find_replace_text(self):
        """Test setting find and replace text."""
        self.processor.set_find_replace_text("foo", "bar")
        self.assertEqual(self.processor.find_text, "foo")
        self.assertEqual(self.processor.replace_text, "bar")
    
    def test_set_output_file_name(self):
        """Test setting output file name."""
        self.processor.set_output_file_name("output.txt")
        self.assertEqual(self.processor.output_file_name, "output.txt")
    
    def test_set_max_random_length_valid(self):
        """Test setting valid random length."""
        self.processor.set_max_random_length(15)
        self.assertEqual(self.processor.max_random_length, 15)
    
    def test_set_max_random_length_invalid(self):
        """Test setting invalid random length."""
        with self.assertRaises(ValueError):
            self.processor.set_max_random_length(0)
        
        with self.assertRaises(ValueError):
            self.processor.set_max_random_length(-5)
    
    def test_generate_random_string_default_length(self):
        """Test generating random string with default length."""
        random_str = self.processor.generate_random_string()
        self.assertEqual(len(random_str), 10)
        self.assertTrue(random_str.isalnum())
    
    def test_generate_random_string_custom_length(self):
        """Test generating random string with custom length."""
        random_str = self.processor.generate_random_string(5)
        self.assertEqual(len(random_str), 5)
        self.assertTrue(random_str.isalnum())
    
    def test_generate_random_string_invalid_length(self):
        """Test generating random string with invalid length."""
        with self.assertRaises(ValueError):
            self.processor.generate_random_string(0)
        
        with self.assertRaises(ValueError):
            self.processor.generate_random_string(-1)
    
    def test_get_default_output_name_no_file(self):
        """Test getting default output name with no source file."""
        result = self.processor.get_default_output_name()
        self.assertEqual(result, "")
    
    def test_get_default_output_name_with_file(self):
        """Test getting default output name with source file."""
        self.processor.set_source_file(self.test_file_path)
        result = self.processor.get_default_output_name()
        self.assertEqual(result, "test_file_updated.txt")
    
    def test_process_file_success(self):
        """Test successful file processing."""
        self.processor.set_source_file(self.test_file_path)
        self.processor.set_find_replace_text("foo", "bar")
        self.processor.set_output_file_name("test_output.txt")
        
        output_path = self.processor.process_file()
        
        # Check output file was created
        self.assertTrue(os.path.exists(output_path))
        
        # Check content was replaced correctly
        with open(output_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        expected_content = self.test_content.replace("foo", "bar")
        self.assertEqual(content, expected_content)
    
    def test_process_file_no_source(self):
        """Test processing file without source file."""
        self.processor.set_output_file_name("output.txt")
        
        with self.assertRaises(ValueError):
            self.processor.process_file()
    
    def test_process_file_no_output_name(self):
        """Test processing file without output name."""
        self.processor.set_source_file(self.test_file_path)
        
        with self.assertRaises(ValueError):
            self.processor.process_file()
    
    def test_process_file_empty_find_text(self):
        """Test processing file with empty find text."""
        self.processor.set_source_file(self.test_file_path)
        self.processor.set_find_replace_text("", "replacement")
        self.processor.set_output_file_name("test_output.txt")
        
        output_path = self.processor.process_file()
        
        # Should create file with original content (no replacement)
        with open(output_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        self.assertEqual(content, self.test_content)
    
    def test_get_file_info(self):
        """Test getting file information."""
        self.processor.set_source_file(self.test_file_path)
        self.processor.set_find_replace_text("foo", "bar")
        self.processor.set_output_file_name("output.txt")
        self.processor.set_max_random_length(20)
        
        info = self.processor.get_file_info()
        
        expected_info = {
            'source_file': self.test_file_path,
            'find_text': 'foo',
            'replace_text': 'bar',
            'output_file': 'output.txt',
            'max_random_length': 20
        }
        
        self.assertEqual(info, expected_info)


if __name__ == '__main__':
    unittest.main()
