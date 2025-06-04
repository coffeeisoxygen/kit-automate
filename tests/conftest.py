"""Global test configuration and fixtures."""

from collections.abc import Generator
from pathlib import Path
import tempfile

import pytest

from kit_automate.config import ApplicationContext
from kit_automate.config.db_config import DatabaseManager
from kit_automate.config.path_config import AppPaths

# ========================================
# CORE FIXTURES
# ========================================


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Provide temporary directory for tests."""
    with tempfile.TemporaryDirectory() as temp_path:
        yield Path(temp_path)


@pytest.fixture
def test_app_paths(temp_dir: Path) -> AppPaths:
    """Provide test AppPaths instance with directories created."""
    paths = AppPaths.create(temp_dir)
    paths.ensure_directories()
    return paths


@pytest.fixture
def test_db_manager(test_app_paths: AppPaths) -> Generator[DatabaseManager, None, None]:
    """Provide initialized test database manager with in-memory DB."""
    from kit_automate.config.db_config import DatabaseManager, DbConfig

    # Use in-memory database for testing to avoid file locking issues
    config = DbConfig(path=":memory:", echo=False, pool_pre_ping=False)
    db_manager = DatabaseManager(config)
    db_manager.initialize()

    yield db_manager

    # Explicit cleanup
    db_manager.cleanup()


@pytest.fixture
def test_db_session(test_db_manager: DatabaseManager):
    """Provide database session for testing (auto-rollback)."""
    with test_db_manager.get_session() as session:
        yield session
        # No commit - automatic rollback for test isolation


@pytest.fixture
def test_app_context(temp_dir: Path) -> Generator[ApplicationContext, None, None]:
    """Provide complete application context for integration testing with in-memory DB."""
    from kit_automate.config.db_config import DatabaseManager, DbConfig
    from kit_automate.config.log_config import setup_testing_logging
    from kit_automate.config.path_config import AppPaths

    # Setup paths
    paths = AppPaths.create(temp_dir)
    paths.ensure_directories()

    # Setup testing logging (minimal)
    setup_testing_logging()

    # Setup in-memory database to avoid file locking
    config = DbConfig(path=":memory:", echo=False, pool_pre_ping=False)
    db_manager = DatabaseManager(config)
    db_manager.initialize()

    # Create context manually
    context = ApplicationContext(paths=paths, db_manager=db_manager)

    yield context

    # Explicit cleanup
    context.cleanup()


# ========================================
# LOGGING FIXTURES
# ========================================


@pytest.fixture
def isolated_logging():
    """Isolate logging for tests to prevent interference."""
    from loguru import logger

    # Store current handlers
    original_handlers = logger._core.handlers.copy()  # type: ignore

    # Remove all handlers
    logger.remove()

    # Add silent handler for tests
    handler_id = logger.add(
        sink=lambda _: None,  # Silent sink
        level="DEBUG",
        format="{time} | {level} | {message}",
    )

    yield logger

    # Restore original handlers
    logger.remove(handler_id)
    for _handler_id, handler in original_handlers.items():
        logger.add(**handler)


# ========================================
# PYTEST CONFIGURATION
# ========================================


def pytest_configure(config):
    """Configure pytest with custom settings."""
    # Add config marker if not defined
    config.addinivalue_line("markers", "config: Configuration module tests")


def pytest_collection_modifyitems(config, items):
    """Auto-mark tests based on location and name patterns."""
    for item in items:
        # Auto-mark based on file path
        test_file = str(item.fspath)

        if "config" in test_file:
            item.add_marker(pytest.mark.config)

        if "integration" in item.name or "full_application" in item.name:
            item.add_marker(pytest.mark.integration)

        if "slow" in item.name or item.get_closest_marker("slow"):
            item.add_marker(pytest.mark.slow)


# ========================================
# FUTURE FIXTURES (Placeholder)
# ========================================


@pytest.fixture
def mock_gsm_port():
    """Mock GSM serial port for testing."""
    return "/dev/ttyUSB0"  # Mock port for future GSM tests


@pytest.fixture
def mock_android_device():
    """Mock Android device for testing."""
    return "emulator-5554"  # Mock device for future Android tests
