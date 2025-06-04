from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
import sys


@lru_cache(maxsize=1)
def get_app_directory() -> Path:
    """Get application base directory (cached)."""
    if getattr(sys, "frozen", False):
        # If running from compiled executable
        return Path(sys.executable).parent
    else:
        # If running from source code
        # Go up from: src/kit_automate/config/path_config.py -> project root
        return Path(__file__).parents[3]


@dataclass
class AppPaths:
    """Application paths configuration."""

    base_path: Path

    @property
    def base(self) -> Path:
        """Base path property for consistency with tests."""
        return self.base_path

    @classmethod
    def create(
        cls, base_path: Path | None = None, dev_mode: bool = False
    ) -> "AppPaths":
        """Create AppPaths with proper dev/prod separation.

        Args:
            base_path: Override base path
            dev_mode: Use development workspace structure
        """
        if base_path is None:
            if dev_mode:
                base_path = Path.cwd() / "dev"  # Development workspace
            else:
                base_path = Path.cwd()  # Production/clean root

        return cls(base_path=base_path)

    @property
    def data(self) -> Path:
        """Data directory."""
        return self.base_path / "data"

    @property
    def logs(self) -> Path:
        """Logs directory."""
        return self.base_path / "logs"

    @property
    def temp(self) -> Path:
        """Temporary files directory."""
        return self.base_path / "temp"

    @property
    def reports(self) -> Path:
        """Reports directory (coverage, tests)."""
        return self.base_path / "reports"

    @property
    def images(self) -> Path:
        """Images directory."""
        return self.base_path / "images"

    @property
    def configs(self) -> Path:
        """Configuration files directory."""
        return self.base_path / "configs"

    @property
    def exports(self) -> Path:
        """Export files directory."""
        return self.base_path / "exports"

    def ensure_directories(self) -> None:
        """Ensure all required directories exist."""
        directories = [
            self.data,
            self.logs,
            self.temp,
            self.reports,
            self.images,
            self.configs,
            self.exports,
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
