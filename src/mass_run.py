import argparse
from pathlib import Path
from main import run
from rules import registry

def mass_run():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Read a folder path from CLI and list its contents."
    )
    parser.add_argument(
        "folder",
        type=str,
        help="Path to the folder"
    )
    #print(len(registry.registry))
    args = parser.parse_args()

    # Convert to Path object
    folder_path = Path(args.folder)

    # List contents
    count = 1
    for item in folder_path.iterdir():
        print(f'Running on {count} of 1095')
        run(item, registry)
        count += 1

if __name__ == "__main__":
    mass_run()