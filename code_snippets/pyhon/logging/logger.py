import logging
import os
from logging import Logger
from typing import Optional, Dict


class LoggerConfig:
    """
    Enhanced logger configuration class with flexible formatting.

    Features:
    - Custom log message formatting
    - File and console logging options
    - Automatic directory creation
    - Type hints and input validation

    Example usage:
    formatter = LoggerConfig.format(name=True, levelname=True)
    logger = LoggerConfig(
        name=__name__,
        level=logging.DEBUG,
        log_file="app.log",
        log_path="logs/",
        formatter=formatter,
        mode='a'
    ).get_logger()
    """

    def __init__(
        self,
        name: str = __name__,
        level: int = logging.INFO,
        log_file: Optional[str] = None,
        log_path: str = "logs/",
        formatter: str = "%(name)s - %(levelname)s - %(message)s",
        mode: str = "a",
    ) -> None:
        """
        Initialize logger configuration with validation.

        Args:
            name: Logger name (usually __name__)
            level: Logging level constant (e.g., logging.INFO)
            log_file: Filename for log output (None for console only)
            log_path: Directory path for log files
            formatter: Log message format string
            mode: File mode ('a' for append, 'w' for overwrite)
        """
        self.name: str = name
        self.level: int = level
        self.log_file: Optional[str] = log_file
        self.log_path: str = log_path
        self.formatter: str = formatter
        self.mode: str = self._validate_mode(mode)

    @staticmethod
    def _validate_mode(mode: str) -> str:
        """Ensure valid file mode is provided."""
        mode = mode.lower()
        if mode not in ("a", "w"):
            raise ValueError("Mode must be either 'a' (append) or 'w' (overwrite)")
        return mode

    @staticmethod
    def format(
        name: bool = False,
        asctime: bool = False,
        levelname: bool = False,
        message: bool = True,
        lineno: bool = False,
        funcName: bool = False,
        **additional_fields: bool,
    ) -> str:
        """
        Generate log format string dynamically.

        Args:
            name: Include logger name
            asctime: Include timestamp
            levelname: Include log level
            message: Include message
            additional_fields: Extra format fields (e.g., lineno=True)

        Returns:
            Format string (e.g., "%(name)s %(asctime)s %(message)s")

        Example:
        >>> LoggerConfig.format(name=True, lineno=True)
        '%(name)s %(lineno)s %(message)s'
        """
        fields: Dict[str, bool] = {
            "name": name,
            "asctime": asctime,
            "levelname": levelname,
            "message": message,
            "lineno": lineno,
            "funcName": funcName,
            **additional_fields,
        }
        return " ".join(f"%({key})s" for key, include in fields.items() if include)

    def _prepare_log_directory(self) -> None:
        """Ensure log directory exists."""
        if self.log_file and not os.path.exists(self.log_path):
            os.makedirs(self.log_path, exist_ok=True)

    def get_logger(self) -> logging.Logger:
        """
        Configure and return a logger instance.

        Returns:
            Configured logger instance

        Raises:
            PermissionError: If log file cannot be accessed
            ValueError: If invalid parameters are detected
        """
        logger: Logger = logging.getLogger(self.name)
        logger.setLevel(self.level)

        # Clear existing handlers to prevent duplicate logs
        logger.handlers.clear()

        formatter = logging.Formatter(self.formatter)

        if self.log_file:
            self._prepare_log_directory()
            try:
                handler = logging.FileHandler(
                    os.path.join(self.log_path, self.log_file),
                    mode=self.mode,
                    encoding="utf-8",
                )
            except (PermissionError, OSError) as e:
                raise PermissionError(
                    f"Failed to create log file at {os.path.join(self.log_path, self.log_file)}: {e}"
                ) from e
        else:
            handler = logging.StreamHandler()

        handler.setFormatter(formatter)
        logger.addHandler(handler)

        return logger


if __name__ == "__main__":
    log_format: str = LoggerConfig.format(
        name=True,
        levelname=True,
        message=True,
        asctime=True,
    )
    log: Logger = LoggerConfig(
        name="test", level=10, log_file="test.log", formatter=log_format
    ).get_logger()

    log.info("Info")
    log.debug("Debug")
    log.warning("Warning")
    log.critical("Critical")
    log.error("Error")
