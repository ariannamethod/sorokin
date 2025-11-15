"""
Advanced prompt analysis functionality.
"""

from typing import Dict, List, Any
from .autopsy import PromptAutopsy
import re


class PromptAnalyzer:
    """
    Provides advanced analysis capabilities for prompts.
    """
    
    # Compiled regex patterns for better performance
    _WORD_PATTERN = re.compile(r'\b[a-z]{3,}\b')
    
    @staticmethod
    def analyze_complexity(autopsy: PromptAutopsy) -> Dict[str, Any]:
        """
        Analyze the complexity of a prompt.
        
        Args:
            autopsy: PromptAutopsy instance to analyze
            
        Returns:
            Dictionary with complexity metrics
        """
        components = autopsy.components
        
        # Calculate average sentence length
        total_sentences = 0
        total_words = 0
        
        for component in components:
            sentences = re.split(r'[.!?]+', component.content)
            sentences = [s for s in sentences if s.strip()]
            total_sentences += len(sentences)
            total_words += component.metadata.get('word_count', 0)
        
        avg_sentence_length = total_words / max(total_sentences, 1)
        
        # Calculate nesting depth (based on parentheses, brackets, etc.)
        max_nesting = 0
        for component in components:
            current_depth = 0
            max_depth = 0
            for char in component.content:
                if char in '([{':
                    current_depth += 1
                    max_depth = max(max_depth, current_depth)
                elif char in ')]}':
                    current_depth = max(0, current_depth - 1)
            max_nesting = max(max_nesting, max_depth)
        
        # Determine complexity level
        complexity_score = 0
        if avg_sentence_length > 25:
            complexity_score += 1
        if max_nesting > 2:
            complexity_score += 1
        if autopsy.total_tokens > 500:
            complexity_score += 1
        if len(components) > 3:
            complexity_score += 1
        
        if complexity_score <= 1:
            level = "low"
        elif complexity_score <= 2:
            level = "medium"
        else:
            level = "high"
        
        return {
            'level': level,
            'score': complexity_score,
            'avg_sentence_length': round(avg_sentence_length, 2),
            'max_nesting_depth': max_nesting,
            'total_components': len(components)
        }
    
    @staticmethod
    def extract_keywords(autopsy: PromptAutopsy, top_n: int = 10) -> List[tuple]:
        """
        Extract the most common keywords from the prompt.
        
        Args:
            autopsy: PromptAutopsy instance to analyze
            top_n: Number of top keywords to return
            
        Returns:
            List of (word, count) tuples
        """
        # Combine all component content
        text = ' '.join(c.content for c in autopsy.components)
        
        # Extract words (excluding common stop words)
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
            'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
            'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this',
            'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they',
            'their', 'them', 'who', 'what', 'when', 'where', 'why', 'how', 'all',
            'each', 'every', 'both', 'few', 'more', 'most', 'other', 'some', 'such',
            'about', 'into', 'through', 'during', 'before', 'after', 'above', 'below'
        }
        
        words = PromptAnalyzer._WORD_PATTERN.findall(text.lower())
        word_freq = {}
        
        for word in words:
            if word not in stop_words:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Sort by frequency
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return sorted_words[:top_n]
    
    @staticmethod
    def detect_patterns(autopsy: PromptAutopsy) -> Dict[str, bool]:
        """
        Detect common patterns in the prompt.
        
        Args:
            autopsy: PromptAutopsy instance to analyze
            
        Returns:
            Dictionary of detected patterns
        """
        patterns = {
            'has_examples': False,
            'has_constraints': False,
            'has_format_specification': False,
            'has_role_playing': False,
            'has_chain_of_thought': False,
            'has_few_shot': False
        }
        
        combined_text = ' '.join(c.content for c in autopsy.components).lower()
        
        # Check for examples
        if re.search(r'\bexample[s]?:', combined_text) or \
           re.search(r'\be\.g\.', combined_text) or \
           re.search(r'\bfor instance', combined_text):
            patterns['has_examples'] = True
        
        # Check for constraints
        if re.search(r"\bmust not\b|\bdon't\b|\bdo not\b|\bshould not\b", combined_text) or \
           re.search(r'\bconstraint[s]?:', combined_text):
            patterns['has_constraints'] = True
        
        # Check for format specification
        if re.search(r'\bformat[:]?', combined_text) or \
           re.search(r'\bjson\b|\bxml\b|\byaml\b|\bmarkdown\b', combined_text) or \
           '```' in combined_text:
            patterns['has_format_specification'] = True
        
        # Check for role playing
        if re.search(r'\byou are\b|\bact as\b|\bpretend\b|\brole[:]?', combined_text):
            patterns['has_role_playing'] = True
        
        # Check for chain of thought
        if re.search(r"\bstep by step\b|\bthink through\b|\breasoning\b|\blet's think\b", combined_text):
            patterns['has_chain_of_thought'] = True
        
        # Check for few-shot (multiple examples)
        example_count = len(re.findall(r'\bexample\s*\d+', combined_text))
        if example_count >= 2:
            patterns['has_few_shot'] = True
        
        return patterns
    
    @staticmethod
    def analyze_sentiment(autopsy: PromptAutopsy) -> Dict[str, Any]:
        """
        Perform basic sentiment analysis on the prompt.
        
        Args:
            autopsy: PromptAutopsy instance to analyze
            
        Returns:
            Dictionary with sentiment information
        """
        positive_words = {
            'good', 'great', 'excellent', 'best', 'please', 'thank', 'helpful',
            'wonderful', 'fantastic', 'amazing', 'positive', 'beneficial'
        }
        
        negative_words = {
            'bad', 'wrong', 'error', 'fail', 'failure', 'problem', 'issue',
            'incorrect', 'mistake', 'avoid', 'never', 'not', 'negative'
        }
        
        command_words = {
            'must', 'shall', 'need', 'require', 'should', 'have to',
            'necessary', 'mandatory', 'obligatory', 'compulsory'
        }
        
        combined_text = ' '.join(c.content for c in autopsy.components).lower()
        words = re.findall(r'\b[a-z]+\b', combined_text)
        
        positive_count = sum(1 for word in words if word in positive_words)
        negative_count = sum(1 for word in words if word in negative_words)
        command_count = sum(1 for word in words if word in command_words)
        
        total_sentiment_words = positive_count + negative_count
        
        if total_sentiment_words == 0:
            tone = 'neutral'
            polarity = 0
        else:
            polarity = (positive_count - negative_count) / total_sentiment_words
            if polarity > 0.2:
                tone = 'positive'
            elif polarity < -0.2:
                tone = 'negative'
            else:
                tone = 'neutral'
        
        # Determine if prompt is imperative
        is_imperative = command_count > 2 or command_count / max(len(words), 1) > 0.02
        
        return {
            'tone': tone,
            'polarity': round(polarity, 3),
            'positive_words': positive_count,
            'negative_words': negative_count,
            'command_words': command_count,
            'is_imperative': is_imperative
        }
