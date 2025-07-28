"""
Integration tests for the String Replacer application.
Tests the complete MVC workflow and component interactions.
"""
import unittest
import tempfile
import os
import sys
import tkinter as tk

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.views.main_view import MainView
from src.controllers.main_controller import MainController


class TestIntegration(unittest.TestCase):
    """Integration test cases for the complete application."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.root = tk.Tk()
        self.root.withdraw()  # Hide window during testing
        
        # Create complete MVC setup
        self.view = MainView(self.root)
        self.controller = MainController(self.view)
        
        # Create temporary test files
        self.temp_dir = tempfile.mkdtemp()
        self.test_file_path = os.path.join(self.temp_dir, "integration_test.txt")
        self.test_content = "Hello foo world!\nThis is a foo test file.\nReplace foo with bar."
        
        with open(self.test_file_path, 'w', encoding='utf-8') as f:
            f.write(self.test_content)
    
    def tearDown(self):
        """Clean up after each test method."""
        # Clean up temporary files
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)
        
        # Clean up any output files
        output_path = os.path.join(self.temp_dir, "integration_test_updated.txt")
        if os.path.exists(output_path):
            os.remove(output_path)
            
        os.rmdir(self.temp_dir)
        self.root.destroy()
    
    def test_complete_workflow(self):
        """Test the complete file processing workflow."""
        # Step 1: Set file path (simulating file selection)
        self.view.set_file_path(self.test_file_path)
        self.controller.model.set_source_file(self.test_file_path)
        
        # Step 2: Set find and replace text
        self.view.find_entry.insert(0, "foo")
        self.view.replace_entry.insert(0, "bar")
        
        # Step 3: Set output file name
        output_name = "integration_test_updated.txt"
        self.view.set_output_file_name(output_name)
        
        # Step 4: Process the file
        self.controller.process_file()
        
        # Step 5: Verify the output
        output_path = os.path.join(self.temp_dir, output_name)
        self.assertTrue(os.path.exists(output_path))
        
        with open(output_path, 'r', encoding='utf-8') as f:
            processed_content = f.read()
        
        expected_content = self.test_content.replace("foo", "bar")
        self.assertEqual(processed_content, expected_content)
        
        # Verify original file is unchanged
        with open(self.test_file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        self.assertEqual(original_content, self.test_content)
    
    def test_random_string_workflow(self):
        """Test the random string generation workflow."""
        # Step 1: Set random string length
        self.view.random_length_var.set("12")
        
        # Step 2: Generate random string
        self.controller.generate_random_string()
        
        # Step 3: Verify random string was set
        replace_text = self.view.get_replace_text()
        self.assertEqual(len(replace_text), 12)
        self.assertTrue(replace_text.isalnum())
    
    def test_file_selection_workflow(self):
        """Test the file selection workflow."""
        # Simulate file selection
        self.controller.model.set_source_file(self.test_file_path)
        self.view.set_file_path(self.test_file_path)
        
        # Verify default output name is generated
        default_name = self.controller.model.get_default_output_name()
        self.assertEqual(default_name, "integration_test_updated.txt")
    
    def test_clear_all_workflow(self):
        """Test the clear all workflow."""
        # Step 1: Set some data
        self.view.set_file_path(self.test_file_path)
        self.view.find_entry.insert(0, "test")
        self.view.set_replace_text("replacement")
        self.view.set_output_file_name("output.txt")
        
        # Step 2: Clear all
        self.controller.clear_all()
        
        # Step 3: Verify everything is cleared
        self.assertEqual(self.view.get_file_path(), "")
        self.assertEqual(self.view.get_find_text(), "")
        self.assertEqual(self.view.get_replace_text(), "")
        self.assertEqual(self.view.get_output_file_name(), "")
    
    def test_error_handling_workflow(self):
        """Test error handling in the complete workflow."""
        # Test with missing file
        self.view.set_file_path("")
        self.view.find_entry.insert(0, "foo")
        self.view.set_replace_text("bar")
        self.view.set_output_file_name("output.txt")
        
        # Should handle error gracefully
        self.controller.process_file()
        # No exception should be raised
    
    def test_mvc_communication(self):
        """Test communication between MVC components."""
        # Test that controller has references to model and view
        self.assertIsNotNone(self.controller.model)
        self.assertIsNotNone(self.controller.view)
        
        # Test that view has reference to controller
        self.assertEqual(self.view.controller, self.controller)
        
        # Test model info retrieval
        info = self.controller.get_model_info()
        self.assertIsInstance(info, dict)
        self.assertIn('source_file', info)
        self.assertIn('find_text', info)
        self.assertIn('replace_text', info)


if __name__ == '__main__':
    unittest.main()
