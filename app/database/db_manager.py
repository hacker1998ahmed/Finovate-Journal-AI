"""
Finovate Journal AI - Database Manager
Copyright © 2025 Ahmed Mostafa Ibrahim — All Rights Reserved.
"""

from pathlib import Path
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session

from app.config.settings import settings


class DatabaseManager:
    """Database manager using SQLAlchemy"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self.db_path = settings.DB_DIR / settings.DB_NAME
            self.engine = None
            self.SessionLocal = None
            self._initialized = False
    
    def initialize(self):
        """Initialize database connection"""
        
        # Create SQLite engine
        self.engine = create_engine(
            f"sqlite:///{self.db_path}",
            echo=False,
            future=True
        )
        
        # Create session factory
        self.SessionLocal = scoped_session(
            sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        )
        
        self._initialized = True
    
    def get_session(self):
        """Get a database session"""
        if not self._initialized:
            self.initialize()
        return self.SessionLocal()
    
    def close(self):
        """Close database connections"""
        if self.SessionLocal:
            self.SessionLocal.remove()
