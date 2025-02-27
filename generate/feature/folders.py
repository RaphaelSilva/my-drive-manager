import os
import argparse
from re import sub


def snake(s):
    return '_'.join(
        sub('([A-Z][a-z]+)', r' \1',
            sub('([A-Z]+)', r' \1',
                s.replace('-', ' '))).split()).lower()


def create_init_files(subdir_path):
    with open(os.path.join(subdir_path, "__init__.py"), "w", encoding="utf-8") as f:
        # Create empty __init__.py files
        f.write("")


def create_feature_structure(base_dir, feature_name):
    """
    Creates the directory structure for features based on the contents of the 'src/features' directory.

    Args:
        base_dir: The base directory where the 'src' directory is located.
        feature_name: The name of the feature to create the directory structure for.
    """
    feature_name = snake(feature_name)
    features_dir = os.path.join(base_dir, "src", "feature")
    if not os.path.exists(features_dir):
        print(f"Error: Directory '{features_dir}' not found.")
        return

    feature_path = os.path.join(features_dir, feature_name)
    if not os.path.exists(feature_path):
        os.makedirs(feature_path, exist_ok=True)
        create_init_files(feature_path)

    if not os.path.isdir(feature_path):
        print(f"Error: '{feature_path}' is not a directory.")
        return

    # Create subdirectories within the feature directory
    subdirectories = [
        "adapters",
        "domain/entities",
        "domain/business",
        "domain/repositories",
        "infrastructure",
        "presentation"]
    for subdir in subdirectories:
        subdir_path = os.path.join(feature_path, subdir)
        os.makedirs(subdir_path, exist_ok=True)
        create_init_files(subdir_path)

    # # Create files within the feature directory
    # files = ["data/data_source.py", "data/repository.py", "domain/entities.py",
    #          "domain/use_cases.py", "presentation/bloc.py", "presentation/event.py", "presentation/state.py"]
    # for file in files:
    #     file_path = os.path.join(feature_root, file)
    #     os.makedirs(os.path.dirname(file_path), exist_ok=True)
    #     with open(file_path, "w") as f:
    #         pass


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
    create_feature_structure(base_directory, feature_name)


if __name__ == "__main__":
    main()
