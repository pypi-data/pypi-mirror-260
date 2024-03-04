from ..settings import LoggerSettings

from .abstract import AbstractLoggerConfig
from .uvicorn import UvicornLogger
from .file import FileLogger
from .console import ConsoleLogger
    
class MainLoggerConfig(
        FileLogger, 
        ConsoleLogger, 
        UvicornLogger, 
        AbstractLoggerConfig,
    ):

    def __init__(
        self,
        settings: LoggerSettings,
        version: int = 1,
    ):
        super().__init__(settings, version)        
        
        self._use_console()

        if settings.use_files:
            self._use_files()

        if settings.use_uvicorn:
            self._use_uvicorn()