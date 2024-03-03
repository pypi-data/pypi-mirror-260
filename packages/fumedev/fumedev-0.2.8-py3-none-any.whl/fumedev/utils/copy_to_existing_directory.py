import shutil
from pathlib import Path

# Function to copy contents into an existing directory, excluding .git
def copy_to_existing_directory(source, destination):
    source_path = Path(source)
    destination_path = Path(destination)

    if not source_path.exists() or not destination_path.exists():
        raise ValueError("Source or destination directory does not exist.")

    for item in source_path.iterdir():
        if item.name == '.git':  # Skip the .git directory
            continue

        destination_item = destination_path / item.name
        try:
            if item.is_dir():
                shutil.copytree(item, destination_item, dirs_exist_ok=True)
            else:
                shutil.copy2(item, destination_item)
        except Exception as e:
                print(f"Error copying {item}: {e}")