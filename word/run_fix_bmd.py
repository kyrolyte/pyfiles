import os
import re

def fix_text(text):
    # 1. Replace 'S with 's
    text = re.sub(r"'S", "'s", text)
    
    # 2. Replace standalone 'A' with 'a' if it's not at the start of a sentence.
    def a_replacer(match):
        start = match.start()
        if start == 0:
            return 'A'
        
        # Look back to see if it's the start of a sentence
        idx = start - 1
        # Skip whitespace
        while idx >= 0 and text[idx].isspace():
            idx -= 1
            
        if idx < 0:
            return 'A' # Start of file
            
        prev_char = text[idx]
        if prev_char in '.!?":|': # Include colon and pipe as they might preserve case
            return 'A'
        
        # If it's not preceded by sentence-ending punctuation, replace with 'a'
        return 'a'

    # Use \bA\b to find standalone 'A'
    # Note: \b might not work as expected with all characters, but for 'A' it's generally okay.
    # We want to find 'A' that is a whole word.
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
