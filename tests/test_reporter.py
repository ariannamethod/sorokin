"""Tests for the AutopsyReport class."""

import pytest
import json
from sorokin.autopsy import PromptAutopsy
from sorokin.reporter import AutopsyReport


class TestAutopsyReport:
    """Test cases for AutopsyReport."""
    
    def test_generate_basic_report(self):
        """Test basic report generation."""
        prompt = "user: Test prompt"
        autopsy = PromptAutopsy(prompt)
        autopsy.analyze()
        
        report = AutopsyReport(autopsy)
        result = report.generate(include_analysis=False)
        
        assert 'timestamp' in result
        assert 'prompt_length' in result
        assert 'total_tokens' in result
        assert 'components' in result
    
    def test_generate_with_analysis(self):
        """Test report generation with analysis."""
        prompt = "user: Test prompt for analysis"
        autopsy = PromptAutopsy(prompt)
        autopsy.analyze()
        
        report = AutopsyReport(autopsy)
        result = report.generate(include_analysis=True)
        
        assert 'analysis' in result
        assert 'complexity' in result['analysis']
        assert 'keywords' in result['analysis']
        assert 'patterns' in result['analysis']
        assert 'sentiment' in result['analysis']
    
    def test_to_json(self):
        """Test JSON report generation."""
        prompt = "user: Test prompt"
        autopsy = PromptAutopsy(prompt)
        autopsy.analyze()
        
        report = AutopsyReport(autopsy)
        json_output = report.to_json()
        
        # Should be valid JSON
        parsed = json.loads(json_output)
        assert isinstance(parsed, dict)
        assert 'components' in parsed
    
    def test_to_json_compact(self):
        """Test compact JSON generation."""
        prompt = "user: Test"
        autopsy = PromptAutopsy(prompt)
        autopsy.analyze()
        
        report = AutopsyReport(autopsy)
        json_output = report.to_json(indent=None)
        
        # Should not have newlines (compact)
        assert '\n' not in json_output or json_output.count('\n') < 5
    
    def test_to_markdown(self):
        """Test Markdown report generation."""
        prompt = "user: Test prompt"
        autopsy = PromptAutopsy(prompt)
        autopsy.analyze()
        
        report = AutopsyReport(autopsy)
        markdown = report.to_markdown()
        
        assert '# Prompt Autopsy Report' in markdown
        assert '## Components' in markdown
        assert '## Analysis' in markdown
        assert '**' in markdown  # Bold text
    
    def test_to_markdown_with_components(self):
        """Test Markdown report with multiple components."""
        prompt = """system: System message
user: User message"""
        autopsy = PromptAutopsy(prompt)
        autopsy.analyze()
        
        report = AutopsyReport(autopsy)
        markdown = report.to_markdown()
        
        assert 'Component 1' in markdown
        assert 'Component 2' in markdown
        assert 'System' in markdown or 'system' in markdown
    
    def test_to_text(self):
        """Test plain text report generation."""
        prompt = "user: Test prompt"
        autopsy = PromptAutopsy(prompt)
        autopsy.analyze()
        
        report = AutopsyReport(autopsy)
        text = report.to_text()
        
        assert 'PROMPT AUTOPSY REPORT' in text
        assert 'COMPONENTS' in text
        assert 'ANALYSIS' in text
        assert '=' in text  # Should have separator lines
    
    def test_to_text_formatting(self):
        """Test text report formatting."""
        prompt = """user: Test prompt with multiple features.
This includes questions? And lists:
- Item 1
- Item 2"""
        autopsy = PromptAutopsy(prompt)
        autopsy.analyze()
        
        report = AutopsyReport(autopsy)
        text = report.to_text()
        
        # Should have proper formatting
        assert '=' * 60 in text  # Header separator
        assert '-' * 60 in text  # Section separator
    
    def test_report_includes_patterns(self):
        """Test that report includes pattern detection."""
        prompt = "user: Example: this is a test. You must follow the format."
        autopsy = PromptAutopsy(prompt)
        autopsy.analyze()
        
        report = AutopsyReport(autopsy)
        result = report.generate(include_analysis=True)
        
        patterns = result['analysis']['patterns']
        assert 'has_examples' in patterns
        assert 'has_constraints' in patterns
    
    def test_report_includes_keywords(self):
        """Test that report includes keywords."""
        prompt = "user: Python Python Python coding programming"
        autopsy = PromptAutopsy(prompt)
        autopsy.analyze()
        
        report = AutopsyReport(autopsy)
        result = report.generate(include_analysis=True)
        
        keywords = result['analysis']['keywords']
        assert len(keywords) > 0
        assert keywords[0][0] == 'python'
    
    def test_markdown_truncates_long_content(self):
        """Test that markdown truncates very long content."""
        prompt = "user: " + "a " * 500  # Very long prompt
        autopsy = PromptAutopsy(prompt)
        autopsy.analyze()
        
        report = AutopsyReport(autopsy)
        markdown = report.to_markdown()
        
        # Should truncate with "..."
        assert '...' in markdown
    
    def test_text_shows_top_keywords(self):
        """Test that text report shows top keywords."""
        prompt = "user: test test test word word other"
        autopsy = PromptAutopsy(prompt)
        autopsy.analyze()
        
        report = AutopsyReport(autopsy)
        text = report.to_text()
        
        assert 'Top Keywords:' in text
        assert 'test' in text.lower()
