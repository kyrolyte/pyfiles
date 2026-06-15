#!/usr/bin/env python3
"""
CLI tool to review and edit markdown files based on JSON lint annotations.

Usage:
    python script.py /path/to/dir
"""

import json
import os
import sys
import subprocess


def run_command(cmd: str) -> str:
    """Run a shell command and return stdout."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip()


def read_file(path: str) -> str:
    """Read and return the contents of a file."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_file(path: str, content: str):
    """Write content to a file."""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def apply_changes(markdown_path: str, line_num: int, span: list, match_str: str, action: str, md_filename: str = ""):
    """Apply the selected change to the markdown file."""
    content = read_file(markdown_path)
    lines = content.split("\n")

    # line_num is 1-indexed (from JSON), convert to 0-indexed for list access
    line_idx = line_num - 1
    if line_idx >= len(lines) or line_idx < 0:
        print("  -> Line number out of range, skipping.")
        return

    original_line = lines[line_idx]
    # Span is 1-indexed (for cut), convert to 0-indexed Python slice
    start = span[0] - 1
    end = span[1]
    current = original_line[start:end]

    if action == "1":
        replacement = current.lower()
    elif action == "2":
        replacement = current.lower()
        if replacement:
            replacement = replacement[0].upper() + replacement[1:]
    else:
        return

    lines[line_idx] = original_line[:start] + replacement + original_line[end:]
    write_file(markdown_path, "\n".join(lines))
    if md_filename:
        print(f"  -> Applied change in '{md_filename}': '{current}' -> '{replacement}'")
    else:
        print(f"  -> Applied change: '{current}' -> '{replacement}'")


def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <directory>")
        sys.exit(1)

    directory = sys.argv[1]
    if not os.path.isdir(directory):
        print(f"Error: '{directory}' is not a valid directory.")
        sys.exit(1)

    json_files = sorted(f for f in os.listdir(directory) if f.endswith(".json"))

    if not json_files:
        print(f"No .json files found in '{directory}'.")
        sys.exit(0)

    print(f"Found {len(json_files)} .json file(s) in '{directory}'.\n")

    for json_file in json_files:
        json_path = os.path.join(directory, json_file)
        md_filename = json_file.replace(".json", ".md")
        md_path = os.path.join(directory, md_filename)

        # Read JSON
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # The primary node is the key in the JSON object (e.g., "sample.md")
        for node_key, entries in data.items():
            if not isinstance(entries, list):
                continue

            # Check if the markdown file exists
            if not os.path.isfile(md_path):
                print(f"Warning: No matching markdown file for '{node_key}' -> '{md_filename}'")
                continue

            print(f"\n{'=' * 60}")
            print(f"Processing: {json_file} -> {md_filename}")
            print(f"{'=' * 60}")

            for entry in entries:
                line = entry.get("Line")
                span = entry.get("Span")
                match_str = entry.get("Match", "")
                description = entry.get("Description", "")
                message = entry.get("Message", "")

                if line is None or span is None:
                    continue

                line_num = line  # 1-indexed line number from JSON

                # Print current string using sed and cut
                print(f"\nCurrent string:")
                cmd = f"sed -n '{line_num}p' '{md_path}' | cut -c{span[0]}-{span[1]}"
                current_str = run_command(cmd)
                print(f"  {current_str}")

                # Print context
                print(f"\nContext of match:")
                cmd = f"sed -n '{line_num}p' '{md_path}'"
                context = run_command(cmd)
                print(f"  {context}")

                # Show metadata
                if description:
                    print(f"\n  Description: {description}")
                if message:
                    print(f"  Message: {message}")

                # Prompt user
                print("\n  Options:")
                print("  0: Do nothing, go to the next value")
                print("  1: Convert the matching string to lowercase in the file")
                print("  2: Convert the string to sentence case (first letter capitalized)")
                print("  e: Cancel, exit program")

                choice = input("\n  Your choice: ").strip().lower()

                if choice == "e":
                    print("\nExiting program.")
                    sys.exit(0)
                elif choice in ("0", "1", "2"):
                    if choice in ("1", "2"):
                        apply_changes(md_path, line_num, span, match_str, choice, md_filename)
                    # If 0, just continue to next entry
                else:
                    confirm = input("\n  Invalid input. Continue? (y/n): ").strip().lower()
                    if confirm != "y":
                        print("\nExiting program.")
                        sys.exit(0)

    print("\nDone.")


if __name__ == "__main__":
    main()
