"""
╔══════════════════════════════════════════════════════════════════════════════╗
║           AI AGENT PIPELINE: CV → Portfolio Website Generator                ║
║══════════════════════════════════════════════════════════════════════════════║
║  Converts a CV PDF into a high-end, production-ready Portfolio Website      ║
║  using local LLMs via Ollama (DeepSeek-R1 + Qwen2.5-Coder).                 ║
║                                                                              ║
║  Hardware: Optimized for RTX 3060 12GB VRAM (sequential model loading)      ║
║  Version: 2.1 - SOLID Architecture Refactored                               ║
╚══════════════════════════════════════════════════════════════════════════════╝

SOLID Principles Applied:
=========================
1. Single Responsibility (SRP):
   - Each class has ONE job (PDFExtractor extracts, OllamaService calls LLM, etc.)
   
2. Open/Closed (OCP):
   - Add new extractors (Word, OCR) without modifying existing code
   - Add new LLM providers (OpenAI, Anthropic) without changes
   - Add new UI implementations (CLI, Web) without changes
   
3. Liskov Substitution (LSP):
   - Any IDocumentExtractor works in place of PDFExtractor
   - Any ILLMService works in place of OllamaService
   
4. Interface Segregation (ISP):
   - Small, focused interfaces (IDocumentExtractor, ILLMService, etc.)
   - Clients depend only on what they need
   
5. Dependency Inversion (DIP):
   - High-level pipeline depends on abstractions (interfaces)
   - DependencyContainer manages concrete implementations
   - Easy to swap implementations for testing or customization

Project Structure:
==================
src/
├── interfaces/          # Abstract contracts (ISP, DIP)
│   ├── document_extractor.py
│   ├── llm_service.py
│   ├── cv_analyzer.py
│   ├── portfolio_generator.py
│   ├── file_service.py
│   └── ui_service.py
├── models/              # Data structures (SRP)
│   ├── cv_data.py
│   └── config.py
├── services/            # Concrete implementations (SRP, LSP)
│   ├── ollama_service.py
│   ├── pdf_extractor.py
│   ├── deepseek_analyzer.py
│   ├── qwen_portfolio_generator.py
│   ├── local_file_service.py
│   └── tkinter_ui_service.py
├── pipeline/            # Orchestration (OCP, DIP)
│   ├── container.py     # Dependency Injection
│   └── cv_portfolio_pipeline.py
└── utils/               # Utilities (SRP)
    ├── logger.py
    └── parsers.py

Usage:
======
# Default usage
python main.py

# Programmatic usage with custom configuration
from src.pipeline import CVPortfolioPipeline
from src.models.config import AppConfig

config = AppConfig.with_models(
    brain_model="deepseek-r1:7b",
    coder_model="qwen2.5-coder:14b"
)
pipeline = CVPortfolioPipeline(config=config)
pipeline.run()

# With custom services (DIP in action)
from src.pipeline import DependencyContainer, CVPortfolioPipeline

container = DependencyContainer()
container.set_llm_service(CustomLLMService())  # Your implementation
pipeline = CVPortfolioPipeline(container=container)
pipeline.run()
"""

from src.pipeline import CVPortfolioPipeline
from src.models.config import AppConfig


def main():
    """
    Entry point for the CV to Portfolio Pipeline.
    Creates and runs the pipeline with default configuration.
    """
    # Create pipeline with default configuration
    # To customize, pass a custom AppConfig or DependencyContainer
    pipeline = CVPortfolioPipeline()
    
    # Run the pipeline
    result = pipeline.run()
    
    if result:
        print(f"\n✅ Portfolio generated successfully: {result}")
    else:
        print("\n❌ Pipeline did not complete successfully")


if __name__ == "__main__":
    main()