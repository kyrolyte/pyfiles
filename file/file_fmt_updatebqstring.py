import os
from pathlib import Path

def update_markdown_blockquotes(directory: str) -> None:
    dir_path = Path(directory)

    # Validate directory
    if not dir_path.is_dir():
        print(f"❌ Error: '{directory}' is not a valid directory.")
        return

    excluded_names = {'_index', 'readme'}
    target_str = '> a '
    replacement_str = '> A '
    updated_count = 0

    print(f"🔍 Scanning directory recursively: {dir_path.resolve()}\n")

    for file_path in dir_path.rglob('*'):
        # Skip directories and non-markdown files
        if not file_path.is_file() or file_path.suffix.lower() != '.md':
            continue

        # Skip excluded filenames (case-insensitive)
        if file_path.stem.lower() in excluded_names:
            continue

        try:
            content = file_path.read_text(encoding='utf-8')

            # Only process files containing the target string
            if target_str in content:
                new_content = content.replace(target_str, replacement_str)
                file_path.write_text(new_content, encoding='utf-8')
                updated_count += 1
                print(f"✅ Updated: {file_path}")

        except PermissionError:
            print(f"⛔ Permission denied: {file_path}")
        except UnicodeDecodeError:
            print(f"⛔ Not a valid UTF-8 text file: {file_path}")
        except Exception as e:
            print(f"⛔ Error processing {file_path}: {e}")

    print(f"\n🎉 Done. Successfully updated {updated_count} file(s).")

if __name__ == "__main__":
    user_dir = input("Enter the directory path: ").strip().strip('"\'')
    update_markdown_blockquotes(user_dir)

