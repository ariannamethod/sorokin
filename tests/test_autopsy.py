"""Tests for the PromptAutopsy class."""

from sorokin.autopsy import PromptAutopsy


class TestPromptAutopsy:
    """Test cases for PromptAutopsy."""
    
    def test_simple_prompt_analysis(self):
        """Test analysis of a simple unstructured prompt."""
        prompt = "Please write a story about a robot learning to love."
        autopsy = PromptAutopsy(prompt)
        autopsy.analyze()
        
        assert autopsy.total_length == len(prompt)
        assert autopsy.total_tokens > 0
        assert len(autopsy.components) == 1
        assert autopsy.components[0].role == "user"
    
    def test_structured_prompt_analysis(self):
        """Test analysis of a structured prompt with roles."""
        prompt = """system: You are a helpful assistant.
user: What is the capital of France?
assistant: The capital of France is Paris.
user: Thank you!"""
        
        autopsy = PromptAutopsy(prompt)
        autopsy.analyze()
        
        assert len(autopsy.components) == 4
        assert autopsy.component_summary == {'system': 1, 'user': 2, 'assistant': 1}
    
    def test_token_counting(self):
        """Test token counting approximation."""
        prompt = "This is a test prompt with exactly ten words here."
        autopsy = PromptAutopsy(prompt)
        autopsy.analyze()
        
        # Should have approximately 10 tokens
        assert 8 <= autopsy.total_tokens <= 12
    
    def test_component_metadata(self):
        """Test that component metadata is correctly generated."""
        prompt = "user: Can you help me?\nThis is a question."
        autopsy = PromptAutopsy(prompt)
        autopsy.analyze()
        
        component = autopsy.components[0]
        assert 'length' in component.metadata
        assert 'word_count' in component.metadata
        assert 'line_count' in component.metadata
        assert 'has_questions' in component.metadata
        assert component.metadata['has_questions'] is True
    
    def test_code_block_detection(self):
        """Test detection of code blocks."""
        prompt = "user: Here's some code:\n```python\nprint('hello')\n```"
        autopsy = PromptAutopsy(prompt)
        autopsy.analyze()
        
        assert autopsy.components[0].metadata['has_code_blocks'] is True
    
    def test_list_detection(self):
        """Test detection of lists."""
        prompt = "user: Items:\n- First item\n- Second item\n* Third item"
        autopsy = PromptAutopsy(prompt)
        autopsy.analyze()
        
        assert autopsy.components[0].metadata['has_lists'] is True
    
    def test_instruction_detection(self):
        """Test detection of instructions."""
        prompt = "user: Please write a function. You must follow these rules."
        autopsy = PromptAutopsy(prompt)
        autopsy.analyze()
        
        assert autopsy.components[0].metadata['has_instructions'] is True
    
    def test_get_component_by_role(self):
        """Test filtering components by role."""
        prompt = """system: System message
user: User message 1
user: User message 2"""
        
        autopsy = PromptAutopsy(prompt)
        autopsy.analyze()
        
        user_components = autopsy.get_component_by_role('user')
        assert len(user_components) == 2
        assert all(c.role == 'user' for c in user_components)
    
    def test_to_dict(self):
        """Test conversion to dictionary."""
        prompt = "user: Test prompt"
        autopsy = PromptAutopsy(prompt, metadata={'source': 'test'})
        result = autopsy.to_dict()
        
        assert 'timestamp' in result
        assert 'prompt_length' in result
        assert 'total_tokens' in result
        assert 'component_summary' in result
        assert 'components' in result
        assert 'metadata' in result
        assert result['metadata']['source'] == 'test'
    
    def test_lazy_analysis(self):
        """Test that analysis happens lazily when accessing properties."""
        prompt = "user: Test"
        autopsy = PromptAutopsy(prompt)
        
        # Accessing properties should trigger analysis
        _ = autopsy.components
        assert autopsy._analyzed is True
    
    def test_empty_prompt(self):
        """Test handling of empty prompt."""
        prompt = ""
        autopsy = PromptAutopsy(prompt)
        autopsy.analyze()
        
        assert autopsy.total_length == 0
        assert len(autopsy.components) == 1  # Should create one empty user component
    
    def test_multiline_component(self):
        """Test handling of multiline components."""
        prompt = """user: This is a long prompt
that spans multiple lines
and has several sentences."""
        
        autopsy = PromptAutopsy(prompt)
        autopsy.analyze()
        
        assert autopsy.components[0].metadata['line_count'] == 3
    
    def test_bracket_style_roles(self):
        """Test parsing of bracket-style role markers."""
        prompt = "[system] System message\n[user] User message"
        autopsy = PromptAutopsy(prompt)
        autopsy.analyze()
        
        assert len(autopsy.components) == 2
        assert autopsy.components[0].role == 'system'
        assert autopsy.components[1].role == 'user'
    
    def test_angle_bracket_style_roles(self):
        """Test parsing of angle bracket-style role markers."""
        prompt = "<system>System message\n<user>User message"
        autopsy = PromptAutopsy(prompt)
        autopsy.analyze()
        
        assert len(autopsy.components) == 2
        assert autopsy.components[0].role == 'system'
        assert autopsy.components[1].role == 'user'
