"""
View class for the main GUI interface.
Handles all UI components and user interactions.
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import Optional, Any


class MainView:
    """View class responsible for the GUI interface."""
    
    def __init__(self, root: tk.Tk) -> None:
        """Initialize the main view with GUI components.
        
        Args:
            root (tk.Tk): The root tkinter window.
        """
        self.root = root
        self.root.title("String Replacer - MVC Architecture")
        self.root.geometry("600x380")
        
        # Controller reference (will be set by controller)
        self.controller: Optional[Any] = None
        
        # Create UI components
        self._create_widgets()
        
    def set_controller(self, controller: Any) -> None:
        """Set the controller reference.
        
        Args:
            controller (Any): The controller instance to handle user actions.
        """
        self.controller = controller
        
    def _create_widgets(self) -> None:
        """Create and layout all UI widgets."""
        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        
        # File selection section
        self._create_file_selection_section()
        
        # Find/Replace section
        self._create_find_replace_section()
        
        # Replace Options section
        self._create_replace_options_section()
        
        # File type section
        self._create_file_type_section()
        
        # Output file section
        self._create_output_file_section()
        
        # Action buttons
        self._create_action_buttons()
        
        # Status section
        self._create_status_section()
        
    def _create_file_selection_section(self) -> None:
        """Create file selection UI components."""
        ttk.Label(self.main_frame, text="Source File:").grid(row=0, column=0, sticky=tk.W, pady=2)
        
        self.file_path_var = tk.StringVar()
        self.file_entry = ttk.Entry(self.main_frame, textvariable=self.file_path_var, width=50)
        self.file_entry.grid(row=0, column=1, padx=5, sticky=(tk.W, tk.E))
        
        self.browse_button = ttk.Button(self.main_frame, text="Browse", command=self._on_browse_file)
        self.browse_button.grid(row=0, column=2, padx=5)
        
    def _create_find_replace_section(self) -> None:
        """Create find/replace UI components."""
        ttk.Label(self.main_frame, text="Find:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.find_entry = ttk.Entry(self.main_frame)
        self.find_entry.grid(row=1, column=1, padx=5, sticky=(tk.W, tk.E))
        
        ttk.Label(self.main_frame, text="Replace:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.replace_entry = ttk.Entry(self.main_frame)
        self.replace_entry.grid(row=2, column=1, padx=5, sticky=(tk.W, tk.E))
        
    def _create_replace_options_section(self) -> None:
        """Create Replace Options section with horizontal separators."""
        # Create top horizontal separator
        separator_top = ttk.Separator(self.main_frame, orient='horizontal')
        separator_top.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 5))
        
        # Add section title
        title_label = ttk.Label(self.main_frame, text="Replace Options", font=('TkDefaultFont', 9, 'bold'))
        title_label.grid(row=4, column=0, sticky=tk.W, pady=2)
        
        # Random button (renamed from "Generate Random String")
        self.generate_button = ttk.Button(self.main_frame, text="Random", 
                                        command=self._on_generate_random)
        self.generate_button.grid(row=5, column=0, sticky=tk.W, pady=2)
        
        # Length field (moved to right of Random button, renamed from "Random String Length")
        ttk.Label(self.main_frame, text="Length:").grid(row=5, column=1, sticky=tk.W, padx=(10, 5), pady=2)
        
        self.random_length_var = tk.StringVar(value="10")
        self.random_length_entry = ttk.Entry(self.main_frame, textvariable=self.random_length_var, width=5)
        self.random_length_entry.grid(row=5, column=1, padx=(60, 0), sticky=tk.W, pady=2)
        
        # Character set selection checkboxes (renamed from "Include Characters")
        ttk.Label(self.main_frame, text="Char:").grid(row=6, column=0, sticky=tk.W, pady=2)
        
        # Create frame for checkboxes
        checkbox_frame = ttk.Frame(self.main_frame)
        checkbox_frame.grid(row=6, column=1, columnspan=2, padx=5, sticky=tk.W)
        
        # Checkbox variables (all checked by default)
        self.use_uppercase_var = tk.BooleanVar(value=True)
        self.use_lowercase_var = tk.BooleanVar(value=True)
        self.use_numbers_var = tk.BooleanVar(value=True)
        
        # Create checkboxes
        self.uppercase_cb = ttk.Checkbutton(checkbox_frame, text="UC", 
                                          variable=self.use_uppercase_var)
        self.uppercase_cb.pack(side=tk.LEFT, padx=5)
        
        self.lowercase_cb = ttk.Checkbutton(checkbox_frame, text="lc", 
                                          variable=self.use_lowercase_var)
        self.lowercase_cb.pack(side=tk.LEFT, padx=5)
        
        self.numbers_cb = ttk.Checkbutton(checkbox_frame, text="number", 
                                        variable=self.use_numbers_var)
        self.numbers_cb.pack(side=tk.LEFT, padx=5)
        
        # Create bottom horizontal separator
        separator_bottom = ttk.Separator(self.main_frame, orient='horizontal')
        separator_bottom.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(5, 10))
        
    def _create_file_type_section(self) -> None:
        """Create file type selection UI components."""
        ttk.Label(self.main_frame, text="File Type:").grid(row=8, column=0, sticky=tk.W, pady=2)
        
        # Create frame for file type options
        filetype_frame = ttk.Frame(self.main_frame)
        filetype_frame.grid(row=8, column=1, columnspan=2, padx=5, sticky=tk.W)
        
        # Database password checkbox (unchecked by default)
        self.db_pwd_var = tk.BooleanVar(value=False)
        self.db_pwd_cb = ttk.Checkbutton(filetype_frame, text="db pwd", 
                                       variable=self.db_pwd_var)
        self.db_pwd_cb.pack(side=tk.LEFT, padx=5)
        
    def _create_output_file_section(self) -> None:
        """Create output file UI components."""
        ttk.Label(self.main_frame, text="Output File Name:").grid(row=9, column=0, sticky=tk.W, pady=2)
        self.output_file_entry = ttk.Entry(self.main_frame)
        self.output_file_entry.grid(row=9, column=1, padx=5, sticky=(tk.W, tk.E))
        
    def _create_action_buttons(self) -> None:
        """Create action buttons."""
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=10, column=0, columnspan=3, pady=20)
        
        self.process_button = ttk.Button(button_frame, text="Process File", 
                                       command=self._on_process_file)
        self.process_button.pack(side=tk.LEFT, padx=5)
        
        self.clear_button = ttk.Button(button_frame, text="Clear All", 
                                     command=self._on_clear_all)
        self.clear_button.pack(side=tk.LEFT, padx=5)
        
    def _create_status_section(self) -> None:
        """Create status display section."""
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(self.main_frame, textvariable=self.status_var, 
                                    foreground="blue")
        self.status_label.grid(row=11, column=0, columnspan=3, pady=10)
        
    def _on_browse_file(self) -> None:
        """Handle browse file button click."""
        if self.controller:
            self.controller.browse_file()
            
    def _on_generate_random(self) -> None:
        """Handle generate random string button click."""
        if self.controller:
            self.controller.generate_random_string()
            
    def _on_process_file(self) -> None:
        """Handle process file button click."""
        if self.controller:
            self.controller.process_file()
            
    def _on_clear_all(self) -> None:
        """Handle clear all button click."""
        if self.controller:
            self.controller.clear_all()
    
    # Public methods for controller to interact with view
    def get_file_path(self) -> str:
        """Get the current file path from the entry widget.
        
        Returns:
            str: The current file path.
        """
        return self.file_path_var.get()
        
    def set_file_path(self, path: str) -> None:
        """Set the file path in the entry widget.
        
        Args:
            path (str): The file path to set.
        """
        self.file_path_var.set(path)
        
    def get_find_text(self) -> str:
        """Get the find text from the entry widget.
        
        Returns:
            str: The current find text.
        """
        return self.find_entry.get()
        
    def get_replace_text(self) -> str:
        """Get the replace text from the entry widget.
        
        Returns:
            str: The current replace text.
        """
        return self.replace_entry.get()
        
    def set_replace_text(self, text: str) -> None:
        """Set the replace text in the entry widget.
        
        Args:
            text (str): The replacement text to set.
        """
        self.replace_entry.delete(0, tk.END)
        self.replace_entry.insert(0, text)
        
    def get_random_length(self) -> str:
        """Get the random length from the entry widget.
        
        Returns:
            str: The current random length value as string.
        """
        return self.random_length_var.get()
    
    def get_use_uppercase(self) -> bool:
        """Get the uppercase checkbox state.
        
        Returns:
            bool: True if uppercase checkbox is checked.
        """
        return self.use_uppercase_var.get()
    
    def get_use_lowercase(self) -> bool:
        """Get the lowercase checkbox state.
        
        Returns:
            bool: True if lowercase checkbox is checked.
        """
        return self.use_lowercase_var.get()
    
    def get_use_numbers(self) -> bool:
        """Get the numbers checkbox state.
        
        Returns:
            bool: True if numbers checkbox is checked.
        """
        return self.use_numbers_var.get()
    
    def get_db_pwd_mode(self) -> bool:
        """Get the database password mode checkbox state.
        
        Returns:
            bool: True if db pwd checkbox is checked.
        """
        return self.db_pwd_var.get()
        
    def get_output_file_name(self) -> str:
        """Get the output file name from the entry widget.
        
        Returns:
            str: The current output file name.
        """
        return self.output_file_entry.get()
        
    def set_output_file_name(self, name: str) -> None:
        """Set the output file name in the entry widget.
        
        Args:
            name (str): The output file name to set.
        """
        self.output_file_entry.delete(0, tk.END)
        self.output_file_entry.insert(0, name)
        
    def set_status(self, message: str, color: str = "blue") -> None:
        """Set the status message.
        
        Args:
            message (str): The status message to display.
            color (str): The color for the status text. Defaults to "blue".
        """
        self.status_var.set(message)
        self.status_label.config(foreground=color)
        
    def show_error(self, title: str, message: str) -> None:
        """Show an error message dialog.
        
        Args:
            title (str): The dialog title.
            message (str): The error message to display.
        """
        messagebox.showerror(title, message)
        
    def show_success(self, title: str, message: str) -> None:
        """Show a success message dialog.
        
        Args:
            title (str): The dialog title.
            message (str): The success message to display.
        """
        messagebox.showinfo(title, message)
        
    def show_file_dialog(self) -> str:
        """Show file selection dialog and return selected file path.
        
        Returns:
            str: Path to the selected file, or empty string if cancelled.
        """
        file_path = filedialog.askopenfilename(
            title="Select file to process",
            filetypes=[
                ("Text files", "*.txt"),
                ("All files", "*.*")
            ]
        )
        return file_path
        
    def clear_all_fields(self) -> None:
        """Clear all input fields."""
        self.file_path_var.set("")
        self.find_entry.delete(0, tk.END)
        self.replace_entry.delete(0, tk.END)
        self.random_length_var.set("10")
        self.output_file_entry.delete(0, tk.END)
        
        # Reset checkboxes to default state (all checked for character sets, unchecked for db pwd)
        self.use_uppercase_var.set(True)
        self.use_lowercase_var.set(True)
        self.use_numbers_var.set(True)
        self.db_pwd_var.set(False)
        
        self.set_status("Ready")
