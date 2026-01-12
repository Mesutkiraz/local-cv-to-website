"""
Qwen Portfolio Generator
========================
Concrete implementation of IPortfolioGenerator using Qwen2.5-Coder.
Single Responsibility: Only handles HTML portfolio generation.
Dependency Inversion: Depends on ILLMService abstraction.
"""

import json
from src.interfaces.portfolio_generator import IPortfolioGenerator
from src.interfaces.llm_service import ILLMService, LLMConfig
from src.models.cv_data import CVData
from src.utils.logger import Logger
from src.utils.parsers import ResponseParser


class GenerationError(Exception):
    """Exception raised when portfolio generation fails."""
    pass


class QwenPortfolioGenerator(IPortfolioGenerator):
    """
    Portfolio generator using Qwen2.5-Coder.
    Implements IPortfolioGenerator with AOS visibility fixes.
    """
    
    def __init__(
        self,
        llm_service: ILLMService,
        model: str = "qwen2.5-coder:14b",
        temperature: float = 0.2
    ):
        """
        Initialize the Qwen portfolio generator.
        
        Args:
            llm_service: LLM service implementation (DIP)
            model: Model identifier to use
            temperature: Temperature for generation
        """
        self._llm = llm_service
        self._model = model
        self._temperature = temperature
        self._logger = Logger(prefix="QwenGenerator")
    
    @property
    def model_name(self) -> str:
        """Return the model name being used."""
        return self._model
    
    def generate(self, cv_data: CVData, original_cv_text: str = "") -> str:
        """
        Generate portfolio HTML from CV data.
        
        Args:
            cv_data: Structured CV data
            original_cv_text: Original CV text for validation
            
        Returns:
            Complete HTML string
            
        Raises:
            GenerationError: If generation fails
        """
        self._logger.code(f"PHASE 2: Activating The Architect ({self._model})")
        self._logger.info("Generating portfolio HTML with AOS fixes...")
        
        # Use original CV text from cv_data if not provided
        if not original_cv_text:
            original_cv_text = cv_data.original_cv_text
        
        prompt = self._build_prompt(cv_data, original_cv_text)
        
        config = LLMConfig(
            temperature=self._temperature,
            context_window=8192,
            max_tokens=4096
        )
        
        response = self._llm.chat(
            messages=[{"role": "user", "content": prompt}],
            model=self._model,
            config=config
        )
        
        if not response.success:
            self._llm.unload_model(self._model)
            raise GenerationError(f"LLM request failed: {response.error}")
        
        html_content = ResponseParser.extract_html(response.content)
        
        # Apply AOS fixes if not present
        if "aos-animate" not in html_content.lower():
            self._logger.warning("Injecting AOS visibility fixes...")
            html_content = self.apply_fixes(html_content)
        
        if not html_content.lower().startswith("<!doctype"):
            self._logger.warning("Output may not be valid HTML")
        
        self._logger.success("Portfolio HTML generated successfully")
        
        # Unload model to free VRAM
        self._llm.unload_model(self._model)
        
        return html_content
    
    def apply_fixes(self, html: str) -> str:
        """
        Apply post-processing fixes to generated HTML.
        Injects AOS visibility fixes if missing.
        
        Args:
            html: Raw generated HTML
            
        Returns:
            Fixed HTML with all patches applied
        """
        aos_css_fix = """
    <style>
        /* AOS Visibility Fallback */
        [data-aos] {
            opacity: 1 !important;
            transform: none !important;
        }
        .aos-init [data-aos] {
            opacity: 0;
            transform: translateY(20px);
        }
        .aos-init .aos-animate {
            opacity: 1 !important;
            transform: none !important;
        }
    </style>
    """
        
        aos_js_fix = """
    <script>
        window.addEventListener('load', function() {
            if (typeof lucide !== 'undefined') lucide.createIcons();
            if (typeof AOS !== 'undefined') {
                AOS.init({ duration: 800, once: true, offset: 50 });
            }
            setTimeout(function() {
                document.querySelectorAll('[data-aos]').forEach(function(el) {
                    el.classList.add('aos-animate');
                });
            }, 1000);
        });
    </script>
    """
        
        # Inject CSS before </head>
        if "</head>" in html:
            html = html.replace("</head>", f"{aos_css_fix}\n</head>")
        
        # Inject JS before </body>
        if "</body>" in html:
            html = html.replace("</body>", f"{aos_js_fix}\n</body>")
        
        return html
    
    def _build_prompt(self, cv_data: CVData, original_cv_text: str) -> str:
        """Build the generation prompt."""
        # Format data section
        if cv_data.raw_analysis:
            data_section = f"## ANALYZED CV DATA:\n{cv_data.raw_analysis}"
        else:
            data_section = f"## PORTFOLIO DATA (JSON):\n```json\n{json.dumps(cv_data.to_dict(), indent=2, ensure_ascii=False)}\n```"
        
        return f"""You are an elite frontend developer. Generate a COMPLETE, PRODUCTION-READY index.html portfolio.

{data_section}

## ORIGINAL CV TEXT (FOR VERIFICATION - USE EXACT DATA):
```
{original_cv_text[:2000]}
```

## CRITICAL: AOS VISIBILITY FIX
The page MUST NOT be black. Include these MANDATORY fixes:

### 1. CSS Fallback (in <style> tag):
```css
/* AOS Fallback - Prevent black screen */
[data-aos] {{
    opacity: 1 !important;
    transform: none !important;
    transition: opacity 0.6s ease, transform 0.6s ease;
}}
.aos-animate {{
    pointer-events: auto;
}}
/* Ensure visibility before JS loads */
body {{
    opacity: 1;
}}
```

### 2. Proper Script Loading (at end of body):
```html
<script src="https://unpkg.com/aos@2.3.1/dist/aos.js"></script>
<script src="https://unpkg.com/lucide@latest/dist/umd/lucide.js"></script>
<script>
    window.addEventListener('load', function() {{
        // Initialize Lucide icons
        if (typeof lucide !== 'undefined') {{
            lucide.createIcons();
        }}
        
        // Initialize AOS with safe settings
        if (typeof AOS !== 'undefined') {{
            AOS.init({{
                duration: 800,
                once: true,
                offset: 50,
                disable: 'mobile'
            }});
        }}
        
        // Fallback: ensure all elements visible after 1 second
        setTimeout(function() {{
            document.querySelectorAll('[data-aos]').forEach(function(el) {{
                el.classList.add('aos-animate');
            }});
        }}, 1000);
    }});
</script>
```

## TECHNICAL STACK:
- Tailwind CSS: <script src="https://cdn.tailwindcss.com"></script>
- AOS.js: <link href="https://unpkg.com/aos@2.3.1/dist/aos.css" rel="stylesheet">
- Lucide Icons: Use <i data-lucide="icon-name"></i>
- Google Fonts: Inter + Space Grotesk

## DESIGN: VERCEL-STYLE BENTO GRID

### Layout Structure:
```html
<div class="grid grid-cols-12 gap-4 p-4">
    <!-- Hero: spans full width -->
    <div class="col-span-12">...</div>
    
    <!-- About: 8 cols, Skills: 4 cols -->
    <div class="col-span-12 md:col-span-8">...</div>
    <div class="col-span-12 md:col-span-4">...</div>
    
    <!-- Projects: varying spans (6, 4, 8, etc.) -->
    <div class="col-span-12 md:col-span-6">...</div>
    <div class="col-span-12 md:col-span-6">...</div>
</div>
```

### Theme: PITCH BLACK + EMERALD
- Background: #000000 (pure black)
- Cards: bg-white/5 backdrop-blur-md border border-white/10 rounded-2xl
- Text: text-white, text-gray-400
- Accent: text-emerald-400, bg-emerald-500/10, border-emerald-500/30
- Hover: hover:bg-white/10 hover:border-emerald-500/50

### Card Style:
```html
<div class="bg-white/5 backdrop-blur-md border border-white/10 rounded-2xl p-6 
            hover:bg-white/10 hover:border-emerald-500/50 transition-all duration-300"
     data-aos="fade-up">
    <!-- content -->
</div>
```

## SECTIONS:
1. **Hero**: Name (large), exact title from CV, tagline, social icons
2. **About**: Bio card (col-span-8)
3. **Skills**: Grouped skill tags (col-span-4)
4. **Projects**: Bento cards with EXACT project names, descriptions, tech stacks
5. **Experience**: Timeline with EXACT roles and dates
6. **Contact**: Footer with real links

## ABSOLUTE RULES:
1. Use ONLY the exact data provided - NO PLACEHOLDERS
2. NO <img> tags - Lucide icons only
3. If title is "Junior Game Developer", use that EXACTLY
4. All links must be real URLs from the data
5. Include the AOS visibility fixes EXACTLY as shown above
6. Start with <!DOCTYPE html>, end with </html>

Generate the COMPLETE HTML now."""
