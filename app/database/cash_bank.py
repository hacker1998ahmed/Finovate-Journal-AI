"""
Finovate Journal AI - Cash and Bank Account Models

Developer: Ahmed Mostafa Ibrahim
Brand: Finovate – AHMED EG
"""

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, Numeric, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from decimal import Decimal

from .base import Base


class CashAccount(Base):
    """Cash Account model (Petty Cash, Safe, etc.)."""

    __tablename__ = "cash_accounts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    
    # Account identification
    code = Column(String(50), unique=True, nullable=False, index=True)
    name_ar = Column(String(200), nullable=False)
    name_en = Column(String(200), nullable=False)
    
    # Financial
    opening_balance = Column(Numeric(20, 3), default=Decimal("0.00"))
    current_balance = Column(Numeric(20, 3), default=Decimal("0.00"))
    
    # Status
    is_active = Column(Boolean, default=True)
    is_default = Column(Boolean, default=False)
    
    # Additional info
    description = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    company = relationship("Company", back_populates="cash_accounts")

    def __repr__(self):
        return f"<CashAccount(id={self.id}, code='{self.code}', name_ar='{self.name_ar}')>"

    def to_dict(self):
        """Convert cash account to dictionary."""
        return {
            "id": self.id,
            "company_id": self.company_id,
            "code": self.code,
            "name_ar": self.name_ar,
            "name_en": self.name_en,
            "opening_balance": str(self.opening_balance) if self.opening_balance else "0.00",
            "current_balance": str(self.current_balance) if self.current_balance else "0.00",
            "is_active": self.is_active,
            "is_default": self.is_default,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class BankAccount(Base):
    """Bank Account model."""

    __tablename__ = "bank_accounts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    
    # Account identification
    code = Column(String(50), unique=True, nullable=False, index=True)
    name_ar = Column(String(200), nullable=False)
    name_en = Column(String(200), nullable=False)
    
    # Bank details
    bank_name = Column(String(200), nullable=True)
    branch_name = Column(String(200), nullable=True)
    account_number = Column(String(50), nullable=True)
    iban = Column(String(34), nullable=True)
    swift_code = Column(String(11), nullable=True)
    currency = Column(String(3), default="EGP")
    
    # Financial
    opening_balance = Column(Numeric(20, 3), default=Decimal("0.00"))
    current_balance = Column(Numeric(20, 3), default=Decimal("0.00"))
    
    # Status
    is_active = Column(Boolean, default=True)
    is_default = Column(Boolean, default=False)
    
    # Additional info
    description = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    company = relationship("Company", back_populates="bank_accounts")

    def __repr__(self):
        return f"<BankAccount(id={self.id}, code='{self.code}', name_ar='{self.name_ar}')>"

    def to_dict(self):
        """Convert bank account to dictionary."""
        return {
            "id": self.id,
            "company_id": self.company_id,
            "code": self.code,
            "name_ar": self.name_ar,
            "name_en": self.name_en,
            "bank_name": self.bank_name,
            "branch_name": self.branch_name,
            "account_number": self.account_number,
            "iban": self.iban,
            "currency": self.currency,
            "opening_balance": str(self.opening_balance) if self.opening_balance else "0.00",
            "current_balance": str(self.current_balance) if self.current_balance else "0.00",
            "is_active": self.is_active,
            "is_default": self.is_default,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
