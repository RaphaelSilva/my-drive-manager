import argparse  # Add argparse for command-line arguments
import datetime
import mimetypes
import os
import shutil

from PIL import Image, UnidentifiedImageError
from PIL.ExifTags import TAGS


def copy_file(source_path, destination_dir):
    """
    Copies a file from a source path to a destination directory.

    Args:
        source_path (str): The full path to the source file.
        destination_dir (str): The full path to the destination directory.
    """
    if not os.path.exists(source_path):
        print(f"Error: Source file '{source_path}' not found.")
        return

    if not os.path.isdir(destination_dir):
        try:
            os.makedirs(destination_dir)
            print(f"Created destination directory: '{destination_dir}'")
        except OSError as e:
            print(f"Error creating destination directory '{destination_dir}': {e}")
            return

    file_name = os.path.basename(source_path)
    destination_path = os.path.join(destination_dir, file_name)

    try:
        shutil.copy2(source_path, destination_path)
        print(f"File '{source_path}' copied to '{destination_path}'")
    except (IOError, shutil.Error) as e: # Catch specific exceptions for file operations
        print(f"Error copying file: {e}")

# Example usage:
# source_file = "/path/to/your/source/file.txt"  # Replace with your source file path
# destination_folder = "/path/to/your/destination/folder"  # Replace with your destination directory path
# copy_file(source_file, destination_folder)


def list_files_in_directory(directory_path):
    """
    Lists all files in a given directory.

    Args:
        directory_path (str): The full path to the directory.

    Returns:
        list: A list of file names in the directory, or an empty list if
              the directory doesn't exist or an error occurs.
    """
    if not os.path.isdir(directory_path):
        print(f"Error: Directory '{directory_path}' not found.")
        return []

    try:
        files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
        print(f"Files in '{directory_path}': {files}")
        return files
    except OSError as e:
        print(f"Error listing files in directory '{directory_path}': {e}")
        return []

# Example usage:
# target_directory = "/path/to/your/directory"  # Replace with your directory path
# files_in_dir = list_files_in_directory(target_directory)
# if files_in_dir:
#     print("Found files:", files_in_dir)

def get_photo_creation_date(file_path):
    """
    Extracts the creation date from a photo's EXIF metadata.

    Args:
        file_path (str): The full path to the photo file.

    Returns:
        str: The creation date as a string (YYYY:MM:DD HH:MM:SS) or None if not found.
    """
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return None

    try:
        image = Image.open(file_path)
        exif_data = image.getexif() # Use public method getexif()

        if not exif_data:
            print(f"No EXIF metadata found in '{file_path}'.")
            return None

        date_time_original = None
        date_time = None

        for tag_id, value in exif_data.items():
            tag_name = TAGS.get(tag_id, tag_id)
            if tag_name == 'DateTimeOriginal':
                date_time_original = str(value)
            elif tag_name == 'DateTime':
                date_time = str(value)

        if date_time_original:
            print(f"Found DateTimeOriginal: {date_time_original} in '{file_path}'")
            return date_time_original
        elif date_time:
            print(f"Found DateTime (fallback): {date_time} in '{file_path}'")
            return date_time

        print(f"Creation date tag not found in EXIF data for '{file_path}'.")
        return None

    except FileNotFoundError:
        print(f"Error: File not found at '{file_path}'.")
        return None
    except UnidentifiedImageError:
        print(f"Error: Cannot identify image file '{file_path}'. It might not be a supported image format or it is corrupted.")
        return None
    except (IOError, SyntaxError) as e: # More specific exceptions for image processing
        print(f"An error occurred while processing '{file_path}': {e}")
        return None

# Example usage:
# photo_file = "/path/to/your/photo.jpg"  # Replace with your photo file path
# creation_date = get_photo_creation_date(photo_file)
# if creation_date:
#     print(f"The photo was taken on: {creation_date}")

def identify_file_type(file_path):
    """
    Identifies if a file is a photo or a video based on its MIME type.

    Args:
        file_path (str): The full path to the file.

    Returns:
        str: 'photo', 'video', or 'unknown' if the type cannot be determined
             or the file doesn't exist.
    """
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return 'unknown'

    if not os.path.isfile(file_path):
        print(f"Error: Path '{file_path}' is not a file.")
        return 'unknown'

    mime_type, _ = mimetypes.guess_type(file_path)

    if mime_type:
        if mime_type.startswith('image/'):
            return 'photo'
        elif mime_type.startswith('video/'):
            return 'video'

    # Fallback for common extensions if MIME type is not definitive
    _, ext = os.path.splitext(file_path.lower())
    photo_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.heic', '.webp']
    video_extensions = ['.mp4', '.mov', '.avi', '.mkv', '.wmv', '.flv', '.webm']

    if ext in photo_extensions:
        return 'photo'
    elif ext in video_extensions:
        return 'video'

    print(f"Could not determine file type for '{file_path}'. MIME type: {mime_type}")
    return 'unknown'

# Example usage:
# file1 = "/path/to/your/image.jpg"
# file2 = "/path/to/your/video.mp4"
# file3 = "/path/to/your/document.txt"

# print(f"'{file1}' is a: {identify_file_type(file1)}")
# print(f"'{file2}' is a: {identify_file_type(file2)}")
# print(f"'{file3}' is a: {identify_file_type(file3)}")

