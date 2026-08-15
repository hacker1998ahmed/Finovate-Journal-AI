"""
Finovate Journal AI - Application Configuration
"""
from pydantic_settings import BaseSettings
from pydantic import Field
from pathlib import Path
from typing import Optional
import os


class DeveloperInfo(BaseSettings):
    """Developer information displayed in About screen and reports."""
    name: str = "Ahmed Mostafa Ibrahim"
    brand: str = "Finovate – AHMED EG"
    office: str = "Finovate – AHMED EG"
    email: str = "GOGOM8870@GMAIL.COM"
    phone: str = "01225155329"
    copyright: str = "© 2025 Ahmed Mostafa Ibrahim — All Rights Reserved."


class AppSettings(BaseSettings):
    """Main application settings."""
    
    # Application Info
    app_name: str = "Finovate Journal AI"
    version: str = "1.0.0"
    organization: str = "Finovate – AHMED EG"
    
    # Paths
    base_dir: Path = Field(default_factory=lambda: Path(__file__).parent.parent.parent)
    data_dir: Path = Field(default_factory=lambda: Path(__file__).parent.parent.parent / "data")
    logs_dir: Path = Field(default_factory=lambda: Path(__file__).parent.parent.parent / "logs")
    backups_dir: Path = Field(default_factory=lambda: Path(__file__).parent.parent.parent / "backups")
    reports_dir: Path = Field(default_factory=lambda: Path(__file__).parent.parent.parent / "reports")
    templates_dir: Path = Field(default_factory=lambda: Path(__file__).parent.parent.parent / "templates")
    assets_dir: Path = Field(default_factory=lambda: Path(__file__).parent.parent.parent / "assets")
    i18n_dir: Path = Field(default_factory=lambda: Path(__file__).parent.parent.parent / "i18n")
    
    # Database
    database_url: str = ""
    
    # Localization
    default_language: str = "ar"  # ar or en
    default_currency: str = "EGP"
    date_format: str = "%Y-%m-%d"
    
    # Accounting
    fiscal_year_start_month: int = 1
    fiscal_year_start_day: int = 1
    journal_numbering_prefix: str = "JE"
    allow_negative_inventory: bool = False
    
    # Security
    password_min_length: int = 8
    session_timeout_minutes: int = 480  # 8 hours
    max_login_attempts: int = 5
    
    # Backup
    auto_backup_enabled: bool = True
    auto_backup_frequency: str = "daily"  # daily, weekly, monthly
    backup_retention_days: int = 30
    
    # Appearance
    theme: str = "light"  # light, dark
    font_size: int = 10
    
    # AI Settings
    ai_mode: str = "disabled"  # disabled, local, online, auto
    ai_provider: str = ""
    ai_api_url: str = ""
    ai_api_key: str = ""
    ai_model: str = ""
    ai_temperature: float = 0.3
    ai_max_tokens: int = 1000
    local_ai_endpoint: str = "http://localhost:11434"
    
    # Privacy
    send_analytics: bool = False
    allow_external_ai: bool = False
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ensure directories exist
        for dir_path in [self.data_dir, self.logs_dir, self.backups_dir, 
                         self.reports_dir, self.templates_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        # Set default database URL if not provided
        if not self.database_url:
            db_path = self.data_dir / "finovate.db"
            self.database_url = f"sqlite:///{db_path}"


class TaxSettings(BaseSettings):
    """Tax configuration settings."""
    vat_rate: float = 14.0  # Egypt VAT rate
    vat_account_input: str = ""
    vat_account_output: str = ""
    tax_registration_number: str = ""
    
    class Config:
        env_file = ".env"


# Global settings instance
_app_settings: Optional[AppSettings] = None
_developer_info: Optional[DeveloperInfo] = None


def get_app_settings() -> AppSettings:
    """Get global app settings instance."""
    global _app_settings
    if _app_settings is None:
        _app_settings = AppSettings()
    return _app_settings


def get_developer_info() -> DeveloperInfo:
    """Get developer info instance."""
    global _developer_info
    if _developer_info is None:
        _developer_info = DeveloperInfo()
    return _developer_info


def reload_settings():
    """Reload settings from file."""
    global _app_settings, _developer_info
    _app_settings = AppSettings()
    _developer_info = DeveloperInfo()
