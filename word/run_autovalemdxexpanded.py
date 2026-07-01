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

    # Step 1: Generate _results.md files
    results_md_files = []
    for json_file in json_files:
        json_path = os.path.join(directory, json_file)
        # Changed extension from .csv to .md
        md_filename = json_file.replace(".json", "_results.md")
        md_path = os.path.join(directory, md_filename)
        results_md_files.append(md_path)

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

    if not results_md_files:
        print("No markdown files were generated to process further.")
        sys.exit(0)

    # Step 2: Iterate through each generated markdown file and process list items
    print("\n--- Processing Markdown files with 'pi' ---")
    
    for md_path in results_md_files:
        print(f"Processing {md_path}...")
        
        # Read the generated results file
        content = read_file(md_path)
        if not content:
            continue

        lines = content.splitlines()
        updated_lines = []
        
        for line in lines:
            # Check if the line is a list item (starts with "- ")
            if line.startswith("- "):
                item_text = line[2:]  # Remove the "- " prefix
                
                # Execute the pi command
                # Note: We assume 'pi' is in PATH and accepts the string as a single argument.
                # If 'pi' expects the string to be passed differently, this command may need adjustment.
                try:
                    result = subprocess.run(
                        ["pi", "-p", f"Create a version of the string that doesn't utilize unnecessary capitals."],
                        input=item_text,
                        capture_output=True,
                        text=True,
                        check=False
                    )
                    
                    # Use stdout as the replacement for the original line
                    output_text = result.stdout.strip()
                    if not output_text:
                        output_text = item_text  # Keep original if output is empty
                    
                    updated_lines.append(f"- {output_text}")
                    
                    # Optional: Print debug info
                    # print(f"  Original: '{item_text}' -> Result: '{output_text}'")
                    
                except FileNotFoundError:
                    print(f"  Warning: 'pi' command not found. Skipping item: '{item_text}'")
                    updated_lines.append(line)
                except Exception as e:
                    print(f"  Error executing 'pi' for item '{item_text}': {e}")
                    updated_lines.append(line)
            else:
                # Keep non-list lines unchanged
                updated_lines.append(line)
        
        # Write the updated content back to the file
        write_file(md_path, "\n".join(updated_lines))
        print(f"  Updated {md_path} with 'pi' results.")

    print("--- Done ---")

if __name__ == "__main__":
    main()

