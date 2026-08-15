"""Account and AccountGroup models for Chart of Accounts."""

from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Enum as SQLEnum, Numeric, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from decimal import Decimal
import enum

from .base import Base


class AccountType(str, enum.Enum):
    """Account type enumeration."""

    ASSET = "asset"
    LIABILITY = "liability"
    EQUITY = "equity"
    REVENUE = "revenue"
    EXPENSE = "expense"


class NormalBalance(str, enum.Enum):
    """Normal balance side."""

    DEBIT = "debit"
    CREDIT = "credit"


class AccountGroup(Base):
    """Account Group model for hierarchical structure."""

    __tablename__ = "account_groups"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False, index=True)
    parent_id = Column(Integer, ForeignKey("account_groups.id"), nullable=True)
    code = Column(String(20), nullable=False)
    name_ar = Column(String(200), nullable=False)
    name_en = Column(String(200), nullable=True)
    description = Column(Text, nullable=True)
    level = Column(Integer, default=1, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    company = relationship("Company", back_populates="accounts")
    parent = relationship("AccountGroup", remote_side=[id], backref="children")
    accounts = relationship("Account", back_populates="group", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<AccountGroup(id={self.id}, code='{self.code}', name='{self.name_ar}')>"


class AccountType(str, enum.Enum):
    """Account type enumeration."""

    ASSET = "asset"
    LIABILITY = "liability"
    EQUITY = "equity"
    REVENUE = "revenue"
    EXPENSE = "expense"


class NormalBalance(str, enum.Enum):
    """Normal balance side."""

    DEBIT = "debit"
    CREDIT = "credit"


class Account(Base):
    """Account model for Chart of Accounts."""

    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False, index=True)
    group_id = Column(Integer, ForeignKey("account_groups.id"), nullable=True)
    code = Column(String(20), unique=True, nullable=False, index=True)
    name_ar = Column(String(200), nullable=False)
    name_en = Column(String(200), nullable=True)
    account_type = Column(SQLEnum(AccountType), nullable=False)
    normal_balance = Column(SQLEnum(NormalBalance), nullable=False)
    parent_id = Column(Integer, ForeignKey("accounts.id"), nullable=True)
    level = Column(Integer, default=1, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_tax_account = Column(Boolean, default=False, nullable=False)
    tax_rate = Column(Numeric(10, 3), default=Decimal("0.00"))
    currency = Column(String(3), default="EGP", nullable=False)
    opening_balance = Column(Numeric(15, 3), default=Decimal("0.00"))
    current_balance = Column(Numeric(15, 3), default=Decimal("0.00"))
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    company = relationship("Company", back_populates="accounts")
    group = relationship("AccountGroup", back_populates="accounts")
    parent = relationship("Account", remote_side=[id], backref="children")
    journal_lines = relationship("JournalLine", back_populates="account")

    def __repr__(self) -> str:
        return f"<Account(id={self.id}, code='{self.code}', name='{self.name_ar}')>"

    @property
    def full_code(self) -> str:
        """Get full hierarchical code."""
        if self.parent:
            return f"{self.parent.full_code}.{self.code}"
        return self.code
