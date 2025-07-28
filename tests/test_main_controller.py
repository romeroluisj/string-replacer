"""
Unit tests for the MainController class.
Tests controller logic and coordination between Model and View.
"""
import unittest
import tempfile
import os
import sys
from unittest.mock import Mock, patch, MagicMock

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.controllers.main_controller import MainController


class TestMainController(unittest.TestCase):
    """Test cases for MainController class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.mock_view = Mock()
        self.controller = MainController(self.mock_view)
        
        # Create temporary test file
        self.temp_dir = tempfile.mkdtemp()
        self.test_file_path = os.path.join(self.temp_dir, "test_file.txt")
        with open(self.test_file_path, 'w', encoding='utf-8') as f:
            f.write("Hello foo world!")
    
    def tearDown(self):
        """Clean up after each test method."""
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)
        
        # Clean up any output files that may have been created
        import glob
        output_files = glob.glob(os.path.join(self.temp_dir, "*"))
        for file_path in output_files:
            if os.path.isfile(file_path):
                os.remove(file_path)
        
        # Remove directory if it exists and is empty
        if os.path.exists(self.temp_dir):
            try:
                os.rmdir(self.temp_dir)
            except OSError:
                # Directory not empty, remove remaining files
                import shutil
                shutil.rmtree(self.temp_dir)
    
    def test_init(self):
        """Test MainController initialization."""
        self.assertIsNotNone(self.controller.view)
        self.assertIsNotNone(self.controller.model)
        self.mock_view.set_controller.assert_called_once_with(self.controller)
    
    def test_browse_file_success(self):
        """Test successful file browsing."""
        self.mock_view.show_file_dialog.return_value = self.test_file_path
        
        self.controller.browse_file()
        
        self.mock_view.show_file_dialog.assert_called_once()
        self.mock_view.set_file_path.assert_called_once_with(self.test_file_path)
        self.mock_view.set_output_file_name.assert_called_once_with("test_file_updated.txt")
        self.mock_view.set_status.assert_called_once()
    
    def test_browse_file_cancelled(self):
        """Test file browsing when user cancels."""
        self.mock_view.show_file_dialog.return_value = ""
        
        self.controller.browse_file()
        
        self.mock_view.show_file_dialog.assert_called_once()
        self.mock_view.set_file_path.assert_not_called()
        self.mock_view.set_output_file_name.assert_not_called()
    
    def test_browse_file_error(self):
        """Test file browsing with file error."""
        self.mock_view.show_file_dialog.return_value = "/nonexistent/file.txt"
        
        self.controller.browse_file()
        
        self.mock_view.show_error.assert_called_once()
        self.mock_view.set_status.assert_called_with("Error selecting file", "red")
    
    def test_generate_random_string_success(self):
        """Test successful random string generation."""
        self.mock_view.get_random_length.return_value = "8"
        
        self.controller.generate_random_string()
        
        self.mock_view.get_random_length.assert_called_once()
        self.mock_view.set_replace_text.assert_called_once()
        self.mock_view.set_status.assert_called_once()
        
        # Check that a string was set (we can't predict the exact string)
        args = self.mock_view.set_replace_text.call_args[0]
        self.assertEqual(len(args[0]), 8)
        self.assertTrue(args[0].isalnum())
    
    def test_generate_random_string_invalid_length(self):
        """Test random string generation with invalid length."""
        self.mock_view.get_random_length.return_value = "invalid"
        
        self.controller.generate_random_string()
        
        self.mock_view.show_error.assert_called_once()
        self.mock_view.set_status.assert_called_with("Error generating random string", "red")
    
    def test_generate_random_string_zero_length(self):
        """Test random string generation with zero length."""
        self.mock_view.get_random_length.return_value = "0"
        
        self.controller.generate_random_string()
        
        self.mock_view.show_error.assert_called_once()
        self.mock_view.set_status.assert_called_with("Error generating random string", "red")
    
    def test_process_file_success(self):
        """Test successful file processing."""
        self.mock_view.get_file_path.return_value = self.test_file_path
        self.mock_view.get_find_text.return_value = "foo"
        self.mock_view.get_replace_text.return_value = "bar"
        self.mock_view.get_output_file_name.return_value = "output.txt"
        
        self.controller.process_file()
        
        self.mock_view.set_status.assert_any_call("Processing file...", "orange")
        self.mock_view.show_success.assert_called_once()
        self.mock_view.set_status.assert_called_with("File processed: output.txt", "green")
    
    def test_process_file_no_source_file(self):
        """Test file processing without source file."""
        self.mock_view.get_file_path.return_value = ""
        self.mock_view.get_find_text.return_value = "foo"
        self.mock_view.get_replace_text.return_value = "bar"
        self.mock_view.get_output_file_name.return_value = "output.txt"
        
        self.controller.process_file()
        
        self.mock_view.show_error.assert_called_with("Missing Input", "Please select a source file")
    
    def test_process_file_no_output_name(self):
        """Test file processing without output name."""
        self.mock_view.get_file_path.return_value = self.test_file_path
        self.mock_view.get_find_text.return_value = "foo"
        self.mock_view.get_replace_text.return_value = "bar"
        self.mock_view.get_output_file_name.return_value = ""
        
        self.controller.process_file()
        
        self.mock_view.show_error.assert_called_with("Missing Input", "Please specify an output file name")
    
    def test_process_file_no_find_replace(self):
        """Test file processing without find/replace text."""
        self.mock_view.get_file_path.return_value = self.test_file_path
        self.mock_view.get_find_text.return_value = ""
        self.mock_view.get_replace_text.return_value = ""
        self.mock_view.get_output_file_name.return_value = "output.txt"
        
        self.controller.process_file()
        
        self.mock_view.show_error.assert_called_with("Missing Input", "Please specify text to find or replace")
    
    def test_process_file_nonexistent_file(self):
        """Test file processing with nonexistent file."""
        self.mock_view.get_file_path.return_value = "/nonexistent/file.txt"
        self.mock_view.get_find_text.return_value = "foo"
        self.mock_view.get_replace_text.return_value = "bar"
        self.mock_view.get_output_file_name.return_value = "output.txt"
        
        self.controller.process_file()
        
        self.mock_view.show_error.assert_called_once()
        self.mock_view.set_status.assert_called_with("File not found", "red")
    
    def test_clear_all_success(self):
        """Test successful clear all operation."""
        self.controller.clear_all()
        
        self.mock_view.clear_all_fields.assert_called_once()
        self.mock_view.set_status.assert_called_with("All fields cleared")
    
    def test_clear_all_error(self):
        """Test clear all with error."""
        self.mock_view.clear_all_fields.side_effect = Exception("Clear error")
        
        self.controller.clear_all()
        
        self.mock_view.show_error.assert_called_once()
    
    def test_get_model_info(self):
        """Test getting model information."""
        # Set up model with some data
        self.controller.model.set_source_file(self.test_file_path)
        self.controller.model.set_find_replace_text("foo", "bar")
        self.controller.model.set_output_file_name("output.txt")
        
        info = self.controller.get_model_info()
        
        self.assertEqual(info['source_file'], self.test_file_path)
        self.assertEqual(info['find_text'], "foo")
        self.assertEqual(info['replace_text'], "bar")
        self.assertEqual(info['output_file'], "output.txt")


if __name__ == '__main__':
    unittest.main()
