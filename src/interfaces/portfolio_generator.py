"""
Portfolio Generator Interface
=============================
Single Responsibility: Define contract for portfolio HTML generation.
Open/Closed: Can add new themes/styles without modifying existing code.
"""

from abc import ABC, abstractmethod
from src.models.cv_data import CVData


class IPortfolioGenerator(ABC):
    """
    Abstract interface for portfolio generation.
    
    Implementations:
    - QwenPortfolioGenerator: Uses Qwen2.5-Coder for HTML generation
    - (Future) TemplateGenerator: Uses HTML templates instead of LLM
    """
    
    @abstractmethod
    def generate(self, cv_data: CVData, original_cv_text: str = "") -> str:
        """
        Generate portfolio HTML from CV data.
        
        Args:
            cv_data: Structured CV data
            original_cv_text: Original CV text for validation
            
        Returns:
            Complete HTML string for the portfolio
            
        Raises:
            GenerationError: If generation fails
        """
        pass
    
    @property
    @abstractmethod
    def model_name(self) -> str:
        """Return the name of the model being used for generation."""
        pass
    
    @abstractmethod
    def apply_fixes(self, html: str) -> str:
        """
        Apply post-processing fixes to generated HTML.
        
        Args:
            html: Raw generated HTML
            
        Returns:
            Fixed HTML with all necessary patches applied
        """
        pass
