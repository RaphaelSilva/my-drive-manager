import os
import shutil
import datetime
from queue import Queue
import threading

# Placeholder for cloud storage interaction (replace with actual cloud library)
def download_from_cloud(cloud_path, local_path):
    """Simulates downloading a file from a cloud drive."""
    try:
        # Replace this with actual cloud download logic
        print(f"Downloading {cloud_path} to {local_path}")
        # Simulate download time
        #time.sleep(1) # remove this line to make the copy faster. It's here to make it look more real
        with open(local_path, 'wb') as f:
            f.write(b'This is a dummy file') # This is a dummy file. Replace with actual file reading

        return True
    except Exception as e:
        print(f"Error downloading {cloud_path}: {e}")
        return False

def backup_photo(source, destination, overwrite=False):
    """Copies a single photo, handling overwrites."""
    try:
        if os.path.exists(destination) and not overwrite:
            print(f"Skipping existing file: {destination}")
            return False  # Skip if exists and overwrite is False

        shutil.copy2(source, destination)  # copy2 preserves metadata
        print(f"Copied {source} to {destination}")
        return True
    except Exception as e:
        print(f"Error copying {source}: {e}")
        return False


def process_queue(queue, destination_root, overwrite):
    while True:
        item = queue.get()
        if item is None:
            break  # Sentinel value to stop workers

        source, destination = item
        backup_photo(source, destination, overwrite)
        queue.task_done()


def backup_photos(source_dir, destination_dir, extensions, overwrite=False):
    """Main backup function."""
    queue = Queue()
    num_threads = 5  # Adjust as needed

    for filename in os.listdir(source_dir):
        source_path = os.path.join(source_dir, filename)
        if os.path.isfile(source_path):
            ext = os.path.splitext(filename)[1].lower()
            if ext in extensions:
                try:
                    timestamp = datetime.datetime.fromtimestamp(os.path.getmtime(source_path))
                    year_dir = os.path.join(destination_dir, str(timestamp.year))
                    month_dir = os.path.join(year_dir, str(timestamp.month).zfill(2))
                    day_dir = os.path.join(month_dir, str(timestamp.day).zfill(2))
                    os.makedirs(day_dir, exist_ok=True)
                    destination_path = os.path.join(day_dir, filename)
                    queue.put((source_path, destination_path))

                except Exception as e:
                    print(f"Error processing {filename}: {e}")


    # Start worker threads
    for i in range(num_threads):
        worker = threading.Thread(target=process_queue, args=(queue, destination_dir, overwrite))
        worker.daemon = True # Allow the program to exit even if threads are still running
        worker.start()

    queue.join()  # Wait for all tasks to finish
    queue.put(None)  # Sentinel value for worker threads to exit


if __name__ == "__main__":
    source_dir = "/path/to/cloud/drive"  # Replace with actual path
    destination_dir = "/path/to/destination/drive"  # Replace with actual path
    extensions = {'.jpg', '.jpeg', '.png', '.gif'} # Add more extensions as needed
    overwrite = False # Set to True to enable overwriting

    # Check if destination directory has enough space (simplified check)
    try:
        if shutil.disk_usage(destination_dir).free < 1024 * 1024 * 1024:  # Check if less than 1GB free
            raise Exception("Insufficient disk space")
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

    backup_photos(source_dir, destination_dir, extensions, overwrite)
    print("Backup complete.")

