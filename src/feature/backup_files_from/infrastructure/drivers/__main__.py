import asyncio
import argparse
import sys

from src.feature.backup_files_from.infrastructure.drivers import mediainfo


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a specific function.")
    parser.add_argument("-r", "--run", type=str,
                        help="Name of the function to run (new_queue, main).", default="main")

    args = parser.parse_args()

    all_functions = {
        "mediainfo": mediainfo.test_mediainfo,
    }

    if args.run in all_functions:
        asyncio.run(all_functions[args.run](args))
    else:
        print(f"Available functions: {', '.join(all_functions.keys())}")
        sys.exit(1)
