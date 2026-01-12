"""
LLM Service Interface
=====================
Single Responsibility: Define contract for LLM interactions.
Open/Closed: Can add new LLM providers (OpenAI, Anthropic) without modifying existing code.
Dependency Inversion: High-level modules depend on this abstraction, not concrete implementations.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class LLMConfig:
    """Configuration for LLM requests."""
    temperature: float = 0.3
    max_tokens: int = 4096
    context_window: int = 8192


@dataclass
class LLMResponse:
    """Standardized response from LLM."""
    content: str
    model: str
    success: bool
    error: Optional[str] = None


class ILLMService(ABC):
    """
    Abstract interface for LLM service providers.
    
    Implementations:
    - OllamaService: Local LLM via Ollama
    - (Future) OpenAIService: OpenAI API
    - (Future) AnthropicService: Claude API
    """
    
    @abstractmethod
    def generate(
        self,
        prompt: str,
        model: str,
        config: Optional[LLMConfig] = None
    ) -> LLMResponse:
        """
        Generate a response from the LLM.
        
        Args:
            prompt: The prompt to send to the LLM
            model: Model identifier to use
            config: Optional configuration for the request
            
        Returns:
            LLMResponse with generated content
        """
        pass
    
    @abstractmethod
    def chat(
        self,
        messages: list[dict],
        model: str,
        config: Optional[LLMConfig] = None
    ) -> LLMResponse:
        """
        Send a chat conversation to the LLM.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Model identifier to use
            config: Optional configuration for the request
            
        Returns:
            LLMResponse with generated content
        """
        pass
    
    @abstractmethod
    def unload_model(self, model: str) -> bool:
        """
        Unload a model from memory/VRAM.
        
        Args:
            model: Model identifier to unload
            
        Returns:
            True if successfully unloaded
        """
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if the LLM service is available and running."""
        pass
