"""Database configuration module for kit-automate."""

from collections.abc import Generator
from contextlib import contextmanager
from dataclasses import dataclass
import os
from pathlib import Path
from typing import Annotated

from loguru import logger
from sqlalchemy import create_engine, event, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from kit_automate.config.path_config import AppPaths

# Custom type for self-documenting code
CommitRequiredSession = Annotated[
    Session,
    "Session that requires explicit commit() - call session.commit() when ready",
]


@dataclass(frozen=True)
class DbConfig:
    """Database configuration dataclass."""

    path: str
    echo: bool = False
    pool_pre_ping: bool = True


def get_db_config(paths: AppPaths) -> DbConfig:
    """Get database configuration."""
    db_path = paths.data / "kit_automate.db"
    db_path_str = os.getenv("DATABASE_PATH", str(db_path))

    return DbConfig(
        path=db_path_str,
        echo=os.getenv("SQL_ECHO", "false").lower() == "true",
        pool_pre_ping=True,
    )


class DatabaseManager:
    """Database manager with proper lifecycle management."""

    def __init__(self, config: DbConfig):
        self.config = config
        self.url = f"sqlite:///{config.path}"
        self.engine = None
        self.SessionLocal = None
        self.Base = None
        self._initialized = False

    def initialize(self) -> None:
        """Initialize database engine and session factory."""
        if self._initialized:
            logger.warning("Database already initialized")
            return

        # Ensure data directory exists
        if self.config.path != ":memory:":
            Path(self.config.path).parent.mkdir(parents=True, exist_ok=True)

        # Create engine
        self.engine = create_engine(
            self.url,
            connect_args={"check_same_thread": False},
            pool_pre_ping=self.config.pool_pre_ping,
            echo=self.config.echo,
        )

        # Enable foreign keys
        @event.listens_for(self.engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record) -> None:  # noqa: ARG001
            """Enable foreign keys for SQLite connections."""
            if self.url.startswith("sqlite"):
                cursor = dbapi_connection.cursor()
                cursor.execute("PRAGMA foreign_keys=ON")
                cursor.close()

        # Create session factory and base
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )
        self.Base = declarative_base()

        self._initialized = True
        logger.info(f"Database initialized - Path: {self.config.path}")

    def cleanup(self) -> None:
        """Cleanup database resources properly."""
        if self.engine is not None:
            try:
                # Close all connections in the pool
                self.engine.dispose()
                logger.debug("Database engine disposed")
            except Exception as e:
                logger.warning(f"Error disposing engine: {e}")

        # Reset state
        self.engine = None
        self.SessionLocal = None
        self.Base = None
        self._initialized = False
        logger.info("Database manager cleaned up")

    def create_tables(self) -> None:
        """Create all database tables."""
        if not self._initialized:
            raise RuntimeError("Database not initialized. Call initialize() first.")

        if self.engine is None or self.Base is None:
            raise RuntimeError("Database components not properly initialized.")

        try:
            self.Base.metadata.create_all(bind=self.engine)
            logger.info("Database tables created successfully")
        except SQLAlchemyError as e:
            logger.error(f"Error creating tables: {e}")
            raise

    def test_connection(self) -> bool:
        """Test database connection."""
        if not self._initialized or self.engine is None:
            return False

        try:
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            logger.info("Database connection test successful")
            return True
        except SQLAlchemyError as e:
            logger.error(f"Database connection failed: {e}")
            return False

    @contextmanager
    def get_session(self) -> Generator[CommitRequiredSession, None, None]:
        """Context manager for database session (manual commit required)."""
        if not self._initialized:
            raise RuntimeError("Database not initialized. Call initialize() first.")

        if self.SessionLocal is None:
            raise RuntimeError("Session factory not properly initialized.")

        session = self.SessionLocal()
        try:
            yield session
            logger.debug("Database session completed (manual commit required)")
        except Exception as e:
            logger.error(f"Database error occurred: {e}")
            session.rollback()
            raise
        finally:
            session.close()


def create_database_manager(paths: AppPaths) -> DatabaseManager:
    """Create database manager with configuration."""
    config = get_db_config(paths)
    return DatabaseManager(config)
