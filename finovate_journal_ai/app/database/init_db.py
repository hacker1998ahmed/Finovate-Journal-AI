"""
Finovate Journal AI - Database Initialization and Schema Creation
"""
from sqlalchemy import inspect
import logging

from app.database.database import get_database
from app.database.base import Base
from app.models import (
    Company, FiscalYear,
    Account, AccountGroup,
    JournalEntry, JournalLine,
    Customer, Supplier,
    CashAccount, BankAccount,
    Tax, User, AuditLog, Setting,
    CostCenter, Project, Item, Invoice, InvoiceLine
)
from app.utils.logging_config import get_logger

logger = get_logger(__name__)


def create_tables() -> None:
    """Create all database tables if they don't exist"""
    logger.info("Creating database tables...")
    
    db = get_database()
    engine = db.engine
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    logger.info("Database tables created successfully")


def drop_tables() -> None:
    """Drop all database tables (use with caution!)"""
    logger.warning("Dropping all database tables...")
    
    db = get_database()
    engine = db.engine
    
    # Drop all tables
    Base.metadata.drop_all(bind=engine)
    
    logger.warning("Database tables dropped")


def table_exists(table_name: str) -> bool:
    """Check if a table exists in the database"""
    db = get_database()
    engine = db.engine
    
    inspector = inspect(engine)
    return table_name in inspector.get_table_names()


def get_table_names() -> list:
    """Get list of all table names in the database"""
    db = get_database()
    engine = db.engine
    
    inspector = inspect(engine)
    return inspector.get_table_names()


def init_database_schema() -> None:
    """Initialize database schema with all tables"""
    logger.info("Initializing database schema...")
    
    try:
        create_tables()
        logger.info(f"Created tables: {get_table_names()}")
    except Exception as e:
        logger.error(f"Error creating tables: {e}")
        raise


if __name__ == "__main__":
    # Run this script to initialize the database
    init_database_schema()
    print(f"Database initialized. Tables: {get_table_names()}")
