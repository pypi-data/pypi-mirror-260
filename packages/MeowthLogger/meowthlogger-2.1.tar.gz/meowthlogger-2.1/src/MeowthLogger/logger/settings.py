class LoggerSettings:
    """### Settings of root logger
    #### Parameters
    - logger_level: level of logger. Example: "INFO" or "DEBUG"
    - use_files: bool argument for use with files mode or without
    - encoding: file encoding mode. Example: "utf-8"
    - path: logging files path. Example: "logs/logfiles"
    - use_uvicorn: bool argument for use with uvicorn
    """
    def __init__(
        self,
        logger_level: str,
        use_files: bool,
        encoding: str,
        path: str,
        use_uvicorn: bool,
    ):
        self.logger_level = logger_level
        self.use_files = use_files
        self.encoding = encoding
        self.path = path
        self.use_uvicorn = use_uvicorn