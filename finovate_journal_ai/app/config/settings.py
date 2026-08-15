"""
Finovate Journal AI - Application Configuration
"""
from pydantic_settings import BaseSettings
from pydantic import Field
from pathlib import Path
from typing import Optional, Literal
import os


class DeveloperInfo(BaseSettings):
    """Developer information displayed in About dialog"""
    name: str = "Ahmed Mostafa Ibrahim"
    brand: str = "Finovate – AHMED EG"
    office: str = "Finovate – AHMED EG"
    email: str = "GOGOM8870@GMAIL.COM"
    phone: str = "01225155329"
    copyright: str = "© 2025 Ahmed Mostafa Ibrahim — All Rights Reserved."


class AppSettings(BaseSettings):
    """Application settings"""
    app_name: str = "Finovate Journal AI"
    version: str = "1.0.0"
    app_env: Literal["development", "production"] = "development"
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    
    # Paths
    base_dir: Path = Field(default_factory=lambda: Path(__file__).parent.parent.parent)
    data_dir: Path = Field(default_factory=lambda: Path(__file__).parent.parent.parent / "data")
    logs_dir: Path = Field(default_factory=lambda: Path(__file__).parent.parent.parent / "logs")
    reports_dir: Path = Field(default_factory=lambda: Path(__file__).parent.parent.parent / "reports")
    backups_dir: Path = Field(default_factory=lambda: Path(__file__).parent.parent.parent / "backups")
    assets_dir: Path = Field(default_factory=lambda: Path(__file__).parent.parent.parent / "assets")
    i18n_dir: Path = Field(default_factory=lambda: Path(__file__).parent.parent.parent / "i18n")
    
    def ensure_directories(self):
        """Ensure all required directories exist"""
        for dir_path in [self.data_dir, self.logs_dir, self.reports_dir, self.backups_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)


class DatabaseSettings(BaseSettings):
    """Database configuration"""
    database_url: str = "sqlite:///data/finovate.db"
    echo: bool = False  # Set to True for SQL debugging
    pool_pre_ping: bool = True
    
    @property
    def db_path(self) -> Path:
        """Get the database file path"""
        if self.database_url.startswith("sqlite:///"):
            db_name = self.database_url.replace("sqlite:///", "")
            return Path(__file__).parent.parent.parent / db_name
        return Path()


class AISettings(BaseSettings):
    """AI Provider configuration"""
    ai_provider: Literal["disabled", "openai", "openrouter", "ollama", "lmstudio"] = "disabled"
    openai_api_key: Optional[str] = None
    openai_base_url: str = "https://api.openai.com/v1"
    openai_model: str = "gpt-4o-mini"
    
    # Ollama
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.1:8b"
    
    # LM Studio
    lmstudio_base_url: str = "http://localhost:1234"
    lmstudio_model: str = "local-model"
    
    # AI Behavior
    temperature: float = 0.1  # Low temperature for consistent accounting
    max_tokens: int = 2000
    timeout: int = 30
    
    # Privacy
    send_data_to_cloud: bool = False
    require_approval_for_ai: bool = True


class CompanySettings(BaseSettings):
    """Default company settings"""
    company_name: str = "Demo Company"
    currency: str = "EGP"
    currency_symbol: str = "ج.م"
    language: Literal["ar", "en"] = "ar"
    fiscal_year_start: str = "01-01"  # MM-DD format
    fiscal_year_end: str = "12-31"
    date_format: str = "%Y-%m-%d"
    tax_number: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    logo_path: Optional[str] = None


class TaxSettings(BaseSettings):
    """Tax configuration"""
    default_tax_rate: float = 14.0  # Egypt VAT default
    tax_inclusive: bool = False
    input_vat_account: Optional[int] = None
    output_vat_account: Optional[int] = None


class BackupSettings(BaseSettings):
    """Backup configuration"""
    auto_backup: bool = True
    backup_frequency: Literal["daily", "weekly", "monthly"] = "daily"
    backup_retention_days: int = 30
    backup_on_close: bool = True


class UISettings(BaseSettings):
    """UI configuration"""
    theme: Literal["light", "dark"] = "light"
    font_size: int = 10
    sidebar_width: int = 250
    window_width: int = 1400
    window_height: int = 900


class Settings(BaseSettings):
    """Main settings class combining all configurations"""
    developer: DeveloperInfo = Field(default_factory=DeveloperInfo)
    app: AppSettings = Field(default_factory=AppSettings)
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    ai: AISettings = Field(default_factory=AISettings)
    company: CompanySettings = Field(default_factory=CompanySettings)
    tax: TaxSettings = Field(default_factory=TaxSettings)
    backup: BackupSettings = Field(default_factory=BackupSettings)
    ui: UISettings = Field(default_factory=UISettings)
    
    class Config:
        env_file = ".env"
        env_nested_delimiter = "__"


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get application settings"""
    return settings
