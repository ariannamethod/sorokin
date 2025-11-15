"""Tests for the PromptAnalyzer class."""

import pytest
from sorokin.autopsy import PromptAutopsy
from sorokin.analyzer import PromptAnalyzer


class TestPromptAnalyzer:
    """Test cases for PromptAnalyzer."""
    
    def test_analyze_complexity_low(self):
        """Test complexity analysis for a simple prompt."""
        prompt = "user: Hello. How are you?"
        autopsy = PromptAutopsy(prompt)
        autopsy.analyze()
        
        complexity = PromptAnalyzer.analyze_complexity(autopsy)
        
        assert 'level' in complexity
        assert 'score' in complexity
        assert complexity['level'] in ['low', 'medium', 'high']
    
    def test_analyze_complexity_high(self):
        """Test complexity analysis for a complex prompt."""
        prompt = """system: You are an expert.
user: """ + " ".join(["word"] * 600) + """
user: Additional complex instructions with nested (parentheses (and more (nesting)))"""
        
        autopsy = PromptAutopsy(prompt)
        autopsy.analyze()
        
        complexity = PromptAnalyzer.analyze_complexity(autopsy)
        
        assert complexity['level'] in ['medium', 'high']
        assert complexity['max_nesting_depth'] > 0
    
    def test_extract_keywords(self):
        """Test keyword extraction."""
        prompt = "user: Python is great. Python is powerful. Python is easy to learn."
        autopsy = PromptAutopsy(prompt)
        autopsy.analyze()
        
        keywords = PromptAnalyzer.extract_keywords(autopsy, top_n=5)
        
        assert len(keywords) <= 5
        assert isinstance(keywords, list)
        # 'python' should be the top keyword
        if keywords:
            assert keywords[0][0] == 'python'
            assert keywords[0][1] == 3
    
    def test_extract_keywords_filters_stopwords(self):
        """Test that stop words are filtered out."""
        prompt = "user: The cat and the dog are friends."
        autopsy = PromptAutopsy(prompt)
        autopsy.analyze()
        
        keywords = PromptAnalyzer.extract_keywords(autopsy)
        keyword_words = [word for word, _ in keywords]
        
        # Stop words like 'the', 'and', 'are' should not be in keywords
        assert 'the' not in keyword_words
        assert 'and' not in keyword_words
        assert 'are' not in keyword_words
    
    def test_detect_patterns_examples(self):
        """Test detection of example patterns."""
        prompt = "user: Here's an example: 2 + 2 = 4. For instance, you can add numbers."
        autopsy = PromptAutopsy(prompt)
        autopsy.analyze()
        
        patterns = PromptAnalyzer.detect_patterns(autopsy)
        
        assert patterns['has_examples'] is True
    
    def test_detect_patterns_constraints(self):
        """Test detection of constraint patterns."""
        prompt = "user: You must not use offensive language. Don't include personal data."
        autopsy = PromptAutopsy(prompt)
        autopsy.analyze()
        
        patterns = PromptAnalyzer.detect_patterns(autopsy)
        
        assert patterns['has_constraints'] is True
    
    def test_detect_patterns_format(self):
        """Test detection of format specification patterns."""
        prompt = "user: Return the result in JSON format:\n```json\n{}\n```"
        autopsy = PromptAutopsy(prompt)
        autopsy.analyze()
        
        patterns = PromptAnalyzer.detect_patterns(autopsy)
        
        assert patterns['has_format_specification'] is True
    
    def test_detect_patterns_role_playing(self):
        """Test detection of role-playing patterns."""
        prompt = "system: You are a pirate. Act as a swashbuckling captain."
        autopsy = PromptAutopsy(prompt)
        autopsy.analyze()
        
        patterns = PromptAnalyzer.detect_patterns(autopsy)
        
        assert patterns['has_role_playing'] is True
    
    def test_detect_patterns_chain_of_thought(self):
        """Test detection of chain-of-thought patterns."""
        prompt = "user: Let's think step by step about this problem."
        autopsy = PromptAutopsy(prompt)
        autopsy.analyze()
        
        patterns = PromptAnalyzer.detect_patterns(autopsy)
        
        assert patterns['has_chain_of_thought'] is True
    
    def test_detect_patterns_few_shot(self):
        """Test detection of few-shot patterns."""
        prompt = """user: Example 1: Input A -> Output B
Example 2: Input C -> Output D
Example 3: Input E -> Output F"""
        autopsy = PromptAutopsy(prompt)
        autopsy.analyze()
        
        patterns = PromptAnalyzer.detect_patterns(autopsy)
        
        assert patterns['has_few_shot'] is True
    
    def test_analyze_sentiment_positive(self):
        """Test sentiment analysis for positive tone."""
        prompt = "user: Please help me. Thank you! This is great."
        autopsy = PromptAutopsy(prompt)
        autopsy.analyze()
        
        sentiment = PromptAnalyzer.analyze_sentiment(autopsy)
        
        assert sentiment['tone'] == 'positive'
        assert sentiment['polarity'] > 0
        assert sentiment['positive_words'] > 0
    
    def test_analyze_sentiment_negative(self):
        """Test sentiment analysis for negative tone."""
        prompt = "user: This is wrong. Bad mistake. Error in the code. Problem detected."
        autopsy = PromptAutopsy(prompt)
        autopsy.analyze()
        
        sentiment = PromptAnalyzer.analyze_sentiment(autopsy)
        
        assert sentiment['tone'] == 'negative'
        assert sentiment['polarity'] < 0
        assert sentiment['negative_words'] > 0
    
    def test_analyze_sentiment_neutral(self):
        """Test sentiment analysis for neutral tone."""
        prompt = "user: What is the capital of France?"
        autopsy = PromptAutopsy(prompt)
        autopsy.analyze()
        
        sentiment = PromptAnalyzer.analyze_sentiment(autopsy)
        
        assert sentiment['tone'] == 'neutral'
    
    def test_analyze_sentiment_imperative(self):
        """Test detection of imperative tone."""
        prompt = "user: You must complete this task. It is required and necessary. You should follow these rules."
        autopsy = PromptAutopsy(prompt)
        autopsy.analyze()
        
        sentiment = PromptAnalyzer.analyze_sentiment(autopsy)
        
        assert sentiment['is_imperative'] is True
        assert sentiment['command_words'] > 0
    
    def test_all_patterns_false(self):
        """Test that patterns are false when not present."""
        prompt = "user: Simple question here."
        autopsy = PromptAutopsy(prompt)
        autopsy.analyze()
        
        patterns = PromptAnalyzer.detect_patterns(autopsy)
        
        # Most patterns should be false for a simple prompt
        assert patterns['has_examples'] is False
        assert patterns['has_few_shot'] is False
