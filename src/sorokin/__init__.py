"""
Sorokin - A Prompt Autopsy Engine

Analyzes and dissects LLM prompts to understand their structure, 
components, and characteristics.
"""

from .autopsy import PromptAutopsy
from .analyzer import PromptAnalyzer
from .reporter import AutopsyReport

__version__ = "0.1.0"
__all__ = ["PromptAutopsy", "PromptAnalyzer", "AutopsyReport"]
