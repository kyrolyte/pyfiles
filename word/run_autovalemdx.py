#!/usr/bin/env python3
import json
import os
import re
import sys
import subprocess

def run_vale_on_file(filepath: str, output_path: str) -> None:
    result = subprocess.run(
        ["vale", filepath, "--output=JSON"],
        capture_output=True,
        text=True,
        check=False,
    )

    output = result.stdout.strip()
    if not output or output == "{}":
        if result.stderr:
            print(f"  [stderr] {result.stderr.strip()}")
        print(f"  [info] No errors reported – skipping JSON file.")
        return

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(result.stdout)

    if result.stderr:
        print(f"  [stderr] {result.stderr.strip()}")


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


def process_sermon_files(n, directory):
    print(f"\n--- Processing iteration for n = {n} in directory: {directory} ---")

    file_n = os.path.join(directory, f"sermon_{n}.md")
    file_results = os.path.join(directory, f"sermon_{n}_results.md")
    file_updates = os.path.join(directory, f"sermon_{n}_updates.md")

    if not all(os.path.exists(f) for f in [file_n, file_results, file_updates]):
        print(f"Skipping n={n}: One or more required files are missing in {directory}.")
        return

    try:
        with open(file_results, 'r') as f_results:
            results_lines = f_results.readlines()

        with open(file_n, 'r') as f_n:
            sermon_content = f_n.read()

        with open(file_updates, 'r') as f_updates:
            updates_content = f_updates.read()

        sermon_lines = sermon_content.splitlines()
        updates_lines = updates_content.splitlines()

        for i, result_line in enumerate(results_lines):
            line_content_raw = result_line.strip()

            if not line_content_raw.startswith('- '):
                continue

            target_string = line_content_raw[2:].strip()

            if not target_string:
                continue

            if target_string in sermon_content:
                print(f"  [Match Found] Searching for '{target_string}' in {file_n}...")

                match_line_index = -1

                for j, line in enumerate(sermon_lines):
                    if target_string in line:
                        match_line_index = j
                        break

                if match_line_index != -1:
                    print(f"    -> Match found at line index {match_line_index + 1} in {file_n}.")

                    if i < len(updates_lines):
                        replacement_line_raw = updates_lines[i].strip()
                        
                        if replacement_line_raw.startswith('- '):
                            replacement_value = replacement_line_raw[2:].strip()
                        else:
                            replacement_value = replacement_line_raw

                        print(f"    -> Extracted replacement value from line {i + 1} in {file_updates}: '{replacement_value}'")

                        new_sermon_line = f"{replacement_value}"
                        sermon_lines[match_line_index] = new_sermon_line

                        new_sermon_content = "\n".join(sermon_lines)

                        with open(file_n, 'w') as f_n_write:
                            f_n_write.write(new_sermon_content)

                        print(f"    -> SUCCESSFULLY UPDATED and SAVED line {match_line_index + 1} in {file_n}.")
                    else:
                        print(f"    [ERROR] Result line index {i} out of bounds for updates file.")
                else:
                    print(f"    [No Match] Target '{target_string}' not found in {file_n}.")
            else:
                print(f"  [No Match] Target '{target_string}' not found in {file_n}.")

    except FileNotFoundError as e:
        print(f"\nCRITICAL ERROR: A file was not found during processing: {e}")
    except IOError as e:
        print(f"\nCRITICAL I/O ERROR: Failed to read or write a file: {e}")
    except Exception as e:
        print(f"\nAn unexpected general error occurred during processing for n={n}: {e}")


def main():
    if len(sys.argv) != 2:
        print("Usage: python run_autovalemdx.py <directory>")
        sys.exit(1)

    directory = sys.argv[1]
    if not os.path.isdir(directory):
        print(f"Error: '{directory}' is not a valid directory.")
        sys.exit(1)

    source_md_files = sorted(
        f for f in os.listdir(directory) if f.lower().endswith(".md")
    )

    if not source_md_files:
        print(f"No markdown files found in '{directory}'.")
        sys.exit(0)

    print(f"Found {len(source_md_files)} markdown file(s) in '{directory}'.\n")

    for filename in source_md_files:
        filepath = os.path.join(directory, filename)
        new_json_name = os.path.splitext(filename)[0] + ".json"
        new_json_path = os.path.join(directory, new_json_name)

        print(f"Processing: {filename} -> {new_json_name}")
        try:
            run_vale_on_file(filepath, new_json_path)
        except Exception as e:
            print(f"  [error] Failed to process {filename}: {e}")

    print(f"\nDone. JSON reports saved to '{directory}'.")

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

    print("--- Done. Starting File Match..... ---")

    mdfile_pattern = re.compile(r'^sermon_(\d+)\.md$')
    number_list = []
    
    for filename in os.listdir(directory):
        match = mdfile_pattern.match(filename)
        if match:
            number_list.append(int(match.group(1)))
    
    if not number_list:
        raise ValueError("No sermon_<n>.md files found in the directory.")
    
    lowest_number = min(number_list)
    highest_number = max(number_list)
    
    for current_number in range(lowest_number, highest_number + 1):
        print()
        process_sermon_files(current_number, directory)
        print("=" * 50)



if __name__ == "__main__":
    main()

