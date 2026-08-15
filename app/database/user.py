"""User model for authentication and authorization."""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
import hashlib

from .base import Base


class UserRole(str, enum.Enum):
    """User role enumeration."""

    ADMIN = "admin"
    ACCOUNTANT = "accountant"
    REVIEWER = "reviewer"
    VIEWER = "viewer"


class User(Base):
    """User model for authentication."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=True)
    role = Column(SQLEnum(UserRole), default=UserRole.VIEWER, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_login = Column(DateTime, nullable=True)
    company_id = Column(Integer, nullable=True)  # Link to company if multi-user

    # Relationships
    audit_logs = relationship("AuditLog", back_populates="user")
    journal_entries = relationship("JournalEntry", foreign_keys="JournalEntry.created_by", back_populates="created_by_user")
    reviewed_entries = relationship("JournalEntry", foreign_keys="JournalEntry.reviewed_by")
    posted_entries = relationship("JournalEntry", foreign_keys="JournalEntry.posted_by")

    def set_password(self, password: str) -> None:
        """Hash and set the user's password."""
        # Simple hash - in production use bcrypt or argon2
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password: str) -> bool:
        """Verify the password against the hash."""
        return self.password_hash == hashlib.sha256(password.encode()).hexdigest()

    def has_permission(self, required_role: str) -> bool:
        """Check if user has required permission level."""
        role_hierarchy = {
            "viewer": 1,
            "reviewer": 2,
            "accountant": 3,
            "admin": 4,
        }
        user_level = role_hierarchy.get(self.role.value, 0)
        required_level = role_hierarchy.get(required_role, 0)
        return user_level >= required_level

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username='{self.username}', role='{self.role.value}')>"
