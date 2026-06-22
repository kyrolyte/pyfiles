import os
import re

def fix_text(text):
    text = re.sub(r"'S", "'s", text)

    def a_replacer(match):
        start = match.start()
        if start == 0:
            return 'A'

        idx = start - 1
        while idx >= 0 and text[idx].isspace():
            idx -= 1

        if idx < 0:
            return 'A'

        prev_char = text[idx]
        if prev_char in '.!?":|':
            return 'A'

        return 'a'

    return re.sub(r'\bA\b', a_replacer, text)

def main():
    files_processed = 0
    for filename in os.listdir('.'):
        if filename.endswith('.md'):
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()

            new_content = fix_text(content)

            if new_content != content:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                files_processed += 1
                print(f"Fixed {filename}")

    print(f"Total files fixed: {files_processed}")

if __name__ == "__main__":
    main()

