"""
Example demonstrating basic usage of the Sorokin Prompt Autopsy Engine.
"""

from sorokin import PromptAutopsy, AutopsyReport, PromptAnalyzer


def main():
    """Run example analysis on sample prompts."""
    
    # Example 1: Simple unstructured prompt
    print("=" * 70)
    print("EXAMPLE 1: Simple Prompt Analysis")
    print("=" * 70)
    
    simple_prompt = "Write a Python function to calculate factorial."
    autopsy1 = PromptAutopsy(simple_prompt)
    autopsy1.analyze()
    
    print(f"\nPrompt: {simple_prompt}")
    print(f"Tokens: {autopsy1.total_tokens}")
    print(f"Components: {autopsy1.component_summary}")
    
    # Example 2: Structured prompt with multiple roles
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Structured Prompt with Roles")
    print("=" * 70)
    
    structured_prompt = """system: You are a helpful coding assistant.
user: Can you write a sorting algorithm?
assistant: I'd be happy to help! What type of sorting would you like?
user: Let's do quicksort, please include comments."""
    
    autopsy2 = PromptAutopsy(structured_prompt)
    autopsy2.analyze()
    
    print(f"\nComponents breakdown:")
    for i, component in enumerate(autopsy2.components, 1):
        print(f"  {i}. {component.role.upper()}: {component.tokens} tokens")
    
    # Example 3: Complex prompt with analysis
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Advanced Analysis")
    print("=" * 70)
    
    complex_prompt = """system: You are an expert Python developer.

user: Please write a comprehensive function for data validation.
The function must:
- Accept a dictionary as input
- Validate against a schema
- Return validation errors if any
- Should not raise exceptions

Example 1:
validate({'name': 'John'}, schema={'name': str}) -> True

Example 2:
validate({'age': 'old'}, schema={'age': int}) -> False

Format: Return the code in a markdown code block with docstrings."""
    
    autopsy3 = PromptAutopsy(complex_prompt)
    autopsy3.analyze()
    
    # Run advanced analysis
    complexity = PromptAnalyzer.analyze_complexity(autopsy3)
    patterns = PromptAnalyzer.detect_patterns(autopsy3)
    sentiment = PromptAnalyzer.analyze_sentiment(autopsy3)
    keywords = PromptAnalyzer.extract_keywords(autopsy3, top_n=5)
    
    print(f"\nComplexity: {complexity['level']} (score: {complexity['score']}/4)")
    print(f"Sentiment: {sentiment['tone']}")
    print(f"Imperative: {sentiment['is_imperative']}")
    
    print("\nPatterns detected:")
    for pattern, detected in patterns.items():
        if detected:
            print(f"  ✓ {pattern.replace('_', ' ').title()}")
    
    print("\nTop keywords:")
    for word, count in keywords:
        print(f"  - {word}: {count}")
    
    # Example 4: Generate reports
    print("\n" + "=" * 70)
    print("EXAMPLE 4: Report Generation")
    print("=" * 70)
    
    report = AutopsyReport(autopsy3)
    
    print("\n--- Text Report Preview ---")
    text_report = report.to_text()
    print('\n'.join(text_report.split('\n')[:15]))
    print("... (truncated)")
    
    print("\n--- JSON Report Available ---")
    print(f"JSON export contains {len(report.to_json())} characters")
    
    print("\n--- Markdown Report Available ---")
    print(f"Markdown export contains {len(report.to_markdown())} characters")


if __name__ == '__main__':
    main()
