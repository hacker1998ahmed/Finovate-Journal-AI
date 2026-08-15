"""Settings model for storing application settings in database."""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from datetime import datetime

from .base import Base


class Settings(Base):
    """Settings model for storing application settings in database."""

    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String(100), unique=True, nullable=False, index=True)
    value = Column(Text, nullable=True)
    value_type = Column(String(20), default="string", nullable=False)  # string, int, float, bool, json
    category = Column(String(50), nullable=True)  # e.g., "general", "accounting", "ai", "backup"
    description = Column(Text, nullable=True)
    is_editable = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return f"<Settings(id={self.id}, key='{self.key}')>"
