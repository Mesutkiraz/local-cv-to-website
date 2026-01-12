"""
DeepSeek CV Analyzer
====================
Concrete implementation of ICVAnalyzer using DeepSeek-R1.
Single Responsibility: Only handles CV analysis logic.
Dependency Inversion: Depends on ILLMService abstraction.
"""

from src.interfaces.cv_analyzer import ICVAnalyzer
from src.interfaces.llm_service import ILLMService, LLMConfig
from src.models.cv_data import CVData
from src.utils.logger import Logger
from src.utils.parsers import ResponseParser


class AnalysisError(Exception):
    """Exception raised when CV analysis fails."""
    pass


class DeepSeekAnalyzer(ICVAnalyzer):
    """
    CV analyzer using DeepSeek-R1 for deep reasoning.
    Implements ICVAnalyzer with anti-hallucination prompts.
    """
    
    def __init__(
        self,
        llm_service: ILLMService,
        model: str = "deepseek-r1:7b",
        temperature: float = 0.3
    ):
        """
        Initialize the DeepSeek analyzer.
        
        Args:
            llm_service: LLM service implementation (DIP)
            model: Model identifier to use
            temperature: Temperature for generation
        """
        self._llm = llm_service
        self._model = model
        self._temperature = temperature
        self._logger = Logger(prefix="DeepSeekAnalyzer")
    
    @property
    def model_name(self) -> str:
        """Return the model name being used."""
        return self._model
    
    def analyze(self, cv_text: str) -> CVData:
        """
        Analyze CV text and extract structured data.
        Uses strict anti-hallucination prompts.
        
        Args:
            cv_text: Raw text from CV document
            
        Returns:
            CVData with extracted information
            
        Raises:
            AnalysisError: If analysis fails
        """
        self._logger.brain(f"PHASE 1: Activating The Brain ({self._model})")
        self._logger.info("Analyzing CV with STRICT anti-hallucination mode...")
        
        prompt = self._build_prompt(cv_text)
        
        config = LLMConfig(
            temperature=self._temperature,
            context_window=8192
        )
        
        response = self._llm.chat(
            messages=[{"role": "user", "content": prompt}],
            model=self._model,
            config=config
        )
        
        if not response.success:
            # Unload model even on failure
            self._llm.unload_model(self._model)
            raise AnalysisError(f"LLM request failed: {response.error}")
        
        # Parse the JSON response
        parsed_data = ResponseParser.extract_json(response.content)
        
        if not parsed_data:
            self._logger.warning("Could not parse structured JSON, using raw analysis")
            cv_data = CVData(
                raw_analysis=response.content,
                original_cv_text=cv_text
            )
        else:
            cv_data = CVData.from_dict(parsed_data, cv_text)
        
        self._logger.success("CV analysis complete - data extracted with validation")
        
        # Unload model to free VRAM
        self._llm.unload_model(self._model)
        
        return cv_data
    
    def _build_prompt(self, cv_text: str) -> str:
        """Build the analysis prompt with anti-hallucination rules."""
        return f"""You are a precise CV data extractor. Your job is to extract ONLY what exists in the CV text below.

## RAW CV TEXT (THIS IS YOUR ONLY SOURCE OF TRUTH):
---
{cv_text}
---

## CRITICAL ANTI-HALLUCINATION RULES:
1. **EXACT TEXT ONLY**: Copy titles, names, dates EXACTLY as written in the CV
2. **NO INVENTION**: Do NOT invent years of experience, degrees, or titles
3. **NO ASSUMPTIONS**: If the CV says "Junior Game Developer", output "Junior Game Developer" - NOT "Senior" or "Lead"
4. **DATES**: Use exact date ranges from CV. If CV says "2023-Present", use that exactly
5. **PROJECTS**: Use the EXACT project names (e.g., "ROWA Space Station", "Untouchables")
6. **VALIDATION**: If you're unsure, set "uncertain": true and copy raw text

## EXTRACTION TASK:
Extract the following into JSON. Use null for missing fields. DO NOT GUESS.

```json
{{
    "validation": {{
        "source": "Extracted from provided CV text only",
        "hallucination_check": "All data verified against source text"
    }},
    "personal": {{
        "name": "EXACT full name from CV",
        "title": "EXACT job title from CV (e.g., 'Junior Game Developer' - no modifications)",
        "tagline": "Brief tagline based on actual CV content",
        "bio": "2-3 sentences using ONLY facts from CV",
        "email": "exact email or null",
        "phone": "exact phone or null",
        "location": "exact location or null"
    }},
    "links": {{
        "linkedin": "exact LinkedIn URL or null",
        "github": "exact GitHub URL or null",
        "website": "exact website URL or null",
        "other": ["any other URLs found"]
    }},
    "experience": [
        {{
            "company": "EXACT company name",
            "role": "EXACT job title from CV",
            "period": "EXACT date range from CV",
            "description": "Summary using ONLY CV content",
            "highlights": ["actual achievements from CV"]
        }}
    ],
    "projects": [
        {{
            "name": "EXACT project name (e.g., 'ROWA Space Station')",
            "description": "Description using ONLY CV content",
            "tech_stack": ["technologies mentioned in CV"],
            "link": "project URL if in CV, else null",
            "type": "Game/Web/App based on CV"
        }}
    ],
    "education": [
        {{
            "institution": "EXACT school name",
            "degree": "EXACT degree/program name",
            "period": "EXACT date range"
        }}
    ],
    "skills": {{
        "languages": ["programming languages from CV"],
        "frameworks": ["frameworks from CV"],
        "tools": ["tools from CV"],
        "specialties": ["specialties from CV"]
    }},
    "certifications": ["EXACT certification names"],
    "languages_spoken": ["languages from CV"]
}}
```

IMPORTANT: Output ONLY the JSON. No explanations. Use EXACT text from CV."""
