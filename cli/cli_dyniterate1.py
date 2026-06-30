import os
import re

# Find all CSV files in the current directory that match the pattern sermon_<n>_results.csv
current_dir = os.getcwd()
pattern = re.compile(r'^sermon_(\d+)_results\.csv$')

found_numbers = []
for filename in os.listdir(current_dir):
    match = pattern.match(filename)
    if match:
        n = int(match.group(1))
        found_numbers.append(n)

if not found_numbers:
    print("No matching CSV files found.")
else:
    start = min(found_numbers)
    end = max(found_numbers)
    
    for n in range(start, end + 1):
        filename = f"sermon_{n}_results.csv"
        filepath = os.path.join(current_dir, filename)
        print(n)
        if os.path.exists(filepath):
            print(f"sermon_{n}_results.csv found")

