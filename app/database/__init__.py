"""
Database initialization and session management.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

# Base class for all models
Base = declarative_base()


class DatabaseManager:
    """Manages database connections and sessions."""
    
    def __init__(self, database_url: str):
        """Initialize database manager with connection URL."""
        self.database_url = database_url
        self.engine = None
        self.SessionLocal = None
        self._session = None
        
    def connect(self):
        """Create database engine and session factory."""
        try:
            # Create engine with SQLite-specific settings
            self.engine = create_engine(
                self.database_url,
                connect_args={"check_same_thread": False},  # SQLite specific
                echo=False,  # Set to True for SQL debugging
                pool_pre_ping=True  # Enable connection health checks
            )
            
            # Create session factory
            self.SessionLocal = scoped_session(
                sessionmaker(
                    autocommit=False,
                    autoflush=False,
                    bind=self.engine
                )
            )
            
            logger.info(f"Database connected: {self.database_url}")
            return True
            
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            raise
    
    def create_tables(self):
        """Create all tables in the database."""
        if self.engine:
            Base.metadata.create_all(bind=self.engine)
            logger.info("Database tables created successfully")
    
    def get_session(self):
        """Get a database session."""
        if not self.SessionLocal:
            raise RuntimeError("Database not connected. Call connect() first.")
        return self.SessionLocal()
    
    def close(self):
        """Close database connections."""
        if self.SessionLocal:
            self.SessionLocal.remove()
        if self.engine:
            self.engine.dispose()
        logger.info("Database connections closed")


# Global database manager instance
_db_manager = None


def get_database_manager(database_url: str) -> DatabaseManager:
    """Get or create database manager instance."""
    global _db_manager
    if _db_manager is None:
        _db_manager = DatabaseManager(database_url)
    return _db_manager


def init_database(database_url: str, create_tables: bool = True) -> scoped_session:
    """
    Initialize database and return session factory.
    
    Args:
        database_url: SQLAlchemy database URL
        create_tables: Whether to create tables if they don't exist
        
    Returns:
        Scoped session factory
    """
    db_manager = get_database_manager(database_url)
    db_manager.connect()
    
    if create_tables:
        db_manager.create_tables()
    
    return db_manager.SessionLocal
