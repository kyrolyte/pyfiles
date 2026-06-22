#!/usr/bin/env python3
import json
import os
import sys
import csv

def read_file(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Error reading file {path}: {e}")
        return ""

def main():
    if len(sys.argv) != 2:
        print("Usage: python run_autovalesingle.py <directory>")
        sys.exit(1)

    directory = sys.argv[1]
    if not os.path.isdir(directory):
        print(f"Error: '{directory}' is not a valid directory.")
        sys.exit(1)

    json_files = sorted(f for f in os.listdir(directory) if f.endswith(".json"))

    if not json_files:
        print(f"No .json files found in '{directory}'.")
        sys.exit(0)

    csv_headers = ["Context"]

    for json_file in json_files:
        json_path = os.path.join(directory, json_file)
        csv_filename = json_file.replace(".json", "_results.csv")
        csv_path = os.path.join(directory, csv_filename)

        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            try:
                contexts = set()

                for node_key, entries in data.items():
                    if not isinstance(entries, list):
                        continue

                    md_path = os.path.join(directory, node_key)

                    if not os.path.isfile(md_path):
                        md_filename = json_file.replace(".json", ".md")
                        md_path = os.path.join(directory, md_filename)

                    if not os.path.isfile(md_path):
                        print(f"Warning: No matching markdown file found for {node_key} (or {json_file.replace('.json', '.md')})")
                        continue

                    content = read_file(md_path)
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

                with open(csv_path, "w", encoding="utf-8", newline="") as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(csv_headers)
                    # Sort contexts for deterministic, reproducible output
                    for ctx in sorted(contexts):
                        writer.writerow([ctx])

            except Exception as e:
                print(f"Error writing CSV file {csv_path}: {e}")
                sys.exit(1)

            print(f"Results successfully written to {csv_path}")

        except Exception as e:
            print(f"Error reading JSON file {json_path}: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()

