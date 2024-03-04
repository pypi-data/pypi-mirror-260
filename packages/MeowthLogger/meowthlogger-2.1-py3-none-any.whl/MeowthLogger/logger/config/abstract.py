from abc import ABC

from MeowthLogger.utilities.abstractions import Dictable

from .utils import (
    ConfigFormatter,
    ConfigHandler,
    ConfigLogger,
    ConfigRoot,
)
from ..settings import LoggerSettings

class AbstractLoggerConfig(Dictable, ABC):
    version: int
    settings: LoggerSettings

    formatters: list[ConfigFormatter]
    handlers: list[ConfigHandler]
    loggers: list[ConfigLogger]

    root: ConfigRoot

    def __init__(
        self,
        settings: LoggerSettings,
        version: int,
    ):
        self.settings = settings
        self.version = version

        self.handlers = []
        self.loggers = []
        self.formatters = []

    def json(self) -> dict:
        return {
            'version': self.version,
            'formatters': {
                formatter.name: formatter.json()
                for formatter
                in self.formatters
            },
            'handlers': {
                handler.name: handler.json()
                for handler
                in self.handlers
            },
            'loggers': {
                logger.name: logger.json()
                for logger
                in self.loggers
            },
            'root': ConfigRoot(
                self.settings.logger_level,
                self.handlers
            ).json(),
        }