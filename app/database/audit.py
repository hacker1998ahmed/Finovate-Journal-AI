"""Audit Log model for tracking all changes."""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
import json

from .base import Base


class ActionType(str, enum.Enum):
    """Action type enumeration."""

    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    POST = "post"
    CANCEL = "cancel"
    LOGIN = "login"
    LOGOUT = "logout"
    EXPORT = "export"
    IMPORT = "import"
    BACKUP = "backup"
    RESTORE = "restore"


class AuditLog(Base):
    """Audit Log model for tracking all system changes."""

    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    action_type = Column(SQLEnum(ActionType), nullable=False)
    entity_type = Column(String(50), nullable=False)  # e.g., "JournalEntry", "Account"
    entity_id = Column(Integer, nullable=True)
    journal_entry_id = Column(Integer, ForeignKey("journal_entries.id"), nullable=True)
    old_values = Column(Text, nullable=True)  # JSON string of old values
    new_values = Column(Text, nullable=True)  # JSON string of new values
    ip_address = Column(String(45), nullable=True)  # IPv6 compatible
    device_info = Column(String(200), nullable=True)
    notes = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    # Relationships
    user = relationship("User", back_populates="audit_logs")
    journal_entry = relationship("JournalEntry", back_populates="audit_logs")

    def __repr__(self) -> str:
        return f"<AuditLog(id={self.id}, action='{self.action_type.value}', entity='{self.entity_type}')>"

    @property
    def old_values_dict(self) -> dict:
        """Get old values as dictionary."""
        if self.old_values:
            try:
                return json.loads(self.old_values)
            except json.JSONDecodeError:
                return {}
        return {}

    @property
    def new_values_dict(self) -> dict:
        """Get new values as dictionary."""
        if self.new_values:
            try:
                return json.loads(self.new_values)
            except json.JSONDecodeError:
                return {}
        return {}

    @staticmethod
    def serialize_value(value) -> str:
        """Serialize a value to JSON string."""
        try:
            return json.dumps(value, default=str, ensure_ascii=False)
        except (TypeError, ValueError):
            return str(value)
