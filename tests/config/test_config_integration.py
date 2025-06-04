"""Integration test for complete config flow."""

from kit_automate.config import ApplicationContext
from kit_automate.config.db_config import DatabaseManager


class TestConfigIntegration:
    """Test complete configuration integration."""

    def test_full_application_startup_flow(self, test_app_context: ApplicationContext):
        """Test complete application startup like main.py."""
        # Use fixture for proper cleanup
        context = test_app_context

        # Verify all components initialized
        assert context.paths.base.exists()

        # Verify db_manager is properly typed and initialized
        assert hasattr(context, "db_manager")
        assert isinstance(context.db_manager, DatabaseManager)
        assert context.db_manager.test_connection()

        # Verify logging works (basic check)
        from loguru import logger

        logger.info("Test log message")  # Should not crash

        # Cleanup is handled by fixture automatically
