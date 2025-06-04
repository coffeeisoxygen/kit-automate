"""Test utility functions."""

import os
from pathlib import Path
from typing import Any


def create_test_file(path: Path, content: str = "test content") -> None:
    """Create test file with content."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def assert_file_exists(path: Path, should_exist: bool = True) -> None:
    """Assert file existence."""
    if should_exist:
        assert path.exists(), f"File should exist: {path}"
        assert path.is_file(), f"Should be file: {path}"
    else:
        assert not path.exists(), f"File should not exist: {path}"


def assert_directory_structure(base_path: Path, expected_dirs: list[str]) -> None:
    """Assert directory structure matches expected."""
    for dir_name in expected_dirs:
        dir_path = base_path / dir_name
        assert dir_path.exists(), f"Directory should exist: {dir_path}"
        assert dir_path.is_dir(), f"Should be directory: {dir_path}"


def set_env_vars(**kwargs: Any) -> None:
    """Set environment variables for testing."""
    for key, value in kwargs.items():
        os.environ[key] = str(value)


def cleanup_env_vars(*keys: str) -> None:
    """Clean up environment variables after testing."""
    for key in keys:
        os.environ.pop(key, None)
