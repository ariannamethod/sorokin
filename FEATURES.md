# Sorokin Feature Overview

## What is Sorokin?

Sorokin is a prompt autopsy engine - a tool for analyzing and dissecting LLM prompts to understand their structure, components, and characteristics. It helps developers, researchers, and prompt engineers understand what makes prompts effective.

## Core Capabilities

### 1. Component Extraction

Automatically identifies and separates different parts of a prompt:
- **System messages**: Instructions for the AI's behavior and role
- **User messages**: The actual requests or questions
- **Assistant messages**: Previous AI responses in a conversation

Supports multiple formats:
- Colon notation: `system: message`
- Bracket notation: `[system] message`
- Angle bracket notation: `<system>message`
- Plain text (treated as user message)

### 2. Token Analysis

- Estimates token count for each component
- Calculates total tokens in prompt
- Uses word-based approximation (~1 token per word)
- Helps understand API costs and context limits

### 3. Complexity Analysis

Evaluates prompt complexity on multiple dimensions:
- **Average sentence length**: Measures readability
- **Nesting depth**: Tracks parentheses and bracket levels
- **Component count**: Number of distinct message parts
- **Overall score**: 0-4 scale (low/medium/high)

### 4. Pattern Detection

Identifies common prompt engineering techniques:

- **Examples**: Detects if prompt includes examples or demonstrations
- **Constraints**: Identifies restrictions and rules ("must not", "don't")
- **Format Specification**: Checks for output format requirements (JSON, XML, etc.)
- **Role Playing**: Detects if AI is assigned a specific persona
- **Chain of Thought**: Identifies step-by-step reasoning prompts
- **Few-Shot Learning**: Detects multiple example patterns

### 5. Sentiment Analysis

Analyzes the tone and style of prompts:
- **Tone**: Positive, neutral, or negative
- **Polarity**: Numerical sentiment score (-1 to 1)
- **Imperative Detection**: Identifies command-style language
- **Word Counts**: Tracks positive, negative, and command words

### 6. Keyword Extraction

- Extracts most frequent meaningful words
- Filters common stop words
- Returns ranked list of keywords
- Helps identify prompt focus areas

### 7. Metadata Analysis

For each component, extracts:
- Character length
- Word count
- Line count
- Presence of code blocks (```)
- Presence of lists (-, *, numbered)
- Presence of questions (?)
- Presence of instructions (please, must, should, etc.)

## Output Formats

### JSON
Structured data format for programmatic access:
```json
{
  "timestamp": "...",
  "total_tokens": 50,
  "components": [...],
  "analysis": {...}
}
```

### Markdown
Human-readable format with formatting:
```markdown
# Prompt Autopsy Report
**Total Tokens:** 50
## Components
...
```

### Plain Text
Simple text report for terminal viewing:
```
============================================================
PROMPT AUTOPSY REPORT
============================================================
...
```

## Use Cases

### For Developers
- Debug prompt issues
- Optimize token usage
- Validate prompt structure
- Compare different prompt versions

### For Researchers
- Analyze prompt patterns at scale
- Study effective prompt characteristics
- Categorize prompt types
- Build prompt datasets

### For Prompt Engineers
- Understand prompt complexity
- Identify missing components
- Ensure best practices
- Document prompt designs

### For QA Teams
- Validate prompt requirements
- Check for constraint violations
- Verify format specifications
- Test edge cases

## Integration Options

### Python API
```python
from sorokin import PromptAutopsy, AutopsyReport

autopsy = PromptAutopsy(prompt_text)
report = AutopsyReport(autopsy)
print(report.to_json())
```

### Command Line
```bash
# Analyze file
sorokin prompt.txt

# Analyze from stdin
echo "prompt" | sorokin -

# Different formats
sorokin prompt.txt --format json
sorokin prompt.txt --format markdown
```

### Batch Processing
```python
from sorokin import PromptAutopsy

prompts = load_prompts()
results = []

for prompt in prompts:
    autopsy = PromptAutopsy(prompt)
    autopsy.analyze()
    results.append(autopsy.to_dict())

save_results(results)
```

## Technical Details

### Dependencies
- Pure Python implementation
- Uses only standard library
- No external API calls
- Works offline

### Performance
- Fast analysis (milliseconds per prompt)
- Memory efficient
- Scales to large prompts
- No rate limits

### Accuracy
- Token counting: ~90% accuracy vs actual tokenizers
- Pattern detection: Rule-based, deterministic
- Sentiment: Basic but consistent
- Component extraction: Handles various formats

## Limitations

1. **Token Estimation**: Approximation only, not exact count
2. **Language**: Optimized for English prompts
3. **Context**: No external context or API access
4. **Sentiment**: Basic analysis, not deep NLP
5. **Patterns**: Rule-based, may miss nuanced patterns

## Future Enhancements

Potential additions:
- Integration with actual tokenizers (tiktoken)
- Multi-language support
- Deep learning-based analysis
- Prompt similarity comparison
- Quality scoring
- Effectiveness prediction
- Interactive web interface

## Getting Started

See [README.md](README.md) for installation and usage instructions.

See [examples/](examples/) for sample code and use cases.
