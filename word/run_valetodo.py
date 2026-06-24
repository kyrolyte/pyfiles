#!/usr/bin/env python3
"""
generate_todo.py
Iterates through JSON files in a specified directory, extracts Vale linting issues,
and generates a sorted TODO.md file.
"""

import os
import json
from pathlib import Path


def generate_todo_markdown(target_dir: str, output_file: str = "TODO.md") -> None:
    target_path = Path(target_dir).resolve()

    if not target_path.is_dir():
        print(f"❌ Error: '{target_dir}' is not a valid directory.")
        return

    todo_items = []
    json_files = list(target_path.glob("*.json"))

    if not json_files:
        print("⚠️  No JSON files found in the specified directory.")
        return

    print(f"📂 Scanning {len(json_files)} JSON file(s) in {target_path}...")

    for json_path in json_files:
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"⚠️  Warning: Skipped {json_path.name} (Invalid JSON: {e})")
            continue
        except Exception as e:
            print(f"⚠️  Warning: Could not read {json_path.name} ({e})")
            continue

        # Iterate through each main node (filename -> list of issues)
        for file_name, issues in data.items():
            if not isinstance(issues, list):
                continue

            for issue in issues:
                # Case-insensitive lookup for robustness
                line = issue.get("Line") or issue.get("line")
                span = issue.get("Span") or issue.get("span")
                message = issue.get("Message") or issue.get("message")

                # Skip incomplete entries
                if line is None or span is None or message is None:
                    continue

                # Format span as a range (e.g., "290-292")
                if isinstance(span, list) and len(span) == 2:
                    span_str = f"{span[0]}-{span[1]}"
                else:
                    span_str = str(span)

                todo_items.append({
                    "file": file_name,
                    "line": int(line),
                    "span": span_str,
                    "message": message
                })

    # Sort by filename, then by line number for a clean TODO list
    todo_items.sort(key=lambda x: (x["file"], x["line"]))

    # Construct markdown lines
    markdown_lines = [
        f"- In {item['file']} on line {item['line']} near position {item['span']}; {item['message']}"
        for item in todo_items
    ]

    # Write to TODO.md in the current working directory
    out_path = Path.cwd() / output_file
    with open(out_path, "w", encoding="utf-8") as f:
        if markdown_lines:
            f.write("\n".join(markdown_lines) + "\n")
        else:
            f.write("# TODO\n\nNo issues found.\n")

    print(f"✅ Successfully wrote {len(markdown_lines)} items to '{out_path}'")


if __name__ == "__main__":
    # Prompt user for directory
    user_dir = input("Enter the directory path containing the JSON files: ").strip().strip("'\"")
    generate_todo_markdown(user_dir)

