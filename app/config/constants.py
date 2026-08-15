"""Application constants."""

from decimal import Decimal

# Application Info
APP_NAME = "Finovate Journal AI"
VERSION = "1.0.0"
ORGANIZATION = "Finovate – AHMED EG"

# Developer Information
DEVELOPER_INFO = {
    "name": "Ahmed Mostafa Ibrahim",
    "brand": "Finovate – AHMED EG",
    "email": "GOGOM8870@GMAIL.COM",
    "phone": "01225155329",
    "copyright": "© 2025 Ahmed Mostafa Ibrahim — All Rights Reserved.",
}

# Supported Languages
SUPPORTED_LANGUAGES = ["ar", "en"]
DEFAULT_LANGUAGE = "ar"

# Currency
DEFAULT_CURRENCY = "EGP"
CURRENCY_SYMBOLS = {
    "EGP": "ج.م",
    "USD": "$",
    "EUR": "€",
    "SAR": "﷼",
    "AED": "د.إ",
    "GBP": "£",
}

# Journal Entry Status
ENTRY_STATUS = {
    "DRAFT": "draft",
    "AI_SUGGESTED": "ai_suggested",
    "USER_EDITED": "user_edited",
    "REVIEWED": "reviewed",
    "POSTED": "posted",
    "CANCELLED": "cancelled",
}

# User Roles
USER_ROLES = {
    "ADMIN": "admin",
    "ACCOUNTANT": "accountant",
    "REVIEWER": "reviewer",
    "VIEWER": "viewer",
}

# Account Types
ACCOUNT_TYPES = {
    "ASSET": "asset",
    "LIABILITY": "liability",
    "EQUITY": "equity",
    "REVENUE": "revenue",
    "EXPENSE": "expense",
}

# Normal Balances (Debit or Credit)
NORMAL_BALANCES = {
    "ASSET": "debit",
    "LIABILITY": "credit",
    "EQUITY": "credit",
    "REVENUE": "credit",
    "EXPENSE": "debit",
}

# Confidence Levels
CONFIDENCE_LEVELS = {
    "VERY_HIGH": (90, 100),
    "HIGH": (75, 89),
    "MEDIUM": (50, 74),
    "LOW": (0, 49),
}

# Date Formats
DATE_FORMATS = {
    "ar": "%Y-%m-%d",
    "en": "%Y-%m-%d",
}

DATETIME_FORMATS = {
    "ar": "%Y-%m-%d %H:%M:%S",
    "en": "%Y-%m-%d %H:%M:%S",
}

# Number Format
DECIMAL_PLACES = 3
MIN_DECIMAL = Decimal("0.001")
MAX_DECIMAL = Decimal("999999999.999")

# File Paths
DATA_DIR = "data"
BACKUP_DIR = "backups"
LOGS_DIR = "logs"
REPORTS_DIR = "reports"
TEMPLATES_DIR = "templates"
I18N_DIR = "i18n"

# Database
DATABASE_NAME = "finovate_journal.db"
DATABASE_URL_TEMPLATE = f"sqlite:///{DATA_DIR}/{DATABASE_NAME}"

# Logging
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_MAX_BYTES = 10 * 1024 * 1024  # 10 MB
LOG_BACKUP_COUNT = 5

# AI Settings
DEFAULT_AI_PROVIDER = "rules_engine"
AI_PROVIDERS = ["rules_engine", "ollama", "lm_studio", "openai_compatible", "openrouter"]
DEFAULT_AI_MODEL = "gpt-4o-mini"
DEFAULT_TEMPERATURE = 0.3

# Backup
BACKUP_ENABLED = True
BACKUP_FREQUENCY = "daily"  # daily, weekly, monthly
MAX_BACKUPS = 10

# Security
PASSWORD_MIN_LENGTH = 8
SESSION_TIMEOUT_MINUTES = 60
MAX_LOGIN_ATTEMPTS = 5

# UI
DEFAULT_THEME = "light"  # light, dark
DEFAULT_WINDOW_WIDTH = 1400
DEFAULT_WINDOW_HEIGHT = 900
SIDEBAR_WIDTH = 250
