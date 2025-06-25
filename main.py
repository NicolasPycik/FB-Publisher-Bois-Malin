#!/usr/bin/env python3
"""
Facebook Publisher Bois Malin - Launcher Script

This script launches the Facebook Publisher Bois Malin application.
It handles the GUI initialization and error handling.

Usage:
    python main.py

Author: Manus AI
Date: June 19, 2025
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from FacebookPublisherBoisMalin import FacebookPublisherApp
except ImportError as e:
    print(f"Error importing application: {e}")
    print("Please make sure all dependencies are installed:")
    print("pip install -r requirements.txt")
    sys.exit(1)

def main():
    """Main entry point for the application"""
    try:
        # Create the main window
        root = tk.Tk()
        
        # Initialize the application
        app = FacebookPublisherApp(root)
        
        # Start the GUI event loop
        root.mainloop()
        
    except Exception as e:
        # Show error dialog if GUI fails to start
        try:
            messagebox.showerror("Application Error", f"Failed to start application:\n{str(e)}")
        except:
            print(f"Failed to start application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

