"""Cross-platform build script for Modkit Automod."""

from pathlib import Path
import shutil
import subprocess
import sys


def run_command(cmd: str, cwd: Path | None = None) -> bool:
    """Run command and return success status."""
    try:
        print(f"Running: {cmd}")
        subprocess.run(
            cmd.split() if isinstance(cmd, str) else cmd, cwd=cwd, check=True, text=True
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return False


def main():
    """Main build function."""
    project_root = Path(__file__).parent.parent
    dist_dir = project_root / "dist"

    print("🚀 Building Modkit Automod with Nuitka...")

    # Clean previous builds
    if dist_dir.exists():
        print("🧹 Cleaning previous builds...")
        shutil.rmtree(dist_dir)

    # Install dependencies
    print("📦 Installing dependencies...")
    if not run_command("uv sync --dev", project_root):
        sys.exit(1)

    # Build with Nuitka
    print("🔨 Building executable...")
    if not run_command("uv run python build_config.py", project_root):
        sys.exit(1)

    # Test executable
    exe_path = dist_dir / "modkit-automod.exe"
    if exe_path.exists():
        print("🧪 Testing executable...")
        run_command(f'"{exe_path}" --version')

        print(f"✅ Build completed! Check {dist_dir}")
        print(f"📄 Executable: {exe_path}")

        # Show file size
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print(f"📊 File size: {size_mb:.1f} MB")
    else:
        print("❌ Executable not found!")
        sys.exit(1)


if __name__ == "__main__":
    main()
