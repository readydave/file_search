# main.py

"""
Main entry point for the File Search application.

This script initializes the Tkinter root window and creates an
instance of the main application class from app/ui/main_window.py.
"""

import tkinter as tk
from app.ui.main_window import FileSearchApp

if __name__ == "__main__":
    # Create the main Tkinter window
    root = tk.Tk()

    # Create an instance of our main application class
    app = FileSearchApp(root)

    # Start the Tkinter event loop
    root.mainloop()
