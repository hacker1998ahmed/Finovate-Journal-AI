"""Application settings using Pydantic."""

from typing import Optional, List
from pydantic import BaseModel, Field
from pathlib import Path
import json

from .constants import (
    DEVELOPER_INFO,
    DEFAULT_LANGUAGE,
    DEFAULT_CURRENCY,
    DEFAULT_AI_PROVIDER,
    DEFAULT_AI_MODEL,
    DEFAULT_TEMPERATURE,
    DEFAULT_THEME,
    DEFAULT_WINDOW_WIDTH,
    DEFAULT_WINDOW_HEIGHT,
    BACKUP_ENABLED,
    BACKUP_FREQUENCY,
    MAX_BACKUPS,
    DATA_DIR,
    BACKUP_DIR,
)


class DeveloperInfo(BaseModel):
    """Developer information model."""

    name: str = Field(default=DEVELOPER_INFO["name"])
    brand: str = Field(default=DEVELOPER_INFO["brand"])
    email: str = Field(default=DEVELOPER_INFO["email"])
    phone: str = Field(default=DEVELOPER_INFO["phone"])
    copyright: str = Field(default=DEVELOPER_INFO["copyright"])


class AppSettings(BaseModel):
    """General application settings."""

    app_name: str = "Finovate Journal AI"
    version: str = "1.0.0"
    language: str = Field(default=DEFAULT_LANGUAGE)
    currency: str = Field(default=DEFAULT_CURRENCY)
    theme: str = Field(default=DEFAULT_THEME)
    window_width: int = Field(default=DEFAULT_WINDOW_WIDTH)
    window_height: int = Field(default=DEFAULT_WINDOW_HEIGHT)
    date_format: str = "%Y-%m-%d"
    number_format: str = "ar_EG"  # Arabic Egypt format


class AccountingSettings(BaseModel):
    """Accounting-specific settings."""

    fiscal_year_start_month: int = Field(default=1)  # January
    fiscal_year_start_day: int = Field(default=1)
    allow_negative_inventory: bool = Field(default=False)
    default_tax_rate: float = Field(default=14.0)  # Egypt VAT
    auto_numbering: bool = Field(default=True)
    journal_prefix: str = Field(default="JE")
    enable_cost_centers: bool = Field(default=True)
    enable_projects: bool = Field(default=True)
    enable_multi_currency: bool = Field(default=False)


class AISettings(BaseModel):
    """AI provider settings."""

    enabled: bool = Field(default=False)
    provider: str = Field(default=DEFAULT_AI_PROVIDER)
    api_url: Optional[str] = Field(default=None)
    api_key: Optional[str] = Field(default=None)
    model: str = Field(default=DEFAULT_AI_MODEL)
    temperature: float = Field(default=DEFAULT_TEMPERATURE)
    max_tokens: int = Field(default=1024)
    timeout_seconds: int = Field(default=30)
    send_data_consent: bool = Field(default=False)
    local_endpoint: Optional[str] = Field(default=None)  # For Ollama/LM Studio


class BackupSettings(BaseModel):
    """Backup settings."""

    enabled: bool = Field(default=BACKUP_ENABLED)
    frequency: str = Field(default=BACKUP_FREQUENCY)
    max_backups: int = Field(default=MAX_BACKUPS)
    backup_dir: str = Field(default=BACKUP_DIR)
    auto_backup_on_close: bool = Field(default=True)


class CompanySettings(BaseModel):
    """Company-specific settings."""

    company_name: str = Field(default="")
    company_address: str = Field(default="")
    tax_number: str = Field(default="")
    commercial_registration: str = Field(default="")
    logo_path: Optional[str] = Field(default=None)
    phone: str = Field(default="")
    email: str = Field(default="")


class Settings(BaseModel):
    """Main settings container."""

    developer: DeveloperInfo = Field(default_factory=DeveloperInfo)
    app: AppSettings = Field(default_factory=AppSettings)
    accounting: AccountingSettings = Field(default_factory=AccountingSettings)
    ai: AISettings = Field(default_factory=AISettings)
    backup: BackupSettings = Field(default_factory=BackupSettings)
    company: CompanySettings = Field(default_factory=CompanySettings)

    class Config:
        arbitrary_types_allowed = True

    def save(self, filepath: Path) -> None:
        """Save settings to JSON file."""
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.model_dump(), f, indent=2, ensure_ascii=False)

    @classmethod
    def load(cls, filepath: Path) -> "Settings":
        """Load settings from JSON file."""
        if not filepath.exists():
            return cls()

        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        return cls(**data)

    def get_developer_info(self) -> dict:
        """Get developer information as dictionary."""
        return self.developer.model_dump()

    def is_ai_enabled(self) -> bool:
        """Check if AI is enabled and consented."""
        return self.ai.enabled and self.ai.send_data_consent
