#!/usr/bin/env python3
"""
md_lister.py

Usage:
    python md_lister.py /path/to/directory

The script walks the given directory tree, looks only at *.md files (except
`_index.md` and `README.md`) and prints the path of every file that can
be opened successfully.

"""

import argparse
import sys
from pathlib import Path


def parse_args() -> Path:
    """Parse the command‑line argument and return a Path object."""
    parser = argparse.ArgumentParser(
        description="Print all readable markdown files in a directory tree."
    )
    parser.add_argument(
        "directory",
        help="Directory to search (recursively).",
    )
    args = parser.parse_args()

    start = Path(args.directory).resolve()
    if not start.is_dir():
        parser.error(f"{start!s} is not a directory or does not exist")
    return start


def main() -> None:
    start_dir = parse_args()

    # Files to ignore (exact names, case‑sensitive)
    ignored = {"_index.md", "README.md"}

    # Walk the tree. `rglob("*.md")` gives us all *.md files recursively.
    for md_file in start_dir.rglob("*.md"):
        if md_file.name in ignored:
            continue  # skip the two names you asked for

        # Try to open the file.  We only care that it can be read.
        try:
            with md_file.open("r", encoding="utf-8") as f:
                f.read(1)  # read a tiny bit just to be sure
        except Exception:
            # If anything goes wrong (permission, encoding, etc.) we skip it.
            # You can uncomment the next line if you want to see the error.
            # print(f"⚠️  Cannot read {md_file}", file=sys.stderr, flush=True)
            continue

        # If we got here the file was opened successfully.
        # Print the path relative to the starting directory – nice for
        # large trees.
        print(md_file.relative_to(start_dir))


if __name__ == "__main__":
    main()

