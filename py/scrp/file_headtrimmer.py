import os

def trim_markdown_files():
    # Get the current working directory
    current_dir = os.getcwd()
    
    for filename in os.listdir(current_dir):
        # Target only markdown files
        if filename.endswith(".md"):
            with open(filename, 'r', encoding='utf-8') as file:
                lines = file.readlines()

            # Find the index of the first H1 header
            h1_index = -1
            for i, line in enumerate(lines):
                if line.strip().startswith('# '):
                    h1_index = i
                    break

            # If an H1 was found and it's not already the first line
            if h1_index != -1:
                # Rewrite the file with content starting from the H1
                with open(filename, 'w', encoding='utf-8') as file:
                    file.writelines(lines[h1_index:])
                print(f"✓ Processed: {filename}")
            else:
                print(f"- Skipped: {filename} (No H1 header found)")

if __name__ == "__main__":
    trim_markdown_files()
