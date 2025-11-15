"""
Core PromptAutopsy class for analyzing prompts.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
import re
from datetime import datetime


@dataclass
class PromptComponent:
    """Represents a component of a prompt."""
    role: str
    content: str
    tokens: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)


class PromptAutopsy:
    """
    Main class for performing autopsy on prompts.
    
    Analyzes prompt structure, extracts components, counts tokens,
    and provides insights into prompt composition.
    """
    
    def __init__(self, prompt: str, metadata: Optional[Dict[str, Any]] = None):
        """
        Initialize PromptAutopsy with a prompt.
        
        Args:
            prompt: The prompt text to analyze
            metadata: Optional metadata about the prompt
        """
        self.prompt = prompt
        self.metadata = metadata or {}
        self.timestamp = datetime.now()
        self._components: List[PromptComponent] = []
        self._analyzed = False
    
    def analyze(self) -> "PromptAutopsy":
        """
        Perform the autopsy analysis on the prompt.
        
        Returns:
            Self for method chaining
        """
        self._extract_components()
        self._count_tokens()
        self._analyze_structure()
        self._analyzed = True
        return self
    
    def _extract_components(self):
        """Extract different components from the prompt."""
        # Try to parse structured prompts (e.g., with role markers)
        role_pattern = r'(?:^|\n)(?:\[|\<)?(system|user|assistant)(?:\]|\>)?:?\s*(.+?)(?=(?:\n(?:\[|\<)?(?:system|user|assistant)|$))'
        matches = re.finditer(role_pattern, self.prompt, re.IGNORECASE | re.DOTALL)
        
        components_found = False
        for match in matches:
            role, content = match.groups()
            self._components.append(PromptComponent(
                role=role.lower(),
                content=content.strip()
            ))
            components_found = True
        
        # If no structured format found, treat entire prompt as user message
        if not components_found:
            self._components.append(PromptComponent(
                role="user",
                content=self.prompt.strip()
            ))
    
    def _count_tokens(self):
        """
        Count tokens for each component.
        Uses a simple approximation: ~4 chars per token for English text.
        """
        for component in self._components:
            # Simple token estimation: split on whitespace and punctuation
            words = re.findall(r'\b\w+\b|[^\w\s]', component.content)
            component.tokens = len(words)
    
    def _analyze_structure(self):
        """Analyze the structure and add metadata to components."""
        for component in self._components:
            metadata = {}
            
            # Analyze content characteristics
            metadata['length'] = len(component.content)
            metadata['word_count'] = len(component.content.split())
            metadata['line_count'] = len(component.content.splitlines())
            
            # Check for special markers
            metadata['has_code_blocks'] = '```' in component.content
            metadata['has_lists'] = bool(re.search(r'^\s*[-*\d]+\.?\s', component.content, re.MULTILINE))
            metadata['has_questions'] = '?' in component.content
            metadata['has_instructions'] = any(word in component.content.lower() 
                                              for word in ['please', 'must', 'should', 'need to', 'required'])
            
            component.metadata = metadata
    
    @property
    def components(self) -> List[PromptComponent]:
        """Get the extracted components."""
        if not self._analyzed:
            self.analyze()
        return self._components
    
    @property
    def total_tokens(self) -> int:
        """Get the total token count."""
        if not self._analyzed:
            self.analyze()
        return sum(c.tokens for c in self._components)
    
    @property
    def total_length(self) -> int:
        """Get the total character length."""
        return len(self.prompt)
    
    @property
    def component_summary(self) -> Dict[str, int]:
        """Get a summary of components by role."""
        if not self._analyzed:
            self.analyze()
        summary = {}
        for component in self._components:
            summary[component.role] = summary.get(component.role, 0) + 1
        return summary
    
    def get_component_by_role(self, role: str) -> List[PromptComponent]:
        """
        Get all components with a specific role.
        
        Args:
            role: The role to filter by (system, user, assistant)
            
        Returns:
            List of components with the specified role
        """
        if not self._analyzed:
            self.analyze()
        return [c for c in self._components if c.role == role]
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the autopsy results to a dictionary.
        
        Returns:
            Dictionary representation of the autopsy
        """
        if not self._analyzed:
            self.analyze()
        
        return {
            'timestamp': self.timestamp.isoformat(),
            'prompt_length': self.total_length,
            'total_tokens': self.total_tokens,
            'component_summary': self.component_summary,
            'components': [
                {
                    'role': c.role,
                    'content': c.content,
                    'tokens': c.tokens,
                    'metadata': c.metadata
                }
                for c in self._components
            ],
            'metadata': self.metadata
        }
