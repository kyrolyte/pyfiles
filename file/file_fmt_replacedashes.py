import os
import sys


def process_markdown_files(directory: str) -> None:
    """Recursively iterate through a directory and replace '--' with '&mdash;' in all .md files."""
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.lower().endswith('.md'):
                filepath = os.path.join(root, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Replace all instances of '--' with '&mdash;'
                    new_content = content.replace('--', '&mdash;')

                    if new_content != content:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"Updated: {filepath}")
                except (IOError, OSError) as e:
                    print(f"Error processing {filepath}: {e}")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        directory = input("Enter the directory path: ").strip()
    else:
        directory = sys.argv[1]

    if not os.path.isdir(directory):
        print(f"Error: '{directory}' is not a valid directory.")
        sys.exit(1)

    process_markdown_files(directory)

