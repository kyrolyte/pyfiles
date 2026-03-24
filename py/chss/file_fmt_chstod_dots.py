import os

def update_markdown_files():
    # Define the pattern and the replacement
    search_text = ".** "
    replace_text = " &mdash;** "
    
    # Get all files in the current directory
    files = [f for f in os.listdir('.') if f.endswith('.md')]
    
    if not files:
        print("No markdown files found.")
        return

    for filename in files:
        try:
            # Read the file content
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.read()

            # Check if the pattern exists in the file to avoid unnecessary writes
            if search_text in content:
                new_content = content.replace(search_text, replace_text)

                # Write the updated content back to the file
                with open(filename, 'w', encoding='utf-8') as file:
                    file.write(new_content)
                
                print(f"Successfully updated: {filename}")
            else:
                print(f"No match found in: {filename}")

        except Exception as e:
            print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    update_markdown_files()
