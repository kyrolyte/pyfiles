#!/usr/bin/env python3
"""
Script to detect Roman numerals in markdown files within a user-specified directory.
Roman numerals are detected as sequences of I, V, X, L (capital formats only).
The script outputs findings to a markdown file with file name, line number, position,
and context around the match.
"""

import os
import re
import sys
import glob


def find_markdown_files(directory):
    """Recursively find all .md files in the given directory."""
    md_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md') or file.endswith('.markdown'):
                md_files.append(os.path.join(root, file))
    return sorted(md_files)


def find_roman_numerals(content):
    """
    Find all Roman numeral occurrences in the content.
    Roman numerals consist of I, V, X, L (capital formats only).
    We look for sequences of at least two Roman numeral characters, or single characters (with 'I' requiring a following dot).
    
    Returns a list of tuples: (start_position, end_position, matched_string)
    where start_position is the character index in the line.
    """
    # Pattern for Roman numerals: sequences of 2+ characters, single V, X, L, or 'I' if followed by a dot.
    # We need to be careful not to match things like "IIII" which aren't valid,
    # but for detection purposes, we'll just find all sequences of Roman numeral chars.
    # The problem states to find all occurrences, so we'll capture any sequence of
    # Roman numeral characters.
    pattern = re.compile(r'\b([IVXL]{2,}|[VXL]|I(?=\.))\b')
    return pattern.findall(content)


def find_roman_numeral_positions_in_line(line):
    """
    Find all Roman numeral occurrences in a single line.
    Returns a list of tuples: (start_position, matched_string)
    """
    pattern = re.compile(r'\b([IVXL]{2,}|[VXL]|I(?=\.))\b')
    matches = []
    for match in pattern.finditer(line):
        matches.append((match.start(), match.group()))
    return matches


def get_context(line, start, match_len, context_chars=10):
    """
    Get context around the match in the line.
    Returns a string with up to context_chars characters before and after the match.
    """
    start_ctx = max(0, start - context_chars)
    end_ctx = min(len(line), start + match_len + context_chars)
    context = line[start_ctx:end_ctx]
    # Add ellipsis if we cut off at the beginning or end
    if start_ctx > 0:
        context = '...' + context
    if end_ctx < len(line):
        context = context + '...'
    return context


def process_files(directory, output_file):
    """Process all markdown files in the directory and write findings to output file."""
    md_files = find_markdown_files(directory)
    
    if not md_files:
        print(f"No markdown files found in {directory}")
        return
    
    findings = []
    
    for filepath in md_files:
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
            continue
        
        rel_path = os.path.basename(filepath)
        
        for line_num, line in enumerate(lines, start=1):
            # Remove newline for processing but keep original for context
            line_stripped = line.rstrip('\n').rstrip('\r')
            positions = find_roman_numeral_positions_in_line(line_stripped)
            
            for start, match in positions:
                match_len = len(match)
                context = get_context(line_stripped, start, match_len, context_chars=10)
                findings.append((rel_path, line_num, start, match, context))
    
    # Write findings to output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Roman Numeral Findings\n\n")
        f.write("| File | Line | Position | Match | Context |\n")
        f.write("|------|------|----------|-------|---------|\n")
        
        for rel_path, line_num, pos, match, context in findings:
            # Escape pipe characters in context if any
            context_escaped = context.replace('|', '\\|')
            f.write(f"| {rel_path} | {line_num} | {pos} | {match} | {context_escaped} |\n")
        
        if not findings:
            f.write("\nNo Roman numerals found.\n")
    
    print(f"Findings written to {output_file}")
    print(f"Total findings: {len(findings)}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <directory> [output_file]")
        sys.exit(1)
    
    directory = sys.argv[1]
    
    if not os.path.isdir(directory):
        print(f"Error: '{directory}' is not a valid directory.")
        sys.exit(1)
    
    output_file = sys.argv[2] if len(sys.argv) > 2 else "roman_numeral_findings.md"
    
    process_files(directory, output_file)


if __name__ == "__main__":
    main()

