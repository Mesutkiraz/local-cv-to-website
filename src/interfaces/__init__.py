"""
Interfaces (Abstract Base Classes)
==================================
Defines contracts for dependency injection and extensibility.
Following Interface Segregation Principle (ISP) and Dependency Inversion Principle (DIP).
"""

from src.interfaces.document_extractor import IDocumentExtractor
from src.interfaces.llm_service import ILLMService
from src.interfaces.cv_analyzer import ICVAnalyzer
from src.interfaces.portfolio_generator import IPortfolioGenerator
from src.interfaces.file_service import IFileService
from src.interfaces.ui_service import IUIService

__all__ = [
    "IDocumentExtractor",
    "ILLMService",
    "ICVAnalyzer",
    "IPortfolioGenerator",
    "IFileService",
    "IUIService",
]
