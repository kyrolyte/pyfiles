#!/usr/bin/env python3
import json
import os
import sys

def read_file(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Error reading file {path}: {e}")
        return ""

def main():
    if len(sys.argv) != 2:
        print("Usage: python run_autovalectx.py <directory>")
        sys.exit(1)

    directory = sys.argv[1]
    if not os.path.isdir(directory):
        print(f"Error: '{directory}' is not a valid directory.")
        sys.exit(1)

    json_files = sorted(f for f in os.listdir(directory) if f.endswith(".json"))

    if not json_files:
        print(f"No .json files found in '{directory}'.")
        sys.exit(0)

    for json_file in json_files:
        json_path = os.path.join(directory, json_file)
        # Changed extension from .csv to .md
        md_filename = json_file.replace(".json", "_results.md")
        md_path = os.path.join(directory, md_filename)

        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            try:
                contexts = set()

                for node_key, entries in data.items():
                    if not isinstance(entries, list):
                        continue

                    md_path_check = os.path.join(directory, node_key)

                    if not os.path.isfile(md_path_check):
                        # Fallback to the original logic for finding the source markdown file
                        source_md_filename = json_file.replace(".json", ".md")
                        md_path_check = os.path.join(directory, source_md_filename)

                    if not os.path.isfile(md_path_check):
                        print(f"Warning: No matching markdown file found for {node_key} (or {json_file.replace('.json', '.md')})")
                        continue

                    content = read_file(md_path_check)
                    if not content:
                        continue

                    lines = content.splitlines()

                    for entry in entries:
                        line_num = entry.get("Line")
                        if line_num is None:
                            continue

                        line_idx = line_num - 1
                        if 0 <= line_idx < len(lines):
                            # Strip whitespace to prevent false duplicates from trailing spaces/newlines
                            context = lines[line_idx].strip()
                            if context:
                                contexts.add(context)

                # Write to Markdown file instead of CSV
                with open(md_path, "w", encoding="utf-8") as md_file:
                    # Sort contexts for deterministic, reproducible output
                    for ctx in sorted(contexts):
                        md_file.write(f"- {ctx}\n")

                print(f"Results successfully written to {md_path}")

            except Exception as e:
                print(f"Error writing Markdown file {md_path}: {e}")
                sys.exit(1)

        except Exception as e:
            print(f"Error reading JSON file {json_path}: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()

