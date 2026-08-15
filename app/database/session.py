"""
Finovate Journal AI - Database Session Management

Developer: Ahmed Mostafa Ibrahim
Brand: Finovate – AHMED EG
"""

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from pathlib import Path
from typing import Generator, Optional

from .base import Base
from app.config.settings import get_settings


# Engine instance (singleton)
_engine: Optional[object] = None
SessionLocal: Optional[sessionmaker] = None


def get_engine():
    """Get or create SQLAlchemy engine."""
    global _engine, SessionLocal
    
    if _engine is None:
        settings = get_settings()
        db_path = settings.database_file
        
        # Ensure directory exists
        db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create SQLite engine with foreign key support
        connection_string = f"sqlite:///{db_path}"
        _engine = create_engine(
            connection_string,
            connect_args={"check_same_thread": False},
            echo=False,  # Set to True for SQL debugging
            pool_pre_ping=True,
        )
        
        # Enable foreign keys for SQLite
        @event.listens_for(_engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()
        
        # Create all tables
        Base.metadata.create_all(bind=_engine)
        
        # Create session factory
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)
    
    return _engine


def get_session() -> Generator[Session, None, None]:
    """Get database session (for dependency injection)."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def init_db() -> None:
    """Initialize database and create all tables."""
    engine = get_engine()
    Base.metadata.create_all(bind=engine)


def reset_db() -> None:
    """Reset database (for testing only)."""
    global _engine, SessionLocal
    if _engine is not None:
        Base.metadata.drop_all(bind=_engine)
        _engine.dispose()
        _engine = None
        SessionLocal = None
