# Finovate Journal AI - Account Models

"""
Chart of Accounts models: AccountGroup and Account.
Supports hierarchical account structure with multi-language names.
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, Numeric, ForeignKey, Enum as SQLEnum, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from decimal import Decimal
import enum
from .base import Base


class AccountType(enum.Enum):
    """Account types for classification."""
    ASSET = "Asset"
    LIABILITY = "Liability"
    EQUITY = "Equity"
    REVENUE = "Revenue"
    EXPENSE = "Expense"


class NormalBalance(enum.Enum):
    """Normal balance side for accounts."""
    DEBIT = "Debit"
    CREDIT = "Credit"


class AccountGroup(Base):
    """Account Group model for hierarchical structure."""
    
    __tablename__ = "account_groups"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    parent_id = Column(Integer, ForeignKey("account_groups.id"), nullable=True)
    
    code = Column(String(20), nullable=False)  # e.g., "1", "11", "1101"
    name_ar = Column(String(255), nullable=False)  # Arabic name
    name_en = Column(String(255), nullable=False)  # English name
    description_ar = Column(Text, default="")
    description_en = Column(Text, default="")
    
    account_type = Column(SQLEnum(AccountType), nullable=False)
    level = Column(Integer, default=1)  # Hierarchy level (1=root, 2=child, etc.)
    
    is_active = Column(Boolean, default=True)
    is_system = Column(Boolean, default=False)  # System accounts cannot be deleted
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    company = relationship("Company", back_populates="account_groups")
    parent = relationship("AccountGroup", remote_side=[id], backref="children")
    accounts = relationship("Account", back_populates="group", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<AccountGroup(id={self.id}, code='{self.code}', name='{self.name_ar}')>"
    
    def get_full_path(self, language: str = "ar") -> str:
        """Get full hierarchical path of the group."""
        path = []
        current = self
        while current:
            name = current.name_ar if language == "ar" else current.name_en
            path.insert(0, name)
            current = current.parent
        return " > ".join(path)


class Account(Base):
    """Account model for individual accounts."""
    
    __tablename__ = "accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("account_groups.id"), nullable=False)
    
    code = Column(String(20), unique=True, nullable=False, index=True)  # Full account code
    name_ar = Column(String(255), nullable=False)  # Arabic name
    name_en = Column(String(255), nullable=False)  # English name
    description_ar = Column(Text, default="")
    description_en = Column(Text, default="")
    
    account_type = Column(SQLEnum(AccountType), nullable=False)
    normal_balance = Column(SQLEnum(NormalBalance), nullable=False)
    
    # Tax settings
    is_taxable = Column(Boolean, default=False)
    tax_id = Column(Integer, ForeignKey("taxes.id"), nullable=True)
    
    # Additional settings
    is_bank_account = Column(Boolean, default=False)
    is_cash_account = Column(Boolean, default=False)
    currency = Column(String(3), default="EGP")
    
    opening_balance = Column(Numeric(20, 6), default=Decimal("0.00"))
    current_balance = Column(Numeric(20, 6), default=Decimal("0.00"))
    
    is_active = Column(Boolean, default=True)
    is_system = Column(Boolean, default=False)  # System accounts cannot be deleted
    
    notes = Column(Text, default="")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    group = relationship("AccountGroup", back_populates="accounts")
    tax = relationship("Tax", backref="accounts")
    journal_lines = relationship("JournalLine", back_populates="account")
    
    def __repr__(self):
        return f"<Account(id={self.id}, code='{self.code}', name='{self.name_ar}')>"
    
    @property
    def name(self) -> str:
        """Get account name based on current context (default Arabic)."""
        return self.name_ar
    
    @property
    def display_name(self) -> str:
        """Get formatted display name with code."""
        return f"{self.code} - {self.name_ar}"
    
    def get_balance_direction(self) -> str:
        """Get the direction of balance increase."""
        if self.normal_balance == NormalBalance.DEBIT:
            return "debit"
        return "credit"
