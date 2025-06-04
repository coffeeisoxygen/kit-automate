"""Configuration package with application initialization utilities."""

from dataclasses import dataclass
from pathlib import Path

from loguru import logger

from kit_automate.config.db_config import DatabaseManager, create_database_manager
from kit_automate.config.log_config import cleanup_logging, setup_logger
from kit_automate.config.path_config import AppPaths


@dataclass
class ApplicationContext:
    """Application context with initialized components."""

    paths: AppPaths
    db_manager: DatabaseManager  # Fixed type annotation

    def cleanup(self) -> None:
        """Cleanup application resources properly."""
        try:
            self.db_manager.cleanup()  # Now properly typed - no hasattr needed
            logger.debug("Database manager cleaned up")
        except Exception as e:
            logger.warning(f"Error during database cleanup: {e}")

        # Cleanup logging to release file handles
        try:
            cleanup_logging()
            logger.debug("Logging cleaned up")
        except Exception as e:
            logger.warning(f"Error during logging cleanup: {e}")

        # Future: Close other resources
        logger.info("Application context cleaned up")


def create_application_context(base_path: Path | None = None) -> ApplicationContext:
    """Create and initialize application context.

    Args:
        base_path: Override base path (useful for testing)

    Returns:
        ApplicationContext with initialized components

    Raises:
        RuntimeError: If initialization fails
    """
    try:
        # Create paths
        app_paths = AppPaths.create(base_path)
        app_paths.ensure_directories()

        # Setup logging
        setup_logger(app_paths.logs)

        # Setup database
        db_manager = create_database_manager(app_paths)
        db_manager.initialize()

        # Test database connection
        if not db_manager.test_connection():
            raise RuntimeError("Database connection failed during initialization")

        return ApplicationContext(paths=app_paths, db_manager=db_manager)

    except Exception as e:
        raise RuntimeError(f"Application initialization failed: {e}") from e


__all__ = [
    "AppPaths",
    "ApplicationContext",
    "cleanup_logging",
    "create_application_context",
    "create_database_manager",
    "setup_logger",
]

# REMINDER : Benahi masalah inisialisasi
# TODO: MINOR IMPROVEMENTS (Later):
# ? [ ] Centralized default settings
# ? [ ] Environment variables documentation
# ? [ ] Configuration validation (if needed)
# ! [ ] 🎯 READY FOR: GSM modem implementation dengan TDD approach!
