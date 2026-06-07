import logging
import os
import sys
import traceback
from datetime import datetime, timezone, timedelta

TZ = timezone(timedelta(hours=-5))

class _ReadableFormatter(logging.Formatter):

    def format(self, record: logging.LogRecord) -> str:
        timestamp = datetime.fromtimestamp(record.created, tz=TZ).strftime("%Y-%m-%d %H:%M:%S")
        filename  = record.filename
        level     = record.levelname
        message   = record.getMessage()

        line = f'{timestamp} UTC-5 ({filename}) | [{level}]: "{message}"'

        if record.exc_info:
            line += f"\n{self.formatException(record.exc_info)}"

        return line


def get_logger(name: str = __name__) -> logging.Logger:
    """
    Retorna un logger con formato legible para CloudWatch.
    """
    level  = os.environ.get("LOG_LEVEL", "INFO").upper()
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(_ReadableFormatter())
        logger.addHandler(handler)

    logger.propagate = False
    return logger


def log_exception(logger: logging.Logger, msg: str = "Unhandled exception") -> None:
    """
    Loguea un ERROR con el stack trace completo.
    """
    logger.error(f"{msg}\n{traceback.format_exc()}")