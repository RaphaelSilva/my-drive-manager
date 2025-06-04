import datetime as dt
import json
import logging.config
import logging.handlers


class CustomJsonFormatter(logging.Formatter):
    def __init__(self, *,
                 fmt_keys: dict[str, str] | None = None,
                 remove_keys: list[str] | None = None,
                 indent: int = None) -> None:
        super().__init__()
        self.fmt_keys = fmt_keys or {}
        self.remove_keys = remove_keys or []
        self.indent = indent

    def format(self, record: logging.LogRecord) -> str:
        log_record = {
            "timestamp": dt.datetime.fromtimestamp(
                record.created, tz=dt.timezone.utc
            ).isoformat(),
            "message": record.getMessage(),
        }
        if record.exc_info is not None:
            log_record["exc_info"] = self.formatException(record.exc_info)

        if record.stack_info is not None:
            log_record["stack_info"] = self.formatException(record.stack_info)

        formatted_message = {
            key: msg_val
            if (msg_val := log_record.pop(key, None)) is not None
            else getattr(record, val)
            for key, val in self.fmt_keys.items()
        }

        record_keys = [k for k in record.__dict__ if k not in self.remove_keys]
        extra = {
            record_key: getattr(record, record_key) for record_key in record_keys
        }
        log_record.update(extra)

        formatted_message.update(log_record)
        return json.dumps(formatted_message, default=str, indent=self.indent)
