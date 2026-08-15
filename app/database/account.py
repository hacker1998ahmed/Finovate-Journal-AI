"""
Finovate Journal AI - Account Models (Chart of Accounts)

Developer: Ahmed Mostafa Ibrahim
Brand: Finovate – AHMED EG
"""

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, Numeric, CheckConstraint, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from decimal import Decimal

from .base import Base


class AccountGroup(Base):
    """Account Group for hierarchical organization."""

    __tablename__ = "account_groups"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    name_ar = Column(String(100), nullable=False)
    name_en = Column(String(100), nullable=False)
    code = Column(String(20), nullable=False)
    parent_id = Column(Integer, ForeignKey("account_groups.id"), nullable=True)
    level = Column(Integer, default=1)
    account_type = Column(String(20), nullable=False)  # asset, liability, equity, revenue, expense
    normal_balance = Column(String(10), nullable=False)  # debit or credit
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    company = relationship("Company")
    parent = relationship("AccountGroup", remote_side=[id], backref="children")
    accounts = relationship("Account", back_populates="group", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<AccountGroup(id={self.id}, code='{self.code}', name_ar='{self.name_ar}')>"


class Account(Base):
    """Account model for Chart of Accounts."""

    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    group_id = Column(Integer, ForeignKey("account_groups.id"), nullable=True)
    
    # Account identification
    code = Column(String(20), nullable=False, index=True)
    name_ar = Column(String(200), nullable=False)
    name_en = Column(String(200), nullable=False)
    
    # Account type and balance
    account_type = Column(String(20), nullable=False)  # asset, liability, equity, revenue, expense
    normal_balance = Column(String(10), nullable=False, default="debit")  # debit or credit
    
    # Hierarchy
    parent_id = Column(Integer, ForeignKey("accounts.id"), nullable=True)
    level = Column(Integer, default=1)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_system = Column(Boolean, default=False)  # System accounts cannot be deleted
    
    # Tax settings
    is_tax_account = Column(Boolean, default=False)
    tax_rate = Column(Numeric(10, 3), nullable=True)
    
    # Additional info
    description = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    
    # Opening balance
    opening_balance = Column(Numeric(20, 3), default=Decimal("0.00"))
    opening_balance_date = Column(DateTime, nullable=True)
    
    # Current balance (calculated)
    current_balance = Column(Numeric(20, 3), default=Decimal("0.00"))
    last_transaction_date = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Constraints
    __table_args__ = (
        CheckConstraint("account_type IN ('asset', 'liability', 'equity', 'revenue', 'expense')", name="chk_account_type"),
        CheckConstraint("normal_balance IN ('debit', 'credit')", name="chk_normal_balance"),
    )
    
    # Relationships
    company = relationship("Company")
    group = relationship("AccountGroup", back_populates="accounts")
    parent = relationship("Account", remote_side=[id], backref="children")
    journal_lines = relationship("JournalLine", back_populates="account")

    def __repr__(self):
        return f"<Account(id={self.id}, code='{self.code}', name_ar='{self.name_ar}')>"

    def to_dict(self):
        """Convert account to dictionary."""
        return {
            "id": self.id,
            "company_id": self.company_id,
            "code": self.code,
            "name_ar": self.name_ar,
            "name_en": self.name_en,
            "account_type": self.account_type,
            "normal_balance": self.normal_balance,
            "parent_id": self.parent_id,
            "level": self.level,
            "is_active": self.is_active,
            "is_system": self.is_system,
            "opening_balance": str(self.opening_balance) if self.opening_balance else "0.00",
            "current_balance": str(self.current_balance) if self.current_balance else "0.00",
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
