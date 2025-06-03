"""setup loguru."""

import inspect
import logging
import sys

from loguru import logger

CONSOLE_FORMAT = (
    "<green>{time:HH:mm:ss}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan> | "
    "{message}"
)

TIME_FORMAT = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green>"
FILE_FORMAT = (
    "{time:YYYY-MM-DD HH:mm:ss.SSS} | "
    "{level: <8} | "
    "T{thread.name}: | "
    "{name}:{function}:{line} | "
    "{message}"
)

# Remove default logger
logger.remove()
# Add console logger (to stdout for better visibility)
logger.add(
    sink=sys.stdout,
    format=CONSOLE_FORMAT,
    level="DEBUG",
    colorize=True,
)

# Add file logger with detailed configuration
logger.add(
    sink="logs/kit-automate.log",
    format=FILE_FORMAT,  # Using plain format for file logs
    level="DEBUG",
    backtrace=True,
    diagnose=True,
    rotation="500 MB",
    retention="30 days",
    compression="zip",
    serialize=False,
    enqueue=True,
    colorize=False,  # No color codes in log files
)


# Intercept Logger from other libraries
class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        # Get corresponding Loguru level if it exists.
        level: str | int
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message.
        frame, depth = inspect.currentframe(), 0
        while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


# Auto-enable intercept by default (current behavior maintained)
logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)


def disable_stdlib_intercept():
    """Disable stdlib logging interception if third-party library logs become noise.

    Usage:
        from kit_automate.shared.custom_log import disable_stdlib_intercept
        disable_stdlib_intercept()
    """
    # Clear all handlers from root logger
    root_logger = logging.getLogger()
    root_logger.handlers.clear()

    # Restore basic logging for stdlib (WARNING level to reduce noise)
    logging.basicConfig(level=logging.WARNING, force=True)

    logger.info("Stdlib logging interception disabled")


def enable_stdlib_intercept():
    """Re-enable stdlib logging interception.

    Usage:
        from kit_automate.shared.custom_log import enable_stdlib_intercept
        enable_stdlib_intercept()
    """
    # Re-establish intercept handler
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

    logger.info("Stdlib logging interception enabled")


# TODO: make more robust logging setup


def setup_logger():
    """Setup logger (legacy function for backward compatibility).

    Logger is already configured during module import.
    """
    pass
