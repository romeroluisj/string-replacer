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
            file_path = self.view.get_file_path()
            find_text = self.view.get_find_text()
            replace_text = self.view.get_replace_text()
            output_name = self.view.get_output_file_name()
            
            # Validate inputs
            if not file_path:
                self.view.show_error("Missing Input", "Please select a source file")
                return
                
            if not output_name:
                self.view.show_error("Missing Input", "Please specify an output file name")
                return
                
            if not find_text and not replace_text:
                self.view.show_error("Missing Input", "Please specify text to find or replace")
                return
            
            # Update model with current data
            self.model.set_source_file(file_path)
            self.model.set_find_replace_text(find_text, replace_text)
            self.model.set_output_file_name(output_name)
            
            # Process the file
            self.view.set_status("Processing file...", "orange")
            output_path = self.model.process_file()
            
            # Show success
            success_msg = f"File processed successfully!\nOutput saved as: {output_name}"
            self.view.show_success("Success", success_msg)
            self.view.set_status(f"File processed: {output_name}", "green")
            
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
