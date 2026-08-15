# Finovate Journal AI - Audit Log Model

"""
Audit Log model for tracking all important system changes.
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base


class AuditLog(Base):
    """Audit log model for tracking system changes."""
    
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # User info
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    username = Column(String(100), nullable=True)  # Stored in case user is deleted
    
    # Action info
    action = Column(String(100), nullable=False, index=True)  # e.g., "CREATE", "UPDATE", "DELETE"
    entity_type = Column(String(100), nullable=False, index=True)  # e.g., "JournalEntry", "Account"
    entity_id = Column(Integer, nullable=True, index=True)
    
    # Change details
    old_value = Column(Text, default="")  # JSON string of old values
    new_value = Column(Text, default="")  # JSON string of new values
    
    # Context
    ip_address = Column(String(50), default="")
    device_info = Column(String(255), default="")
    notes = Column(Text, default="")
    
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    user = relationship("User", backref="audit_logs")
    
    def __repr__(self):
        return f"<AuditLog(id={self.id}, action='{self.action}', entity='{self.entity_type}', timestamp={self.timestamp})>"
    
    @staticmethod
    def log_action(db_session, action: str, entity_type: str, entity_id: int = None,
                   old_value: dict = None, new_value: dict = None,
                   user_id: int = None, username: str = None,
                   ip_address: str = "", device_info: str = "", notes: str = ""):
        """Create and save an audit log entry."""
        import json
        
        audit_entry = AuditLog(
            user_id=user_id,
            username=username,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            old_value=json.dumps(old_value) if old_value else "",
            new_value=json.dumps(new_value) if new_value else "",
            ip_address=ip_address,
            device_info=device_info,
            notes=notes
        )
        
        db_session.add(audit_entry)
        return audit_entry
