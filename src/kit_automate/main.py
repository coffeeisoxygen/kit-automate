"""Main entry point for the kit_automate application."""

import sys

from loguru import logger


def main():
    """Main entry point for the kit_automate application."""
    app_context = None
    try:
        # ✅ ONE LINE INITIALIZATION
        from kit_automate.config import create_application_context

        app_context = create_application_context()

        logger.info("Starting kit_automate application...")
        logger.info("Database connection successful")

        # TODO: Add actual application logic here
        # - GSM modem initialization
        # - Android device detection
        # - GUI startup

        logger.info("kit_automate application finished successfully.")

    except RuntimeError as e:
        logger.error(f"Application failed to start: {e}")
        return 1
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        return 0
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return 1
    finally:
        # Cleanup if context exists
        if app_context is not None:
            app_context.cleanup()

    return 0


if __name__ == "__main__":
    sys.exit(main())
