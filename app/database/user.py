# Finovate Journal AI - User Model

"""
User model with role-based access control.
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
import bcrypt
from .base import Base


class UserRole(enum.Enum):
    """User roles for access control."""
    ADMINISTRATOR = "Administrator"
    ACCOUNTANT = "Accountant"
    REVIEWER = "Reviewer"
    VIEWER = "Viewer"


class User(Base):
    """User model with authentication and authorization."""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    
    full_name_ar = Column(String(255), nullable=False)
    full_name_en = Column(String(255), default="")
    phone = Column(String(20), default="")
    
    role = Column(SQLEnum(UserRole), default=UserRole.VIEWER)
    
    is_active = Column(Boolean, default=True)
    is_locked = Column(Boolean, default=False)
    failed_login_attempts = Column(Integer, default=0)
    last_login_at = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"
    
    @property
    def full_name(self) -> str:
        """Get full name based on context."""
        return self.full_name_ar or self.full_name_en
    
    def set_password(self, password: str):
        """Hash and set password."""
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def verify_password(self, password: str) -> bool:
        """Verify password against hash."""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def has_permission(self, required_role: UserRole) -> bool:
        """Check if user has required permission level."""
        role_hierarchy = {
            UserRole.VIEWER: 1,
            UserRole.REVIEWER: 2,
            UserRole.ACCOUNTANT: 3,
            UserRole.ADMINISTRATOR: 4
        }
        return role_hierarchy.get(self.role, 0) >= role_hierarchy.get(required_role, 0)
