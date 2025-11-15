# Sorokin - Prompt Autopsy Engine

A Python tool for analyzing and dissecting LLM prompts to understand their structure, components, and characteristics.

## Features

- 🔍 **Component Extraction**: Automatically identifies and separates system, user, and assistant messages
- 📊 **Token Counting**: Estimates token count for prompt components
- 🧠 **Complexity Analysis**: Evaluates prompt complexity with detailed metrics
- 🎯 **Pattern Detection**: Identifies common prompt engineering patterns (few-shot, chain-of-thought, etc.)
- 😊 **Sentiment Analysis**: Analyzes tone and sentiment of prompts
- 🔑 **Keyword Extraction**: Finds the most important keywords in prompts
- 📝 **Multiple Report Formats**: Generate reports in JSON, Markdown, or plain text

## Installation

```bash
# Clone the repository
git clone https://github.com/ariannamethod/sorokin.git
cd sorokin

# Install the package
pip install -e .

# Or install with development dependencies
pip install -e ".[dev]"
```

## Usage

### Command Line Interface

```bash
# Analyze a prompt from a file
sorokin prompt.txt

# Specify output format
sorokin prompt.txt --format json
sorokin prompt.txt --format markdown

# Save report to file
sorokin prompt.txt --output report.md --format markdown

# Analyze from stdin
echo "Your prompt here" | sorokin -
```

### Python API

```python
from sorokin import PromptAutopsy, AutopsyReport

# Create and analyze a prompt
prompt = """system: You are a helpful assistant.
user: Explain quantum computing in simple terms."""

autopsy = PromptAutopsy(prompt)
autopsy.analyze()

# Access analysis results
print(f"Total tokens: {autopsy.total_tokens}")
print(f"Components: {autopsy.component_summary}")

# Generate a report
report = AutopsyReport(autopsy)

# Get different format outputs
json_report = report.to_json()
markdown_report = report.to_markdown()
text_report = report.to_text()
```

### Advanced Analysis

```python
from sorokin import PromptAutopsy, PromptAnalyzer

autopsy = PromptAutopsy("Your prompt here")
autopsy.analyze()

# Analyze complexity
complexity = PromptAnalyzer.analyze_complexity(autopsy)
print(f"Complexity level: {complexity['level']}")

# Extract keywords
keywords = PromptAnalyzer.extract_keywords(autopsy, top_n=5)
print(f"Top keywords: {keywords}")

# Detect patterns
patterns = PromptAnalyzer.detect_patterns(autopsy)
print(f"Has examples: {patterns['has_examples']}")
print(f"Has chain-of-thought: {patterns['has_chain_of_thought']}")

# Analyze sentiment
sentiment = PromptAnalyzer.analyze_sentiment(autopsy)
print(f"Tone: {sentiment['tone']}")
```

## What it Analyzes

### Component Analysis
- Identifies different roles (system, user, assistant)
- Counts tokens per component
- Measures character and word counts
- Detects special features (code blocks, lists, questions)

### Complexity Metrics
- Average sentence length
- Nesting depth
- Overall complexity score (low/medium/high)
- Component count

### Pattern Detection
- **Examples**: Checks if the prompt includes examples
- **Constraints**: Identifies restrictions and rules
- **Format Specification**: Detects if output format is specified
- **Role Playing**: Identifies role-playing instructions
- **Chain of Thought**: Detects step-by-step reasoning prompts
- **Few-Shot Learning**: Identifies multiple example patterns

### Sentiment Analysis
- Tone (positive/neutral/negative)
- Polarity score
- Imperative detection (command-style prompts)
- Word counts (positive/negative/command words)

### Keyword Extraction
- Filters common stop words
- Ranks by frequency
- Returns top N keywords

## Example Output

### Text Format
```
============================================================
PROMPT AUTOPSY REPORT
============================================================

Timestamp: 2024-01-01T12:00:00.000000
Total Length: 125 characters
Total Tokens: 28 (estimated)

COMPONENTS
------------------------------------------------------------
  System: 1 component(s)
  User: 1 component(s)

ANALYSIS
------------------------------------------------------------

Complexity: medium (score: 2/4)
Tone: neutral
Imperative: No

Patterns:
  + Has Instructions
  + Has Questions

Top Keywords:
  - quantum: 2
  - computing: 2
  - explain: 1
```

### JSON Format
```json
{
  "timestamp": "2024-01-01T12:00:00.000000",
  "prompt_length": 125,
  "total_tokens": 28,
  "component_summary": {
    "system": 1,
    "user": 1
  },
  "analysis": {
    "complexity": {
      "level": "medium",
      "score": 2
    },
    "patterns": {
      "has_examples": false,
      "has_constraints": false,
      "has_chain_of_thought": false
    }
  }
}
```

## Development

### Running Tests

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run tests with coverage
pytest --cov=sorokin --cov-report=html
```

### Project Structure

```
sorokin/
├── src/
│   └── sorokin/
│       ├── __init__.py
│       ├── autopsy.py      # Core autopsy functionality
│       ├── analyzer.py     # Advanced analysis tools
│       ├── reporter.py     # Report generation
│       └── cli.py          # Command-line interface
├── tests/
│   ├── test_autopsy.py
│   ├── test_analyzer.py
│   └── test_reporter.py
├── setup.py
├── requirements.txt
└── README.md
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

Named after Pitirim Sorokin, a sociologist known for his work in analyzing social and cultural patterns.