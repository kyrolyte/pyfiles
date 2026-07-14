import os

def process_sermon_files(n):
    print(f"\n--- Processing iteration for n = {n} ---")

    file_n = f"sermon_{n}.md"
    file_results = f"sermon_{n}_results.md"
    file_updates = f"sermon_{n}_updates.md"

    if not all(os.path.exists(f) for f in [file_n, file_results, file_updates]):
        print(f"Skipping n={n}: One or more required files are missing.")
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


if __name__ == "__main__":
    for i in range(3387, 3388):
        process_sermon_files(i)
        print("=" * 50)
    
    print("\nAll iterations complete.")

