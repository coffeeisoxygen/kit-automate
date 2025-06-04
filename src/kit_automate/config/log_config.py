"""Simple Loguru configuration with configurable stdlib intercept."""

import inspect
import logging
from pathlib import Path
import sys

from loguru import logger

CONSOLE_FORMAT = (
    "<green>{time:HH:mm:ss}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan> | "
    "{message}"
)

FILE_FORMAT = (
    "{time:YYYY-MM-DD HH:mm:ss.SSS} | "
    "{level: <8} | "
    "{name}:{function}:{line} | "
    "{message}"
)


def setup_logger(
    log_dir: Path | None = None,
    level: str = "DEBUG",
    intercept_stdlib: bool = True,
    quiet_libraries: bool = True,
) -> None:
    """Setup loguru logging with configurable options.

    Args:
        log_dir: Directory for log files (optional)
        level: Logging level for our app
        intercept_stdlib: Redirect stdlib logging to loguru
        quiet_libraries: Reduce noise from third-party libraries
    """
    # Remove default handler
    logger.remove()

    # Console logging
    logger.add(
        sys.stdout,
        format=CONSOLE_FORMAT,
        level=level,
        colorize=True,
        filter=_create_filter(quiet_libraries),
    )

    # File logging if directory provided
    if log_dir is not None:
        log_dir.mkdir(parents=True, exist_ok=True)
        logger.add(
            log_dir / "kit-automate.log",
            format=FILE_FORMAT,
            level="DEBUG",  # Always DEBUG in file
            rotation="10 MB",
            retention="1 week",
            compression="zip",
            filter=None,  # No filter for file (capture everything)
        )
        logger.info(f"File logging enabled: {log_dir / 'kit-automate.log'}")

    # Optional stdlib interception
    if intercept_stdlib:
        _enable_stdlib_intercept(quiet_libraries)
        logger.debug("Stdlib logging interception enabled")


def _create_filter(quiet_libraries: bool):
    """Create filter function for reducing library noise."""
    if not quiet_libraries:
        return None

    # Libraries to quiet down
    noisy_loggers = {
        "sqlalchemy.engine",
        "sqlalchemy.pool",
        "PySide6",
        "Qt",
        "asyncio",
        "urllib3",
        "requests",
    }

    def filter_record(record):
        # Allow all our app logs
        if record["name"].startswith("kit_automate"):
            return True

        # Quiet noisy libraries (only WARNING and above)
        for noisy in noisy_loggers:
            if record["name"].startswith(noisy):
                return record["level"].no >= logger.level("WARNING").no

        # Allow everything else
        return True

    return filter_record


def _enable_stdlib_intercept(quiet_libraries: bool) -> None:
    """Enable stdlib logging interception with optional filtering."""

    class InterceptHandler(logging.Handler):
        def emit(self, record: logging.LogRecord) -> None:
            # Get loguru level
            try:
                level = logger.level(record.levelname).name
            except ValueError:
                level = record.levelno

            # Apply library filtering if enabled
            if quiet_libraries:
                noisy_loggers = [
                    "sqlalchemy.engine",
                    "sqlalchemy.pool",
                    "PySide6",
                    "asyncio",
                ]

                for noisy in noisy_loggers:
                    if (
                        record.name.startswith(noisy)
                        and record.levelno < logging.WARNING
                    ):
                        return  # Skip DEBUG/INFO from noisy libraries

            # Find caller and log to loguru
            frame, depth = inspect.currentframe(), 0
            while frame and (
                depth == 0 or frame.f_code.co_filename == logging.__file__
            ):
                frame = frame.f_back
                depth += 1

            logger.opt(depth=depth, exception=record.exc_info).log(
                level, record.getMessage()
            )

    # Replace stdlib handlers
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)


def disable_stdlib_intercept() -> None:
    """Disable stdlib logging interception."""
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    logging.basicConfig(level=logging.WARNING, force=True)
    logger.info("Stdlib logging interception disabled")


# ✅ Convenience aliases for different scenarios
def setup_development_logging(log_dir: Path | None = None) -> None:
    """Setup logging for development (verbose, see everything)."""
    setup_logger(log_dir, "DEBUG", intercept_stdlib=True, quiet_libraries=False)


def setup_production_logging(log_dir: Path) -> None:
    """Setup logging for production (clean, file required)."""
    setup_logger(log_dir, "INFO", intercept_stdlib=True, quiet_libraries=True)


def setup_testing_logging() -> None:
    """Setup logging for testing (minimal, console only)."""
    setup_logger(None, "WARNING", intercept_stdlib=False, quiet_libraries=True)


def cleanup_logging() -> None:
    """Cleanup all loguru handlers and reset logging."""
    # Remove all loguru handlers to release file handles
    logger.remove()

    # Reset stdlib logging
    disable_stdlib_intercept()

    logger.debug("Logging cleanup completed")
