import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import random
import string
import os

class StringReplacer:
    def __init__(self, root):
        self.root = root
        self.root.title("String Replacer")
        
        # Create main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # File selection
        self.file_path = tk.StringVar()
        ttk.Label(self.main_frame, text="Select File:").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(self.main_frame, textvariable=self.file_path, width=50).grid(row=0, column=1, padx=5)
        ttk.Button(self.main_frame, text="Browse", command=self.select_file).grid(row=0, column=2)
        
        # Find and Replace
        ttk.Label(self.main_frame, text="Find:").grid(row=1, column=0, sticky=tk.W)
        self.find_entry = ttk.Entry(self.main_frame)
        self.find_entry.grid(row=1, column=1, padx=5)
        
        ttk.Label(self.main_frame, text="Replace:").grid(row=2, column=0, sticky=tk.W)
        self.replace_entry = ttk.Entry(self.main_frame)
        self.replace_entry.grid(row=2, column=1, padx=5)
        
        # Random String Generation
        ttk.Label(self.main_frame, text="Length:").grid(row=3, column=0, sticky=tk.W)
        self.max_chars = tk.StringVar(value="10")
        ttk.Entry(self.main_frame, textvariable=self.max_chars, width=5).grid(row=3, column=1, padx=5)
        ttk.Button(self.main_frame, text="Random", command=self.generate_random_string).grid(row=3, column=2)
        
        # New File Name
        ttk.Label(self.main_frame, text="New File Name:").grid(row=4, column=0, sticky=tk.W)
        self.new_file_name = ttk.Entry(self.main_frame)
        self.new_file_name.grid(row=4, column=1, padx=5)
        
        # Process Button
        ttk.Button(self.main_frame, text="Process File", command=self.process_file).grid(row=5, column=0, columnspan=3, pady=10)
        
        # Status Label
        self.status_label = ttk.Label(self.main_frame, text="")
        self.status_label.grid(row=6, column=0, columnspan=3, pady=5)
        
    def select_file(self):
        file_path = filedialog.askopenfilename(
            title="Select File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            self.file_path.set(file_path)
            # Set default new file name
            base_name = os.path.basename(file_path)
            name, ext = os.path.splitext(base_name)
            self.new_file_name.delete(0, tk.END)
            self.new_file_name.insert(0, f"{name}_updated{ext}")
            
    def generate_random_string(self):
        try:
            length = int(self.max_chars.get())
            if length > 0:
                random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
                self.replace_entry.delete(0, tk.END)
                self.replace_entry.insert(0, random_string)
            else:
                messagebox.showerror("Error", "Length must be a positive number")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")
        
    def process_file(self):
        if not self.file_path.get():
            messagebox.showerror("Error", "Please select a file first")
            return
            
        if not self.new_file_name.get():
            messagebox.showerror("Error", "Please specify a new file name")
            return
            
        try:
            # Read original file
            with open(self.file_path.get(), 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Perform replacement
            find_text = self.find_entry.get()
            replace_text = self.replace_entry.get()
            new_content = content.replace(find_text, replace_text)
            
            # Write to new file
            new_file_path = os.path.join(os.path.dirname(self.file_path.get()), self.new_file_name.get())
            with open(new_file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
                
            self.status_label.config(text=f"Successfully created: {new_file_name.get()}")
            messagebox.showinfo("Success", f"File has been processed and saved as {new_file_name.get()}")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = StringReplacer(root)
    root.mainloop()
