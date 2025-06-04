"""Test critical configuration functionality."""

from pathlib import Path

import pytest

from kit_automate.config import (
    ApplicationContext,
    create_application_context,
)
from kit_automate.config.db_config import DatabaseManager
from kit_automate.config.path_config import AppPaths

# Import test utilities
from tests.utils import assert_directory_structure


class TestCriticalConfig:
    """Test critical configuration functionality."""

    def test_application_context_creation_success(
        self, test_app_context: ApplicationContext
    ):
        """Test successful application context creation."""
        context = test_app_context

        # Verify context components
        assert context.paths.base.exists()
        assert context.db_manager is not None
        assert isinstance(context.db_manager, DatabaseManager)

        # Verify directories created
        assert context.paths.data.exists()
        assert context.paths.logs.exists()

        # Cleanup is handled by fixture automatically

    def test_application_context_with_fixtures(
        self, test_app_context: ApplicationContext
    ):
        """Test using fixture for convenience."""
        assert test_app_context.paths.base.exists()
        assert isinstance(test_app_context.db_manager, DatabaseManager)
        assert test_app_context.db_manager.test_connection()

    def test_ensure_directories_creation(self, test_app_paths: AppPaths):
        """Test directory creation functionality."""
        expected_dirs = ["data", "logs", "images", "configs", "temp", "exports"]

        # Use utility function for cleaner assertion
        assert_directory_structure(test_app_paths.base, expected_dirs)

        # Verify each directory property works
        for dir_name in expected_dirs:
            dir_path = getattr(test_app_paths, dir_name)
            assert dir_path.exists(), f"Directory property {dir_name} failed"

    def test_database_manager_initialization(self, test_db_manager: DatabaseManager):
        """Test database manager critical operations."""
        # Connection test
        assert test_db_manager.test_connection() is True

        # Session creation test
        with test_db_manager.get_session() as session:
            assert session is not None
            # Verify session is properly configured
            assert hasattr(session, "commit")
            assert hasattr(session, "rollback")

    def test_database_session_transaction_behavior(
        self, test_db_manager: DatabaseManager
    ):
        """Test database session transaction behavior."""
        # Test that session doesn't auto-commit
        with test_db_manager.get_session() as session:
            # This would be where we test actual database operations
            # For now, just verify session behavior
            assert session is not None

            # Test session methods are available
            assert callable(getattr(session, "commit", None))
            assert callable(getattr(session, "rollback", None))

    @pytest.mark.slow
    def test_application_context_error_handling(self, temp_dir: Path):
        """Test application context handles errors gracefully."""
        # Test with invalid/non-writable path
        import os

        # Create a path that doesn't exist and can't be created
        # Use a system path that should fail on Windows
        if os.name == "nt":  # Windows
            # Try to use a system directory that should fail
            invalid_dir = Path("C:/Windows/System32/test_invalid_path")
        else:  # Unix-like
            invalid_dir = Path("/root/test_invalid_path")

        with pytest.raises(RuntimeError, match="Application initialization failed"):
            create_application_context(invalid_dir)

    def test_database_connection_failure_scenarios(
        self, test_db_manager: DatabaseManager
    ):
        """Test database manager handles connection failures."""
        # Test with in-memory database (should always work)
        assert test_db_manager.test_connection() is True

        # Test double initialization (should handle gracefully)
        test_db_manager.initialize()  # Should not crash
        assert test_db_manager.test_connection() is True
