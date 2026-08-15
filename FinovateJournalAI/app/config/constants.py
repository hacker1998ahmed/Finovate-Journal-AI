# Finovate Journal AI - Constants

"""
Application constants including developer info, app info, and system constants.
"""

from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True)
class DeveloperInfo:
    """Developer information displayed in About screen and reports."""
    name: str = "Ahmed Mostafa Ibrahim"
    brand: str = "Finovate – AHMED EG"
    office: str = "Finovate – AHMED EG"
    email: str = "GOGOM8870@GMAIL.COM"
    phone: str = "01225155329"
    copyright: str = "© 2025 Ahmed Mostafa Ibrahim — All Rights Reserved."


@dataclass(frozen=True)
class AppInfo:
    """Application metadata."""
    name: str = "Finovate Journal AI"
    version: str = "1.0.0"
    description: str = "AI-Powered Accounting Journal Assistant"
    organization: str = "Finovate – AHMED EG"
    
    # Version components for semantic versioning
    version_major: int = 1
    version_minor: int = 0
    version_patch: int = 0


class Constants:
    """System-wide constants."""
    
    # Application
    APP_NAME: Final[str] = "Finovate Journal AI"
    APP_VERSION: Final[str] = "1.0.0"
    
    # Database
    DATABASE_FILENAME: Final[str] = "finovate_journal.db"
    BACKUP_EXTENSION: Final[str] = ".bak"
    
    # Languages
    DEFAULT_LANGUAGE: Final[str] = "ar"  # Arabic
    SUPPORTED_LANGUAGES: Final[tuple] = ("ar", "en")
    
    # Currencies
    DEFAULT_CURRENCY: Final[str] = "EGP"
    CURRENCY_SYMBOLS: Final[dict] = {
        "EGP": "ج.م",
        "USD": "$",
        "EUR": "€",
        "SAR": "ر.س",
        "AED": "د.إ",
        "GBP": "£"
    }
    
    # Date formats
    DATE_FORMAT_AR: Final[str] = "%Y-%m-%d"
    DATE_FORMAT_EN: Final[str] = "%Y-%m-%d"
    DATETIME_FORMAT: Final[str] = "%Y-%m-%d %H:%M:%S"
    
    # Journal Entry Status
    STATUS_DRAFT: Final[str] = "Draft"
    STATUS_AI_SUGGESTED: Final[str] = "AI Suggested"
    STATUS_USER_EDITED: Final[str] = "User Edited"
    STATUS_REVIEWED: Final[str] = "Reviewed"
    STATUS_POSTED: Final[str] = "Posted"
    STATUS_CANCELLED: Final[str] = "Cancelled"
    
    # User Roles
    ROLE_ADMINISTRATOR: Final[str] = "Administrator"
    ROLE_ACCOUNTANT: Final[str] = "Accountant"
    ROLE_REVIEWER: Final[str] = "Reviewer"
    ROLE_VIEWER: Final[str] = "Viewer"
    
    # Confidence Levels
    CONFIDENCE_HIGH: Final[int] = 90
    CONFIDENCE_MEDIUM: Final[int] = 75
    CONFIDENCE_LOW: Final[int] = 50
    
    # Tax
    DEFAULT_VAT_RATE: Final[float] = 0.14  # 14% Egypt VAT
    
    # File paths
    LOG_DIR: Final[str] = "logs"
    BACKUP_DIR: Final[str] = "backups"
    REPORTS_DIR: Final[str] = "reports"
    DATA_DIR: Final[str] = "data"
    I18N_DIR: Final[str] = "i18n"
    
    # Logging
    LOG_MAX_BYTES: Final[int] = 10 * 1024 * 1024  # 10 MB
    LOG_BACKUP_COUNT: Final[int] = 5
    
    # Error codes prefix
    ERROR_PREFIX: Final[str] = "FJA"
    
    # Developer Info
    DEVELOPER: Final[DeveloperInfo] = DeveloperInfo()
    APP_INFO: Final[AppInfo] = AppInfo()


# Global instances
DEVELOPER_INFO = DeveloperInfo()
APP_INFO = AppInfo()
