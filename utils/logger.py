import logging
import os
import sys
from datetime import datetime, timezone, timedelta

TZ = timezone(timedelta(hours=-5))
class _ReadableFormatter(logging.Formatter):
 
    def format(self, record: logging.LogRecord) -> str:
        timestamp = datetime.fromtimestamp(record.created, tz=TZ).strftime("%Y-%m-%d %H:%M:%S")
        level     = record.levelname
        filename  = record.filename
        message   = record.getMessage()
 
        line = f'{timestamp} UTC-5 | ({filename}) | [{level}] | "{message}"'
 
        if record.exc_info:
            line += f"\n{self.formatException(record.exc_info)}"
 
        return line
 
 
class _LambdaLogger(logging.Logger):
    """
    Logger con deteccion automatica de excepciones en error() y critical().
    Si se llama dentro de un bloque except, captura el traceback sin necesidad
    de pasar exc_info=True manualmente.
    """
 
    def error(self, msg, *args, **kwargs):
        if sys.exc_info()[0] is not None:
            kwargs.setdefault("exc_info", True)
        super().error(msg, *args, **kwargs)
 
    def critical(self, msg, *args, **kwargs):
        if sys.exc_info()[0] is not None:
            kwargs.setdefault("exc_info", True)
        super().critical(msg, *args, **kwargs)
 
 
def get_logger(name: str = __name__) -> _LambdaLogger:
    """
    Retorna un logger configurado con salida legible para CloudWatch.
    El nivel se resuelve desde LOG_LEVEL (default: INFO).
    """
    logging.setLoggerClass(_LambdaLogger)
 
    level  = os.environ.get("LOG_LEVEL", "INFO").upper()
    logger = logging.getLogger(name)
    logger.setLevel(level)
 
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(_ReadableFormatter())
        logger.addHandler(handler)
 
    logger.propagate = False
    return logger  # type: ignore[return-value]