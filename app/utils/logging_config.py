"""
Logging Configuration for Finovate Journal AI
"""
import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from pathlib import Path
from datetime import datetime


def setup_logging(
    logs_dir: Path,
    level: int = logging.INFO,
    max_bytes: int = 10 * 1024 * 1024,  # 10 MB
    backup_count: int = 5
) -> None:
    """
    Set up logging configuration for the application.
    
    Args:
        logs_dir: Directory to store log files
        level: Logging level (default: INFO)
        max_bytes: Maximum size of log file before rotation
        backup_count: Number of backup log files to keep
    """
    # Ensure logs directory exists
    logs_dir.mkdir(parents=True, exist_ok=True)
    
    # Log file paths
    app_log = logs_dir / "app.log"
    error_log = logs_dir / "errors.log"
    ai_log = logs_dir / "ai.log"
    audit_log = logs_dir / "audit.log"
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - '
        '%(filename)s:%(lineno)d - %(funcName)s() - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    simple_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(simple_formatter)
    root_logger.addHandler(console_handler)
    
    # App log - Rotating file handler
    app_file_handler = RotatingFileHandler(
        app_log,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding='utf-8'
    )
    app_file_handler.setLevel(logging.DEBUG)
    app_file_handler.setFormatter(detailed_formatter)
    root_logger.addHandler(app_file_handler)
    
    # Error log - Only errors and above
    error_file_handler = RotatingFileHandler(
        error_log,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding='utf-8'
    )
    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(detailed_formatter)
    root_logger.addHandler(error_file_handler)
    
    # AI log - For AI-related operations
    ai_logger = logging.getLogger('ai')
    ai_logger.setLevel(logging.DEBUG)
    ai_file_handler = TimedRotatingFileHandler(
        ai_log,
        when='D',  # Daily rotation
        interval=1,
        backupCount=backup_count,
        encoding='utf-8'
    )
    ai_file_handler.setFormatter(detailed_formatter)
    ai_logger.addHandler(ai_file_handler)
    
    # Audit log - For security and compliance
    audit_logger = logging.getLogger('audit')
    audit_logger.setLevel(logging.INFO)
    audit_file_handler = TimedRotatingFileHandler(
        audit_log,
        when='D',  # Daily rotation
        interval=1,
        backupCount=30,  # Keep 30 days of audit logs
        encoding='utf-8'
    )
    audit_file_handler.setFormatter(detailed_formatter)
    audit_logger.addHandler(audit_file_handler)
    
    # Prevent propagation to root logger for specialized loggers
    ai_logger.propagate = False
    audit_logger.propagate = False
    
    # Log startup message
    root_logger.info("=" * 60)
    root_logger.info(f"Finovate Journal AI - Application Started")
    root_logger.info(f"Log directory: {logs_dir}")
    root_logger.info(f"Log level: {logging.getLevelName(level)}")
    root_logger.info("=" * 60)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the given name.
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)
