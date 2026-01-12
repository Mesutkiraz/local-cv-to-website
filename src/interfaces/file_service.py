"""
File Service Interface
======================
Single Responsibility: Define contract for file operations.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional


class IFileService(ABC):
    """
    Abstract interface for file operations.
    
    Implementations:
    - LocalFileService: Handles local filesystem operations
    - (Future) CloudFileService: Handles cloud storage operations
    """
    
    @abstractmethod
    def save(
        self,
        content: str,
        filename: str,
        extension: str = "html",
        directory: Optional[Path] = None
    ) -> Path:
        """
        Save content to a file.
        
        Args:
            content: Content to save
            filename: Base filename (without extension)
            extension: File extension
            directory: Optional directory override
            
        Returns:
            Path to saved file
        """
        pass
    
    @abstractmethod
    def read(self, file_path: Path) -> str:
        """
        Read content from a file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            File content as string
        """
        pass
    
    @abstractmethod
    def ensure_directory(self, directory: Path) -> Path:
        """
        Ensure a directory exists, creating it if necessary.
        
        Args:
            directory: Directory path
            
        Returns:
            The directory path
        """
        pass
    
    @property
    @abstractmethod
    def output_directory(self) -> Path:
        """Return the default output directory."""
        pass
