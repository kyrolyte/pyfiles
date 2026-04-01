#!/usr/bin/env python3
"""
update_front_matter.py

Recursively scans a directory for Markdown files (.md) and
adds a front‑matter block at the top of each file.

The script:
1. Skips files named `_index.md` or `README.md`.
2. Extracts the H1 header as `title`.
3. Extracts the paragraph(s) that follow each H2 header into a list called `passages`.
4. Builds a `readings` string from each passage:
   • Split the passage on the literal string ' — '.
   • Take the last split part.
   • Join multiple results with ', '.
5. Prepends a front‑matter block using the template supplied in the prompt,
   inserting a blank line between the block and the original H1 header.
"""

import sys
import re
from pathlib import Path
from typing import List

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def extract_title(content: str) -> str:
    """
    Return the first H1 header (line starting with '# ') without the leading '# '.
    If no H1 is found, returns an empty string.
    """
    match = re.search(r'^#\s+(.*)', content, flags=re.MULTILINE)
    return match.group(1).strip() if match else ""

def extract_passages(content: str) -> List[str]:
    """
    Return a list of the paragraph(s) that follow each H2 header.
    Only the first paragraph after each H2 is captured.
    """
    # Split content into sections by H2 headings
    sections = re.split(r'^##\s+.*$', content, flags=re.MULTILINE)
    # The first element is everything before the first H2 (ignore it)
    passages = []
    for section in sections[1:]:
        # Strip leading whitespace/newlines
        section = section.lstrip('\n')
        # Find the first paragraph (consecutive non-empty lines)
        match = re.match(r'([^\n]+(?:\n(?!#|$)[^\n]+)*)', section)
        if match:
            paragraph = match.group(1).strip()
            passages.append(paragraph)
    return passages

def build_readings(passages: List[str]) -> str:
    """
    Build the readings string from the passages list.
    Each passage is split on ' — ' and the last part is taken.
    Multiple results are joined with ', '.
    The string starts with 'Bible passages for this day: '.
    """
    results = []
    for passage in passages:
        parts = passage.split(' — ')
        if parts:
            results.append(parts[-1].strip())
    readings = "Passages for this day: "
    readings += ", ".join(results)
    return readings

def build_front_matter(title: str, readings: str) -> str:
    """
    Build the YAML front‑matter block with the provided title and readings.
    """
    fm = f"""---
title: "{title} | Read Online"
linkTitle: "{title}"
description: >
  Readings for {title}. {readings}
layout: single-section
---
"""
    return fm

def process_file(md_path: Path) -> None:
    """
    Read the Markdown file, generate front‑matter, and write back.
    """
    original_content = md_path.read_text(encoding="utf-8")

    title = extract_title(original_content)
    if not title:
        print(f"[WARN] No H1 header found in {md_path}. Skipping.")
        return

    passages = extract_passages(original_content)
    readings = build_readings(passages)
    front_matter = build_front_matter(title, readings)

    # Insert a blank line between front‑matter and original content
    new_content = front_matter.rstrip() + "\n\n" + original_content.lstrip("\n")

    md_path.write_text(new_content, encoding="utf-8")
    print(f"[OK] Updated front‑matter in {md_path}")

# --------------------------------------------------------------------------- #
# Main entry point
# --------------------------------------------------------------------------- #

def main(root_dir: Path) -> None:
    if not root_dir.is_dir():
        print(f"Error: {root_dir} is not a directory.")
        sys.exit(1)

    # Find all .md files, excluding _index.md and README.md
    md_files = [
        p for p in root_dir.rglob("*.md")
        if p.name not in {"_index.md", "README.md"}
    ]

    if not md_files:
        print("No Markdown files found.")
        return

    for md_file in md_files:
        process_file(md_file)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python update_front_matter.py /path/to/markdown/directory")
        sys.exit(1)

    root = Path(sys.argv[1]).resolve()
    main(root)


