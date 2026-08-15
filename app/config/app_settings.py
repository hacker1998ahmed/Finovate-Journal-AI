# Finovate Journal AI - Application Settings

"""
Application settings using Pydantic for validation.
Handles user preferences, company settings, and AI configuration.
"""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional, Literal
from pathlib import Path
from datetime import date


class AppSettings(BaseSettings):
    """Application settings with validation."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # General Settings
    app_name: str = Field(default="Finovate Journal AI", description="Application name")
    language: Literal["ar", "en"] = Field(default="ar", description="UI Language")
    currency: str = Field(default="EGP", description="Default currency")
    date_format: str = Field(default="%Y-%m-%d", description="Date display format")
    fiscal_year_start: date = Field(default=date.today().replace(month=1, day=1), description="Fiscal year start")
    
    # Company Settings
    company_name: str = Field(default="", description="Company name")
    company_address: str = Field(default="", description="Company address")
    company_tax_number: str = Field(default="", description="Company tax number")
    company_phone: str = Field(default="", description="Company phone")
    company_email: str = Field(default="", description="Company email")
    
    # Database Settings
    database_path: Path = Field(default=Path("data/finovate_journal.db"), description="Database file path")
    
    # AI Settings
    ai_mode: Literal["disabled", "local", "online", "auto"] = Field(default="auto", description="AI operation mode")
    ai_provider: Literal["openai", "openrouter", "ollama", "lmstudio", "disabled"] = Field(default="disabled", description="AI provider")
    ai_api_url: Optional[str] = Field(default=None, description="AI API endpoint URL")
    ai_api_key: Optional[str] = Field(default=None, description="AI API key")
    ai_model: str = Field(default="gpt-3.5-turbo", description="AI model name")
    ai_temperature: float = Field(default=0.3, ge=0.0, le=2.0, description="AI temperature for responses")
    local_ai_endpoint: str = Field(default="http://localhost:11434", description="Local AI endpoint (Ollama/LM Studio)")
    
    # Privacy Settings
    allow_data_send_to_ai: bool = Field(default=False, description="Allow sending data to external AI")
    log_ai_requests: bool = Field(default=True, description="Log AI requests for debugging")
    
    # Backup Settings
    backup_enabled: bool = Field(default=True, description="Enable automatic backups")
    backup_frequency: Literal["daily", "weekly", "monthly"] = Field(default="daily", description="Backup frequency")
    backup_path: Path = Field(default=Path("backups"), description="Backup directory")
    max_backup_count: int = Field(default=10, description="Maximum number of backups to keep")
    
    # Appearance Settings
    theme: Literal["light", "dark", "system"] = Field(default="system", description="UI theme")
    font_size: int = Field(default=12, ge=10, le=20, description="UI font size")
    rtl_enabled: bool = Field(default=True, description="Right-to-left layout for Arabic")
    
    # Accounting Settings
    journal_numbering_format: str = Field(default="JE-{year}-{seq:06d}", description="Journal entry numbering format")
    allow_negative_inventory: bool = Field(default=False, description="Allow negative inventory quantities")
    require_cost_center: bool = Field(default=False, description="Require cost center on entries")
    require_project: bool = Field(default=False, description="Require project on entries")
    
    # Security Settings
    session_timeout_minutes: int = Field(default=60, description="Session timeout in minutes")
    max_login_attempts: int = Field(default=5, description="Maximum login attempts before lockout")
    password_min_length: int = Field(default=8, description="Minimum password length")
    
    @property
    def is_rtl(self) -> bool:
        """Check if RTL layout should be used."""
        return self.rtl_enabled and self.language == "ar"
    
    @property
    def is_ai_enabled(self) -> bool:
        """Check if AI is enabled."""
        return self.ai_mode != "disabled" and self.ai_provider != "disabled"
    
    @property
    def is_online_ai(self) -> bool:
        """Check if online AI is being used."""
        return self.ai_mode == "online" or (self.ai_mode == "auto" and self.ai_provider in ["openai", "openrouter"])
    
    def get_journal_number(self, year: int, sequence: int) -> str:
        """Generate journal entry number based on format."""
        return self.journal_numbering_format.format(year=year, seq=sequence)


# Global settings instance
settings = AppSettings()
