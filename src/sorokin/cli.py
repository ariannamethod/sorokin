"""
Command-line interface for the prompt autopsy engine.
"""

import argparse
import sys
import json
from pathlib import Path
from .autopsy import PromptAutopsy
from .reporter import AutopsyReport
from . import __version__


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Sorokin - Prompt Autopsy Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze a prompt from file
  sorokin prompt.txt
  
  # Analyze with specific output format
  sorokin prompt.txt --format json
  
  # Analyze from stdin
  echo "Your prompt here" | sorokin -
  
  # Save report to file
  sorokin prompt.txt --output report.json --format json
        """
    )
    
    parser.add_argument(
        'input',
        help='Input file containing the prompt (use "-" for stdin)'
    )
    
    parser.add_argument(
        '-f', '--format',
        choices=['text', 'markdown', 'json'],
        default='text',
        help='Output format (default: text)'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Output file (default: stdout)'
    )
    
    parser.add_argument(
        '--no-analysis',
        action='store_true',
        help='Skip advanced analysis'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version=f'%(prog)s {__version__}'
    )
    
    args = parser.parse_args()
    
    # Read input
    try:
        if args.input == '-':
            MAX_STDIN_SIZE = 10 * 1024 * 1024  # 10MB
            prompt_text = sys.stdin.read(MAX_STDIN_SIZE)
            if len(prompt_text) == MAX_STDIN_SIZE:
                print("Warning: Input truncated at maximum size (10MB)", file=sys.stderr)
        else:
            prompt_path = Path(args.input)
            if not prompt_path.exists():
                print(f"Error: File not found: {args.input}", file=sys.stderr)
                sys.exit(1)
            MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB limit
            file_size = prompt_path.stat().st_size
            if file_size > MAX_FILE_SIZE:
                print(f"Error: File too large ({file_size} bytes). Maximum size is {MAX_FILE_SIZE} bytes.", file=sys.stderr)
                sys.exit(1)
            prompt_text = prompt_path.read_text()
    except Exception as e:
        print(f"Error reading input: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Perform autopsy
    try:
        autopsy = PromptAutopsy(prompt_text)
        autopsy.analyze()
        
        report = AutopsyReport(autopsy)
        
        # Generate output based on format
        include_analysis = not args.no_analysis
        if args.format == 'json':
            output = report.to_json(include_analysis=include_analysis)
        elif args.format == 'markdown':
            output = report.to_markdown(include_analysis=include_analysis)
        else:  # text
            output = report.to_text(include_analysis=include_analysis)
        
        # Write output
        if args.output:
            Path(args.output).write_text(output)
            print(f"Report saved to {args.output}")
        else:
            print(output)
            
    except Exception as e:
        print(f"Error during analysis: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
