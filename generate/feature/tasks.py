import os
import argparse
from common import snake, create_files, create_folders


def create_structure(base_dir, feature_name):
    """
    Creates the directory structure for features based on the contents of the 'src/features' directory.

    Args:
        base_dir: The base directory where the 'src' directory is located.
        feature_name: The name of the feature to create the directory structure for.
    """
    feature_name = snake(feature_name)
    tasks_dir = os.path.join(base_dir, "tasks")

    if not os.path.exists(tasks_dir):
        os.makedirs(tasks_dir, exist_ok=True)

    create_folders([f"todo/{feature_name}",
                    f"inprogress/{feature_name}",
                    f"done/{feature_name}"], tasks_dir)
    todo_dir = os.path.join(tasks_dir, f"todo/{feature_name}")

    create_files(todo_dir, '.feature')
    create_files(todo_dir, '.mermaid')


def main():
    """
    Main function to execute the feature structure creation.
    """
    parser = argparse.ArgumentParser(
        description="Create feature directory structure.")
    parser.add_argument("-b", "--base_directory", required=True,
                        help="Base directory for the project.")
    parser.add_argument("-f", "--feature_name",
                        required=True, help="Name of the feature.")

    args = parser.parse_args()
    base_directory = args.base_directory
    feature_name = args.feature_name
    create_structure(base_directory, feature_name)


if __name__ == "__main__":
    main()
