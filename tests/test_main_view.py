"""
Unit tests for the MainView class.
Tests GUI components and user interface interactions.
"""
import unittest
import tkinter as tk
import sys
import os
from unittest.mock import Mock, patch

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.views.main_view import MainView


class TestMainView(unittest.TestCase):
    """Test cases for MainView class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.root = tk.Tk()
        self.root.withdraw()  # Hide window during testing
        self.view = MainView(self.root)
        self.mock_controller = Mock()
        self.view.set_controller(self.mock_controller)
    
    def tearDown(self):
        """Clean up after each test method."""
        self.root.destroy()
    
    def test_init(self):
        """Test MainView initialization."""
        self.assertIsNotNone(self.view.root)
        self.assertEqual(self.view.root.title(), "String Replacer - MVC Architecture")
        self.assertIsNotNone(self.view.main_frame)
    
    def test_set_controller(self):
        """Test setting controller reference."""
        new_controller = Mock()
        self.view.set_controller(new_controller)
        self.assertEqual(self.view.controller, new_controller)
    
    def test_get_set_file_path(self):
        """Test getting and setting file path."""
        test_path = "/test/path/file.txt"
        self.view.set_file_path(test_path)
        self.assertEqual(self.view.get_file_path(), test_path)
    
    def test_get_find_text(self):
        """Test getting find text."""
        test_text = "test_find"
        self.view.find_entry.insert(0, test_text)
        self.assertEqual(self.view.get_find_text(), test_text)
    
    def test_get_set_replace_text(self):
        """Test getting and setting replace text."""
        test_text = "test_replace"
        self.view.set_replace_text(test_text)
        self.assertEqual(self.view.get_replace_text(), test_text)
    
    def test_get_random_length(self):
        """Test getting random length."""
        test_length = "15"
        self.view.random_length_var.set(test_length)
        self.assertEqual(self.view.get_random_length(), test_length)
    
    def test_get_set_output_file_name(self):
        """Test getting and setting output file name."""
        test_name = "output_test.txt"
        self.view.set_output_file_name(test_name)
        self.assertEqual(self.view.get_output_file_name(), test_name)
    
    def test_set_status(self):
        """Test setting status message."""
        test_message = "Test status"
        test_color = "red"
        self.view.set_status(test_message, test_color)
        self.assertEqual(self.view.status_var.get(), test_message)
        # Convert color object to string for comparison
        actual_color = str(self.view.status_label.cget("foreground"))
        self.assertTrue(test_color in actual_color or actual_color == test_color)
    
    def test_set_status_default_color(self):
        """Test setting status with default color."""
        test_message = "Test status default"
        self.view.set_status(test_message)
        self.assertEqual(self.view.status_var.get(), test_message)
        # Convert color object to string for comparison
        actual_color = str(self.view.status_label.cget("foreground"))
        self.assertTrue("blue" in actual_color or actual_color == "blue")
    
    @patch('tkinter.messagebox.showerror')
    def test_show_error(self, mock_showerror):
        """Test showing error dialog."""
        title = "Error Title"
        message = "Error Message"
        self.view.show_error(title, message)
        mock_showerror.assert_called_once_with(title, message)
    
    @patch('tkinter.messagebox.showinfo')
    def test_show_success(self, mock_showinfo):
        """Test showing success dialog."""
        title = "Success Title"
        message = "Success Message"
        self.view.show_success(title, message)
        mock_showinfo.assert_called_once_with(title, message)
    
    @patch('tkinter.filedialog.askopenfilename')
    def test_show_file_dialog(self, mock_filedialog):
        """Test showing file dialog."""
        mock_filedialog.return_value = "/test/file.txt"
        result = self.view.show_file_dialog()
        self.assertEqual(result, "/test/file.txt")
        mock_filedialog.assert_called_once()
    
    def test_clear_all_fields(self):
        """Test clearing all input fields."""
        # Set some values first
        self.view.set_file_path("/test/path")
        self.view.find_entry.insert(0, "find_text")
        self.view.set_replace_text("replace_text")
        self.view.random_length_var.set("20")
        self.view.set_output_file_name("output.txt")
        
        # Clear all fields
        self.view.clear_all_fields()
        
        # Verify all fields are cleared
        self.assertEqual(self.view.get_file_path(), "")
        self.assertEqual(self.view.get_find_text(), "")
        self.assertEqual(self.view.get_replace_text(), "")
        self.assertEqual(self.view.get_random_length(), "10")
        self.assertEqual(self.view.get_output_file_name(), "")
        self.assertEqual(self.view.status_var.get(), "Ready")
    
    def test_browse_file_button_callback(self):
        """Test browse file button callback."""
        self.view._on_browse_file()
        self.mock_controller.browse_file.assert_called_once()
    
    def test_generate_random_button_callback(self):
        """Test generate random button callback."""
        self.view._on_generate_random()
        self.mock_controller.generate_random_string.assert_called_once()
    
    def test_process_file_button_callback(self):
        """Test process file button callback."""
        self.view._on_process_file()
        self.mock_controller.process_file.assert_called_once()
    
    def test_clear_all_button_callback(self):
        """Test clear all button callback."""
        self.view._on_clear_all()
        self.mock_controller.clear_all.assert_called_once()
    
    def test_browse_file_no_controller(self):
        """Test browse file with no controller."""
        self.view.controller = None
        # Should not raise exception
        self.view._on_browse_file()
    
    def test_widget_creation(self):
        """Test that all required widgets are created."""
        # Check main components exist
        self.assertIsNotNone(self.view.main_frame)
        self.assertIsNotNone(self.view.file_entry)
        self.assertIsNotNone(self.view.browse_button)
        self.assertIsNotNone(self.view.find_entry)
        self.assertIsNotNone(self.view.replace_entry)
        self.assertIsNotNone(self.view.random_length_entry)
        self.assertIsNotNone(self.view.generate_button)
        self.assertIsNotNone(self.view.output_file_entry)
        self.assertIsNotNone(self.view.process_button)
        self.assertIsNotNone(self.view.clear_button)
        self.assertIsNotNone(self.view.status_label)


if __name__ == '__main__':
    unittest.main()
