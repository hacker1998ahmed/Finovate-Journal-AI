# Finovate Journal AI - Configuration Manager

"""
Configuration manager for loading and saving settings.
"""

import json
from pathlib import Path
from typing import Any, Dict, Optional
from .app_settings import AppSettings, settings


class ConfigManager:
    """Manages application configuration persistence."""
    
    def __init__(self, config_file: Path = Path("data/config.json")):
        self.config_file = config_file
        self._config_data: Dict[str, Any] = {}
        
    def load(self) -> Dict[str, Any]:
        """Load configuration from file."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self._config_data = json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                # Log error but return empty config
                print(f"Error loading config: {e}")
                self._config_data = {}
        return self._config_data
    
    def save(self, config_data: Optional[Dict[str, Any]] = None) -> bool:
        """Save configuration to file."""
        if config_data is not None:
            self._config_data = config_data
        
        try:
            # Ensure directory exists
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self._config_data, f, indent=2, ensure_ascii=False)
            return True
        except IOError as e:
            print(f"Error saving config: {e}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        return self._config_data.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set a configuration value."""
        self._config_data[key] = value
    
    def update_settings(self, app_settings: AppSettings) -> None:
        """Update settings from app_settings instance."""
        # Convert pydantic model to dict
        settings_dict = app_settings.model_dump()
        self._config_data.update(settings_dict)
    
    def apply_to_settings(self, app_settings: AppSettings) -> AppSettings:
        """Apply loaded config to app_settings instance."""
        # Update settings with loaded values
        updates = {}
        for field_name in app_settings.model_fields.keys():
            if field_name in self._config_data:
                updates[field_name] = self._config_data[field_name]
        
        if updates:
            return app_settings.model_copy(update=updates)
        return app_settings
    
    def reset(self) -> None:
        """Reset configuration to defaults."""
        self._config_data = {}
        if self.config_file.exists():
            self.config_file.unlink()


# Global config manager instance
config_manager = ConfigManager()
