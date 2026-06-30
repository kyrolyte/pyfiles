import os
import re
import subprocess

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
            
            # Execute the pi command
            pi_command = f'pi -p "Read the sermon_{n}_results.csv file. For each row, find the string under Match column in the markdown file under the File column using the Line and Span columns to determine location. Read the value under the Context column to determine how the string is used. Update the string to be lower case."'
            result = subprocess.run(pi_command, shell=True, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"Error executing pi command for sermon_{n}: {result.stderr}")
                continue
            
            # Execute git add and commit
            git_add_command = f"git add sermon_{n}.md"
            result_add = subprocess.run(git_add_command, shell=True, capture_output=True, text=True)
            if result_add.returncode != 0:
                print(f"Error executing git add for sermon_{n}: {result_add.stderr}")
                continue
            
            git_commit_command = f'git commit -m "chore: clean up on sermon {n}"'
            result_commit = subprocess.run(git_commit_command, shell=True, capture_output=True, text=True)
            if result_commit.returncode != 0:
                print(f"Error executing git commit for sermon_{n}: {result_commit.stderr}")
                continue
            
            # Execute rm commands
            rm_json_command = f"rm sermon_{n}.json"
            result_rm_json = subprocess.run(rm_json_command, shell=True, capture_output=True, text=True)
            if result_rm_json.returncode != 0:
                print(f"Error executing rm sermon_{n}.json for sermon_{n}: {result_rm_json.stderr}")
                continue
            
            rm_csv_command = f"rm sermon_{n}_results.csv"
            result_rm_csv = subprocess.run(rm_csv_command, shell=True, capture_output=True, text=True)
            if result_rm_csv.returncode != 0:
                print(f"Error executing rm sermon_{n}_results.csv for sermon_{n}: {result_rm_csv.stderr}")
                continue
            
            print(f"All commands completed successfully for sermon_{n}")

