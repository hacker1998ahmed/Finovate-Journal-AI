"""
Finovate Journal AI - Audit Log Model
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON
from datetime import datetime

from app.database.base import Base


class AuditLog(Base):
    """Audit log for tracking all important system changes"""
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    username = Column(String(50))  # Denormalized for performance
    action = Column(String(50), nullable=False)  # CREATE, UPDATE, DELETE, LOGIN, LOGOUT, etc.
    entity_type = Column(String(50), nullable=False)  # JournalEntry, Account, Customer, etc.
    entity_id = Column(Integer)
    entity_name = Column(String(200))  # Denormalized for easier reading
    old_values = Column(JSON)  # Previous values (for UPDATE/DELETE)
    new_values = Column(JSON)  # New values (for CREATE/UPDATE)
    ip_address = Column(String(45))  # IPv4 or IPv6
    device_info = Column(String(200))
    session_id = Column(String(100))
    notes = Column(Text)
    
    def __repr__(self):
        return f"<AuditLog(id={self.id}, action='{self.action}', entity='{self.entity_type}')>"
