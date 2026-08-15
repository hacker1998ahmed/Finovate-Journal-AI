"""
Finovate Journal AI - User Model
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from datetime import datetime

from app.database.base import Base


class User(Base):
    """User model for authentication and authorization"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(200))
    full_name_ar = Column(String(200))  # Arabic name
    phone = Column(String(20))
    role = Column(String(50), default="Accountant")  # Administrator, Accountant, Reviewer, Viewer
    department = Column(String(100))
    active = Column(Boolean, default=True)
    last_login = Column(DateTime)
    failed_login_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime)
    must_change_password = Column(Boolean, default=False)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"
