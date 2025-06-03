"""Nuitka build configuration for Modkit Automod."""

from pathlib import Path
import subprocess
import sys


def build_exe():
    """Build standalone executable with Nuitka."""
    project_root = Path(__file__).parent
    main_file = project_root / "src" / "modkit_automod" / "__main__.py"

    # Nuitka command with optimizations
    cmd = [
        sys.executable,
        "-m",
        "nuitka",
        # Output configuration
        "--standalone",  # Create standalone distribution
        "--onefile",  # Single executable file
        "--output-dir=dist",  # Output directory
        "--output-filename=modkit-automod",  # Executable name
        # Optimization flags
        "--enable-plugins=pyside6",  # PySide6 plugin
        "--assume-yes-for-downloads",  # Auto-download dependencies
        "--remove-output",  # Clean previous builds
        # Include/exclude patterns
        "--include-package=modkit_automod",
        "--include-package=loguru",
        "--include-package=sqlalchemy",
        "--include-package=pydantic",
        "--include-package=pyserial",
        # Exclude unnecessary packages
        "--noinclude-pytest-mode=nofollow",
        "--noinclude-setuptools-mode=nofollow",
        # Performance optimizations
        "--lto=yes",  # Link time optimization
        "--jobs=4",  # Parallel compilation
        # Windows specific
        "--windows-console-mode=attach",  # Attach to console if available
        "--windows-icon-from-ico=assets/icon.ico"
        if (project_root / "assets" / "icon.ico").exists()
        else "",
        # Main file
        str(main_file),
    ]

    # Remove empty icon argument if no icon
    cmd = [arg for arg in cmd if arg]

    print("Building with Nuitka...")
    print(f"Command: {' '.join(cmd)}")

    try:
        subprocess.run(cmd, cwd=project_root, check=True)
        print("✅ Build successful!")
        print(f"Executable: {project_root}/dist/modkit-automod.exe")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return False


if __name__ == "__main__":
    build_exe()
