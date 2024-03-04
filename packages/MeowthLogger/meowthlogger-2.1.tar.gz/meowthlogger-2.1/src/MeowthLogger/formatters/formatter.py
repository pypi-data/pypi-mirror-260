import logging
import os
import time

from MeowthLogger.constants import DEFAULT_FORMATTER

class AbstractFormatter(logging.Formatter):
    def __init__(self):
        logging.Formatter.__init__(self, "")

    def format(self, record):
        return self.prepare_log_string(
            datetime=time.strftime(self.default_time_format, self.converter(record.created)),
            levelname=self.prepare_levelname(record.levelno),
            filename=record.pathname.replace(os.path.abspath(""), "."),
            line=str(record.lineno),
            message=record.getMessage(),
        )

    def prepare_log_string(self, datetime, levelname, filename, line, message):
        return DEFAULT_FORMATTER.format(
            datetime=datetime,
            levelname=levelname,
            filename=filename,
            line=line,
            message=message,
        )
    
    def prepare_levelname(self, levelname):
        match levelname:
            case logging.INFO:
                return "INFO"
            case logging.ERROR:
                return "ERROR"
            case logging.WARN:
                return "WARNING"
            case logging.DEBUG:
                return "DEBUG"
            case logging.CRITICAL:
                return "CRITICAL"
            case _:
                return f"LEVEL :{levelname}"