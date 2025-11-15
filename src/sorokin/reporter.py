"""
Report generation for autopsy results.
"""

from typing import Dict, Any, Optional
from .autopsy import PromptAutopsy
from .analyzer import PromptAnalyzer
import json


class AutopsyReport:
    """
    Generates formatted reports from autopsy results.
    """
    
    def __init__(self, autopsy: PromptAutopsy):
        """
        Initialize report with an autopsy.
        
        Args:
            autopsy: PromptAutopsy instance to report on
        """
        self.autopsy = autopsy
        self.analyzer = PromptAnalyzer()
    
    def generate(self, include_analysis: bool = True) -> Dict[str, Any]:
        """
        Generate a complete report.
        
        Args:
            include_analysis: Whether to include advanced analysis
            
        Returns:
            Dictionary with complete report data
        """
        report = self.autopsy.to_dict()
        
        if include_analysis:
            report['analysis'] = {
                'complexity': self.analyzer.analyze_complexity(self.autopsy),
                'keywords': self.analyzer.extract_keywords(self.autopsy),
                'patterns': self.analyzer.detect_patterns(self.autopsy),
                'sentiment': self.analyzer.analyze_sentiment(self.autopsy)
            }
        
        return report
    
    def to_json(self, indent: Optional[int] = 2, include_analysis: bool = True) -> str:
        """
        Generate JSON report.
        
        Args:
            indent: JSON indentation level (None for compact)
            include_analysis: Whether to include advanced analysis
            
        Returns:
            JSON string
        """
        return json.dumps(self.generate(include_analysis=include_analysis), indent=indent)
    
    def to_markdown(self, include_analysis: bool = True) -> str:
        """
        Generate Markdown report.
        
        Args:
            include_analysis: Whether to include advanced analysis
            
        Returns:
            Markdown formatted string
        """
        report = self.generate(include_analysis=include_analysis)
        
        lines = [
            "# Prompt Autopsy Report",
            "",
            f"**Timestamp:** {report['timestamp']}",
            f"**Total Length:** {report['prompt_length']} characters",
            f"**Total Tokens:** {report['total_tokens']} (estimated)",
            "",
            "## Components",
            ""
        ]
        
        for role, count in report['component_summary'].items():
            lines.append(f"- **{role.capitalize()}:** {count} component(s)")
        
        lines.extend(["", "## Detailed Components", ""])
        
        for i, component in enumerate(report['components'], 1):
            lines.extend([
                f"### Component {i}: {component['role'].capitalize()}",
                "",
                f"**Tokens:** {component['tokens']}",
                f"**Length:** {component['metadata']['length']} characters",
                f"**Lines:** {component['metadata']['line_count']}",
                "",
                "**Content Preview:**",
                "```",
                component['content'][:200] + ("..." if len(component['content']) > 200 else ""),
                "```",
                ""
            ])
        
        if 'analysis' in report:
            analysis = report['analysis']
            
            lines.extend([
                "## Analysis",
                "",
                "### Complexity",
                f"- **Level:** {analysis['complexity']['level']}",
                f"- **Score:** {analysis['complexity']['score']}/4",
                f"- **Average Sentence Length:** {analysis['complexity']['avg_sentence_length']} words",
                "",
                "### Patterns Detected",
                ""
            ])
            
            for pattern, detected in analysis['patterns'].items():
                status = "✓" if detected else "✗"
                pattern_name = pattern.replace('_', ' ').title()
                lines.append(f"- {status} {pattern_name}")
            
            lines.extend([
                "",
                "### Sentiment",
                f"- **Tone:** {analysis['sentiment']['tone']}",
                f"- **Polarity:** {analysis['sentiment']['polarity']}",
                f"- **Is Imperative:** {'Yes' if analysis['sentiment']['is_imperative'] else 'No'}",
                "",
                "### Top Keywords",
                ""
            ])
            
            for word, count in analysis['keywords'][:5]:
                lines.append(f"- **{word}**: {count} occurrences")
        
        return '\n'.join(lines)
    
    def to_text(self, include_analysis: bool = True) -> str:
        """
        Generate plain text report.
        
        Args:
            include_analysis: Whether to include advanced analysis
            
        Returns:
            Plain text formatted string
        """
        report = self.generate(include_analysis=include_analysis)
        
        lines = [
            "=" * 60,
            "PROMPT AUTOPSY REPORT",
            "=" * 60,
            "",
            f"Timestamp: {report['timestamp']}",
            f"Total Length: {report['prompt_length']} characters",
            f"Total Tokens: {report['total_tokens']} (estimated)",
            "",
            "COMPONENTS",
            "-" * 60
        ]
        
        for role, count in report['component_summary'].items():
            lines.append(f"  {role.capitalize()}: {count} component(s)")
        
        lines.extend(["", "DETAILED COMPONENTS", "-" * 60])
        
        for i, component in enumerate(report['components'], 1):
            content_preview = component['content'][:100]
            if len(component['content']) > 100:
                content_preview += "..."
            lines.extend([
                "",
                f"Component {i}: {component['role'].upper()}",
                f"  Tokens: {component['tokens']}",
                f"  Length: {component['metadata']['length']} characters",
                f"  Lines: {component['metadata']['line_count']}",
                f"  Content: {content_preview}",
                ""
            ])
        
        if 'analysis' in report:
            analysis = report['analysis']
            
            lines.extend([
                "",
                "ANALYSIS",
                "-" * 60,
                "",
                f"Complexity: {analysis['complexity']['level']} (score: {analysis['complexity']['score']}/4)",
                f"Tone: {analysis['sentiment']['tone']}",
                f"Imperative: {'Yes' if analysis['sentiment']['is_imperative'] else 'No'}",
                "",
                "Patterns:",
            ])
            
            for pattern, detected in analysis['patterns'].items():
                if detected:
                    pattern_name = pattern.replace('_', ' ').title()
                    lines.append(f"  + {pattern_name}")
            
            lines.extend(["", "Top Keywords:"])
            for word, count in analysis['keywords'][:5]:
                lines.append(f"  - {word}: {count}")
        
        lines.append("\n" + "=" * 60)
        
        return '\n'.join(lines)