def ensure_path_exists(directory_path):
    """
    Ensures that a directory path exists, creating any missing directories.

    Args:
        directory_path (str): The full path to the directory.

    Returns:
        bool: True if the path exists or was successfully created, False otherwise.
    """
    try:
        os.makedirs(directory_path, exist_ok=True)
        print(f"Path '{directory_path}' ensured.")
        return True
    except OSError as e:
        print(f"Error creating directory path '{directory_path}': {e}")
        return False

# Example usage:
# path_to_check = "/path/to/your/new/or/existing/folder"
# if ensure_path_exists(path_to_check):
#     print(f"Directory '{path_to_check}' is ready.")
# else:
#     print(f"Failed to create or ensure directory '{path_to_check}'.")

def organize_photo_by_date(file_path, destination_path_root):
    """
    Checks if a file is a photo, extracts its creation date, and creates a
    YYYY/MM/DD directory structure under destination_path_root.

    Args:
        file_path (str): The full path to the photo file.
        destination_path_root (str): The root directory for the new structure.

    Returns:
        str: The full path to the YYYY/MM/DD directory if successful, None otherwise.
    """
    file_type = identify_file_type(file_path)
    if file_type != 'photo':
        print(f"File '{file_path}' is not a photo (type: {file_type}). Skipping organization.")
        return None

    creation_date_str = get_photo_creation_date(file_path)
    if not creation_date_str:
        print(f"Could not extract creation date for photo '{file_path}'. Skipping organization.")
        return None

    try:
        # EXIF date format is often YYYY:MM:DD HH:MM:SS
        # Sometimes it might be just YYYY:MM:DD
        if ' ' in creation_date_str:
            date_obj = datetime.datetime.strptime(creation_date_str.split(' ')[0], "%Y:%m:%d")
        else:
            date_obj = datetime.datetime.strptime(creation_date_str, "%Y:%m:%d")
        
        year = date_obj.strftime("%Y")
        month = date_obj.strftime("%m")
        day = date_obj.strftime("%d")

        organized_path = os.path.join(destination_path_root, year, month, day)

        if ensure_path_exists(organized_path):
            print(f"Successfully created/ensured path: {organized_path} for file '{file_path}'")
            return organized_path
        else:
            print(f"Failed to create directory structure for '{file_path}' at '{organized_path}'.")
            return None

    except ValueError as e:
        print(f"Error parsing date string '{creation_date_str}' for file '{file_path}': {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while organizing photo '{file_path}': {e}")
        return None

# Example usage:
# photo_to_organize = "/path/to/your/photo.jpg" # Replace with your photo file
# root_for_organization = "/path/to/organized_photos_root" # Replace with your desired root

# final_path = organize_photo_by_date(photo_to_organize, root_for_organization)
# if final_path:
#     print(f"Photo can be moved to: {final_path}")
# else:
#     print(f"Photo organization failed for: {photo_to_organize}")

def execute(origin_dir, destination_root):
    """
    Lists all files in the origin directory, and for each photo, organizes it
    into a YYYY/MM/DD structure under the destination_root.

    Args:
        origin_dir (str): The directory containing files to process.
        destination_root (str): The root directory where photos will be organized.
    """
    if not os.path.isdir(origin_dir):
        print(f"Error: Origin directory '{origin_dir}' not found or is not a directory.")
        return

    if not os.path.isdir(destination_root):
        print(f"Warning: Destination root '{destination_root}' not found. It will be created if needed.")
        # ensure_path_exists will handle creation if it's a valid path to be created

    print(f"Starting to process files from '{origin_dir}' to be organized under '{destination_root}'")
    files_to_process = list_files_in_directory(origin_dir)

    if not files_to_process:
        print(f"No files found in '{origin_dir}'.")
        return

    organized_count = 0
    skipped_count = 0
    skipped_list = []

    for file_name in files_to_process:
        full_file_path = os.path.join(origin_dir, file_name)
        print(f"Processing file: {full_file_path}")
        organized_path = organize_photo_by_date(full_file_path, destination_root)
        if organized_path:
            copy_file(full_file_path, organized_path)
            print(f"  -> Copied '{file_name}' to '{organized_path}'")
            organized_count += 1
        else:
            print(f"  -> Skipped organization for '{file_name}'")
            skipped_count += 1
            skipped_list.append(full_file_path)
    if skipped_list:
        print(f"Skipped files: {skipped_count}. Details: {', '.join(skipped_list)}")
        with open("skipped_files.txt", "w", encoding="utf-8") as f:
            for item in skipped_list:   
                f.write(item + "\n")
    
    print(f"Processing complete. Organized: {organized_count} files. Skipped: {skipped_count} files.")

# Example usage:
# source_directory = "/path/to/your/source_photos_folder"  # Replace with your source folder
# target_organization_root = "/path/to/your/organized_library" # Replace with your target root
# execute(source_directory, target_organization_root)

def main():
    """
    Main function to parse command-line arguments and execute the photo organization.
    """
    parser = argparse.ArgumentParser(description="Organize photos by date into a directory structure.")
    parser.add_argument(
        "-o", "--origin", 
        required=True, 
        help="The source directory containing photos to organize."
    )
    parser.add_argument(
        "-d", "--destination", 
        required=True, 
        help="The root directory where photos will be organized into YYYY/MM/DD subdirectories."
    )

    args = parser.parse_args()

    print(f"Origin directory: {args.origin}")
    print(f"Destination root: {args.destination}")

    execute(args.origin, args.destination)

if __name__ == "__main__":
    main()
