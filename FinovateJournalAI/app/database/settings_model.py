# Finovate Journal AI - Settings Model

"""
Settings model for storing application settings in database.
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base


class SettingsModel(Base):
    """Settings model for database-stored configuration."""
    
    __tablename__ = "settings"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True)  # Null for global settings
    
    key = Column(String(100), nullable=False, index=True)
    value = Column(Text, nullable=False)
    value_type = Column(String(20), default="string")  # string, integer, float, boolean, json
    
    description_ar = Column(Text, default="")
    description_en = Column(Text, default="")
    
    is_system = Column(Boolean, default=False)  # System settings cannot be deleted by users
    is_encrypted = Column(Boolean, default=False)  # Indicates if value is encrypted
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    company = relationship("Company", backref="settings")
    
    def __repr__(self):
        return f"<SettingsModel(id={self.id}, key='{self.key}')>"
    
    def get_typed_value(self):
        """Get value converted to its proper type."""
        import json
        
        if self.value_type == "integer":
            return int(self.value)
        elif self.value_type == "float":
            return float(self.value)
        elif self.value_type == "boolean":
            return self.value.lower() in ("true", "1", "yes")
        elif self.value_type == "json":
            return json.loads(self.value)
        else:
            return self.value
