import os


def replace_question_mark_in_markdown_files():
    """
    Iterate through all markdown files in the current directory.
    Replace the pattern '" ?' with '? "' (i.e., replace '"' followed by '?' followed by space
    with '?' followed by '"' followed by space).
    """
    # Get all .md files in the current directory
    md_files = [f for f in os.listdir('.') if f.endswith('.md') and os.path.isfile(f)]
    
    # The pattern to find: '" ' + '?' + ' ' => '" ?'
    old_pattern = '"? '
    # The replacement: '?' + '"' + ' ' => '? "'
    new_pattern = '?" '
    
    for md_file in md_files:
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replace all occurrences of the old pattern with the new pattern
            new_content = content.replace(old_pattern, new_pattern)
            
            # Only write if content changed
            if new_content != content:
                with open(md_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Updated: {md_file}")
            else:
                print(f"No changes: {md_file}")
        except Exception as e:
            print(f"Error processing {md_file}: {e}")


if __name__ == '__main__':
    replace_question_mark_in_markdown_files()

