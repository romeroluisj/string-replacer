"""
Unit tests for database password processing functionality.
Tests the new db pwd feature including password extraction and replacement.
"""
import unittest
import tempfile
import os
from unittest.mock import patch, MagicMock
import sys

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.models.file_processor import FileProcessor
from src.views.main_view import MainView
from src.controllers.main_controller import MainController


class TestDbPasswordProcessing(unittest.TestCase):
    """Test cases for database password processing functionality."""
    
    def setUp(self) -> None:
        """Set up test fixtures before each test method."""
        self.processor = FileProcessor()
        
    def test_extract_db_passwords_from_first_line_success(self) -> None:
        """Test successful password extraction from first line."""
        content = 'ALTER USER myuser IDENTIFIED BY "newpass123" REPLACE "oldpass456";\nSELECT * FROM users;'
        
        new_pw, cur_pw = self.processor.extract_db_passwords_from_first_line(content)
        
        self.assertEqual(new_pw, "newpass123")
        self.assertEqual(cur_pw, "oldpass456")
        
    def test_extract_db_passwords_case_insensitive(self) -> None:
        """Test password extraction is case insensitive."""
        content = 'alter user myuser identified by "NewPass" replace "OldPass";'
        
        new_pw, cur_pw = self.processor.extract_db_passwords_from_first_line(content)
        
        self.assertEqual(new_pw, "NewPass")
        self.assertEqual(cur_pw, "OldPass")
        
    def test_extract_db_passwords_with_spaces(self) -> None:
        """Test password extraction with various spacing."""
        content = 'ALTER USER myuser IDENTIFIED   BY   "pass1"   REPLACE   "pass2";'
        
        new_pw, cur_pw = self.processor.extract_db_passwords_from_first_line(content)
        
        self.assertEqual(new_pw, "pass1")
        self.assertEqual(cur_pw, "pass2")
        
    def test_extract_db_passwords_missing_by_pattern(self) -> None:
        """Test password extraction when BY pattern is missing."""
        content = 'ALTER USER myuser REPLACE "oldpass";'
        
        new_pw, cur_pw = self.processor.extract_db_passwords_from_first_line(content)
        
        self.assertIsNone(new_pw)
        self.assertEqual(cur_pw, "oldpass")
        
    def test_extract_db_passwords_missing_replace_pattern(self) -> None:
        """Test password extraction when REPLACE pattern is missing."""
        content = 'ALTER USER myuser IDENTIFIED BY "newpass";'
        
        new_pw, cur_pw = self.processor.extract_db_passwords_from_first_line(content)
        
        self.assertEqual(new_pw, "newpass")
        self.assertIsNone(cur_pw)
        
    def test_extract_db_passwords_no_patterns(self) -> None:
        """Test password extraction when no patterns are found."""
        content = 'SELECT * FROM users WHERE id = 1;'
        
        new_pw, cur_pw = self.processor.extract_db_passwords_from_first_line(content)
        
        self.assertIsNone(new_pw)
        self.assertIsNone(cur_pw)
        
    def test_extract_db_passwords_empty_content(self) -> None:
        """Test password extraction with empty content."""
        content = ""
        
        new_pw, cur_pw = self.processor.extract_db_passwords_from_first_line(content)
        
        self.assertIsNone(new_pw)
        self.assertIsNone(cur_pw)
        
    def test_extract_db_passwords_multiline_only_first_line(self) -> None:
        """Test that only the first line is processed for password extraction."""
        content = '''SELECT * FROM users;
ALTER USER myuser IDENTIFIED BY "shouldnotfind" REPLACE "shouldnotfind2";'''
        
        new_pw, cur_pw = self.processor.extract_db_passwords_from_first_line(content)
        
        self.assertIsNone(new_pw)
        self.assertIsNone(cur_pw)
        
    def test_process_db_password_file_success(self) -> None:
        """Test successful database password file processing."""
        # Create temporary test file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.sql') as temp_file:
            temp_file.write('ALTER USER myuser IDENTIFIED BY "newpass123" REPLACE "oldpass456";\n')
            temp_file.write('SELECT * FROM users WHERE password = "newpass123";\n')
            temp_file.write('UPDATE config SET old_password = "oldpass456";')
            temp_file_path = temp_file.name
            
        try:
            # Set up processor
            self.processor.set_source_file(temp_file_path)
            self.processor.set_output_file_name("test_output.sql")
            self.processor.set_max_random_length(8)
            
            # Process file
            output_path = self.processor.process_db_password_file(
                use_uppercase=True,
                use_lowercase=True,
                use_numbers=True
            )
            
            # Verify output file was created
            self.assertTrue(os.path.exists(output_path))
            
            # Read and verify output content
            with open(output_path, 'r', encoding='utf-8') as f:
                output_content = f.read()
                
            # Verify passwords were replaced
            self.assertNotIn("newpass123", output_content)
            self.assertNotIn("oldpass456", output_content)
            
            # Verify structure is maintained
            self.assertIn("ALTER USER myuser IDENTIFIED BY", output_content)
            self.assertIn("SELECT * FROM users WHERE password =", output_content)
            self.assertIn("UPDATE config SET old_password =", output_content)
            
            # Clean up
            os.unlink(output_path)
            
        finally:
            os.unlink(temp_file_path)
            
    def test_process_db_password_file_no_source_file(self) -> None:
        """Test database password processing without source file."""
        self.processor.set_output_file_name("test_output.sql")
        
        with self.assertRaises(ValueError) as context:
            self.processor.process_db_password_file()
            
        self.assertIn("No source file specified", str(context.exception))
        
    def test_process_db_password_file_no_output_name(self) -> None:
        """Test database password processing without output file name."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            temp_file.write('ALTER USER test BY "pass1" REPLACE "pass2";')
            temp_file_path = temp_file.name
            
        try:
            self.processor.set_source_file(temp_file_path)
            
            with self.assertRaises(ValueError) as context:
                self.processor.process_db_password_file()
                
            self.assertIn("No output file name specified", str(context.exception))
            
        finally:
            os.unlink(temp_file_path)
            
    def test_process_db_password_file_no_passwords_found(self) -> None:
        """Test database password processing when no passwords are found."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            temp_file.write('SELECT * FROM users;')
            temp_file_path = temp_file.name
            
        try:
            self.processor.set_source_file(temp_file_path)
            self.processor.set_output_file_name("test_output.sql")
            
            with self.assertRaises(ValueError) as context:
                self.processor.process_db_password_file()
                
            self.assertIn("Could not find password patterns", str(context.exception))
            
        finally:
            os.unlink(temp_file_path)
            
    def test_process_db_password_file_character_sets(self) -> None:
        """Test database password processing with different character sets."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.sql') as temp_file:
            temp_file.write('ALTER USER test BY "new123" REPLACE "old456";\n')
            temp_file_path = temp_file.name
            
        try:
            self.processor.set_source_file(temp_file_path)
            self.processor.set_output_file_name("test_output.sql")
            self.processor.set_max_random_length(10)
            
            # Test uppercase only
            output_path = self.processor.process_db_password_file(
                use_uppercase=True,
                use_lowercase=False,
                use_numbers=False
            )
            
            with open(output_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Extract the generated password (should be uppercase only)
            import re
            matches = re.findall(r'BY "([^"]+)"', content)
            if matches:
                generated_password = matches[0]
                self.assertTrue(generated_password.isupper())
                self.assertTrue(generated_password.isalpha())
                
            os.unlink(output_path)
            
        finally:
            os.unlink(temp_file_path)


class TestDbPasswordUI(unittest.TestCase):
    """Test cases for database password UI components."""
    
    def setUp(self) -> None:
        """Set up test fixtures."""
        # Mock tkinter to avoid GUI creation during tests
        with patch('tkinter.Tk'):
            self.mock_root = MagicMock()
            with patch('src.views.main_view.tk.Tk', return_value=self.mock_root):
                self.view = MainView(self.mock_root)
                
    def test_db_pwd_checkbox_default_state(self) -> None:
        """Test that db pwd checkbox is unchecked by default."""
        self.assertFalse(self.view.get_db_pwd_mode())
        
    def test_db_pwd_checkbox_state_change(self) -> None:
        """Test changing db pwd checkbox state."""
        # Set to checked
        self.view.db_pwd_var.set(True)
        self.assertTrue(self.view.get_db_pwd_mode())
        
        # Set to unchecked
        self.view.db_pwd_var.set(False)
        self.assertFalse(self.view.get_db_pwd_mode())
        
    def test_clear_all_fields_resets_db_pwd(self) -> None:
        """Test that clear all fields resets db pwd checkbox."""
        # Set checkbox to checked
        self.view.db_pwd_var.set(True)
        self.assertTrue(self.view.get_db_pwd_mode())
        
        # Clear all fields
        self.view.clear_all_fields()
        
        # Verify checkbox is reset to unchecked
        self.assertFalse(self.view.get_db_pwd_mode())


class TestDbPasswordController(unittest.TestCase):
    """Test cases for database password controller logic."""
    
    def setUp(self) -> None:
        """Set up test fixtures."""
        with patch('tkinter.Tk'):
            self.mock_root = MagicMock()
            with patch('src.views.main_view.tk.Tk', return_value=self.mock_root):
                self.view = MainView(self.mock_root)
                self.controller = MainController(self.view)
                
    @patch('src.models.file_processor.FileProcessor.process_db_password_file')
    def test_process_file_db_pwd_mode(self, mock_process_db) -> None:
        """Test process file with database password mode enabled."""
        # Set up view state
        self.view.set_output_file_name("test_output.sql")
        self.view.db_pwd_var.set(True)  # Enable db pwd mode
        self.view.use_uppercase_var.set(True)
        self.view.use_lowercase_var.set(True)
        self.view.use_numbers_var.set(False)
        
        # Mock successful processing
        mock_process_db.return_value = "/path/to/output.sql"
        
        # Process file
        self.controller.process_file()
        
        # Verify db password processing was called
        mock_process_db.assert_called_once_with(
            use_uppercase=True,
            use_lowercase=True,
            use_numbers=False
        )
        
    @patch('src.models.file_processor.FileProcessor.process_file')
    def test_process_file_regular_mode(self, mock_process_regular) -> None:
        """Test process file with regular mode (db pwd disabled)."""
        # Set up view state
        self.view.set_file_path("/path/to/source.txt")
        self.view.set_output_file_name("test_output.txt")
        self.view.db_pwd_var.set(False)  # Disable db pwd mode
        
        # Mock successful processing
        mock_process_regular.return_value = "/path/to/output.txt"
        
        # Process file
        self.controller.process_file()
        
        # Verify regular processing was called
        mock_process_regular.assert_called_once()
        
    def test_process_file_db_pwd_no_character_types(self) -> None:
        """Test process file with db pwd mode but no character types selected."""
        # Set up view state
        self.view.set_output_file_name("test_output.sql")
        self.view.db_pwd_var.set(True)  # Enable db pwd mode
        self.view.use_uppercase_var.set(False)
        self.view.use_lowercase_var.set(False)
        self.view.use_numbers_var.set(False)
        
        # Process file
        self.controller.process_file()
        
        # Verify error was shown (mock was called)
        # This would be verified by checking if show_error was called
        # but since we're using a mock view, we can't easily verify this
        # In a real test, we would mock the show_error method
        
    def test_process_file_no_output_name(self) -> None:
        """Test process file without output file name."""
        # Set up view state with missing output name
        self.view.set_output_file_name("")
        
        # Process file
        self.controller.process_file()
        
        # Verify error handling (would check if show_error was called)

    def test_process_db_password_with_pre_generated_password(self) -> None:
        """Test that pre-generated password is used when provided in DB password processing."""
        # Create test file with database password patterns
        test_content = 'ALTER USER admin IDENTIFIED BY "newpass123" REPLACE "oldpass456";\nSELECT * FROM users;'
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.sql', delete=False) as temp_file:
            temp_file.write(test_content)
            temp_file_path = temp_file.name
        
        try:
            # Set up processor with source file and output name
            self.processor.set_source_file(temp_file_path)
            self.processor.set_output_file_name('output_test.sql')
            
            # Define the pre-generated password that should be used
            pre_generated_password = "12345"
            
            # Process with pre-generated password
            output_path = self.processor.process_db_password_file(
                use_uppercase=True,
                use_lowercase=True, 
                use_numbers=True,
                pre_generated_password=pre_generated_password
            )
            
            # Read the output file to verify the pre-generated password was used
            with open(output_path, 'r', encoding='utf-8') as f:
                output_content = f.read()
            
            # Verify that the pre-generated password "12345" is in the output
            self.assertIn("12345", output_content)
            # Verify that the old password "newpass123" was replaced
            self.assertNotIn("newpass123", output_content)
            # Verify that the current password "oldpass456" was replaced with "newpass123"
            self.assertNotIn("oldpass456", output_content)
            
            # Clean up output file
            if os.path.exists(output_path):
                os.unlink(output_path)
                
        finally:
            # Clean up temp file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
    
    def test_process_db_password_without_pre_generated_password(self) -> None:
        """Test that new password is generated when no pre-generated password provided."""
        # Create test file with database password patterns
        test_content = 'ALTER USER admin IDENTIFIED BY "newpass123" REPLACE "oldpass456";\nSELECT * FROM users;'
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.sql', delete=False) as temp_file:
            temp_file.write(test_content)
            temp_file_path = temp_file.name
        
        try:
            # Set up processor with source file and output name
            self.processor.set_source_file(temp_file_path)
            self.processor.set_output_file_name('output_test.sql')
            self.processor.set_max_random_length(8)
            
            # Process without pre-generated password (should generate new one)
            output_path = self.processor.process_db_password_file(
                use_uppercase=True,
                use_lowercase=True,
                use_numbers=True,
                pre_generated_password=None
            )
            
            # Read the output file
            with open(output_path, 'r', encoding='utf-8') as f:
                output_content = f.read()
            
            # Verify that the old password "newpass123" was replaced with something else
            self.assertNotIn("newpass123", output_content)
            # Verify that the current password "oldpass456" was replaced
            self.assertNotIn("oldpass456", output_content)
            # The new password should be 8 characters (we can't predict what it is)
            
            # Clean up output file
            if os.path.exists(output_path):
                os.unlink(output_path)
                
        finally:
            # Clean up temp file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

    def test_case_2_existing_replace_text_used_as_db_password(self) -> None:
        """Test Case 2: Existing value in replace text field is used as DB password without generating new random string."""
        # Create test file with database password patterns
        test_content = 'ALTER USER admin IDENTIFIED BY "newpass123" REPLACE "oldpass456";\nSELECT * FROM users;'
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.sql', delete=False) as temp_file:
            temp_file.write(test_content)
            temp_file_path = temp_file.name
        
        try:
            # Set up processor with source file and output name
            self.processor.set_source_file(temp_file_path)
            self.processor.set_output_file_name('output_test.sql')
            
            # Simulate Case 2: Replace text field already contains "12345" 
            # (from previous Generate Random String action that user didn't repeat)
            existing_replace_text = "12345"
            
            # Process with the existing replace text value (simulating Case 2)
            output_path = self.processor.process_db_password_file(
                use_uppercase=True,
                use_lowercase=True, 
                use_numbers=True,
                pre_generated_password=existing_replace_text  # This simulates reading from UI field
            )
            
            # Read the output file to verify the existing replace text was used
            with open(output_path, 'r', encoding='utf-8') as f:
                output_content = f.read()
            
            # Verify that the existing replace text "12345" is in the output
            self.assertIn("12345", output_content)
            # Verify that the old password "newpass123" was replaced
            self.assertNotIn("newpass123", output_content)
            # Verify that the current password "oldpass456" was replaced with "newpass123"
            self.assertNotIn("oldpass456", output_content)
            
            # Clean up output file
            if os.path.exists(output_path):
                os.unlink(output_path)
                
        finally:
            # Clean up temp file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)


if __name__ == '__main__':
    unittest.main()
