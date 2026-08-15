"""
Finovate Journal AI - Settings Management

Developer: Ahmed Mostafa Ibrahim
Brand: Finovate – AHMED EG
"""

import os
from pathlib import Path
from typing import Optional, List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

from .constants import (
    APP_NAME,
    APP_VERSION,
    DEVELOPER_NAME,
    DEVELOPER_BRAND,
    DEVELOPER_EMAIL,
    DEVELOPER_PHONE,
    COPYRIGHT_TEXT,
    DEFAULT_LANGUAGE,
    DEFAULT_CURRENCY,
    SUPPORTED_LANGUAGES,
    SUPPORTED_CURRENCIES,
    DATABASE_DIR,
    LOGS_DIR,
    BACKUPS_DIR,
    REPORTS_DIR,
    DATABASE_FILENAME,
    AI_PROVIDER_DISABLED,
    DEFAULT_TAX_RATE,
    DARK_MODE_DEFAULT,
    RTL_DEFAULT_FOR_AR,
)


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    model_config = SettingsConfigDict(
        env_prefix="FINOVATE_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application Info (Read-only from code)
    app_name: str = Field(default=APP_NAME, frozen=True)
    app_version: str = Field(default=APP_VERSION, frozen=True)
    developer_name: str = Field(default=DEVELOPER_NAME, frozen=True)
    developer_brand: str = Field(default=DEVELOPER_BRAND, frozen=True)
    developer_email: str = Field(default=DEVELOPER_EMAIL, frozen=True)
    developer_phone: str = Field(default=DEVELOPER_PHONE, frozen=True)
    copyright_text: str = Field(default=COPYRIGHT_TEXT, frozen=True)

    # General Settings
    language: str = Field(default=DEFAULT_LANGUAGE, description="Application language (ar/en)")
    currency: str = Field(default=DEFAULT_CURRENCY, description="Default currency")
    date_format: str = Field(default="%Y-%m-%d", description="Date display format")
    dark_mode: bool = Field(default=DARK_MODE_DEFAULT, description="Enable dark mode")
    rtl_enabled: bool = Field(default=RTL_DEFAULT_FOR_AR, description="Right-to-left layout")

    # Company Settings
    company_name: str = Field(default="", description="Company name")
    company_address: str = Field(default="", description="Company address")
    company_tax_number: str = Field(default="", description="Company tax number")
    company_phone: str = Field(default="", description="Company phone")
    company_email: str = Field(default="", description="Company email")

    # Fiscal Year
    fiscal_year_start_month: int = Field(default=1, description="Fiscal year start month (1-12)")
    fiscal_year_start_day: int = Field(default=1, description="Fiscal year start day (1-31)")
    current_fiscal_year: int = Field(default=2025, description="Current fiscal year")

    # Accounting Settings
    journal_prefix: str = Field(default="JE", description="Journal entry prefix")
    default_tax_rate: float = Field(default=DEFAULT_TAX_RATE, description="Default VAT rate")
    tax_inclusive: bool = Field(default=False, description="Prices include tax by default")
    allow_negative_stock: bool = Field(default=False, description="Allow negative inventory")
    enable_cost_centers: bool = Field(default=True, description="Enable cost centers")
    enable_projects: bool = Field(default=True, description="Enable project accounting")

    # Database
    database_path: str = Field(default="", description="Path to database file")
    
    # Paths
    base_dir: Path = Field(default=Path(__file__).parent.parent.parent)
    data_dir: str = Field(default=DATABASE_DIR)
    logs_dir: str = Field(default=LOGS_DIR)
    backups_dir: str = Field(default=BACKUPS_DIR)
    reports_dir: str = Field(default=REPORTS_DIR)

    # AI Settings
    ai_provider: str = Field(default=AI_PROVIDER_DISABLED, description="AI provider (disabled/local/online/auto)")
    ai_api_key: str = Field(default="", description="API key for online AI providers")
    ai_api_url: str = Field(default="", description="API URL for custom/OpenAI-compatible providers")
    ai_model: str = Field(default="", description="AI model name")
    ai_temperature: float = Field(default=0.3, ge=0.0, le=2.0, description="AI temperature")
    ai_local_url: str = Field(default="http://localhost:1234/v1", description="Local AI endpoint (LM Studio/Ollama)")
    ai_send_data_consent: bool = Field(default=False, description="User consent to send data to external AI")

    # Backup Settings
    auto_backup_enabled: bool = Field(default=True, description="Enable automatic backup")
    auto_backup_frequency: str = Field(default="daily", description="Backup frequency (daily/weekly/monthly)")
    backup_retention_days: int = Field(default=30, description="Days to keep backups")
    backup_path: str = Field(default="", description="Custom backup path")

    # Security
    session_timeout_minutes: int = Field(default=60, description="Session timeout in minutes")
    max_login_attempts: int = Field(default=5, description="Maximum login attempts before lockout")
    password_min_length: int = Field(default=8, description="Minimum password length")

    # UI
    window_width: int = Field(default=1400, description="Default window width")
    window_height: int = Field(default=900, description="Default window height")
    sidebar_width: int = Field(default=250, description="Sidebar width")
    font_size: int = Field(default=12, description="Default font size")

    @property
    def database_file(self) -> Path:
        """Get full path to database file."""
        db_dir = self.base_dir / self.data_dir
        db_dir.mkdir(parents=True, exist_ok=True)
        if self.database_path:
            return Path(self.database_path)
        return db_dir / DATABASE_FILENAME

    @property
    def logs_directory(self) -> Path:
        """Get full path to logs directory."""
        logs_dir = self.base_dir / self.logs_dir
        logs_dir.mkdir(parents=True, exist_ok=True)
        return logs_dir

    @property
    def backups_directory(self) -> Path:
        """Get full path to backups directory."""
        backups_dir = self.base_dir / self.backups_dir
        backups_dir.mkdir(parents=True, exist_ok=True)
        if self.backup_path:
            return Path(self.backup_path)
        return backups_dir

    @property
    def reports_directory(self) -> Path:
        """Get full path to reports directory."""
        reports_dir = self.base_dir / self.reports_dir
        reports_dir.mkdir(parents=True, exist_ok=True)
        return reports_dir

    @property
    def is_rtl(self) -> bool:
        """Check if RTL layout should be enabled."""
        return self.rtl_enabled and self.language == "ar"

    @property
    def supported_languages(self) -> List[str]:
        """Get list of supported languages."""
        return SUPPORTED_LANGUAGES

    @property
    def supported_currencies(self) -> List[str]:
        """Get list of supported currencies."""
        return SUPPORTED_CURRENCIES

    def validate_settings(self) -> bool:
        """Validate critical settings."""
        if self.language not in self.supported_languages:
            return False
        if self.currency not in self.supported_currencies:
            return False
        if self.default_tax_rate < 0 or self.default_tax_rate > 100:
            return False
        return True


# Singleton instance
_settings_instance: Optional[Settings] = None


def get_settings() -> Settings:
    """Get or create settings singleton instance."""
    global _settings_instance
    if _settings_instance is None:
        _settings_instance = Settings()
    return _settings_instance


def reset_settings() -> None:
    """Reset settings singleton (for testing)."""
    global _settings_instance
    _settings_instance = None
