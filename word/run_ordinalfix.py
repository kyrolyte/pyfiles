#!/usr/bin/env python3

import sys
import re
from pathlib import Path


def number_to_ordinal_word(n: int) -> str:
    if n < 1 or n > 200:
        return None

    ones = ["", "first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth",
            "tenth", "eleventh", "twelfth", "thirteenth", "fourteenth", "fifteenth", "sixteenth",
            "seventeenth", "eighteenth", "nineteenth", "twentieth"]
    tens_base = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
    tens_ord = ["", "", "twentieth", "thirtieth", "fortieth", "fiftieth", "sixtieth", "seventieth", "eightieth", "ninetieth"]

    if n <= 20:
        return ones[n]
    elif n < 100:
        t, o = divmod(n, 10)
        if o == 0:
            return tens_ord[t]
        else:
            return f"{tens_base[t]}-{ones[o]}"
    elif n == 100:
        return "one hundredth"
    elif n < 200:
        return f"one hundred and {number_to_ordinal_word(n - 100)}"
    else:
        return "two hundredth"


def replace_ordinal(match: re.Match) -> str:
    num = int(match.group(1))
    if 1 <= num <= 200:
        return number_to_ordinal_word(num)
    return match.group(0)


def process_directory(dir_path: str) -> None:
    target_dir = Path(dir_path)

    if not target_dir.exists():
        print(f"❌ Error: Directory '{target_dir}' does not exist.")
        sys.exit(1)
    if not target_dir.is_dir():
        print(f"❌ Error: '{target_dir}' is not a directory.")
        sys.exit(1)

    pattern = re.compile(r'\b(\d+)(?:st|nd|rd|th)\b', re.IGNORECASE)
    total_replacements = 0

    for md_file in target_dir.glob('*.md'):
        try:
            content = md_file.read_text(encoding='utf-8')
        except Exception as e:
            print(f"⚠️  Warning: Could not read '{md_file}': {e}")
            continue

        new_content, count = pattern.subn(replace_ordinal, content)

        if count > 0:
            try:
                md_file.write_text(new_content, encoding='utf-8')
                print(f"✅ Updated: {md_file.name} ({count} ordinal(s) replaced)")
                total_replacements += count
            except Exception as e:
                print(f"⚠️  Warning: Could not write to '{md_file}': {e}")
        else:
            print(f"⏭️  Skipped: {md_file.name} (no ordinals found)")

    print(f"\n🏁 Done. Total ordinals replaced: {total_replacements}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scriptmd.py <directory_path>")
        sys.exit(1)

    process_directory(sys.argv[1])

