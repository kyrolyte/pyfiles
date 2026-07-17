import os
import re

def natural_sort_key(s):
    """ Helper to sort strings containing numbers correctly """
    return [int(text) if text.isdigit() else text.lower() 
            for text in re.split('([0-9]+)', s)]

def combine_markdown(output_filename="combined.md"):
    # Get all markdown files in current directory
    files = [f for f in os.listdir('.') if f.endswith('.md') and f != output_filename]
    
    # Sort them naturally (1, 2, 10 instead of 1, 10, 2)
    files.sort(key=natural_sort_key)
    
    print(f"Found {len(files)} files. Combining in this order:")
    for f in files:
        print(f" - {f}")

    with open(output_filename, 'w', encoding='utf-8') as outfile:
        for filename in files:
            with open(filename, 'r', encoding='utf-8') as infile:
                outfile.write(infile.read())
                # Add two newlines between files to prevent text merging
                outfile.write("\n\n")

    print(f"\nSuccess! Created {output_filename}")

if __name__ == "__main__":
    combine_markdown()

