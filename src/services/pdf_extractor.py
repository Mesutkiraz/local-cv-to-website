"""
PDF Extractor Service
=====================
Concrete implementation of IDocumentExtractor for PDF files.
Single Responsibility: Only handles PDF text extraction.
"""

from pathlib import Path

import pdfplumber

from src.interfaces.document_extractor import IDocumentExtractor
from src.utils.logger import Logger


class PDFExtractor(IDocumentExtractor):
    """
    PDF document text extractor using pdfplumber.
    Implements IDocumentExtractor for PDF files.
    """
    
    def __init__(self):
        """Initialize the PDF extractor."""
        self._logger = Logger(prefix="PDFExtractor")
        self._supported_extensions = [".pdf"]
    
    def extract(self, file_path: Path) -> str:
        """
        Extract all text content from a PDF file.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Extracted text content
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file is not a PDF
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"PDF file not found: {file_path}")
        
        if not self.supports(file_path):
            raise ValueError(f"Unsupported file type: {file_path.suffix}")
        
        self._logger.file(f"Extracting text from: {file_path.name}")
        
        full_text = []
        with pdfplumber.open(file_path) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text:
                    full_text.append(text)
        
        extracted = "\n\n".join(full_text)
        word_count = len(extracted.split())
        self._logger.success(f"Extracted {word_count} words from {len(full_text)} pages")
        
        return extracted
    
    def supports(self, file_path: Path) -> bool:
        """
        Check if this extractor supports the given file.
        
        Args:
            file_path: Path to check
            
        Returns:
            True if file is a PDF
        """
        return Path(file_path).suffix.lower() in self._supported_extensions
    
    @property
    def supported_extensions(self) -> list[str]:
        """Return list of supported extensions."""
        return self._supported_extensions.copy()
