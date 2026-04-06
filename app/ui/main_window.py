# app/ui/main_window.py

import os
import csv
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import threading
import queue
import platform  # To check the operating system

# Import our separated components
from app.utils.config import FILE_TYPES
from app.search.search_worker import SearchWorker

# Try to import psutil for the Windows Search check
try:
    import psutil
except ImportError:
    psutil = None

class FileSearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced File Search")
        self.root.geometry("800x600")

        self.found_files = []
        self.search_thread = None
        self.cancel_search_event = threading.Event()

        # Check for necessary libraries on startup
        try:
            import PyPDF2, docx, openpyxl
        except ImportError:
            messagebox.showerror("Missing Libraries", "Please install required libraries:\npip install PyPDF2 python-docx openpyxl")
            self.root.destroy()
            return

        self._create_widgets()
        self._check_windows_search_status()

    def _create_widgets(self):
        # Main content frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # --- Directory Selection ---
        dir_frame = ttk.LabelFrame(main_frame, text="1. Select a folder to search")
        dir_frame.pack(pady=5, fill="x")
        browse_button = ttk.Button(dir_frame, text="Browse...", command=self.browse_directory)
        browse_button.pack(side="left", padx=5, pady=5)
        self.selected_dir_label = ttk.Label(dir_frame, text="No folder selected")
        self.selected_dir_label.pack(side="left", padx=5, pady=5)

        # --- Search Criteria ---
        search_frame = ttk.LabelFrame(main_frame, text="2. Define search criteria")
        search_frame.pack(pady=5, fill="x")
        ttk.Label(search_frame, text="Search for:").pack(side="left", padx=5, pady=5)
        self.search_entry = ttk.Entry(search_frame, width=30)
        self.search_entry.pack(side="left", padx=5, pady=5, fill="x", expand=True)
        self.search_type_var = tk.StringVar(value="filename")
        ttk.Radiobutton(search_frame, text="File Name", variable=self.search_type_var, value="filename").pack(side="left", padx=5)
        ttk.Radiobutton(search_frame, text="File Content", variable=self.search_type_var, value="content").pack(side="left", padx=5)

        # --- File Type Selection ---
        self.types_frame = ttk.LabelFrame(main_frame, text="3. Select file types")
        self.types_frame.pack(pady=5, fill="x")
        self.file_type_vars = {}
        for i, (label, _) in enumerate(FILE_TYPES.items()):
            var = tk.BooleanVar()
            cb = ttk.Checkbutton(self.types_frame, text=label, variable=var, command=self.on_file_type_select)
            cb.grid(row=i // 4, column=i % 4, sticky="w", padx=5, pady=2)
            self.file_type_vars[label] = var
        self.file_type_vars["All Files"].set(True)
        self.on_file_type_select()

        # --- Action Buttons ---
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(pady=10, fill="x")
        self.search_button = ttk.Button(action_frame, text="Search", command=self.start_search)
        self.search_button.pack(side="left")
        self.cancel_button = ttk.Button(action_frame, text="Cancel", command=self.cancel_search, state="disabled")
        self.cancel_button.pack(side="left", padx=5)
        self.export_button = ttk.Button(action_frame, text="Export Results...", command=self.export_results, state="disabled")
        self.export_button.pack(side="right")
        
        # --- Results Display ---
        results_frame = ttk.LabelFrame(main_frame, text="Results")
        results_frame.pack(fill="both", expand=True)
        self.results_listbox = tk.Listbox(results_frame)
        self.results_listbox.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.results_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.results_listbox.config(yscrollcommand=scrollbar.set)
        
        # --- Status Bar ---
        status_bar = ttk.Frame(self.root, relief="sunken")
        status_bar.pack(side="bottom", fill="x")
        
        self.results_count_var = tk.StringVar(value="Results: 0")
        results_count_label = ttk.Label(status_bar, textvariable=self.results_count_var)
        results_count_label.pack(side="left", padx=5)

        self.win_search_status_var = tk.StringVar(value="")
        win_search_status_label = ttk.Label(status_bar, textvariable=self.win_search_status_var)
        win_search_status_label.pack(side="right", padx=5)

    def _check_windows_search_status(self):
        """Checks if the Windows Search service is running and updates the status bar."""
        if platform.system() != "Windows":
            self.win_search_status_var.set("N/A on this OS")
            return
        
        if not psutil:
            self.win_search_status_var.set("Windows Search: `psutil` not installed")
            return

        try:
            service = psutil.win_service_get('WSearch')
            if service.status() == 'running':
                self.win_search_status_var.set("Windows Search: Available")
            else:
                self.win_search_status_var.set("Windows Search: Not Running")
        except psutil.NoSuchProcess:
            self.win_search_status_var.set("Windows Search: Not Found")

    def start_search(self):
        # ... (rest of the function is the same, but we add counter reset)
        if not hasattr(self, 'directory'):
            messagebox.showwarning("No Directory", "Please select a directory first.")
            return
        keyword = self.search_entry.get()
        if not keyword:
            messagebox.showwarning("No Keyword", "Please enter a search term.")
            return

        self.search_button.config(state="disabled")
        self.cancel_button.config(state="normal")
        self.export_button.config(state="disabled")
        self.results_listbox.delete(0, tk.END)
        self.results_listbox.insert(tk.END, "Searching, please wait...")
        self.found_files.clear()
        self.results_count_var.set("Results: 0") # Reset counter
        self.cancel_search_event.clear()

        self.result_queue = queue.Queue()
        worker = SearchWorker(
            directory=self.directory,
            keyword=keyword,
            extensions=self.get_selected_extensions(),
            search_mode=self.search_type_var.get(),
            result_queue=self.result_queue,
            cancel_event=self.cancel_search_event
        )
        self.search_thread = threading.Thread(target=worker.run)
        self.search_thread.start()
        self.root.after(100, self.process_queue)
    
    def process_queue(self):
        try:
            while True:
                msg = self.result_queue.get_nowait()
                if msg in ("FINISHED", "CANCELLED"):
                    self.search_finished(cancelled=(msg == "CANCELLED"))
                    return
                else: # It's a file path
                    if self.results_listbox.get(0) == "Searching, please wait...":
                        self.results_listbox.delete(0, tk.END)
                    self.results_listbox.insert(tk.END, msg)
                    self.found_files.append(msg)
                    # Update the counter as results come in
                    self.results_count_var.set(f"Results: {len(self.found_files)}")
        except queue.Empty:
            if self.search_thread.is_alive():
                self.root.after(100, self.process_queue)
            else:
                self.search_finished()

    # --- Other functions (browse_directory, on_file_type_select, etc.) remain unchanged ---
    
    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.directory = directory
            self.selected_dir_label.config(text=self.directory)

    def on_file_type_select(self):
        is_all_checked = self.file_type_vars["All Files"].get()
        state = "disabled" if is_all_checked else "normal"
        for label, _ in self.file_type_vars.items():
            if label != "All Files":
                for child in self.types_frame.winfo_children():
                    if child.cget("text") == label:
                        child.config(state=state)

    def get_selected_extensions(self):
        if self.file_type_vars["All Files"].get():
            return ["*"]
        selected_extensions = [
            ext for label, var in self.file_type_vars.items() if var.get() 
            for ext in (FILE_TYPES.get(label) if isinstance(FILE_TYPES.get(label), list) else [FILE_TYPES.get(label)])
        ]
        return list(set(selected_extensions) - {'*'})

    def cancel_search(self):
        if self.search_thread and self.search_thread.is_alive():
            self.cancel_search_event.set()
            self.cancel_button.config(text="Cancelling...", state="disabled")

    def search_finished(self, cancelled=False):
        self.search_button.config(state="normal")
        self.cancel_button.config(text="Cancel", state="disabled")
        if self.found_files:
            self.export_button.config(state="normal")
        if self.results_listbox.get(0) == "Searching, please wait...":
            self.results_listbox.delete(0, tk.END)
        if cancelled:
            self.results_listbox.insert(tk.END, "--- Search Cancelled ---")
        elif not self.found_files:
            self.results_listbox.insert(tk.END, "No matching files found.")
        self.results_listbox.yview_moveto(1.0)

    def export_results(self):
        if not self.found_files:
            messagebox.showinfo("No Results", "There are no results to export.")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV file", "*.csv"), ("Text file", "*.txt")]
        )

        if not file_path:
            return

        try:
            # --- CSV EXPORT LOGIC ---
            if file_path.endswith('.csv'):
                # The 'newline=""' argument prevents blank rows between entries.
                with open(file_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    
                    # 1. Write the header as a single row.
                    writer.writerow(["File Path"])
                    
                    # 2. Use writerows to write each path as a new, separate row.
                    # This list comprehension formats the data correctly for writerows.
                    writer.writerows([[path] for path in self.found_files])

            # --- TXT EXPORT LOGIC ---
            else:
                with open(file_path, 'w', encoding='utf-8') as f:
                    # This generator expression adds a newline character after each path
                    # and writelines() writes each one to the file.
                    f.writelines(f"{path}\n" for path in self.found_files)
            
            messagebox.showinfo("Export Successful", f"Results successfully exported to {os.path.basename(file_path)}")
        except Exception as e:
            messagebox.showerror("Export Error", f"An error occurred during export: {e}")
