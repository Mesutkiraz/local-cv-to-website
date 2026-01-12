"""
Local File Service
==================
Concrete implementation of IFileService for local filesystem.
Single Responsibility: Only handles file I/O operations.
"""

from pathlib import Path
from typing import Optional

from src.interfaces.file_service import IFileService
from src.utils.logger import Logger


class LocalFileService(IFileService):
    """
    Local filesystem service implementation.
    Implements IFileService for local file operations.
    """
    
    def __init__(self, output_dir: Path = Path("outputs")):
        """
        Initialize the local file service.
        
        Args:
            output_dir: Default output directory
        """
        self._output_dir = Path(output_dir)
        self._logger = Logger(prefix="FileService")
        self.ensure_directory(self._output_dir)
    
    @property
    def output_directory(self) -> Path:
        """Return the default output directory."""
        return self._output_dir
    
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
            filename: Base filename
            extension: File extension
            directory: Optional directory override
            
        Returns:
            Path to saved file
        """
        target_dir = Path(directory) if directory else self._output_dir
        self.ensure_directory(target_dir)
        
        output_path = target_dir / f"{filename}.{extension}"
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        self._logger.file(f"Saved: {output_path}")
        return output_path
    
    def read(self, file_path: Path) -> str:
        """
        Read content from a file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            File content as string
            
        Raises:
            FileNotFoundError: If file doesn't exist
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    
    def ensure_directory(self, directory: Path) -> Path:
        """
        Ensure directory exists.
        
        Args:
            directory: Directory path
            
        Returns:
            The directory path
        """
        directory = Path(directory)
        directory.mkdir(parents=True, exist_ok=True)
        return directory
