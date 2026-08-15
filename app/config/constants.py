"""
Finovate Journal AI - Application Constants

Developer: Ahmed Mostafa Ibrahim
Brand: Finovate – AHMED EG
"""

# Application Information
APP_NAME = "Finovate Journal AI"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "AI-Powered Desktop Accounting & Journal Entry Assistant"

# Developer Information
DEVELOPER_NAME = "Ahmed Mostafa Ibrahim"
DEVELOPER_BRAND = "Finovate – AHMED EG"
DEVELOPER_OFFICE = "Finovate – AHMED EG"
DEVELOPER_EMAIL = "GOGOM8870@GMAIL.COM"
DEVELOPER_PHONE = "01225155329"
COPYRIGHT_TEXT = "© 2025 Ahmed Mostafa Ibrahim — All Rights Reserved."

# Default Settings
DEFAULT_LANGUAGE = "ar"  # Arabic default
DEFAULT_CURRENCY = "EGP"
SUPPORTED_LANGUAGES = ["ar", "en"]
SUPPORTED_CURRENCIES = ["EGP", "USD", "EUR", "SAR", "AED", "GBP"]

# Journal Entry Numbering
JOURNAL_ENTRY_PREFIX = "JE"
JOURNAL_NUMBER_FORMAT = "{prefix}-{year}-{sequence:06d}"

# Account Types
ACCOUNT_TYPES = [
    "asset",
    "liability",
    "equity",
    "revenue",
    "expense",
]

# Normal Balances
NORMAL_BALANCES = {
    "asset": "debit",
    "liability": "credit",
    "equity": "credit",
    "revenue": "credit",
    "expense": "debit",
}

# Journal Entry Status
ENTRY_STATUS_DRAFT = "draft"
ENTRY_STATUS_REVIEWED = "reviewed"
ENTRY_STATUS_POSTED = "posted"
ENTRY_STATUS_CANCELLED = "cancelled"

ENTRY_STATUSES = [
    ENTRY_STATUS_DRAFT,
    ENTRY_STATUS_REVIEWED,
    ENTRY_STATUS_POSTED,
    ENTRY_STATUS_CANCELLED,
]

# User Roles
ROLE_ADMINISTRATOR = "administrator"
ROLE_ACCOUNTANT = "accountant"
ROLE_REVIEWER = "reviewer"
ROLE_VIEWER = "viewer"

USER_ROLES = [
    ROLE_ADMINISTRATOR,
    ROLE_ACCOUNTANT,
    ROLE_REVIEWER,
    ROLE_VIEWER,
]

# AI Providers
AI_PROVIDER_DISABLED = "disabled"
AI_PROVIDER_LOCAL = "local"
AI_PROVIDER_ONLINE = "online"
AI_PROVIDER_AUTO = "auto"

AI_PROVIDERS = [
    AI_PROVIDER_DISABLED,
    AI_PROVIDER_LOCAL,
    AI_PROVIDER_ONLINE,
    AI_PROVIDER_AUTO,
]

# Confidence Levels
CONFIDENCE_HIGH = 90  # 90-100%
CONFIDENCE_MEDIUM = 75  # 75-89%
CONFIDENCE_LOW = 50  # 50-74%
# Below 50% needs review

# Paths (relative to app root)
DATABASE_DIR = "data"
LOGS_DIR = "logs"
BACKUPS_DIR = "backups"
REPORTS_DIR = "reports"
TEMPLATES_DIR = "templates"
I18N_DIR = "i18n"
ASSETS_DIR = "assets"

# Database
DATABASE_FILENAME = "finovate_journal.db"

# Logging
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_MAX_BYTES = 10 * 1024 * 1024  # 10 MB
LOG_BACKUP_COUNT = 5

# Excel
EXCEL_DATE_FORMAT = "%Y-%m-%d"
EXCEL_NUMBER_FORMAT = "#,##0.00"

# PDF
PDF_FONT_ARABIC = "Arial"
PDF_FONT_ENGLISH = "Arial"
PDF_FONT_SIZE = 12
PDF_PAGE_SIZE = "A4"

# Security
PASSWORD_MIN_LENGTH = 8
SESSION_TIMEOUT_MINUTES = 60
MAX_LOGIN_ATTEMPTS = 5

# Backup
BACKUP_RETENTION_DAYS = 30
AUTO_BACKUP_ENABLED = True
AUTO_BACKUP_FREQUENCY = "daily"  # daily, weekly, monthly

# Tax
DEFAULT_TAX_RATE = 14.0  # Egypt VAT default
TAX_CALCULATION_METHOD = "exclusive"  # exclusive or inclusive

# Decimal Precision
DECIMAL_PRECISION = 3  # For financial calculations

# UI
DEFAULT_WINDOW_WIDTH = 1400
DEFAULT_WINDOW_HEIGHT = 900
SIDEBAR_WIDTH = 250
DARK_MODE_DEFAULT = False
RTL_DEFAULT_FOR_AR = True
