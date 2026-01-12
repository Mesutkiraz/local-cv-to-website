"""
Application Configuration
=========================
Centralized configuration for the application.
Single Responsibility: Manage application settings only.
"""

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class LLMModelsConfig:
    """LLM model configuration."""
    brain_model: str = "deepseek-r1:7b"      # Deep reasoning & data extraction
    coder_model: str = "qwen2.5-coder:14b"   # High-fidelity frontend coding


@dataclass
class AppConfig:
    """
    Application-wide configuration.
    Follows Single Responsibility: Only manages configuration values.
    """
    models: LLMModelsConfig = field(default_factory=LLMModelsConfig)
    output_dir: Path = field(default_factory=lambda: Path("outputs"))
    debug_mode: bool = False
    
    # LLM settings
    analysis_temperature: float = 0.3   # Lower for factual extraction
    generation_temperature: float = 0.2  # Lower for consistent code
    context_window: int = 8192
    max_tokens: int = 4096
    
    @classmethod
    def default(cls) -> "AppConfig":
        """Create default configuration."""
        return cls()
    
    @classmethod
    def with_models(
        cls,
        brain_model: str = "deepseek-r1:7b",
        coder_model: str = "qwen2.5-coder:14b"
    ) -> "AppConfig":
        """Create configuration with custom models."""
        return cls(
            models=LLMModelsConfig(
                brain_model=brain_model,
                coder_model=coder_model
            )
        )
