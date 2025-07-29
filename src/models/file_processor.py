"""
Model class for file processing operations.
Handles all business logic for string replacement and file operations.
"""
import os
import random
import string
import re
from datetime import datetime
from typing import Optional, Dict, Any, Tuple
from pydantic import BaseModel, validator


class FileProcessorConfig(BaseModel):
    """Configuration model for file processor validation."""
    source_file_path: str = ""
    find_text: str = ""
    replace_text: str = ""
    output_file_name: str = ""
    max_random_length: int = 10
    
    @validator('max_random_length')
    def validate_max_random_length(cls, v: int) -> int:
        """Validate that max_random_length is positive.
        
        Args:
            v (int): The max random length value to validate.
            
        Returns:
            int: The validated max random length.
            
        Raises:
            ValueError: If length is not positive.
        """
        if v <= 0:
            raise ValueError("Length must be a positive number")
        return v


class FileProcessor:
    """Model class responsible for file processing operations."""
    
    def __init__(self) -> None:
        """Initialize FileProcessor with default configuration."""
        self.config = FileProcessorConfig()
    
    def set_source_file(self, file_path: str) -> None:
        """Set the source file path.
        
        Args:
            file_path (str): Path to the source file to process.
            
        Raises:
            FileNotFoundError: If the specified file does not exist.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        self.config.source_file_path = file_path
    
    def set_find_replace_text(self, find_text: str, replace_text: str) -> None:
        """Set the find and replace text.
        
        Args:
            find_text (str): Text to search for in the file.
            replace_text (str): Text to replace the found text with.
        """
        self.config.find_text = find_text
        self.config.replace_text = replace_text
    
    def set_output_file_name(self, output_file_name: str) -> None:
        """Set the output file name.
        
        Args:
            output_file_name (str): Name for the output file.
        """
        self.config.output_file_name = output_file_name
    
    def set_max_random_length(self, length: int) -> None:
        """Set maximum length for random string generation.
        
        Args:
            length (int): Maximum length for generated random strings.
            
        Raises:
            ValueError: If length is not positive.
        """
        # Reason: Using pydantic validation through config update
        self.config.max_random_length = length
    
    def generate_random_string(
        self, 
        length: Optional[int] = None, 
        use_uppercase: bool = True,
        use_lowercase: bool = True,
        use_numbers: bool = True
    ) -> str:
        """Generate a random string of specified length with customizable character sets.
        
        Args:
            length (Optional[int]): Length of random string to generate.
                                  If None, uses max_random_length.
            use_uppercase (bool): Include uppercase letters. Defaults to True.
            use_lowercase (bool): Include lowercase letters. Defaults to True.
            use_numbers (bool): Include numbers. Defaults to True.
                                  
        Returns:
            str: Generated random string containing specified character types.
            
        Raises:
            ValueError: If length is not positive or no character sets selected.
        """
        if length is None:
            length = self.config.max_random_length
        
        if length <= 0:
            raise ValueError("Length must be a positive number")
        
        # Build character set based on selections
        char_set = ""
        if use_uppercase:
            char_set += string.ascii_uppercase
        if use_lowercase:
            char_set += string.ascii_lowercase
        if use_numbers:
            char_set += string.digits
        
        if not char_set:
            raise ValueError("At least one character type must be selected")
        
        # Reason: Using customizable character sets for flexible random string generation
        return ''.join(random.choices(char_set, k=length))
    
    def get_default_output_name(self) -> str:
        """Generate a default output file name based on source file with today's date.
        
        Returns:
            str: Default output filename with '_yyyy_mm_dd' suffix, or empty string
                if no source file is set.
        """
        if not self.config.source_file_path:
            return ""
        
        base_name = os.path.basename(self.config.source_file_path)
        name, ext = os.path.splitext(base_name)
        
        # Get today's date in yyyy_mm_dd format
        today = datetime.now().strftime("%Y_%m_%d")
        
        return f"{name}_{today}{ext}"
    
    def process_file(self) -> str:
        """Process the file with find/replace operations.
        
        Returns:
            str: Path to the created output file.
            
        Raises:
            ValueError: If source file or output file name not specified.
            IOError: If file reading or writing fails.
        """
        if not self.config.source_file_path:
            raise ValueError("No source file specified")
        
        if not self.config.output_file_name:
            raise ValueError("No output file name specified")
        
        # Read source file
        try:
            with open(self.config.source_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            raise IOError(f"Error reading source file: {str(e)}")
        
        # Perform replacement
        if self.config.find_text:
            # Reason: Only perform replacement if find_text is not empty
            content = content.replace(self.config.find_text, self.config.replace_text)
        
        # Write to output file
        output_path = os.path.join(
            os.path.dirname(self.config.source_file_path), 
            self.config.output_file_name
        )
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            raise IOError(f"Error writing output file: {str(e)}")
        
        return output_path
    
    def extract_db_passwords_from_first_line(self, content: str) -> Tuple[Optional[str], Optional[str]]:
        """Extract database passwords from the first line of content.
        
        Looks for patterns like:
        - 'BY "password"' -> new password
        - 'REPLACE "password"' -> current password
        
        Args:
            content (str): File content to parse.
            
        Returns:
            Tuple[Optional[str], Optional[str]]: (new_password, current_password)
                Returns (None, None) if patterns not found.
        """
        if not content.strip():
            return None, None
            
        first_line = content.split('\n')[0]
        
        # Extract password after "BY" (new password)
        by_pattern = r'BY\s+"([^"]+)"'
        by_match = re.search(by_pattern, first_line, re.IGNORECASE)
        new_password = by_match.group(1) if by_match else None
        
        # Extract password after "REPLACE" (current password)
        replace_pattern = r'REPLACE\s+"([^"]+)"'
        replace_match = re.search(replace_pattern, first_line, re.IGNORECASE)
        current_password = replace_match.group(1) if replace_match else None
        
        return new_password, current_password
    
    def process_db_password_file(
        self,
        use_uppercase: bool = True,
        use_lowercase: bool = True,
        use_numbers: bool = True
    ) -> str:
        """Process file with database password replacement logic.
        
        Extracts passwords from first line, generates new passwords,
        and performs replacements throughout the file.
        
        Args:
            use_uppercase (bool): Include uppercase in generated password.
            use_lowercase (bool): Include lowercase in generated password.
            use_numbers (bool): Include numbers in generated password.
            
        Returns:
            str: Path to the created output file.
            
        Raises:
            ValueError: If source file, output file name not specified,
                       or no passwords found in first line.
            IOError: If file reading or writing fails.
        """
        if not self.config.source_file_path:
            raise ValueError("No source file specified")
        
        if not self.config.output_file_name:
            raise ValueError("No output file name specified")
        
        # Read source file
        try:
            with open(self.config.source_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            raise IOError(f"Error reading source file: {str(e)}")
        
        # Extract passwords from first line
        str_sel_file_new_pw, str_sel_file_cur_pw = self.extract_db_passwords_from_first_line(content)
        
        if not str_sel_file_new_pw or not str_sel_file_cur_pw:
            raise ValueError("Could not find password patterns in first line. Expected 'BY \"password\"' and 'REPLACE \"password\"' patterns.")
        
        # Generate new passwords
        str_updated_file_new_pw = self.generate_random_string(
            length=self.config.max_random_length,
            use_uppercase=use_uppercase,
            use_lowercase=use_lowercase,
            use_numbers=use_numbers
        )
        str_updated_file_cur_pw = str_sel_file_new_pw
        
        # Perform replacements
        # Reason: Replace all instances of old passwords with new ones
        updated_content = content.replace(str_sel_file_new_pw, str_updated_file_new_pw)
        updated_content = updated_content.replace(str_sel_file_cur_pw, str_updated_file_cur_pw)
        
        # Write to output file
        output_path = os.path.join(
            os.path.dirname(self.config.source_file_path), 
            self.config.output_file_name
        )
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
        except Exception as e:
            raise IOError(f"Error writing output file: {str(e)}")
        
        return output_path
    
    def get_file_info(self) -> Dict[str, Any]:
        """Get information about the current file configuration.
        
        Returns:
            Dict[str, Any]: Dictionary containing current configuration values.
        """
        return {
            'source_file': self.config.source_file_path,
            'find_text': self.config.find_text,
            'replace_text': self.config.replace_text,
            'output_file': self.config.output_file_name,
            'max_random_length': self.config.max_random_length
        }
