"""
Finovate Journal AI - Logging Configuration
"""
import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from datetime import datetime
from typing import Optional


class SensitiveDataFilter(logging.Filter):
    """Filter to remove sensitive data from logs"""
    
    SENSITIVE_PATTERNS = [
        'api_key',
        'password',
        'secret',
        'token',
        'credential',
    ]
    
    def filter(self, record: logging.LogRecord) -> bool:
        """Filter out sensitive information"""
        if hasattr(record, 'msg'):
            msg = str(record.msg).lower()
            for pattern in self.SENSITIVE_PATTERNS:
                if pattern in msg:
                    return False
        return True


def setup_logging(
    log_dir: Path,
    level: str = "INFO",
    console_output: bool = True
) -> None:
    """
    Setup application logging
    
    Args:
        log_dir: Directory for log files
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        console_output: Whether to output logs to console
    """
    # Ensure log directory exists
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Log format
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level.upper()))
    
    # Remove existing handlers
    root_logger.handlers.clear()
    
    # Console handler
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)
    
    # Application log file
    app_log_file = log_dir / f"app_{datetime.now().strftime('%Y%m%d')}.log"
    app_handler = RotatingFileHandler(
        app_log_file,
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5,
        encoding='utf-8'
    )
    app_handler.setLevel(logging.DEBUG)
    app_handler.setFormatter(formatter)
    app_handler.addFilter(SensitiveDataFilter())
    root_logger.addHandler(app_handler)
    
    # Error log file
    error_log_file = log_dir / f"errors_{datetime.now().strftime('%Y%m%d')}.log"
    error_handler = RotatingFileHandler(
        error_log_file,
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
        encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    error_handler.addFilter(SensitiveDataFilter())
    root_logger.addHandler(error_handler)
    
    # Audit log file
    audit_log_file = log_dir / f"audit_{datetime.now().strftime('%Y%m%d')}.log"
    audit_handler = TimedRotatingFileHandler(
        audit_log_file,
        when='D',
        interval=1,
        backupCount=30,
        encoding='utf-8'
    )
    audit_handler.setLevel(logging.INFO)
    audit_handler.setFormatter(formatter)
    audit_handler.addFilter(SensitiveDataFilter())
    
    # Create audit logger
    audit_logger = logging.getLogger('audit')
    audit_logger.setLevel(logging.INFO)
    audit_logger.addHandler(audit_handler)
    audit_logger.propagate = False
    
    # AI log file
    ai_log_file = log_dir / f"ai_{datetime.now().strftime('%Y%m%d')}.log"
    ai_handler = RotatingFileHandler(
        ai_log_file,
        maxBytes=10 * 1024 * 1024,
        backupCount=3,
        encoding='utf-8'
    )
    ai_handler.setLevel(logging.DEBUG)
    ai_handler.setFormatter(formatter)
    ai_handler.addFilter(SensitiveDataFilter())
    
    # Create AI logger
    ai_logger = logging.getLogger('ai')
    ai_logger.setLevel(logging.DEBUG)
    ai_logger.addHandler(ai_handler)
    ai_logger.propagate = False


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance
    
    Args:
        name: Logger name (usually __name__)
    
    Returns:
        Logger instance
    """
    return logging.getLogger(name)


def log_audit(
    action: str,
    user: str,
    entity_type: str,
    entity_id: Optional[int] = None,
    details: Optional[dict] = None
) -> None:
    """
    Log an audit event
    
    Args:
        action: Action performed (CREATE, UPDATE, DELETE, etc.)
        user: Username performing the action
        entity_type: Type of entity affected
        entity_id: ID of the entity
        details: Additional details
    """
    audit_logger = logging.getLogger('audit')
    
    log_data = {
        'action': action,
        'user': user,
        'entity_type': entity_type,
        'entity_id': entity_id,
    }
    
    if details:
        log_data['details'] = details
    
    audit_logger.info(f"AUDIT: {log_data}")
