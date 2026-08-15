"""
Finovate Journal AI - Database Connection and Session Management
"""
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, scoped_session, Session
from sqlalchemy.engine import Engine
from typing import Optional
import logging

from app.config.settings import get_settings
from app.utils.logging_config import get_logger

logger = get_logger(__name__)


class Database:
    """Database connection and session manager"""
    
    _instance: Optional["Database"] = None
    _engine: Optional[Engine] = None
    _session_factory: Optional[scoped_session] = None
    
    def __new__(cls) -> "Database":
        """Singleton pattern"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize database connection"""
        if self._engine is not None:
            return
        
        settings = get_settings()
        settings.app.ensure_directories()
        
        self.database_url = settings.database.database_url
        
        # Ensure data directory exists
        db_path = settings.database.db_path
        if db_path and not db_path.parent.exists():
            db_path.parent.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Initializing database connection to: {self.database_url}")
        
        # Create engine with SQLite-specific optimizations
        connect_args = {}
        if self.database_url.startswith("sqlite"):
            connect_args = {
                "check_same_thread": False,
                "timeout": 30
            }
        
        self._engine = create_engine(
            self.database_url,
            echo=settings.database.echo,
            pool_pre_ping=settings.database.pool_pre_ping,
            connect_args=connect_args
        )
        
        # Enable foreign keys for SQLite
        if self.database_url.startswith("sqlite"):
            @event.listens_for(self._engine, "connect")
            def set_sqlite_pragma(dbapi_connection, connection_record):
                cursor = dbapi_connection.cursor()
                cursor.execute("PRAGMA foreign_keys=ON")
                cursor.close()
        
        # Create session factory
        self._session_factory = scoped_session(
            sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine
            )
        )
        
        logger.info("Database connection initialized successfully")
    
    @property
    def engine(self) -> Engine:
        """Get database engine"""
        if self._engine is None:
            raise RuntimeError("Database not initialized. Call init_database() first.")
        return self._engine
    
    @property
    def session(self) -> Session:
        """Get database session"""
        if self._session_factory is None:
            raise RuntimeError("Database not initialized. Call init_database() first.")
        return self._session_factory()
    
    def get_session(self) -> Session:
        """Get a new database session"""
        if self._session_factory is None:
            raise RuntimeError("Database not initialized. Call init_database() first.")
        return self._session_factory()
    
    def close(self):
        """Close database connections"""
        if self._session_factory:
            self._session_factory.remove()
        if self._engine:
            self._engine.dispose()
        logger.info("Database connections closed")


# Global database instance
_db_instance: Optional[Database] = None


def get_database() -> Database:
    """Get database instance"""
    global _db_instance
    if _db_instance is None:
        _db_instance = Database()
    return _db_instance


def init_database() -> Database:
    """Initialize database and return instance"""
    return get_database()


def get_session() -> Session:
    """Get database session from global instance"""
    return get_database().get_session()
