"""Logging configuration for Finovate Journal AI."""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import sys

from ..config.constants import LOGS_DIR, LOG_FORMAT, LOG_MAX_BYTES, LOG_BACKUP_COUNT


def setup_logging():
    """Setup logging configuration."""
    # Ensure logs directory exists
    Path(LOGS_DIR).mkdir(parents=True, exist_ok=True)

    # Create formatters
    detailed_formatter = logging.Formatter(LOG_FORMAT)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(detailed_formatter)
    console_handler.setLevel(logging.INFO)

    # General app log
    app_log_file = Path(LOGS_DIR) / "app.log"
    app_handler = RotatingFileHandler(
        app_log_file,
        maxBytes=LOG_MAX_BYTES,
        backupCount=LOG_BACKUP_COUNT,
        encoding="utf-8",
    )
    app_handler.setFormatter(detailed_formatter)
    app_handler.setLevel(logging.DEBUG)

    # Error log
    error_log_file = Path(LOGS_DIR) / "errors.log"
    error_handler = RotatingFileHandler(
        error_log_file,
        maxBytes=LOG_MAX_BYTES,
        backupCount=LOG_BACKUP_COUNT,
        encoding="utf-8",
    )
    error_handler.setFormatter(detailed_formatter)
    error_handler.setLevel(logging.ERROR)

    # AI log
    ai_log_file = Path(LOGS_DIR) / "ai.log"
    ai_handler = RotatingFileHandler(
        ai_log_file,
        maxBytes=LOG_MAX_BYTES,
        backupCount=LOG_BACKUP_COUNT,
        encoding="utf-8",
    )
    ai_handler.setFormatter(detailed_formatter)
    ai_handler.setLevel(logging.DEBUG)

    # Audit log
    audit_log_file = Path(LOGS_DIR) / "audit.log"
    audit_handler = RotatingFileHandler(
        audit_log_file,
        maxBytes=LOG_MAX_BYTES,
        backupCount=LOG_BACKUP_COUNT,
        encoding="utf-8",
    )
    audit_handler.setFormatter(detailed_formatter)
    audit_handler.setLevel(logging.INFO)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(app_handler)
    root_logger.addHandler(error_handler)

    return root_logger


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with the given name."""
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        # Ensure logs directory exists
        Path(LOGS_DIR).mkdir(parents=True, exist_ok=True)
        
        detailed_formatter = logging.Formatter(LOG_FORMAT)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(detailed_formatter)
        console_handler.setLevel(logging.INFO)
        
        # File handler
        log_file = Path(LOGS_DIR) / f"{name.replace('.', '_')}.log"
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=LOG_MAX_BYTES,
            backupCount=LOG_BACKUP_COUNT,
            encoding="utf-8",
        )
        file_handler.setFormatter(detailed_formatter)
        file_handler.setLevel(logging.DEBUG)
        
        logger.setLevel(logging.DEBUG)
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
    
    return logger


# Initialize logging on module import
setup_logging()
