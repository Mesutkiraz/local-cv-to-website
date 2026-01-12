"""
Document Extractor Interface
============================
Single Responsibility: Define contract for document text extraction.
Open/Closed: Can add new extractors (Word, Image OCR) without modifying existing code.
"""

from abc import ABC, abstractmethod
from pathlib import Path


class IDocumentExtractor(ABC):
    """
    Abstract interface for document text extraction.
    
    Implementations:
    - PDFExtractor: Extracts text from PDF files
    - (Future) WordExtractor: Extracts text from DOCX files
    - (Future) OCRExtractor: Extracts text from images
    """
    
    @abstractmethod
    def extract(self, file_path: Path) -> str:
        """
        Extract text content from a document.
        
        Args:
            file_path: Path to the document file
            
        Returns:
            Extracted text content as string
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file format is not supported
        """
        pass
    
    @abstractmethod
    def supports(self, file_path: Path) -> bool:
        """
        Check if this extractor supports the given file type.
        
        Args:
            file_path: Path to check
            
        Returns:
            True if this extractor can handle the file
        """
        pass
    
    @property
    @abstractmethod
    def supported_extensions(self) -> list[str]:
        """Return list of supported file extensions (e.g., ['.pdf'])."""
        pass
