import os
import sys

PREVIEW_LINES = 15
PREVIEW_CHARS = 100


def get_markdown_files(directory):
    return [
        os.path.join(directory, f)
        for f in os.listdir(directory)
        if f.lower().endswith(".md") and os.path.isfile(os.path.join(directory, f))
    ]


def preview_file(filepath):
    print(f"\n{'=' * 60}")
    print(f"File: {filepath}")
    print(f"{'=' * 60}")

    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for i, line in enumerate(lines[:PREVIEW_LINES], start=1):
        preview_text = line.rstrip("\n")[:PREVIEW_CHARS]
        print(f"{i:>3}: {preview_text}")

    return lines


def get_line_range(max_lines):
    try:
        start = int(input("\nEnter starting line number (0 to skip): "))
        if start == 0:
            return 0, 0

        end = int(input("Enter ending line number (0 to skip): "))
        if end == 0:
            return 0, 0

        if start < 1 or end < 1 or start > max_lines or end > max_lines:
            print("Invalid line numbers. Skipping file.")
            return 0, 0

        if start > end:
            print("Start cannot be greater than end. Skipping file.")
            return 0, 0

        return start, end

    except ValueError:
        print("Invalid input. Skipping file.")
        return 0, 0


def delete_lines(filepath, lines, start, end):
    # Convert to zero-based index
    new_lines = lines[: start - 1] + lines[end:]

    with open(filepath, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

    print(f"Deleted lines {start} to {end} from {filepath}")


def main():
    directory = input("Enter directory path: ").strip()

    if not os.path.isdir(directory):
        print("Invalid directory.")
        sys.exit(1)

    markdown_files = get_markdown_files(directory)

    if not markdown_files:
        print("No markdown files found.")
        return

    for filepath in markdown_files:
        lines = preview_file(filepath)

        if not lines:
            print("File is empty. Skipping.")
            continue

        start, end = get_line_range(len(lines))

        if start == 0 or end == 0:
            print("Skipping file.")
            continue

        delete_lines(filepath, lines, start, end)

    print("\nDone.")


if __name__ == "__main__":
    main()
