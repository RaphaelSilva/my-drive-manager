from re import sub
import os


def snake(s):
    return '_'.join(
        sub('([A-Z][a-z]+)', r' \1',
            sub('([A-Z]+)', r' \1',
                s.replace('-', ' '))).split()).lower()


def create_files(subdir_path, file_name):
    file_path = os.path.join(subdir_path, file_name)
    with open(file_path, "w", encoding="utf-8") as f:
        # Create empty __init__.py files
        f.write("")
    return file_path


def create_folders(subdirectories, base_path):
    for subdir in subdirectories:
        subdir_path = os.path.join(base_path, subdir)
        os.makedirs(subdir_path, exist_ok=True)



