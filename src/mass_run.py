# Source - https://stackoverflow.com/a/30896056
# Posted by fferri
# Retrieved 2026-10-01, License - CC BY-SA 3.0

import libcst
import argparse
from pathlib import Path
import sys
import subprocess

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Read a folder path from CLI and list its contents."
    )
    parser.add_argument(
        "folder",
        type=str,
        help="Path to the folder"
    )

    args = parser.parse_args()

    # Convert to Path object
    folder_path = Path(args.folder)

    # Validate folder existence
    if not folder_path.exists():
        print(f"Error: The path '{folder_path}' does not exist.")
        sys.exit(1)
    if not folder_path.is_dir():
        print(f"Error: The path '{folder_path}' is not a directory.")
        sys.exit(1)

    # List contents
    for item in folder_path.iterdir():
        subprocess.call(["python", "main.py", item])

if __name__ == "__main__":
    main()