#!/usr/bin/env python3
"""
Main entry point for the String Replacer application.
This file initializes the MVC components and starts the application.
"""
import tkinter as tk
import sys
import os

# Add src directory to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.views import MainView
from src.controllers import MainController


class StringReplacerApp:
    """Main application class that initializes and runs the String Replacer."""
    
    def __init__(self) -> None:
        """Initialize the application with MVC components."""
        # Create root window
        self.root = tk.Tk()
        
        # Initialize MVC components
        self.view = MainView(self.root)
        self.controller = MainController(self.view)
        
        # Configure window properties
        self._configure_window()
        
    def _configure_window(self) -> None:
        """Configure main window properties."""
        # Center the window on screen
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        # Set minimum window size
        self.root.minsize(500, 250)
        
        # Configure window closing behavior
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
        
    def _on_closing(self) -> None:
        """Handle application closing."""
        self.root.quit()
        self.root.destroy()
        
    def run(self) -> None:
        """Start the application main loop."""
        try:
            print("Starting String Replacer Application...")
            print("Architecture: MVC (Model-View-Controller)")
            print("GUI Framework: tkinter")
            self.root.mainloop()
        except KeyboardInterrupt:
            print("\nApplication interrupted by user")
        except Exception as e:
            print(f"Application error: {e}")
        finally:
            print("Application closed")


def main() -> None:
    """Main function to run the application."""
    app = StringReplacerApp()
    app.run()


if __name__ == "__main__":
    main()
