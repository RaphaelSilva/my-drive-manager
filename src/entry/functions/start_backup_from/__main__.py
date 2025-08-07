import sys
import argparse
import asyncio
import time
from src.entry.functions.start_backup_from import list_all_files_into_queue
from src.shared.infrastructure.logging.syslog import logger

all_functions = {
    "list_all_files_into_queue": lambda args: list_all_files_into_queue.execute(
        args.origin, args.destination),
    "execute_workflow": lambda args: execute_workflow(args),
}


async def execute_workflow(args):
    io_tasks = [
        list_all_files_into_queue.execute(args.origin, args.destination),
    ]
    io_results = await asyncio.gather(*io_tasks)
    logger.info("Resultados I/O: %s", io_results)

if __name__ == "__main__":
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
    parser.add_argument(
        "-f", "--function",
        required=False,
        default="execute_workflow",
        help=f"The function to run (e.g., execute_workflow, {', '.join(all_functions.keys())}).",
    )

    args = parser.parse_args()

    if args.function not in all_functions:
        print(f"Available functions: {', '.join(all_functions.keys())}")
        sys.exit(1)

    if args.log_level:
        logger.setLevel(args.log_level.upper())

    logger.info("Running function: %s", args.function)
    logger.info("Origin directory: %s", args.origin)
    logger.info("Destination root: %s", args.destination)

    start_time = time.time()
    asyncio.run(all_functions[args.function](args))
    end_time = time.time()

    elapsed_time = end_time - start_time
    logger.info("Function %s completed in %.2f seconds",
                args.function, elapsed_time)
