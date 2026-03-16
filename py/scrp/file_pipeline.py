import requests
from bs4 import BeautifulSoup
import html2text
import re
import os

def clean_numbers(number_range):
    """Removes leading zeros from the URL segment (e.g., '025-032' -> '25-32')."""
    # Split by hyphen, strip leading zeros, and join back
    return "-".join(part.lstrip('0') for part in number_range.split('-'))

def process_links(urls):
    converter = html2text.HTML2Text()
    converter.ignore_links = False
    headers = {'User-Agent': 'Mozilla/5.0'}

    for url in urls:
        try:
            # 1. Extract the number range from the end of the URL
            match = re.search(r'(\d+-\d+)/?$', url)
            if not match:
                print(f"Skipping {url}: No number range found at end.")
                continue
            
            raw_range = match.group(1)
            formatted_range = clean_numbers(raw_range)
            filename = f"verses-{formatted_range}.md"

            print(f"Processing: {url} -> {filename}")

            # 2. Scrape the content
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            main_content = soup.find('main')

            if not main_content:
                print(f"Error: No <main> tag found at {url}")
                continue

            markdown_text = converter.handle(str(main_content))

            # 3. Demote Headers (Applying logic directly to the string)
            demoted_lines = []
            for line in markdown_text.splitlines():
                # if line.startswith('#'):
                    # demoted_lines.append('##' + line)
                # else:
                demoted_lines.append(line)
            
            final_output = "\n".join(demoted_lines)

            # 4. Save to the specific filename
            with open(filename, "w", encoding="utf-8") as f:
                f.write(final_output)
            
            print(f"Successfully saved {filename}")

        except Exception as e:
            print(f"An error occurred with {url}: {e}")

# --- CONFIGURATION ---
link_array = [
    "https://url.com/025-032",
]

if __name__ == "__main__":
    process_links(link_array)
