import logging
from logging.handlers import RotatingFileHandler

from rich.console import Console
from rich.theme import Theme


class RichLogger:
    def __init__(self, log_file_path: str = None):
        # Define custom theme
        custom_theme = Theme(
            {
                "info": "dim cyan",
                "success": "bold green",
                "error": "bold red",
                "warning": "bold yellow",
            }
        )
        self.console = Console(theme=custom_theme)

        # Set up file logging if a path is provided
        if log_file_path:
            self.file_logger = logging.getLogger("rich_logger")
            self.file_logger.setLevel(logging.DEBUG)  # Or adjust to your needs
            file_handler = RotatingFileHandler(
                log_file_path, maxBytes=1048576, backupCount=5
            )
            log_formatter = logging.Formatter(
                "%(asctime)s - %(levelname)s - %(message)s"
            )
            file_handler.setFormatter(log_formatter)
            self.file_logger.addHandler(file_handler)
        else:
            self.file_logger = None

    def log(self, message: str, level: str = "info"):
        # Print to console with Rich
        self.console.print(message, style=level)

        # Log to file if file logging is set up
        if self.file_logger:
            if level == "info":
                self.file_logger.info(message)
            elif level == "success":
                self.file_logger.info(
                    message
                )  # Logging libraries typically don't have a 'success' level
            elif level == "error":
                self.file_logger.error(message)
            elif level == "warning":
                self.file_logger.warning(message)

    def log_info(self, message: str):
        self.log(message, level="info")

    def log_success(self, message: str):
        self.log(message, level="success")

    def log_error(self, message: str):
        self.log(message, level="error")

    def log_warning(self, message: str):
        self.log(message, level="warning")
