"""
CV Portfolio Pipeline
=====================
Main orchestrator for the CV to Portfolio generation process.
Single Responsibility: Orchestrates the pipeline steps only.
Open/Closed: Can extend with new steps without modifying existing code.
Dependency Inversion: Depends on abstractions via DependencyContainer.
"""

import json
import traceback
from datetime import datetime
from pathlib import Path
from typing import Optional

from src.pipeline.container import DependencyContainer
from src.models.cv_data import CVData
from src.models.config import AppConfig
from src.utils.logger import Logger


class PipelineError(Exception):
    """Exception raised when pipeline execution fails."""
    pass


class CVPortfolioPipeline:
    """
    Main pipeline orchestrator for CV to Portfolio generation.
    
    Follows SOLID principles:
    - SRP: Only orchestrates the pipeline flow
    - OCP: Can be extended with new steps
    - DIP: Depends on abstractions via container
    
    Usage:
        pipeline = CVPortfolioPipeline()
        pipeline.run()
        
        # Or with custom config:
        config = AppConfig.with_models(brain_model="custom:model")
        pipeline = CVPortfolioPipeline(config=config)
        pipeline.run()
        
        # Or with custom container:
        container = DependencyContainer()
        container.set_llm_service(CustomLLMService())
        pipeline = CVPortfolioPipeline(container=container)
        pipeline.run()
    """
    
    def __init__(
        self,
        config: Optional[AppConfig] = None,
        container: Optional[DependencyContainer] = None
    ):
        """
        Initialize the pipeline.
        
        Args:
            config: Application configuration (ignored if container provided)
            container: Pre-configured dependency container
        """
        if container:
            self._container = container
        else:
            self._container = DependencyContainer(config or AppConfig.default())
        
        self._logger = Logger(prefix="Pipeline")
    
    def run(self) -> Optional[Path]:
        """
        Execute the complete pipeline.
        
        Returns:
            Path to generated portfolio, or None if failed
        """
        self._print_banner()
        
        try:
            # Step 1: Select PDF file
            pdf_path = self._select_pdf()
            if not pdf_path:
                self._logger.warning("No file selected. Exiting.")
                return None
            
            # Step 2: Extract text from PDF
            cv_text = self._extract_text(pdf_path)
            if not cv_text:
                return None
            
            # Step 3: Analyze CV with AI
            cv_data = self._analyze_cv(cv_text)
            if not cv_data:
                return None
            
            # Step 4: Generate portfolio HTML
            html_content = self._generate_portfolio(cv_data)
            if not html_content:
                return None
            
            # Step 5: Save outputs
            output_path = self._save_outputs(html_content, pdf_path)
            
            self._print_success(output_path)
            return output_path
            
        except Exception as e:
            self._handle_error(e)
            return None
    
    def _print_banner(self) -> None:
        """Print the startup banner."""
        print("\n")
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║     🚀 AI AGENT PIPELINE: CV → Portfolio Website             ║")
        print("║     Hardware: RTX 3060 12GB | Sequential Model Loading       ║")
        print("║     Version: 2.1 - SOLID Architecture                        ║")
        print("╚══════════════════════════════════════════════════════════════╝")
        print("\n")
    
    def _select_pdf(self) -> Optional[Path]:
        """Step 1: Select PDF file via UI."""
        self._logger.info("Opening file selector...")
        
        pdf_path = self._container.ui_service.select_file(
            title="Select Your CV (PDF)",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        
        if pdf_path:
            self._logger.success(f"Selected: {pdf_path.name}")
        
        return pdf_path
    
    def _extract_text(self, pdf_path: Path) -> Optional[str]:
        """Step 2: Extract text from PDF."""
        print("\n" + "─" * 50)
        
        cv_text = self._container.document_extractor.extract(pdf_path)
        
        if not cv_text.strip():
            self._logger.error("No text could be extracted from PDF")
            return None
        
        # Save raw text for debugging
        self._container.file_service.save(cv_text, "cv_raw_text", "txt")
        
        return cv_text
    
    def _analyze_cv(self, cv_text: str) -> Optional[CVData]:
        """Step 3: Analyze CV with DeepSeek."""
        print("\n" + "─" * 50)
        self._logger.vram(f"Loading {self._container.config.models.brain_model} into VRAM...")
        
        cv_data = self._container.cv_analyzer.analyze(cv_text)
        
        if not cv_data:
            self._logger.error("CV analysis failed - no data returned")
            return None
        
        # Save intermediate JSON for debugging
        json_output = self._container.file_service.save(
            json.dumps(cv_data.to_dict(), indent=2, ensure_ascii=False),
            "cv_extracted_data",
            "json"
        )
        self._logger.file(f"Extracted data saved: {json_output}")
        
        return cv_data
    
    def _generate_portfolio(self, cv_data: CVData) -> Optional[str]:
        """Step 4: Generate portfolio with Qwen."""
        print("\n" + "─" * 50)
        self._logger.vram(f"Loading {self._container.config.models.coder_model} into VRAM...")
        
        html_content = self._container.portfolio_generator.generate(cv_data)
        
        if not html_content:
            self._logger.error("Portfolio generation failed")
            return None
        
        return html_content
    
    def _save_outputs(self, html_content: str, pdf_path: Path) -> Path:
        """Step 5: Save generated portfolio."""
        print("\n" + "─" * 50)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = pdf_path.stem
        
        # Save timestamped version
        output_path = self._container.file_service.save(
            html_content,
            f"{base_name}_portfolio_{timestamp}"
        )
        
        # Also save as index.html for easy access
        self._container.file_service.save(html_content, "index")
        
        return output_path
    
    def _print_success(self, output_path: Path) -> None:
        """Print success message and show dialog."""
        print("\n")
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║                    ✅ PIPELINE COMPLETE                      ║")
        print("╚══════════════════════════════════════════════════════════════╝")
        
        index_path = self._container.file_service.output_directory / "index.html"
        
        self._logger.rocket(f"Portfolio saved: {output_path}")
        self._logger.file(f"Quick access: {index_path}")
        print("\n")
        
        self._container.ui_service.show_success(
            "Success! 🎉",
            f"Your portfolio has been generated!\n\n"
            f"Main file:\n{output_path}\n\n"
            f"Quick access:\n{index_path}"
        )
    
    def _handle_error(self, error: Exception) -> None:
        """Handle pipeline errors."""
        self._logger.error(f"Pipeline failed: {error}")
        traceback.print_exc()
        
        self._container.ui_service.show_error(
            "Pipeline Error",
            f"An error occurred:\n\n{str(error)}"
        )
