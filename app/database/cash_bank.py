"""Cash and Bank Account models."""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Numeric, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from decimal import Decimal
import enum

from .base import Base


class AccountStatus(str, enum.Enum):
    """Account status enumeration."""

    ACTIVE = "active"
    INACTIVE = "inactive"
    CLOSED = "closed"


class CashAccount(Base):
    """Cash Account model for petty cash and cash boxes."""

    __tablename__ = "cash_accounts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False, index=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    name_ar = Column(String(200), nullable=False)
    name_en = Column(String(200), nullable=True)
    currency = Column(String(3), default="EGP", nullable=False)
    opening_balance = Column(Numeric(15, 3), default=Decimal("0.00"), nullable=False)
    current_balance = Column(Numeric(15, 3), default=Decimal("0.00"), nullable=False)
    status = Column(SQLEnum(AccountStatus), default=AccountStatus.ACTIVE, nullable=False)
    location = Column(String(200), nullable=True)
    responsible_person = Column(String(100), nullable=True)
    max_balance = Column(Numeric(15, 3), nullable=True)
    min_balance = Column(Numeric(15, 3), nullable=True)
    notes = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    company = relationship("Company", back_populates="cash_accounts")

    def __repr__(self) -> str:
        return f"<CashAccount(id={self.id}, code='{self.code}', name='{self.name_ar}')>"


class BankAccount(Base):
    """Bank Account model for bank accounts."""

    __tablename__ = "bank_accounts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False, index=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    name_ar = Column(String(200), nullable=False)
    name_en = Column(String(200), nullable=True)
    bank_name = Column(String(200), nullable=False)
    branch_name = Column(String(200), nullable=True)
    account_number = Column(String(50), nullable=False)
    iban = Column(String(34), nullable=True)
    swift_code = Column(String(11), nullable=True)
    currency = Column(String(3), default="EGP", nullable=False)
    opening_balance = Column(Numeric(15, 3), default=Decimal("0.00"), nullable=False)
    current_balance = Column(Numeric(15, 3), default=Decimal("0.00"), nullable=False)
    status = Column(SQLEnum(AccountStatus), default=AccountStatus.ACTIVE, nullable=False)
    account_type = Column(String(50), nullable=True)  # Current, Savings, etc.
    check_book_number = Column(String(50), nullable=True)
    last_check_number = Column(Integer, nullable=True)
    notes = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    company = relationship("Company", back_populates="bank_accounts")

    def __repr__(self) -> str:
        return f"<BankAccount(id={self.id}, code='{self.code}', bank='{self.bank_name}')>"
