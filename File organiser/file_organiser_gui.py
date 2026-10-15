"""
File Organiser (GUI version 2.0)
A simple window to sort the files in a folder into subfolders by type.

How to use:
1. Click "Choose folder" and pick the folder you want to sort.
2. Click "Preview" to see what would happen (nothing is moved).
3. Click "Organise files" to move the files for real.

Or click "Organise everything in Downloads" to sort your Downloads
folder in one go (it asks you to confirm first).
"""

import shutil
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, scrolledtext

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


def organise(folder, dry_run):
    """Sort the files in a folder. Returns a list of messages to show."""
    messages = []
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
            messages.append(f"Skipped (already exists): {item.name}")
            continue

        if dry_run:
            messages.append(f"Would move: {item.name} -> {category}")
        else:
            destination_folder.mkdir(exist_ok=True)
            shutil.move(str(item), str(destination))
            messages.append(f"Moved: {item.name} -> {category}")
        moved += 1

    word = "would be moved" if dry_run else "moved"
    messages.append(f"\nDone. {moved} file(s) {word}.")
    return messages


class FileOrganiserApp:
    """The window and its buttons."""

    def __init__(self, window):
        self.window = window
        self.folder = None

        window.title("File Organiser")
        window.geometry("620x460")

        # Top row: choose folder button and the chosen folder's name.
        top = tk.Frame(window)
        top.pack(fill="x", padx=10, pady=10)

        tk.Button(top, text="Choose folder", command=self.choose_folder).pack(
            side="left"
        )
        self.folder_label = tk.Label(top, text="No folder chosen", anchor="w")
        self.folder_label.pack(side="left", padx=10)

        # Middle row: preview and organise buttons.
        buttons = tk.Frame(window)
        buttons.pack(fill="x", padx=10)

        tk.Button(buttons, text="Preview", command=self.preview).pack(side="left")
        tk.Button(buttons, text="Organise files", command=self.run_for_real).pack(
            side="left", padx=10
        )
        tk.Button(
            buttons, text="Organise everything in Downloads", command=self.quick_downloads
        ).pack(side="left")

        # Bottom: a box that shows what the program is doing.
        self.output = scrolledtext.ScrolledText(window, state="disabled")
        self.output.pack(fill="both", expand=True, padx=10, pady=10)

    def choose_folder(self):
        """Open the folder picker pop-up."""
        chosen = filedialog.askdirectory(title="Choose a folder to organise")
        if chosen:
            self.folder = Path(chosen)
            self.folder_label.config(text=str(self.folder))
            self.show([f"Folder chosen: {self.folder}"])

    def check_folder(self):
        """Make sure a folder has been chosen before doing anything."""
        if self.folder is None:
            messagebox.showwarning("No folder", "Please choose a folder first.")
            return False
        return True

    def preview(self):
        """Show what would happen without moving anything."""
        if self.check_folder():
            self.show(organise(self.folder, dry_run=True))

    def quick_downloads(self):
        """One click: pick the Downloads folder and organise it (like version 1)."""
        downloads = Path.home() / "Downloads"
        if not downloads.exists():
            messagebox.showwarning("Not found", "Couldn't find your Downloads folder.")
            return
        self.folder = downloads
        self.folder_label.config(text=str(self.folder))
        self.run_for_real()

    def run_for_real(self):
        """Ask for confirmation, then move the files."""
        if not self.check_folder():
            return
        sure = messagebox.askyesno(
            "Are you sure?",
            f"This will move files in:\n{self.folder}\n\nContinue?",
        )
        if sure:
            self.show(organise(self.folder, dry_run=False))

    def show(self, messages):
        """Put messages in the output box."""
        self.output.config(state="normal")
        self.output.delete("1.0", "end")
        self.output.insert("end", "\n".join(messages))
        self.output.config(state="disabled")


if __name__ == "__main__":
    window = tk.Tk()
    FileOrganiserApp(window)
    window.mainloop()
