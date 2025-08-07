import time
from src.entry.functions.start_budo_backup.workflow import main_budo_backup
from src.shared.infrastructure.logging.syslog import logger


if __name__ == "__main__":

    start_time = time.time()
    main_budo_backup()
    end_time = time.time()

    elapsed_time = end_time - start_time
    logger.info("Function budo_backup completed in %.2f seconds", elapsed_time)
