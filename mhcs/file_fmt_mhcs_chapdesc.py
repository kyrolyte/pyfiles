import os
import re

def process_markdown_files():
    
    for filename in os.listdir('.'):
        if filename.startswith("chapter-") and filename.endswith(".md"):
            
            match = re.match(r"chapter-(\d+)\.md", filename)
            
            if match:
                chapter_num = int(match.group(1))
                description_file_name = f"description-{chapter_num}.md"
                
                if os.path.exists(description_file_name):
                    try:
                        with open(filename, 'r', encoding='utf-8') as f:
                            lines = f.readlines()

                        if len(lines) >= 5:
                            with open(description_file_name, 'r', encoding='utf-8') as desc_f:
                                description_content = desc_f.read().strip()
                            
                            if description_content:
                                lines[4] = "  " + description_content + "\n"
                                
                                with open(filename, 'w', encoding='utf-8') as f:
                                    f.writelines(lines)
                                
                    except Exception:
                        pass

if __name__ == "__main__":
    process_markdown_files()

