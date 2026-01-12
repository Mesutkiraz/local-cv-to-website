"""
Ollama LLM Service
==================
Concrete implementation of ILLMService using Ollama.
Dependency Inversion: Implements abstract interface.
Single Responsibility: Only handles Ollama API interactions.
"""

import time
from typing import Optional

import ollama

from src.interfaces.llm_service import ILLMService, LLMConfig, LLMResponse
from src.utils.logger import Logger


class OllamaService(ILLMService):
    """
    Ollama-based LLM service implementation.
    Implements ILLMService for local LLM inference.
    """
    
    def __init__(self):
        """Initialize the Ollama service."""
        self._logger = Logger(prefix="Ollama")
    
    def generate(
        self,
        prompt: str,
        model: str,
        config: Optional[LLMConfig] = None
    ) -> LLMResponse:
        """
        Generate a response using Ollama's generate API.
        
        Args:
            prompt: The prompt to send
            model: Model identifier
            config: Optional configuration
            
        Returns:
            LLMResponse with generated content
        """
        config = config or LLMConfig()
        
        try:
            response = ollama.generate(
                model=model,
                prompt=prompt,
                options={
                    "temperature": config.temperature,
                    "num_ctx": config.context_window,
                    "num_predict": config.max_tokens,
                }
            )
            
            return LLMResponse(
                content=response.get("response", ""),
                model=model,
                success=True
            )
            
        except Exception as e:
            self._logger.error(f"Generation failed: {e}")
            return LLMResponse(
                content="",
                model=model,
                success=False,
                error=str(e)
            )
    
    def chat(
        self,
        messages: list[dict],
        model: str,
        config: Optional[LLMConfig] = None
    ) -> LLMResponse:
        """
        Send a chat conversation using Ollama's chat API.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Model identifier
            config: Optional configuration
            
        Returns:
            LLMResponse with generated content
        """
        config = config or LLMConfig()
        
        try:
            response = ollama.chat(
                model=model,
                messages=messages,
                options={
                    "temperature": config.temperature,
                    "num_ctx": config.context_window,
                    "num_predict": config.max_tokens,
                }
            )
            
            content = response.get("message", {}).get("content", "")
            
            return LLMResponse(
                content=content,
                model=model,
                success=True
            )
            
        except Exception as e:
            self._logger.error(f"Chat failed: {e}")
            return LLMResponse(
                content="",
                model=model,
                success=False,
                error=str(e)
            )
    
    def unload_model(self, model: str) -> bool:
        """
        Unload a model from VRAM to free memory.
        
        Args:
            model: Model identifier to unload
            
        Returns:
            True if successfully unloaded
        """
        try:
            self._logger.vram(f"Purging {model} from VRAM...")
            # Setting keep_alive to 0 immediately unloads the model
            ollama.generate(model=model, prompt="", keep_alive=0)
            # Give GPU time to fully release memory
            time.sleep(2)
            self._logger.success(f"{model} purged successfully - VRAM freed")
            return True
            
        except Exception as e:
            self._logger.warning(f"Model unload warning (may not be loaded): {e}")
            return False
    
    def is_available(self) -> bool:
        """Check if Ollama is running and available."""
        try:
            ollama.list()
            return True
        except Exception:
            return False
