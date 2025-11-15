"""Integration tests for the entire prompt autopsy engine."""

import json
from sorokin import PromptAutopsy, AutopsyReport, PromptAnalyzer


class TestIntegration:
    """End-to-end integration tests."""
    
    def test_full_workflow_simple_prompt(self):
        """Test complete workflow with a simple prompt."""
        prompt = "user: What is machine learning?"
        
        # Create and analyze
        autopsy = PromptAutopsy(prompt)
        autopsy.analyze()
        
        # Should have basic results
        assert autopsy.total_tokens > 0
        assert autopsy.total_length > 0
        assert len(autopsy.components) > 0
        
        # Generate report
        report = AutopsyReport(autopsy)
        result = report.generate()
        
        # Should have all expected sections
        assert 'timestamp' in result
        assert 'components' in result
        assert 'analysis' in result
        
        # All output formats should work
        json_output = report.to_json()
        assert json.loads(json_output)  # Valid JSON
        
        markdown = report.to_markdown()
        assert '# Prompt Autopsy Report' in markdown
        
        text = report.to_text()
        assert 'PROMPT AUTOPSY REPORT' in text
    
    def test_full_workflow_complex_prompt(self):
        """Test complete workflow with a complex structured prompt."""
        prompt = """system: You are an AI assistant specializing in data science.

user: Can you help me build a machine learning model?
I need to:
- Load data from CSV
- Preprocess the data
- Train a classification model
- Evaluate performance

Example workflow:
1. Load data: pandas.read_csv()
2. Split data: train_test_split()
3. Train: model.fit()

Please provide code in Python with comments.
"""
        
        # Full analysis
        autopsy = PromptAutopsy(prompt)
        autopsy.analyze()
        
        # Verify component extraction
        assert len(autopsy.components) == 2
        assert autopsy.component_summary['system'] == 1
        assert autopsy.component_summary['user'] == 1
        
        # Verify advanced analysis
        complexity = PromptAnalyzer.analyze_complexity(autopsy)
        assert complexity['level'] in ['low', 'medium', 'high']
        assert 0 <= complexity['score'] <= 4
        
        patterns = PromptAnalyzer.detect_patterns(autopsy)
        # The prompt has role-playing pattern
        assert patterns['has_role_playing'] is True
        # Check that pattern detection is working
        assert isinstance(patterns, dict)
        assert all(isinstance(v, bool) for v in patterns.values())
        
        sentiment = PromptAnalyzer.analyze_sentiment(autopsy)
        assert sentiment['tone'] in ['positive', 'neutral', 'negative']
        
        keywords = PromptAnalyzer.extract_keywords(autopsy)
        assert len(keywords) > 0
        assert all(isinstance(kw, tuple) and len(kw) == 2 for kw in keywords)
        
        # Generate comprehensive report
        report = AutopsyReport(autopsy)
        full_report = report.generate(include_analysis=True)
        
        # Verify report structure
        assert 'analysis' in full_report
        assert 'complexity' in full_report['analysis']
        assert 'patterns' in full_report['analysis']
        assert 'sentiment' in full_report['analysis']
        assert 'keywords' in full_report['analysis']
    
    def test_end_to_end_with_metadata(self):
        """Test workflow including custom metadata."""
        prompt = "user: Hello world"
        metadata = {
            'source': 'test_suite',
            'version': '1.0',
            'author': 'test_user'
        }
        
        autopsy = PromptAutopsy(prompt, metadata=metadata)
        autopsy.analyze()
        
        report = AutopsyReport(autopsy)
        result = report.generate()
        
        # Metadata should be preserved
        assert result['metadata']['source'] == 'test_suite'
        assert result['metadata']['version'] == '1.0'
        assert result['metadata']['author'] == 'test_user'
    
    def test_multiple_prompts_analysis(self):
        """Test analyzing multiple prompts in sequence."""
        prompts = [
            "user: Simple question?",
            "system: You are helpful.\nuser: Complex question with context?",
            "user: " + "word " * 100  # Long prompt
        ]
        
        autopsies = []
        for prompt in prompts:
            autopsy = PromptAutopsy(prompt)
            autopsy.analyze()
            autopsies.append(autopsy)
        
        # Verify each autopsy is independent
        assert len(autopsies) == 3
        assert autopsies[0].total_tokens != autopsies[2].total_tokens
        assert len(autopsies[1].components) == 2
        
        # Generate reports for all
        reports = [AutopsyReport(a) for a in autopsies]
        outputs = [r.to_json() for r in reports]
        
        # All should be valid JSON
        for output in outputs:
            parsed = json.loads(output)
            assert 'total_tokens' in parsed
    
    def test_component_filtering_and_analysis(self):
        """Test filtering components and analyzing specific parts."""
        prompt = """system: System instructions here.
user: First user message.
assistant: Assistant response.
user: Follow-up question."""
        
        autopsy = PromptAutopsy(prompt)
        autopsy.analyze()
        
        # Filter by role
        user_components = autopsy.get_component_by_role('user')
        system_components = autopsy.get_component_by_role('system')
        
        assert len(user_components) == 2
        assert len(system_components) == 1
        
        # Analyze specific components
        for component in user_components:
            assert component.role == 'user'
            assert component.tokens > 0
            assert 'length' in component.metadata
    
    def test_report_format_consistency(self):
        """Test that all report formats contain consistent information."""
        prompt = """user: Test prompt with various features:
- Lists
- Code blocks: ```python\nprint('test')\n```
- Questions?
- Instructions: please follow these steps"""
        
        autopsy = PromptAutopsy(prompt)
        autopsy.analyze()
        
        report = AutopsyReport(autopsy)
        
        # Get all formats
        json_str = report.to_json()
        markdown_str = report.to_markdown()
        text_str = report.to_text()
        
        # Parse JSON
        json_data = json.loads(json_str)
        
        # All formats should reference the same token count
        token_count = str(autopsy.total_tokens)
        assert token_count in text_str
        assert token_count in markdown_str
        
        # All formats should mention components
        assert 'component' in text_str.lower()
        assert 'component' in markdown_str.lower()
        assert 'components' in json_data
    
    def test_error_handling_empty_prompt(self):
        """Test handling of edge cases like empty prompts."""
        prompt = ""
        
        # Should not raise an error
        autopsy = PromptAutopsy(prompt)
        autopsy.analyze()
        
        assert autopsy.total_length == 0
        assert len(autopsy.components) >= 0
        
        # Report should still be generated
        report = AutopsyReport(autopsy)
        json_output = report.to_json()
        assert json.loads(json_output)  # Valid JSON
    
    def test_pattern_detection_accuracy(self):
        """Test that pattern detection is working correctly."""
        # Prompt with known patterns
        prompt_with_patterns = """user: You are a teacher. Act as an educator.
Let's think step by step about this problem.
Example 1: 2 + 2 = 4
Example 2: 3 + 3 = 6
You must not provide answers directly.
Format: Return results as JSON."""
        
        autopsy = PromptAutopsy(prompt_with_patterns)
        autopsy.analyze()
        
        patterns = PromptAnalyzer.detect_patterns(autopsy)
        
        # Should detect multiple patterns
        assert patterns['has_role_playing'] is True
        assert patterns['has_chain_of_thought'] is True
        assert patterns['has_few_shot'] is True
        assert patterns['has_constraints'] is True
        assert patterns['has_format_specification'] is True
        
        # Prompt without patterns
        prompt_without_patterns = "What is the weather?"
        autopsy2 = PromptAutopsy(prompt_without_patterns)
        autopsy2.analyze()
        
        patterns2 = PromptAnalyzer.detect_patterns(autopsy2)
        
        # Most patterns should be false
        false_count = sum(1 for v in patterns2.values() if not v)
        assert false_count >= 4  # At least 4 patterns should be false
