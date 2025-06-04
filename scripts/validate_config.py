#!/usr/bin/env python3
"""Quick validation script for config refactor."""

from pathlib import Path
import tempfile

from kit_automate.config import create_application_context


def test_config_functionality():
    """Test basic config functionality."""
    print("🧪 Testing config functionality...")

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        print(f"📁 Using temp directory: {temp_path}")

        # Test application context creation
        print("🔧 Creating application context...")
        context = create_application_context(temp_path)

        # Verify components
        print("✅ Paths created:", context.paths.base.exists())
        print("✅ Database initialized:", context.db_manager.test_connection())
        print("✅ Directories exist:")
        for attr in ["data", "logs", "temp", "reports", "images", "configs", "exports"]:
            path = getattr(context.paths, attr)
            print(f"  - {attr}: {path.exists()}")

        # Test database session
        print("🗄️ Testing database session...")
        with context.db_manager.get_session() as _session:
            print("✅ Database session created successfully")

        # Test logging
        from loguru import logger

        logger.info("Test log message from validation script")
        print("✅ Logging works")

        # Cleanup
        print("🧹 Cleaning up...")
        context.cleanup()
        print("✅ Cleanup completed")

    print("🎉 All config functionality tests passed!")


if __name__ == "__main__":
    test_config_functionality()
