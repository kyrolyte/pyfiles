   #!/usr/bin/env python3
   """
   run_valetodo_pi.py
   Executes run_valetodo.py to generate TODO.md, then iterates through each line
   and executes the `pi` command with each line as the -p argument.
   """

   import subprocess
   import time
   import sys
   import os
   from pathlib import Path

   def run_valetodo_script(directory: str) -> None:
       script_path = Path(__file__).resolve().parent / "run_valetodo.py"
       if not script_path.exists():
           print(f"❌ Error: '{script_path}' not found in the same directory.")
           sys.exit(1)

       print(f"🚀 Executing run_valetodo.py for directory: {directory}")
       result = subprocess.run(
           ["python3", str(script_path)],
           input=directory,
           text=True,
           check=True
       )

   def parse_todo_md(todo_path: Path) -> list[str]:
       if not todo_path.exists():
           print(f"❌ Error: '{todo_path}' not found. Ensure run_valetodo.py ran successfully.")
           sys.exit(1)

       items = []
       with open(todo_path, "r", encoding="utf-8") as f:
           for line in f:
               stripped = line.strip()
               if not stripped or stripped.startswith("#"):
                   continue
               items.append(stripped)
       return items

   def main():
       # Accept directory from CLI argument or prompt
       if len(sys.argv) > 1:
           target_dir = sys.argv[1]
       else:
           target_dir = input("Enter the directory path containing the JSON files: ").strip()

       target_path = Path(target_dir).resolve()
       if not target_path.is_dir():
           print(f"❌ Error: '{target_dir}' is not a valid directory.")
           sys.exit(1)

       # 1. Generate TODO.md
       run_valetodo_script(str(target_path))

       # 2. Parse TODO.md
       todo_path = Path.cwd() / "TODO.md"
       todo_items = parse_todo_md(todo_path)

       if not todo_items:
           print("✅ No issues found in TODO.md. Exiting.")
           return

       print(f"\n📝 Found {len(todo_items)} item(s) in TODO.md.\n")

       # 3. Process each item with `pi`
       for i, item in enumerate(todo_items, 1):
           print(f"=== Processing item {i}/{len(todo_items)} ===")
           try:
               subprocess.run(["pi", "-p", item], check=True)
           except subprocess.CalledProcessError as e:
               print(f"⚠️  Command failed for item {i}: {e}")
           except FileNotFoundError:
               print("❌ 'pi' command not found. Please ensure it's installed and in your PATH.")
               sys.exit(1)

           print("\n⏳ Waiting 30 seconds before next iteration...")
           time.sleep(30)

       print("\n🎉 All TODO.md items have been processed.")

   if __name__ == "__main__":
       main()

