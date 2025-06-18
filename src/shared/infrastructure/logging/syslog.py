import datetime as dt
import logging.config
import logging.handlers
import os

from src.shared.infrastructure.logging.custom_json_formatter import CustomJsonFormatter

LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG").upper()

today_date = dt.datetime.now().strftime("%Y-%m-%d")

logging.config.dictConfig(config={
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "%(levelname)s - %(message)s"
        },
        "json": {
            "()": CustomJsonFormatter,
            "fmt_keys": {
                "level": "levelname",
                "message": "message",
                "funcName": "funcName",
                "fileName": "filename",
                "name": "name",
            },
            "remove_keys": [
                "asctime",
                "created",
                "pathname",
                "process",
                "processName",
                "relativeCreated",
                "levelname",
                "levelno",
                "lineno",
                "exc_info",
                "exc_text",
                "stack_info",
                "thread",
                "threadName",
                "taskName",
                "MallocNanoZone",
                "PATH",
                "args",
                "msg",
                "module",
                "msecs",
            ],
            "indent": 2
        }
    },
    "handlers": {
        "console": {
            "class": logging.StreamHandler,
            "formatter": "json",
            "stream": "ext://sys.stdout"
        },
        "stdout": {
            "class": logging.StreamHandler,
            "formatter": "simple",
            "stream": "ext://sys.stdout"
        },
        "file": {
            "class": logging.handlers.RotatingFileHandler,
            "level": LOG_LEVEL,
            "formatter": "json",
            "filename": f"logs-processor-{today_date}.jsonl",
            "maxBytes": 1024,
            "backupCount": 3,
        },
        "queue": {
            "class": logging.handlers.QueueHandler,
            "handlers": ["stdout", "file"],
            "respect_handler_level": True
        }
    },
    "loggers": {
        "newrelic": {
            "level": LOG_LEVEL,
            "handlers": ["console"]
        },
        "console": {
            "level": LOG_LEVEL,
            "handlers": ["stdout"]
        },
        "file": {
            "level": LOG_LEVEL,
            "handlers": ["file"]
        }
    }
})


# def start_queue_listener():
#     queue_handle = logging.getHandlerByName("queue")
#     if queue_handle is not None:
#         queue_handle.listener.start()
#         atexit.register(queue_handle.listener.stop)


logger = logging.getLogger(os.getenv("LOGGERS", "console"))
