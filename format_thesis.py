#!/usr/bin/env python3
"""Command-line interface for CMNU thesis document formatting."""

import argparse
import os
import sys
from pathlib import Path
from src.formatter import DocumentFormatter
from src.exceptions import FormattingError, InvalidFileFormatError, FileCorruptedError


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Format thesis documents according to CMNU standards',
        prog='format_thesis'
    )

    parser.add_argument(
        'input',
        help='Path to input .docx file'
    )

    parser.add_argument(
        '-o', '--output',
        help='Path for output file (default: input_formatted.docx)',
        default=None
    )

    args = parser.parse_args()

    try:
        input_path = Path(args.input)

        # Format document (DocumentFormatter handles validation)
        formatter = DocumentFormatter()
        formatted_path = formatter.format_document(str(input_path), keep_original=False)

        # Handle output path if specified
        if args.output:
            try:
                output_path = Path(args.output)
                os.rename(formatted_path, output_path)
                formatted_path = str(output_path)
            except OSError as e:
                print(f"Error: Failed to write output file - {str(e)}", file=sys.stderr)
                return 1

        print(f"Successfully formatted thesis document")
        print(f"  Input:  {input_path}")
        print(f"  Output: {formatted_path}")
        return 0

    except InvalidFileFormatError as e:
        print(f"Error: Invalid file format - {str(e)}", file=sys.stderr)
        return 1
    except FileCorruptedError as e:
        print(f"Error: File error - {str(e)}", file=sys.stderr)
        return 1
    except FormattingError as e:
        print(f"Error: Formatting failed - {str(e)}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: Unexpected error - {str(e)}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
