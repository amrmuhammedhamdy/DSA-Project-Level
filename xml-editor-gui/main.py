#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import sys

# Import your modules from operations folder
from operations import compressor, decompressor, minifier, parser, formatter, converter

class XMLProcessorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("XML Processor")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Variables
        self.input_file = tk.StringVar()
        self.output_file = tk.StringVar()
        
        # Create UI
        self.create_widgets()
        
    def create_widgets(self):
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights for responsiveness
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        # ===== Input File Section =====
        ttk.Label(main_frame, text="Input File:", font=('Arial', 10, 'bold')).grid(
            row=0, column=0, sticky=tk.W, pady=5
        )
        
        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=0, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        input_frame.columnconfigure(0, weight=1)
        
        ttk.Entry(input_frame, textvariable=self.input_file, width=50).grid(
            row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5)
        )
        ttk.Button(input_frame, text="Browse", command=self.browse_input).grid(
            row=0, column=1
        )
        
        # ===== Output File Section =====
        ttk.Label(main_frame, text="Output File:", font=('Arial', 10, 'bold')).grid(
            row=1, column=0, sticky=tk.W, pady=5
        )
        
        output_frame = ttk.Frame(main_frame)
        output_frame.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        output_frame.columnconfigure(0, weight=1)
        
        ttk.Entry(output_frame, textvariable=self.output_file, width=50).grid(
            row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5)
        )
        ttk.Button(output_frame, text="Save As", command=self.browse_output).grid(
            row=0, column=1
        )
        
        # ===== Operation Buttons Section =====
        ttk.Label(main_frame, text="Operations:", font=('Arial', 10, 'bold')).grid(
            row=2, column=0, sticky=tk.W, pady=(15, 5)
        )
        
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=(15, 5))
        
        # Create operation buttons
        operations = [
            ("Verify XML", self.verify_xml),
            ("Fix XML", self.fix_xml),
            ("Format XML", self.format_xml),
            ("Minify XML", self.minify_xml),
            ("Convert to JSON", self.convert_to_json),
            ("Compress", self.compress_file),
            ("Decompress", self.decompress_file),
            ("Clear Output", self.clear_output),
        ]
        
        for idx, (text, command) in enumerate(operations):
            btn = ttk.Button(button_frame, text=text, command=command, width=15)
            btn.grid(row=idx // 3, column=idx % 3, padx=5, pady=5, sticky=(tk.W, tk.E))
            button_frame.columnconfigure(idx % 3, weight=1)
        
        # ===== Output Display Section =====
        ttk.Label(main_frame, text="Output:", font=('Arial', 10, 'bold')).grid(
            row=3, column=0, sticky=tk.W, pady=(15, 5)
        )
        
        # Create scrolled text widget for output
        self.output_text = scrolledtext.ScrolledText(
            main_frame, 
            wrap=tk.WORD, 
            width=80, 
            height=20,
            font=('Courier', 9),
            state='disabled'
        )
        self.output_text.grid(
            row=4, column=0, columnspan=3, 
            sticky=(tk.W, tk.E, tk.N, tk.S), 
            pady=5
        )
        
        # ===== Status Bar =====
        self.status_bar = ttk.Label(
            main_frame, 
            text="Ready", 
            relief=tk.SUNKEN, 
            anchor=tk.W
        )
        self.status_bar.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
    def browse_input(self):
        """Open file dialog to select input file"""
        filename = filedialog.askopenfilename(
            title="Select Input File",
            filetypes=[
                ("XML files", "*.xml"),
                ("JSON files", "*.json"),
                ("Compressed files", "*.gz"),
                ("All files", "*.*")
            ]
        )
        if filename:
            self.input_file.set(filename)
            self.update_status(f"Input file selected: {os.path.basename(filename)}")
            
    def browse_output(self):
        """Open file dialog to select output file location"""
        filename = filedialog.asksaveasfilename(
            title="Save Output As",
            filetypes=[
                ("XML files", "*.xml"),
                ("JSON files", "*.json"),
                ("Compressed files", "*.gz"),
                ("All files", "*.*")
            ]
        )
        if filename:
            self.output_file.set(filename)
            self.update_status(f"Output location set: {os.path.basename(filename)}")
    
    def update_status(self, message):
        """Update status bar message"""
        self.status_bar.config(text=message)
        self.root.update_idletasks()
    
    def append_output(self, text):
        """Append text to the output display"""
        self.output_text.config(state='normal')
        self.output_text.insert(tk.END, text + "\n")
        self.output_text.see(tk.END)
        self.output_text.config(state='disabled')
    
    def clear_output(self):
        """Clear the output display"""
        self.output_text.config(state='normal')
        self.output_text.delete(1.0, tk.END)
        self.output_text.config(state='disabled')
        self.update_status("Output cleared")
    
    def validate_input(self):
        """Validate that input file is specified"""
        if not self.input_file.get():
            messagebox.showerror("Error", "Please select an input file")
            return False
        if not os.path.exists(self.input_file.get()):
            messagebox.showerror("Error", "Input file does not exist")
            return False
        return True
    
    def capture_output(self, func, *args):
        """Capture printed output from functions"""
        import io
        from contextlib import redirect_stdout
        
        output_buffer = io.StringIO()
        with redirect_stdout(output_buffer):
            try:
                func(*args)
            except Exception as e:
                print(f"Error: {str(e)}")
        
        return output_buffer.getvalue()
    
    def verify_xml(self):
        """Verify XML file"""
        if not self.validate_input():
            return
        
        self.update_status("Verifying XML...")
        # Use parser.verify instead of just verify
        output = self.capture_output(parser.verify, self.input_file.get(), self.output_file.get() or None)
        self.append_output("=== Verify XML ===")
        self.append_output(output)
        self.update_status("Verification complete")
    
    def fix_xml(self):
        """Fix XML errors using recovery parser"""
        if not self.validate_input():
            return
        
        # Require output file for fix operation
        if not self.output_file.get():
            # Auto-suggest output filename
            input_path = self.input_file.get()
            base, ext = os.path.splitext(input_path)
            suggested_output = base + "_fixed" + ext
            self.output_file.set(suggested_output)
        
        self.update_status("Fixing XML errors...")
        # Use parser.fix_xml_with_recovery
        output = self.capture_output(
            parser.fix_xml_with_recovery, 
            self.input_file.get(), 
            self.output_file.get()
        )
        self.append_output("=== Fix XML ===")
        if output:
            self.append_output(output)
        else:
            self.append_output(f"XML fixed and saved to: {self.output_file.get()}")
        self.update_status("Fix complete")
    
    def format_xml(self):
        """Format XML file"""
        if not self.validate_input():
            return
        
        self.update_status("Formatting XML...")
        # Use formatter.format_xml
        output = self.capture_output(formatter.format_xml, self.input_file.get(), self.output_file.get() or None)
        self.append_output("=== Format XML ===")
        self.append_output(output)
        self.update_status("Formatting complete")
    
    def minify_xml(self):
        """Minify XML file"""
        if not self.validate_input():
            return
        
        self.update_status("Minifying XML...")
        # Use minifier.minify
        output = self.capture_output(minifier.minify, self.input_file.get(), self.output_file.get() or None)
        self.append_output("=== Minify XML ===")
        self.append_output(output)
        self.update_status("Minification complete")
    
    def convert_to_json(self):
        """Convert XML to JSON"""
        if not self.validate_input():
            return
        
        # Suggest .json extension if no output specified
        output_path = self.output_file.get()
        if not output_path:
            base = os.path.splitext(self.input_file.get())[0]
            output_path = base + ".json"
            self.output_file.set(output_path)
        
        self.update_status("Converting to JSON...")
        # Use converter.xml_to_json
        output = self.capture_output(converter.xml_to_json, self.input_file.get(), output_path)
        self.append_output("=== Convert to JSON ===")
        self.append_output(output)
        self.update_status("Conversion complete")
    
    def compress_file(self):
        """Compress file to .gz"""
        if not self.validate_input():
            return
        
        # Suggest .gz extension if no output specified
        output_path = self.output_file.get()
        if not output_path:
            output_path = self.input_file.get() + ".gz"
            self.output_file.set(output_path)
        
        self.update_status("Compressing file...")
        # Use compressor.compress
        output = self.capture_output(compressor.compress, self.input_file.get(), output_path)
        self.append_output("=== Compress File ===")
        self.append_output(output)
        self.update_status("Compression complete")
    
    def decompress_file(self):
        """Decompress .gz file"""
        if not self.validate_input():
            return
        
        if not self.output_file.get():
            messagebox.showerror("Error", "Please specify an output file for decompression")
            return
        
        self.update_status("Decompressing file...")
        # Use decompressor.decompress
        output = self.capture_output(decompressor.decompress, self.input_file.get(), self.output_file.get())
        self.append_output("=== Decompress File ===")
        self.append_output(output)
        self.update_status("Decompression complete")

def main():
    root = tk.Tk()
    app = XMLProcessorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()