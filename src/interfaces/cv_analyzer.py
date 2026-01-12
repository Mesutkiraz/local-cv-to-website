"""
CV Analyzer Interface
=====================
Single Responsibility: Define contract for CV analysis and data extraction.
Liskov Substitution: Any analyzer implementation can be used interchangeably.
"""

from abc import ABC, abstractmethod
from src.models.cv_data import CVData


class ICVAnalyzer(ABC):
    """
    Abstract interface for CV analysis.
    
    Implementations:
    - DeepSeekAnalyzer: Uses DeepSeek-R1 for deep reasoning
    - (Future) GPT4Analyzer: Uses GPT-4 for analysis
    """
    
    @abstractmethod
    def analyze(self, cv_text: str) -> CVData:
        """
        Analyze CV text and extract structured data.
        
        Args:
            cv_text: Raw text extracted from CV document
            
        Returns:
            CVData model with structured information
            
        Raises:
            AnalysisError: If analysis fails
        """
        pass
    
    @property
    @abstractmethod
    def model_name(self) -> str:
        """Return the name of the model being used for analysis."""
        pass
