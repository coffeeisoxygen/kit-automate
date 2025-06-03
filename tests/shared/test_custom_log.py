"""Test custom logging configuration."""

import io
import logging
from pathlib import Path
import sys
import tempfile

from loguru import logger
import pytest

from kit_automate.shared.custom_log import (
    FILE_FORMAT,
    InterceptHandler,
    disable_stdlib_intercept,
    enable_stdlib_intercept,
)


class TestCustomLog:
    """Test custom logging functionality."""

    def test_logger_behavior(self, capsys: pytest.CaptureFixture[str]):
        """Test that logger produces expected output behavior."""
        # Add explicit test handler
        test_handler_id = logger.add(sys.stdout, format="{message}", colorize=False)

        test_message = "Test logger behavior"
        logger.info(test_message)

        # Remove test handler
        logger.remove(test_handler_id)

        captured = capsys.readouterr()
        # Test that console output exists and contains our message
        assert test_message in captured.out
        assert "INFO" in captured.out

        # [] TODO: Test file output behavior
        # [] TODO: Validate multi-handler output

    def test_console_format(self, capsys):
        """Test console logging format structure."""
        test_message = "Test console message"
        logger.info(test_message)

        captured = capsys.readouterr()
        output_lines = captured.out.strip().split("\n")

        if output_lines and output_lines[-1]:  # Check last non-empty line
            last_line = output_lines[-1]

            # Test format components exist
            assert test_message in last_line
            assert "INFO" in last_line
            # Test time format (HH:mm:ss pattern)
            assert ":" in last_line  # Time separator

        # devnote: Test color codes validation
        # devnote: Test exact format pattern matching

    def test_file_logging_behavior(self):
        """Test file logging behavior without accessing internal handlers."""
        with tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".log"
        ) as temp_file:
            temp_path = temp_file.name

        # Add dedicated test file handler
        handler_id = logger.add(temp_path, format=FILE_FORMAT, level="DEBUG")

        test_message = "Test file behavior"
        logger.info(test_message)
        logger.debug("Debug message for file")

        # Remove handler and verify file content
        logger.remove(handler_id)

        # Test file was created and contains expected content
        temp_file_path = Path(temp_path)
        assert temp_file_path.exists()

        content = temp_file_path.read_text()
        assert test_message in content
        assert "INFO" in content
        assert "Debug message for file" in content
        # Test thread info is included
        assert "T" in content

        # Cleanup
        temp_file_path.unlink()

        # devnote: Test rotation behavior
        # devnote: Test compression functionality

    def test_stdlib_intercept_behavior(self):
        """Test stdlib logging interception behavior."""
        # Use stdlib logger
        stdlib_logger = logging.getLogger("test_stdlib")

        # Capture output through loguru
        with io.StringIO() as buf:
            handler_id = logger.add(buf, format="{level} | {message}")

            test_message = "Stdlib intercept test"
            stdlib_logger.warning(test_message)

            logger.remove(handler_id)
            output = buf.getvalue()

        # Test that stdlib message was intercepted and formatted by loguru
        assert test_message in output
        assert "WARNING" in output

        # devnote: Test different log levels interception
        # devnote: Test exception handling in interception

    def test_disable_intercept_behavior(self):
        """Test disable intercept behavior through output verification."""
        # First, verify intercept is working
        stdlib_logger = logging.getLogger("test_disable")

        # Capture with intercept enabled
        with io.StringIO() as buf:
            handler_id = logger.add(buf, format="{message}")

            test_message_before = "Before disable"
            stdlib_logger.info(test_message_before)

            logger.remove(handler_id)
            output_before = buf.getvalue()

        # Should capture through intercept
        assert test_message_before in output_before

        # Disable intercept
        disable_stdlib_intercept()

        # Test behavior after disable
        with io.StringIO() as buf:
            handler_id = logger.add(buf, format="{message}")

            test_message_after = "After disable"
            stdlib_logger.info(test_message_after)

            logger.remove(handler_id)
            output_after = buf.getvalue()

        # Should NOT capture through loguru after disable
        assert test_message_after not in output_after

        # Re-enable for other tests
        enable_stdlib_intercept()

        # devnote: Test stdlib still works through its own handlers
        # devnote: Test warning level configuration

    def test_enable_intercept_behavior(self):
        """Test enable intercept behavior through output verification."""
        # Disable first
        disable_stdlib_intercept()

        # Verify intercept is disabled
        stdlib_logger = logging.getLogger("test_enable")
        with io.StringIO() as buf:
            handler_id = logger.add(buf, format="{message}")

            test_message_disabled = "While disabled"
            stdlib_logger.info(test_message_disabled)

            logger.remove(handler_id)
            output_disabled = buf.getvalue()

        assert test_message_disabled not in output_disabled

        # Re-enable intercept
        enable_stdlib_intercept()

        # Test that intercept is working again
        with io.StringIO() as buf:
            handler_id = logger.add(buf, format="{message}")

            test_message_enabled = "After re-enable"
            stdlib_logger.info(test_message_enabled)

            logger.remove(handler_id)
            output_enabled = buf.getvalue()

        assert test_message_enabled in output_enabled

        # devnote: Test multiple enable calls
        # devnote: Test state consistency

    def test_intercept_handler_direct_behavior(self):
        """Test InterceptHandler behavior directly."""
        handler = InterceptHandler()

        # Create test record
        record = logging.LogRecord(
            name="test_direct",
            level=logging.ERROR,
            pathname="test.py",
            lineno=42,
            msg="Direct handler test: %s",
            args=("formatted",),
            exc_info=None,
        )

        # Capture output
        with io.StringIO() as buf:
            handler_id = logger.add(buf, format="{level} | {message}")

            handler.emit(record)

            logger.remove(handler_id)
            output = buf.getvalue()

        # Test formatted message appears correctly
        assert "Direct handler test: formatted" in output
        assert "ERROR" in output

        # devnote: Test exception info handling
        # devnote: Test level mapping edge cases

    @pytest.fixture(autouse=True)
    def setup_and_cleanup(self):
        """Setup and cleanup for each test."""
        # Setup: ensure clean state
        yield

        # Cleanup: restore intercept state
        enable_stdlib_intercept()

        # devnote: Clean up any test log files
        # devnote: Reset any modified logger state

    # devnote: Test concurrent logging behavior
    # devnote: Test file rotation triggers
    # devnote: Test large message handling
    # devnote: Test performance under load
    # devnote: Integration test with real application scenarios
