#!/usr/bin/env python3
"""
update_front_matter.py

Walks through all Markdown files in a user‑supplied directory (recursively),
detects the YAML front‑matter block (the section between the first two
lines that contain only `---`), and, if the file name contains a number,
appends a line `weight: <number>` at the bottom of that block.

Usage:
    python update_front_matter.py /path/to/markdown/dir
"""

import argparse
import os
import re
import sys
from pathlib import Path

# ------------------------------------------------------------
# Utility helpers
# ------------------------------------------------------------
def find_front_matter(lines):
    """
    Return a tuple (start_idx, end_idx) of the indices of the opening
    and closing `---` lines that delimit the front‑matter block.
    If no front‑matter is found, return (None, None).
    """
    # Search for the opening marker at the very first line
    if not lines:
        return None, None
    if not lines[0].strip() == "---":
        return None, None

    # Look for the next `---` line after the first one
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return 0, i
    return None, None

def extract_number_from_filename(filename):
    """
    Return the first integer found in the file name (without the path),
    or None if no number is present.
    """
    match = re.search(r"(\d+)", filename)
    return match.group(1) if match else None

# ------------------------------------------------------------
# Core processing
# ------------------------------------------------------------
def process_markdown_file(file_path):
    """
    Read the Markdown file, modify its front‑matter if required,
    and write it back. Returns a tuple (modified, skipped, error)
    where exactly one element is True.
    """
    try:
        lines = Path(file_path).read_text(encoding="utf-8").splitlines(keepends=True)
    except Exception as exc:
        print(f"❌ ERROR reading {file_path!r}: {exc}", file=sys.stderr)
        return False, False, True

    start, end = find_front_matter(lines)
    if start is None or end is None:
        # No front‑matter – skip
        return False, True, False

    # Grab the filename (without directory)
    basename = os.path.basename(file_path)
    number = extract_number_from_filename(basename)
    if number is None:
        # No number – nothing to add
        return False, False, False

    # Check if a weight already exists to avoid duplicates
    weight_exists = any(
        re.match(r"^\s*weight\s*:\s*\d+.*$", line.strip())
        for line in lines[start + 1 : end]
    )
    if weight_exists:
        # Already has a weight, skip adding another
        return False, False, False

    # Insert the weight line just before the closing `---`
    weight_line = f"weight: {number}\n"
    new_lines = lines[:end] + [weight_line] + lines[end:]

    try:
        Path(file_path).write_text("".join(new_lines), encoding="utf-8")
    except Exception as exc:
        print(f"❌ ERROR writing {file_path!r}: {exc}", file=sys.stderr)
        return False, False, True

    return True, False, False

# ------------------------------------------------------------
# Main driver
# ------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Add weight to Markdown front‑matter.")
    parser.add_argument(
        "directory",
        help="Root directory to scan for Markdown files (recursively).",
    )
    args = parser.parse_args()

    root = Path(args.directory)
    if not root.is_dir():
        print(f"❌ {root!r} is not a directory.", file=sys.stderr)
        sys.exit(1)

    total_files = 0
    updated_files = 0
    skipped_files = 0
    error_files = 0

    for dirpath, _, filenames in os.walk(root):
        for fname in filenames:
            if not fname.lower().endswith(".md"):
                continue
            full_path = Path(dirpath) / fname
            total_files += 1
            modified, skipped, error = process_markdown_file(full_path)
            if modified:
                updated_files += 1
                print(f"✅ Updated: {full_path}")
            elif skipped:
                skipped_files += 1
                print(f"⚠️  Skipped (no front‑matter or no number): {full_path}")
            elif error:
                error_files += 1
                print(f"❌ Error processing: {full_path}")

    # Summary
    print("\n===== SUMMARY =====")
    print(f"Total Markdown files processed: {total_files}")
    print(f"Files updated: {updated_files}")
    print(f"Files skipped: {skipped_files}")
    print(f"Files with errors: {error_files}")

if __name__ == "__main__":
    main()


