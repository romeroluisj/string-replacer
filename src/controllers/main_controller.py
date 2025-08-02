"""
Controller class that coordinates between Model and View.
Handles user interactions and business logic coordination.
"""
from typing import Dict, Any
from src.models import FileProcessor
from src.views import MainView


class MainController:
    """Controller class that manages the interaction between Model and View."""
    
    def __init__(self, view: MainView) -> None:
        """Initialize the controller with view and model instances.
        
        Args:
            view (MainView): The view instance to control.
        """
        self.view = view
        self.model = FileProcessor()
        
        # Set controller reference in view
        self.view.set_controller(self)
        
    def browse_file(self) -> None:
        """Handle file browsing request."""
        try:
            file_path = self.view.show_file_dialog()
            if file_path:
                self.model.set_source_file(file_path)
                self.view.set_file_path(file_path)
                
                # Auto-generate default output file name
                default_name = self.model.get_default_output_name()
                self.view.set_output_file_name(default_name)
                
                self.view.set_status(f"File selected: {file_path}")
                
        except Exception as e:
            self.view.show_error("File Selection Error", str(e))
            self.view.set_status("Error selecting file", "red")
            
    def generate_random_string(self) -> None:
        """Handle random string generation request."""
        try:
            length_str = self.view.get_random_length()
            length = int(length_str)
            
            # Get checkbox states for character set selection
            use_uppercase = self.view.get_use_uppercase()
            use_lowercase = self.view.get_use_lowercase()
            use_numbers = self.view.get_use_numbers()
            
            # Validate that at least one character type is selected
            if not (use_uppercase or use_lowercase or use_numbers):
                self.view.show_error("Selection Error", "Please select at least one character type (UC, lc, or number)")
                self.view.set_status("Error: No character types selected", "red")
                return
            
            self.model.set_max_random_length(length)
            random_string = self.model.generate_random_string(
                length=length,
                use_uppercase=use_uppercase,
                use_lowercase=use_lowercase,
                use_numbers=use_numbers
            )
            
            self.view.set_replace_text(random_string)
            
            # Build status message with selected character types
            char_types = []
            if use_uppercase:
                char_types.append("UC")
            if use_lowercase:
                char_types.append("lc")
            if use_numbers:
                char_types.append("numbers")
            
            char_types_str = ", ".join(char_types)
            self.view.set_status(f"Generated random string of length {length} with {char_types_str}")
            
        except ValueError as e:
            if "invalid literal" in str(e):
                self.view.show_error("Invalid Input", "Please enter a valid number for string length")
            else:
                self.view.show_error("Generation Error", str(e))
            self.view.set_status("Error generating random string", "red")
            
    def process_file(self) -> None:
        """Handle file processing request."""
        try:
            # Get data from view
            find_text = self.view.get_find_text()
            replace_text = self.view.get_replace_text()
            output_file_name = self.view.get_output_file_name()
            db_pwd_mode = self.view.get_db_pwd_mode()
            
            # Validate required fields
            if not output_file_name:
                self.view.show_error("Validation Error", "Please specify an output file name")
                self.view.set_status("Error: No output file name", "red")
                return
            
            # Set model data
            self.model.set_find_replace_text(find_text, replace_text)
            self.model.set_output_file_name(output_file_name)
            
            # Check if database password mode is enabled
            if db_pwd_mode:
                # Process with database password logic
                use_uppercase = self.view.get_use_uppercase()
                use_lowercase = self.view.get_use_lowercase()
                use_numbers = self.view.get_use_numbers()
                
                # Validate that at least one character type is selected
                if not (use_uppercase or use_lowercase or use_numbers):
                    self.view.show_error("Selection Error", "Please select at least one character type (UC, lc, or number) for password generation")
                    self.view.set_status("Error: No character types selected", "red")
                    return
                
                # Check if there's a pre-generated password in the replace text field
                pre_generated_password = replace_text.strip() if replace_text.strip() else None
                
                output_path = self.model.process_db_password_file(
                    use_uppercase=use_uppercase,
                    use_lowercase=use_lowercase,
                    use_numbers=use_numbers,
                    pre_generated_password=pre_generated_password
                )
                
                # Show success message for database password processing
                char_types = []
                if use_uppercase:
                    char_types.append("UC")
                if use_lowercase:
                    char_types.append("lc")
                if use_numbers:
                    char_types.append("numbers")
                
                char_types_str = ", ".join(char_types)
                self.view.show_success("Database Password Processing Complete", 
                                     f"Database passwords updated successfully!\n"
                                     f"New passwords generated with: {char_types_str}\n"
                                     f"Output saved to: {output_path}")
                self.view.set_status(f"DB passwords processed: {output_path}", "green")
            else:
                # Process with regular find/replace logic
                file_path = self.view.get_file_path()
                self.model.set_source_file(file_path)
                output_path = self.model.process_file()
                
                # Show success message for regular processing
                self.view.show_success("Success", f"File processed successfully!\nOutput saved to: {output_path}")
                self.view.set_status(f"File processed: {output_path}", "green")
            
        except FileNotFoundError as e:
            self.view.show_error("File Not Found", str(e))
            self.view.set_status("File not found", "red")
            
        except ValueError as e:
            self.view.show_error("Invalid Input", str(e))
            self.view.set_status("Invalid input", "red")
            
        except IOError as e:
            self.view.show_error("File Operation Error", str(e))
            self.view.set_status("File operation failed", "red")
            
        except Exception as e:
            self.view.show_error("Unexpected Error", f"An unexpected error occurred: {str(e)}")
            self.view.set_status("Unexpected error", "red")
            
    def clear_all(self) -> None:
        """Handle clear all fields request."""
        try:
            self.view.clear_all_fields()
            
            # Reset model
            self.model = FileProcessor()
            
            self.view.set_status("All fields cleared")
            
        except Exception as e:
            self.view.show_error("Clear Error", f"Error clearing fields: {str(e)}")
            
    def get_model_info(self) -> Dict[str, Any]:
        """Get current model information for debugging.
        
        Returns:
            Dict[str, Any]: Dictionary containing current model configuration.
        """
        return self.model.get_file_info()
