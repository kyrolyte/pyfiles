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

def main():
    # Get all json files in the current directory
    json_files = [f for f in os.listdir('.') if f.endswith('.json')]

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
                else:
                    print(f"    No changes needed for {md_filename}")

            except Exception as e:
                print(f"    Error processing {md_filename}: {e}")

if __name__ == "__main__":
    main()
