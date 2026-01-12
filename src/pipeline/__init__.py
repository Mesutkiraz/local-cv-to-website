"""
Pipeline Module
===============
Contains the main pipeline orchestrator.
"""

from src.pipeline.cv_portfolio_pipeline import CVPortfolioPipeline
from src.pipeline.container import DependencyContainer

__all__ = [
    "CVPortfolioPipeline",
    "DependencyContainer",
]
