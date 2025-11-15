# Sorokin Architecture

## Overview

Sorokin is built with a modular architecture separating concerns into distinct components:

```
┌─────────────────────────────────────────────────────────────┐
│                        User Interface                        │
├─────────────────────────┬───────────────────────────────────┤
│   CLI (cli.py)          │   Python API (__init__.py)        │
│   - File input          │   - Direct imports                │
│   - Stdin input         │   - Programmatic access           │
│   - Format selection    │   - Library usage                 │
└─────────────────────────┴───────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                      Core Analysis Layer                     │
├──────────────────────┬──────────────────────────────────────┤
│  PromptAutopsy       │  PromptAnalyzer                      │
│  (autopsy.py)        │  (analyzer.py)                       │
│  - Parse prompt      │  - Complexity analysis               │
│  - Extract roles     │  - Pattern detection                 │
│  - Count tokens      │  - Keyword extraction                │
│  - Metadata          │  - Sentiment analysis                │
└──────────────────────┴──────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                      Report Generation                       │
│                     (reporter.py)                            │
│  - JSON output                                              │
│  - Markdown output                                          │
│  - Plain text output                                        │
└─────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. PromptAutopsy (autopsy.py)

**Purpose**: Core analysis engine for prompt dissection

**Key Classes**:
- `PromptComponent`: Data class representing a single component
- `PromptAutopsy`: Main autopsy class

**Responsibilities**:
- Parse prompt text into components
- Extract system, user, and assistant messages
- Count tokens (approximation)
- Analyze structure and metadata
- Provide component access methods

**Key Methods**:
```python
analyze()                    # Perform full analysis
_extract_components()        # Parse prompt into parts
_count_tokens()             # Estimate token count
_analyze_structure()        # Add metadata
get_component_by_role()     # Filter by role
to_dict()                   # Export to dictionary
```

**Data Flow**:
```
Raw Prompt Text
    ↓
Parse with Regex
    ↓
Extract Components
    ↓
Count Tokens
    ↓
Analyze Metadata
    ↓
PromptComponent Objects
```

### 2. PromptAnalyzer (analyzer.py)

**Purpose**: Advanced analysis tools for prompts

**Key Methods**:
- `analyze_complexity()`: Multi-dimensional complexity scoring
- `extract_keywords()`: Frequency-based keyword extraction
- `detect_patterns()`: Rule-based pattern recognition
- `analyze_sentiment()`: Basic sentiment analysis

**Analysis Patterns**:
```
Input: PromptAutopsy
    ↓
┌───────────────────────┐
│ Complexity Analysis   │ → Score (0-4), Level (low/med/high)
├───────────────────────┤
│ Keyword Extraction    │ → List[(word, count)]
├───────────────────────┤
│ Pattern Detection     │ → Dict[pattern_name, bool]
├───────────────────────┤
│ Sentiment Analysis    │ → Tone, Polarity, Imperative
└───────────────────────┘
    ↓
Analysis Results Dict
```

**Pattern Detection Rules**:
- Examples: `example:`, `e.g.`, `for instance`
- Constraints: `must not`, `don't`, `should not`
- Format: `format:`, `json`, `xml`, code blocks
- Role Playing: `you are`, `act as`, `pretend`
- Chain of Thought: `step by step`, `think through`
- Few-Shot: Multiple numbered examples

### 3. AutopsyReport (reporter.py)

**Purpose**: Generate formatted reports from analysis

**Output Formats**:
1. **JSON**: Structured data for APIs
2. **Markdown**: Documentation format
3. **Text**: Terminal-friendly output

**Report Structure**:
```
{
  "timestamp": ISO-8601 datetime,
  "prompt_length": int,
  "total_tokens": int,
  "component_summary": {role: count},
  "components": [
    {
      "role": str,
      "content": str,
      "tokens": int,
      "metadata": {...}
    }
  ],
  "analysis": {
    "complexity": {...},
    "keywords": [...],
    "patterns": {...},
    "sentiment": {...}
  }
}
```

### 4. CLI (cli.py)

**Purpose**: Command-line interface

**Features**:
- File input support
- Stdin input support
- Multiple output formats
- Output file support

**Usage Flow**:
```
Command Line Args
    ↓
Parse Arguments
    ↓
Read Input (file/stdin)
    ↓
Create PromptAutopsy
    ↓
Generate Report
    ↓
Format Output
    ↓
Write to stdout/file
```

## Data Structures

### PromptComponent

```python
@dataclass
class PromptComponent:
    role: str              # "system", "user", "assistant"
    content: str           # The actual text
    tokens: int = 0        # Estimated token count
    metadata: Dict = {}    # Additional info
```

### Metadata Dictionary

```python
{
    'length': int,              # Character count
    'word_count': int,          # Word count
    'line_count': int,          # Line count
    'has_code_blocks': bool,    # Contains ```
    'has_lists': bool,          # Contains - or *
    'has_questions': bool,      # Contains ?
    'has_instructions': bool    # Contains please, must, etc.
}
```

## Processing Pipeline

### Full Analysis Pipeline

```
1. Input: Raw prompt text
   ↓
2. PromptAutopsy.analyze()
   ├─ Extract components (regex parsing)
   ├─ Count tokens (word-based approximation)
   └─ Analyze structure (metadata extraction)
   ↓
3. PromptAnalyzer (optional advanced analysis)
   ├─ Complexity analysis
   ├─ Pattern detection
   ├─ Keyword extraction
   └─ Sentiment analysis
   ↓
4. AutopsyReport.generate()
   ├─ Combine all results
   └─ Format output (JSON/Markdown/Text)
   ↓
5. Output: Formatted report
```

## Design Principles

### 1. Separation of Concerns
- Core analysis separated from reporting
- Advanced analysis is optional
- CLI separated from library code

### 2. Lazy Evaluation
- Analysis only performed when needed
- Properties trigger analysis on first access
- Efficient for partial data access

### 3. Extensibility
- Easy to add new pattern detectors
- Simple to add output formats
- Can extend with new analysis methods

### 4. No External Dependencies
- Pure Python standard library
- No API calls or external services
- Works completely offline

### 5. Testability
- Each component independently testable
- Clear interfaces between layers
- Minimal side effects

## Testing Strategy

```
Unit Tests
├── test_autopsy.py       # Core autopsy functionality
├── test_analyzer.py      # Advanced analysis
└── test_reporter.py      # Report generation

Integration Tests
└── test_integration.py   # End-to-end workflows

Manual Tests
└── CLI testing           # Command-line interface
```

## Performance Characteristics

- **Time Complexity**: O(n) where n is prompt length
- **Space Complexity**: O(n) for storing components
- **Token Counting**: ~1ms for typical prompts
- **Full Analysis**: ~5-10ms for typical prompts
- **Report Generation**: ~1-2ms per format

## Extension Points

### Adding New Patterns

```python
def detect_new_pattern(autopsy: PromptAutopsy) -> bool:
    combined_text = ' '.join(c.content for c in autopsy.components)
    # Add detection logic
    return pattern_found
```

### Adding New Output Formats

```python
def to_new_format(self) -> str:
    report = self.generate()
    # Format report data
    return formatted_output
```

### Adding New Analysis

```python
@staticmethod
def analyze_new_aspect(autopsy: PromptAutopsy) -> Dict:
    # Perform new analysis
    return analysis_results
```

## Future Architecture Considerations

Potential enhancements:
1. Plugin system for custom analyzers
2. Database integration for storing analyses
3. Web API wrapper
4. Real-time analysis streaming
5. Caching layer for repeated analyses
6. Parallel processing for batch operations
