from loguru import logger


def nice_main():
    # Use a regular print statement to verify terminal output
    print("Starting kit-automate...")

    # Log messages at different levels
    logger.debug("Debug message from kit-automate")
    logger.info("Info message from kit-automate")
    logger.warning("Warning message from kit-automate")

    # More complex message to test formatting
    logger.success("Kit-automate started successfully!")
    logger.error("This is an error message from kit-automate")
    logger.critical("Critical error in kit-automate")

    # Simulate a warning with a custom message
    logger.warning("This is a custom warning message from kit-automate")

    # Log an exception (uncomment to test)
    # try:
    #     1 / 0  # This will raise a ZeroDivisionError
    # except ZeroDivisionError as e:
    #     logger.exception("An exception occurred: {}", e)


if __name__ == "__main__":
    nice_main()
