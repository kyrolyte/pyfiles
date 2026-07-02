--- File: run_quotehyphenfix.py ---
import json
import os
import re

def process_spacing(match_text):
    # Find the first punctuation symbol (.,?!) and insert a space after it
    for i, char in enumerate(match_text):
        if char in '.,?!':
            return match_text[:i+1] + ' ' + match_text[i+1:]
    return match_text

def process_ly_hyphens(match_text):
    # Replace hyphen with a space
    return match_text.replace('-', ' ')

def process_question_mark(match_text):
    """
    Replaces '" ?' with '? "'
    """
    # The pattern to find: '" ?'
    old_pattern = '"? '
    # The replacement: '? "'
    new_pattern = '?" '
    return match_text.replace(old_pattern, new_pattern)

def fix_question_marks_in_markdown_files():
    """
    Iterate through all markdown files in the current directory.
    Replace the pattern '" ?' with '? "'
    """
    # Get all .md files in the current directory
    md_files = [f for f in os.listdir('.') if f.endswith('.md') and os.path.isfile(f)]
    
    for md_file in md_files:
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replace all occurrences of the old pattern with the new pattern
            new_content = process_question_mark(content)
            
            # Only write if content changed
            if new_content != content:
                with open(md_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"    Updated {md_file} (Question Mark Fix)")
            else:
                print(f"    No changes needed: {md_file} (Question Mark Fix)")
        except Exception as e:
            print(f"    Error processing {md_file}: {e}")

def main():
    # 1. Process JSON files and fix Google errors
    json_files = [f for f in os.listdir('.') if f.endswith('.json')]

    # Track files that have been modified during this step to exclude them later
    processed_md_files = set()

    if not json_files:
        print("No JSON files found.")
    else:
        print("Processing JSON files...")
        for json_file in json_files:
            print(f"Processing {json_file}...")
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except Exception as e:
                print(f"Error reading {json_file}: {e}")
                continue

            for md_filename, errors in data.items():
                if not os.path.exists(md_filename):
                    print(f"Markdown file {md_filename} not found, skipping.")
                    continue

                print(f"  Applying fixes to {md_filename}...")
                try:
                    with open(md_filename, 'r', encoding='utf-8') as f:
                        content = f.read()

                    changed = False
                    for error in errors:
                        check = error.get('Check')
                        match_text = error.get('Match')

                        if not match_text:
                            continue

                        replacement = None
                        if check == 'Google.Spacing':
                            replacement = process_spacing(match_text)
                        elif check == 'Google.LyHyphens':
                            replacement = process_ly_hyphens(match_text)

                        if replacement and replacement != match_text:
                            if match_text in content:
                                content = content.replace(match_text, replacement)
                                changed = True
                    
                    if changed:
                        with open(md_filename, 'w', encoding='utf-8') as f:
                            f.write(content)
                        print(f"    Updated {md_filename}")
                        # Mark this file as processed so we don't apply the generic question mark fix to it
                        processed_md_files.add(md_filename)
                    else:
                        print(f"    No changes needed for {md_filename}")

                except Exception as e:
                    print(f"    Error processing {md_filename}: {e}")

    # 2. Apply Question Mark fix to remaining markdown files
    print("\nApplying Question Mark fix to remaining Markdown files...")
    fix_question_marks_in_markdown_files()

if __name__ == "__main__":
    main()

