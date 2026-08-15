"""
Finovate Journal AI - Application Settings
Copyright © 2025 Ahmed Mostafa Ibrahim — All Rights Reserved.
"""

from pathlib import Path
from dataclasses import dataclass, field


@dataclass
class DeveloperInfo:
    """Developer information"""
    name: str = "Ahmed Mostafa Ibrahim"
    brand: str = "Finovate – AHMED EG"
    office: str = "Finovate – AHMED EG"
    email: str = "GOGOM8870@GMAIL.COM"
    phone: str = "01225155329"
    copyright: str = "© 2025 Ahmed Mostafa Ibrahim — All Rights Reserved."


@dataclass
class AppSettings:
    """Application settings"""
    
    # Application info
    NAME: str = "Finovate Journal AI"
    VERSION: str = "1.0.0"
    
    # Paths
    BASE_DIR: Path = Path(__file__).parent.parent.parent
    DATA_DIR: Path = field(default_factory=lambda: Path(__file__).parent.parent.parent / "data")
    DB_DIR: Path = field(default_factory=lambda: Path(__file__).parent.parent.parent / "data" / "database")
    LOGS_DIR: Path = field(default_factory=lambda: Path(__file__).parent.parent.parent / "logs")
    BACKUP_DIR: Path = field(default_factory=lambda: Path(__file__).parent.parent.parent / "data" / "backups")
    
    # Database
    DB_NAME: str = "finovate_journal.db"
    
    # Developer info
    DEVELOPER: DeveloperInfo = field(default_factory=DeveloperInfo)
    
    # Default settings
    DEFAULT_CURRENCY: str = "EGP"
    DEFAULT_LANGUAGE: str = "ar"
    DEFAULT_VAT_RATE: float = 14.0
    
    def __post_init__(self):
        """Create directories if they don't exist"""
        self.DATA_DIR.mkdir(parents=True, exist_ok=True)
        self.DB_DIR.mkdir(parents=True, exist_ok=True)
        self.LOGS_DIR.mkdir(parents=True, exist_ok=True)
        self.BACKUP_DIR.mkdir(parents=True, exist_ok=True)


# Create singleton instance
settings = AppSettings()
