#!/usr/bin/env python3
import json
import os
import sys
import subprocess

def read_file(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Error reading file {path}: {e}")
        return ""

def write_file(path: str, content: str) -> None:
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
    except Exception as e:
        print(f"Error writing file {path}: {e}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python run_autovalemdx.py <directory>")
        sys.exit(1)

    directory = sys.argv[1]
    if not os.path.isdir(directory):
        print(f"Error: '{directory}' is not a valid directory.")
        sys.exit(1)

    json_files = sorted(f for f in os.listdir(directory) if f.endswith(".json"))

    if not json_files:
        print(f"No .json files found in '{directory}'.")
        sys.exit(0)

    results_md_files = []
    for json_file in json_files:
        json_path = os.path.join(directory, json_file)
        md_filename = json_file.replace(".json", "_results.md")
        md_path = os.path.join(directory, md_filename)
        results_md_files.append(md_path)

        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            contexts = set()

            for node_key, entries in data.items():
                if not isinstance(entries, list):
                    continue

                md_path_check = os.path.join(directory, node_key)

                if not os.path.isfile(md_path_check):
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
                        context = lines[line_idx].strip()
                        if context:
                            contexts.add(context)

            with open(md_path, "w", encoding="utf-8") as md_file:
                for ctx in sorted(contexts):
                    md_file.write(f"- {ctx}\n")

            print(f"Results successfully written to {md_path}")

        except Exception as e:
            print(f"Error writing Markdown file {md_path}: {e}")
            sys.exit(1)

    if not results_md_files:
        print("No markdown files were generated to process further.")
        sys.exit(0)

    print("\n--- Processing Markdown files with 'pi' ---")
    
    for md_path in results_md_files:
        print(f"Processing {md_path}...")
        
        content = read_file(md_path)
        if not content:
            continue

        lines = content.splitlines()
        updated_lines = []
        
        for line in lines:
            if line.startswith("- "):
                item_text = line[2:]
                
                try:
                    result = subprocess.run(
                        ["pi", "-p", f"Update the provided text to adhere to English capitalization rules: keep capital letters if part of Roman Numerals or a title; lowercase the rest; capitalize only the first letter of sentences, and the first letter of proper nouns (persons, places, things of importance); if a word only has the first letter capitalized, leave it as-is. Output only the resulting text string on a single line. Do not include any preamble, explanation, commentary, or any other text whatsoever."],
                        input=item_text,
                        capture_output=True,
                        text=True,
                        check=False
                    )
                    
                    output_text = result.stdout.strip()
                    if not output_text:
                        output_text = item_text
                    
                    updated_lines.append(f"- {output_text}")
                    
                except FileNotFoundError:
                    print(f"  Warning: 'pi' command not found. Skipping item: '{item_text}'")
                    updated_lines.append(line)
                except Exception as e:
                    print(f"  Error executing 'pi' for item '{item_text}': {e}")
                    updated_lines.append(line)
            else:
                updated_lines.append(line)
        
        new_md_filename = md_path.replace("_results.md", "_updates.md")
        new_md_path = os.path.join(os.path.dirname(md_path), new_md_filename)

        write_file(new_md_path, "\n".join(updated_lines))
        print(f"  Updated results saved to {new_md_path}")

    print("--- Done ---")

if __name__ == "__main__":
    main()

