"""Database connection and session management."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from pathlib import Path
import os

from ..config.constants import DATA_DIR, DATABASE_NAME, LOG_FORMAT
from ..utils.logging_config import get_logger

logger = get_logger(__name__)

# Ensure data directory exists
Path(DATA_DIR).mkdir(parents=True, exist_ok=True)

# Database URL
DATABASE_URL = f"sqlite:///{Path(DATA_DIR) / DATABASE_NAME}"

# Create engine with SQLite-specific settings
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # Required for SQLite
    echo=False,  # Set to True for SQL debugging
    pool_pre_ping=True,  # Enable connection health checks
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_engine():
    """Get the database engine."""
    return engine


def get_session_local():
    """Get a new session factory."""
    return SessionLocal


def get_session():
    """Get a database session (generator for dependency injection)."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize the database by creating all tables."""
    try:
        logger.info("Initializing database...")
        Base.metadata.create_all(bind=engine)
        logger.info(f"Database created successfully at {DATABASE_URL}")
        return True
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        return False


def drop_db():
    """Drop all tables (use with caution!)."""
    try:
        logger.warning("Dropping all database tables...")
        Base.metadata.drop_all(bind=engine)
        logger.info("All tables dropped successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to drop database: {e}")
        return False


def backup_database(backup_path: str) -> bool:
    """Create a backup of the database file."""
    try:
        import shutil
        
        db_path = Path(DATA_DIR) / DATABASE_NAME
        if not db_path.exists():
            logger.warning("Database file does not exist, nothing to backup")
            return False
        
        backup_dest = Path(backup_path)
        backup_dest.parent.mkdir(parents=True, exist_ok=True)
        
        shutil.copy2(db_path, backup_dest)
        logger.info(f"Database backed up to {backup_dest}")
        return True
    except Exception as e:
        logger.error(f"Failed to backup database: {e}")
        return False


def restore_database(backup_path: str) -> bool:
    """Restore database from a backup file."""
    try:
        import shutil
        
        backup_src = Path(backup_path)
        if not backup_src.exists():
            logger.error(f"Backup file does not exist: {backup_path}")
            return False
        
        db_path = Path(DATA_DIR) / DATABASE_NAME
        
        # Close any active connections
        engine.dispose()
        
        shutil.copy2(backup_src, db_path)
        logger.info(f"Database restored from {backup_path}")
        return True
    except Exception as e:
        logger.error(f"Failed to restore database: {e}")
        return False
