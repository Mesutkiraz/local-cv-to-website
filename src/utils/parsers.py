"""
Response Parsers
================
Utilities for parsing LLM responses.
Single Responsibility: Parse and extract structured data from text.
"""

import json
import re
from typing import Optional


class ResponseParser:
    """
    Parses LLM responses to extract structured data.
    Single Responsibility: Only handles parsing logic.
    """
    
    @staticmethod
    def extract_json(text: str) -> Optional[dict]:
        """
        Extract JSON object from LLM response.
        Handles thinking tags and code blocks.
        
        Args:
            text: Raw LLM response text
            
        Returns:
            Parsed dictionary or None if parsing fails
        """
        # Remove DeepSeek-R1 thinking tags
        text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
        
        # Try to find JSON in markdown code blocks
        json_match = re.search(r'```(?:json)?\s*(\{[\s\S]*?\})\s*```', text)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError:
                pass
        
        # Try to find raw JSON object (greedy match for nested objects)
        json_match = re.search(r'\{[\s\S]*\}', text)
        if json_match:
            try:
                return json.loads(json_match.group(0))
            except json.JSONDecodeError:
                pass
        
        return None
    
    @staticmethod
    def extract_html(text: str) -> str:
        """
        Extract HTML from LLM response.
        Handles markdown code blocks.
        
        Args:
            text: Raw LLM response text
            
        Returns:
            Extracted HTML string
        """
        # Try to find HTML in code blocks first
        html_match = re.search(
            r'```(?:html)?\s*(<!DOCTYPE[\s\S]*?</html>)\s*```',
            text,
            re.IGNORECASE
        )
        if html_match:
            return html_match.group(1).strip()
        
        # Try to find raw HTML document
        html_match = re.search(
            r'(<!DOCTYPE[\s\S]*</html>)',
            text,
            re.IGNORECASE
        )
        if html_match:
            return html_match.group(1).strip()
        
        return text.strip()
    
    @staticmethod
    def clean_thinking_tags(text: str) -> str:
        """Remove thinking tags from response."""
        return re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL).strip()
