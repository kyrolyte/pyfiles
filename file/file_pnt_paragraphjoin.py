#!/usr/bin/env python3
"""
collapse_paragraphs.py  <path/to/file.md>

Read the supplied markdown file, collapse every paragraph that is split
across several lines into a *single* line per paragraph.

Rule
----
* A paragraph ends when the next line is empty or starts with a block‑quote
  (`>`) or a list item (`*`).
* All other non‑empty lines are considered part of the same paragraph
  and are joined with a single space between them.
"""

import sys
import argparse
from pathlib import Path


def collapse_paragraphs(lines):
    """
    Accept a list of raw lines (with the trailing '\n' removed)
    and return a new list of lines where paragraphs are collapsed.

    Parameters
    ----------
    lines : list of str
        Each line without the trailing newline character.

    Returns
    -------
    list of str
        The collapsed lines, ready to be joined with '\n'.
    """
    out_lines = []
    buffer = ""

    for raw in lines:
        line = raw.rstrip()          # remove trailing whitespace

        # 1. Blank line → paragraph break
        if line == "":
            if buffer:
                out_lines.append(buffer)
                buffer = ""
            out_lines.append("")     # keep the blank line
            continue

        # 2. Block quote or list item → new paragraph
        if line.startswith(">") or line.startswith("*"):
            if buffer:
                out_lines.append(buffer)
                buffer = ""
            out_lines.append(line)
            continue

        # 3. Normal paragraph line → join to buffer
        if buffer:
            buffer += " " + line
        else:
            buffer = line

    # flush the last paragraph if any
    if buffer:
        out_lines.append(buffer)

    return out_lines


def main():
    parser = argparse.ArgumentParser(
        description="Collapse multiline paragraphs in a markdown file.")
    parser.add_argument("md_file", type=Path,
                        help="Path to the markdown file to process")
    parser.add_argument("-o", "--output", type=Path, default=None,
                        help="Output file (default: overwrite input)")
    args = parser.parse_args()

    if not args.md_file.is_file():
        print(f"Error: {args.md_file!s} is not a file", file=sys.stderr)
        sys.exit(1)

    # read file
    raw_lines = args.md_file.read_text(encoding="utf-8").splitlines()

    # process
    collapsed = collapse_paragraphs(raw_lines)

    # decide where to write
    out_path = args.output or args.md_file
    out_path.write_text("\n".join(collapsed) + "\n", encoding="utf-8")
    print(f"Processed {args.md_file!s} → {out_path!s}")


if __name__ == "__main__":
    main()

