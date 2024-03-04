from logging.config import dictConfig
from logging import getLogger

from MeowthLogger.constants import (
    DEFAULT_ENCODING,
    DEFAULT_LOGGING_LEVEL,
    DEFAULT_PATH,
)
from .parser import LogParser
from .config import MainLoggerConfig
from .settings import LoggerSettings

class AbstractLogger:
    def __init__(self, logger):
        self.info = logger.info
        self.critical = logger.critical
        self.debug = logger.debug
        self.error = logger.error
        self.warning = logger.warning

class Logger(LogParser, AbstractLogger):
    settings: LoggerSettings

    def __init__(
            self,
            logger_level: str = DEFAULT_LOGGING_LEVEL,
            use_files: bool = True,
            encoding: str = DEFAULT_ENCODING,
            path: str = DEFAULT_PATH,
            use_uvicorn: bool = False,
        ):

        self.settings = LoggerSettings(
            logger_level=logger_level,
            use_files=use_files,
            encoding=encoding,
            path=path,
            use_uvicorn=use_uvicorn,
        )

        dictConfig(self.__config)
        super().__init__(getLogger())

    @property
    def __config(self) -> dict:
        return MainLoggerConfig(self.settings).json()