"""
Finovate Journal AI - Setting Model
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from datetime import datetime

from app.database.base import Base


class Setting(Base):
    """Application settings stored in database"""
    __tablename__ = "settings"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String(100), unique=True, nullable=False, index=True)
    value = Column(Text)  # JSON string for complex settings
    value_type = Column(String(20), default="string")  # string, number, boolean, json
    category = Column(String(50))  # General, Accounting, Tax, AI, UI, etc.
    description = Column(Text)
    description_ar = Column(Text)  # Arabic description
    is_system = Column(Boolean, default=False)  # System settings cannot be deleted
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Setting(id={self.id}, key='{self.key}')>"
