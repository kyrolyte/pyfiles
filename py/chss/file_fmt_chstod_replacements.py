import os

# Function to perform replacements on a file
def process_markdown_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Perform the replacements in sequence
        content = content.replace('.**', ' &mdash;**')
        content = content.replace(' * ', '* ')
        content = content.replace(' )', ')')

        # Write the modified content back to the file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)

        print(f"Processed: {file_path}")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

# Iterate through all .md files in the current directory
for filename in os.listdir('.'):
    if filename.endswith('.md'):
        process_markdown_file(filename)

