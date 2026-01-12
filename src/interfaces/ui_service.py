"""
UI Service Interface
====================
Single Responsibility: Define contract for user interface operations.
Open/Closed: Can add new UI implementations (CLI, Web) without modifying existing code.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional


class IUIService(ABC):
    """
    Abstract interface for user interface operations.
    
    Implementations:
    - TkinterUIService: Desktop GUI using tkinter
    - (Future) CLIUIService: Command-line interface
    - (Future) WebUIService: Web-based interface
    """
    
    @abstractmethod
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
        pass
    
    @abstractmethod
    def show_success(self, title: str, message: str) -> None:
        """
        Display a success message to the user.
        
        Args:
            title: Message title
            message: Message content
        """
        pass
    
    @abstractmethod
    def show_error(self, title: str, message: str) -> None:
        """
        Display an error message to the user.
        
        Args:
            title: Error title
            message: Error content
        """
        pass
    
    @abstractmethod
    def show_info(self, title: str, message: str) -> None:
        """
        Display an informational message to the user.
        
        Args:
            title: Message title
            message: Message content
        """
        pass
