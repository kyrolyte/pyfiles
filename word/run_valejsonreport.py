#!/usr/bin/env python3
"""
Run vale linter on all markdown files in a directory and save JSON output to files.

Usage:
    python vale_json_report.py /path/to/dir
"""

import sys
import os
import subprocess
import json


def run_vale_on_file(filepath: str, output_path: str) -> None:
    """Run vale on a single markdown file and save JSON output."""
    result = subprocess.run(
        ["vale", filepath, "--output=JSON"],
        capture_output=True,
        text=True,
        check=False,
    )
    # Write JSON output to file (stdout is JSON)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(result.stdout)
    # If there was stderr, include it in the output for debugging
    if result.stderr:
        print(f"  [stderr] {result.stderr.strip()}")


def main():
    if len(sys.argv) != 2:
        print("Usage: python vale_json_report.py <directory>")
        sys.exit(1)

    target_dir = sys.argv[1]

    if not os.path.isdir(target_dir):
        print(f"Error: '{target_dir}' is not a valid directory.")
        sys.exit(1)

    # Find all .md files in the directory
    md_files = sorted(
        f for f in os.listdir(target_dir) if f.lower().endswith(".md")
    )

    if not md_files:
        print(f"No markdown files found in '{target_dir}'.")
        sys.exit(0)

    print(f"Found {len(md_files)} markdown file(s) in '{target_dir}'.\n")

    for filename in md_files:
        filepath = os.path.join(target_dir, filename)
        json_name = os.path.splitext(filename)[0] + ".json"
        json_path = os.path.join(target_dir, json_name)

        print(f"Processing: {filename} -> {json_name}")
        try:
            run_vale_on_file(filepath, json_path)
        except Exception as e:
            print(f"  [error] Failed to process {filename}: {e}")

    print(f"\nDone. JSON reports saved to '{target_dir}'.")


if __name__ == "__main__":
    main()
