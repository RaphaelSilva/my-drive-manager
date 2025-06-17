import argparse
from src.entry.functions.start_backup_from_icloud_photos  import workflow


def main():
    """
    Main function to parse command-line arguments and execute the photo organization.
    """
    parser = argparse.ArgumentParser(
        description="Organize photos by date into a directory structure.")
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
    parser.add_argument(
        "-l", "--log-level",
        required=False,
        default="info",
        help="The log level (info, debug, warner)"
    )

    args = parser.parse_args()

    print(f"Origin directory: {args.origin}")
    print(f"Destination root: {args.destination}")

    workflow.execute(args.origin, args.destination)


if __name__ == "__main__":
    main()
