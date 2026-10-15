# File Organiser

A Python script that sorts the files in a folder into subfolders by file type (Images, Documents, Videos, Audio, Archives, Programs, Blender, Code and Other).

## How it works

The script looks at each file's ending (for example .jpg or .pdf), checks it against a list of categories, and moves the file into a folder with the matching name. Files it doesn't recognise go into "Other".

## How to run it

1. Install Python 3.
2. Download file_organiser.py.
3. Run it from a terminal: `py file_organiser.py`

By default it organises your Downloads folder. To use a different folder, change the `FOLDER` line at the top of the script.

## Preview mode

The script starts with `DRY_RUN = True`, which only prints what it would move and doesn't change any files. Once the preview looks right, set `DRY_RUN = False` to move the files for real. It never overwrites a file that already exists.

## What I learned

- Working with files and folders in Python using pathlib and shutil
- Fixing indentation and syntax errors
- Adding a preview mode so the script is safe to test

## Ideas for improving it

- Sort files by date as well as type
- Let the user type in which folder to organise
- Add an undo option
- Add a simple window (GUI) so the script can be used without the terminal (Done)
