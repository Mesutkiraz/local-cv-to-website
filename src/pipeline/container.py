"""
Dependency Container
====================
Dependency Injection container for managing service instances.
Follows Dependency Inversion Principle (DIP).
Open/Closed: Can add new services without modifying existing code.
"""

from typing import Optional
from pathlib import Path

from src.interfaces import (
    IDocumentExtractor,
    ILLMService,
    ICVAnalyzer,
    IPortfolioGenerator,
    IFileService,
    IUIService,
)
from src.models.config import AppConfig
from src.services import (
    OllamaService,
    PDFExtractor,
    DeepSeekAnalyzer,
    QwenPortfolioGenerator,
    LocalFileService,
    TkinterUIService,
)


class DependencyContainer:
    """
    Dependency Injection container.
    
    Manages service instances and their dependencies.
    Follows DIP: High-level modules depend on abstractions.
    
    Usage:
        container = DependencyContainer(config)
        analyzer = container.cv_analyzer
        generator = container.portfolio_generator
    """
    
    def __init__(self, config: Optional[AppConfig] = None):
        """
        Initialize the container with configuration.
        
        Args:
            config: Application configuration (uses default if not provided)
        """
        self._config = config or AppConfig.default()
        
        # Service instances (lazy initialization)
        self._llm_service: Optional[ILLMService] = None
        self._document_extractor: Optional[IDocumentExtractor] = None
        self._cv_analyzer: Optional[ICVAnalyzer] = None
        self._portfolio_generator: Optional[IPortfolioGenerator] = None
        self._file_service: Optional[IFileService] = None
        self._ui_service: Optional[IUIService] = None
    
    @property
    def config(self) -> AppConfig:
        """Get the application configuration."""
        return self._config
    
    @property
    def llm_service(self) -> ILLMService:
        """
        Get the LLM service instance.
        Lazy initialization with singleton pattern.
        """
        if self._llm_service is None:
            self._llm_service = OllamaService()
        return self._llm_service
    
    @property
    def document_extractor(self) -> IDocumentExtractor:
        """Get the document extractor instance."""
        if self._document_extractor is None:
            self._document_extractor = PDFExtractor()
        return self._document_extractor
    
    @property
    def cv_analyzer(self) -> ICVAnalyzer:
        """Get the CV analyzer instance (with dependencies injected)."""
        if self._cv_analyzer is None:
            self._cv_analyzer = DeepSeekAnalyzer(
                llm_service=self.llm_service,
                model=self._config.models.brain_model,
                temperature=self._config.analysis_temperature
            )
        return self._cv_analyzer
    
    @property
    def portfolio_generator(self) -> IPortfolioGenerator:
        """Get the portfolio generator instance (with dependencies injected)."""
        if self._portfolio_generator is None:
            self._portfolio_generator = QwenPortfolioGenerator(
                llm_service=self.llm_service,
                model=self._config.models.coder_model,
                temperature=self._config.generation_temperature
            )
        return self._portfolio_generator
    
    @property
    def file_service(self) -> IFileService:
        """Get the file service instance."""
        if self._file_service is None:
            self._file_service = LocalFileService(
                output_dir=self._config.output_dir
            )
        return self._file_service
    
    @property
    def ui_service(self) -> IUIService:
        """Get the UI service instance."""
        if self._ui_service is None:
            self._ui_service = TkinterUIService()
        return self._ui_service
    
    # === Setters for custom implementations (DIP) ===
    
    def set_llm_service(self, service: ILLMService) -> "DependencyContainer":
        """
        Set a custom LLM service implementation.
        Useful for testing or alternative providers.
        """
        self._llm_service = service
        # Reset dependent services
        self._cv_analyzer = None
        self._portfolio_generator = None
        return self
    
    def set_document_extractor(self, extractor: IDocumentExtractor) -> "DependencyContainer":
        """Set a custom document extractor implementation."""
        self._document_extractor = extractor
        return self
    
    def set_cv_analyzer(self, analyzer: ICVAnalyzer) -> "DependencyContainer":
        """Set a custom CV analyzer implementation."""
        self._cv_analyzer = analyzer
        return self
    
    def set_portfolio_generator(self, generator: IPortfolioGenerator) -> "DependencyContainer":
        """Set a custom portfolio generator implementation."""
        self._portfolio_generator = generator
        return self
    
    def set_file_service(self, service: IFileService) -> "DependencyContainer":
        """Set a custom file service implementation."""
        self._file_service = service
        return self
    
    def set_ui_service(self, service: IUIService) -> "DependencyContainer":
        """Set a custom UI service implementation."""
        self._ui_service = service
        return self
