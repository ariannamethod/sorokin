# Examples

This directory contains example scripts demonstrating the usage of the Sorokin Prompt Autopsy Engine.

## Running the Examples

Make sure you have installed the package first:

```bash
cd /home/runner/work/sorokin/sorokin
pip install -e .
```

Then run any example:

```bash
python examples/basic_usage.py
```

## Available Examples

### basic_usage.py

Demonstrates:
- Simple prompt analysis
- Structured prompts with multiple roles
- Advanced analysis features (complexity, patterns, sentiment)
- Report generation in different formats

Run it:
```bash
python examples/basic_usage.py
```

## Creating Your Own Examples

Feel free to create your own examples based on these templates. The basic structure is:

```python
from sorokin import PromptAutopsy, AutopsyReport, PromptAnalyzer

# 1. Create an autopsy with your prompt
prompt = "Your prompt text here"
autopsy = PromptAutopsy(prompt)
autopsy.analyze()

# 2. Access basic results
print(f"Tokens: {autopsy.total_tokens}")
print(f"Components: {autopsy.component_summary}")

# 3. Perform advanced analysis
complexity = PromptAnalyzer.analyze_complexity(autopsy)
patterns = PromptAnalyzer.detect_patterns(autopsy)
keywords = PromptAnalyzer.extract_keywords(autopsy)

# 4. Generate reports
report = AutopsyReport(autopsy)
print(report.to_text())
```
