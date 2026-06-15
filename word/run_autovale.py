#!/usr/bin/env python3
"""
CLI tool to export Vale lint annotations to a CSV file.

Usage:
    python run_autovale.py /path/to/dir
"""

import json
import os
import sys
import csv

def read_file(path: str) -> str:
    """Read and return the contents of a file."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Error reading file {path}: {e}")
        return ""

def main():
    if len(sys.argv) != 2:
        print("Usage: python run_autovale.py <directory>")
        sys.exit(1)

    directory = sys.argv[1]
    if not os.path.isdir(directory):
        print(f"Error: '{directory}' is not a valid directory.")
        sys.exit(1)

    json_files = sorted(f for f in os.listdir(directory) if f.endswith(".json"))

    if not json_files:
        print(f"No .json files found in '{directory}'.")
        sys.exit(0)

    output_csv = "vale_results.csv"
    csv_headers = ["File", "Line", "Span", "Match", "Description", "Message", "Context"]

    try:
        with open(output_csv, "w", encoding="utf-8", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(csv_headers)

            for json_file in json_files:
                json_path = os.path.join(directory, json_file)
                
                with open(json_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                # In Vale JSON, the keys are the filenames of the documents being linted.
                for node_key, entries in data.items():
                    if not isinstance(entries, list):
                        continue

                    # We try to find the markdown file.
                    # 1. Try using node_key (the filename from Vale)
                    md_path = os.path.join(directory, node_key)
                    
                    # 2. If not found, try replacing .json with .md (as done in run_comparevale.py)
                    if not os.path.isfile(md_path):
                        md_filename = json_file.replace(".json", ".md")
                        md_path = os.path.join(directory, md_filename)

                    if not os.path.isfile(md_path):
                        print(f"Warning: No matching markdown file found for {node_key} (or {json_file.replace('.json', '.md')})")
                        continue

                    content = read_file(md_path)
                    lines = content.splitlines()

                    for entry in entries:
                        line_num = entry.get("Line")
                        span = entry.get("Span")
                        match_str = entry.get("Match", "")
                        description = entry.get("Description", "")
                        message = entry.get("Message", "")

                        if line_num is None or span is None:
                            continue

                        # Get context (the line)
                        line_idx = line_num - 1
                        if 0 <= line_idx < len(lines):
                            context = lines[line_idx]
                        else:
                            context = ""

                        writer.writerow([
                            node_key,
                            line_num,
                            f"{span[0]}-{span[1]}",
                            match_str,
                            description,
                            message,
                            context
                        ])

    except Exception as e:
        print(f"Error writing CSV: {e}")
        sys.exit(1)

    print(f"Results successfully written to {output_csv}")

if __name__ == "__main__":
    main()
