#!/usr/bin/env python3
import sys
import re

def format_bible_reading(file_path: str) -> None:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)

    # 1. Extract title from front-matter
    title_match = re.search(r'title:\s*["\']?([^\n"\']+)', content)
    if not title_match:
        print("Error: Could not find 'title' in front-matter.")
        sys.exit(1)
    title = title_match.group(1).strip()

    # 2. Extract body content after front-matter
    # Front-matter is delimited by '---' at the start and end
    fm_parts = content.split('---', 2)
    if len(fm_parts) < 3:
        print("Error: Invalid front-matter format (missing closing '---').")
        sys.exit(1)
    body = fm_parts[2].strip()

    # 3. Build table
    header = "| Day | Family Morning | Family Evening | Private Morning | Private Evening |"
    separator = "|---|---|---|---|---|"
    rows = []

    for line in body.splitlines():
        line = line.strip()
        if not line:
            continue

        parts = line.split()
        # Expected pattern: Book Ch Book Ch Day Book Ch Book Ch
        if len(parts) < 9:
            print(f"Warning: Skipping malformed line: {line}")
            continue

        # Reconstruct passages to preserve original chapter formatting
        p1 = f"{parts[0].strip()} {parts[1].strip()}"
        p2 = f"{parts[2].strip()} {parts[3].strip()}"
        day = parts[4].strip()
        p3 = f"{parts[5].strip()} {parts[6].strip()}"
        p4 = f"{parts[7].strip()} {parts[8].strip()}"

        rows.append(f"| {day} | {p1} | {p2} | {p3} | {p4} |")

    # 4. Output formatted markdown
    print(f"# {title}")
    print()
    print(header)
    print(separator)
    for row in rows:
        print(row)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py /path/to/file.md")
        sys.exit(1)
    format_bible_reading(sys.argv[1])

