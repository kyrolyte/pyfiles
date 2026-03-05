import os
import re
import sys

# Regex patterns
NO_PATTERN = re.compile(r'No\. ((?:\d+[A-Za-z]?)(?:\s*[&-]\s*\d+[A-Za-z]?)*)')
H1_PATTERN = re.compile(r'^# (.+)', re.MULTILINE)


def extrano_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    updated_lines = []
    for line in lines:
        no_match = NO_PATTERN.search(line)
        if not no_match:
            updated_lines.append(line)

    if len(updated_lines) < len(lines):  # Check if any lines were removed
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(updated_lines)
        
        print(f"Updated: {filepath}")



def process_markdown_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Search for "No. <number>"
    no_match = NO_PATTERN.search(content)
    if not no_match:
        return  # No match found, skip file

    number = no_match.group(1)

    # Search for first H1 header
    h1_match = H1_PATTERN.search(content)
    if not h1_match:
        return  # No H1 found, skip file

    original_header = h1_match.group(1)

    # Avoid modifying if already formatted
    if original_header.startswith(f"{number} |"):
        return

    new_header = f"# Sermon {number} | {original_header}"

    # Replace only the first H1 occurrence
    updated_content = (
        content[:h1_match.start()] +
        new_header +
        content[h1_match.end():]
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(updated_content)

    print(f"Updated: {filepath}")


def process_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                filepath = os.path.join(root, file)
                # process_markdown_file(filepath)
                extrano_file(filepath)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <directory>")
        sys.exit(1)

    target_directory = sys.argv[1]
    process_directory(target_directory)
