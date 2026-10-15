"""
File Organiser
Sorts the files in a folder into subfolders by file type.
Change DRY_RUN to False to actually move the files.
"""

from pathlib import Path
import shutil

# Folder to organise. Change this to any folder you like.
FOLDER = Path.home() / "Downloads"

# True = only print what would happen. False = actually move files.
DRY_RUN = False

# Which file extensions go in which folder.
CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".xlsx", ".pptx", ".csv"],
    "Videos": [".mp4", ".mov", ".avi", ".mkv"],
    "Audio": [".mp3", ".wav", ".flac", ".m4a"],
    "Archives": [".zip", ".rar", ".7z"],
    "Programs": [".exe", ".msi"],
    "Blender": [".blend"],
    "Code": [".py", ".js", ".html", ".css"],
}


def get_category(file_path):
    """Return the folder name a file belongs in, based on its extension."""
    extension = file_path.suffix.lower()
    for category, extensions in CATEGORIES.items():
        if extension in extensions:
            return category
    return "Other"


def organise(folder):
    """Move every file in the folder into a subfolder for its type."""
    if not folder.exists():
        print(f"Folder not found: {folder}")
        return

    moved = 0
    for item in folder.iterdir():
        # Skip folders, only move files.
        if not item.is_file():
            continue

        category = get_category(item)
        destination_folder = folder / category
        destination = destination_folder / item.name

        # Don't overwrite a file that already exists there.
        if destination.exists():
            print(f"Skipped (already exists): {item.name}")
            continue

        if DRY_RUN:
            print(f"Would move: {item.name} -> {category} ({item.suffix})")
        else:
            destination_folder.mkdir(exist_ok=True)
            shutil.move(str(item), str(destination))
            print(f"Moved: {item.name} -> {category}")
        moved += 1

    action = "would be moved" if DRY_RUN else "moved"
    print(f"\nDone. {moved} file(s) {action}.")


if __name__ == "__main__":
    organise(FOLDER)
