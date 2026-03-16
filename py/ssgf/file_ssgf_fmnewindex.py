import os
import re

# --- Constants ---
EXTRA_ONE = "MyBrand"
EXTRA_TWO = "Docs"
EXTRA_DESC = "Learn more about this section in our comprehensive guide."
DIRECTORY_PATH = "./content"

def extract_first_sentence(content):
    """Finds the first sentence after the '## Introduction' header."""
    match = re.search(r'## Introduction\s*\n+(.+)', content, re.MULTILINE)
    if match:
        paragraph = match.group(1).strip()
        sentence_match = re.split(r'(?<=[.!?])\s+', paragraph)
        if sentence_match:
            return sentence_match[0]
    return None

def process_content(content):
    # Regex to split front matter (between ---) from the body
    fm_match = re.match(r'^---\s*\n(.*?)\n---\s*\n?(.*)', content, re.DOTALL)
    
    if not fm_match:
        return content

    fm_block = fm_match.group(1)
    body_content = fm_match.group(2).lstrip() # Remove leading whitespace for header check
    
    # 1. Handle Title logic
    title_match = re.search(r'^title:\s*["\']?(.*?)["\']?\s*$', fm_block, re.MULTILINE)
    original_title = "Untitled" # Fallback
    
    if title_match:
        original_title = title_match.group(1)
        new_title = f"{original_title} {EXTRA_ONE} | {EXTRA_TWO}"
        
        # Add linkTitle if missing (using original title)
        if 'linkTitle:' not in fm_block:
            fm_block = re.sub(
                r'(^title:.*$)', 
                f'\\1\nlinkTitle: "{original_title}"', 
                fm_block, 
                flags=re.MULTILINE
            )
        
        # Update the main title with extras
        fm_block = re.sub(
            r'^title:.*$', 
            f'title: "{new_title}"', 
            fm_block, 
            flags=re.MULTILINE
        )

    # 2. Add Description if missing
    if 'description:' not in fm_block:
        intro_sentence = extract_first_sentence(body_content)
        desc_value = intro_sentence if intro_sentence else EXTRA_DESC
        fm_block += f"\ndescription: >\n  {desc_value}"

    # 3. Add Layout attribute to the end of front-matter
    if 'layout:' not in fm_block:
        fm_block = fm_block.strip() + "\nlayout: single-section"

    # 4. Check for H1 Header (# Title) in the body
    # This regex looks for a line starting with # (H1)
    if not re.search(r'^#\s+', body_content, re.MULTILINE):
        # Prepend the H1 header using the original title
        body_content = f"# {original_title}\n\n" + body_content

    # Reconstruct the file
    return f"---\n{fm_block}\n---\n\n{body_content}"

def main():
    if not os.path.exists(DIRECTORY_PATH):
        print(f"Error: Directory '{DIRECTORY_PATH}' not found.")
        return

    for root, dirs, files in os.walk(DIRECTORY_PATH):
        for file in files:
            if file == "_index.md":
                file_path = os.path.join(root, file)
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                updated_content = process_content(content)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                
                print(f"Updated: {file_path}")

if __name__ == "__main__":
    main()
