"""
Tkinter UI Service
==================
Concrete implementation of IUIService using tkinter.
Single Responsibility: Only handles tkinter GUI operations.
"""

import os
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
from typing import Optional

from src.interfaces.ui_service import IUIService


class TkinterUIService(IUIService):
    """
    Tkinter-based UI service implementation.
    Implements IUIService for desktop GUI operations.
    """
    
    def select_file(
        self,
        title: str = "Select File",
        filetypes: Optional[list[tuple[str, str]]] = None,
        initial_dir: Optional[Path] = None
    ) -> Optional[Path]:
        """
        Open a file selection dialog.
        
        Args:
            title: Dialog title
            filetypes: List of (description, pattern) tuples
            initial_dir: Starting directory
            
        Returns:
            Selected file path or None if cancelled
        """
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        
        if filetypes is None:
            filetypes = [("All files", "*.*")]
        
        if initial_dir is None:
            initial_dir = Path(os.path.expanduser("~"))
        
        file_path = filedialog.askopenfilename(
            title=title,
            filetypes=filetypes,
            initialdir=str(initial_dir)
        )
        
        root.destroy()
        
        return Path(file_path) if file_path else None
    
    def show_success(self, title: str, message: str) -> None:
        """Display a success message dialog."""
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo(title, message)
        root.destroy()
    
    def show_error(self, title: str, message: str) -> None:
        """Display an error message dialog."""
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(title, message)
        root.destroy()
    
    def show_info(self, title: str, message: str) -> None:
        """Display an informational message dialog."""
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo(title, message)
        root.destroy()
