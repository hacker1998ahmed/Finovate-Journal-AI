"""
Finovate Journal AI - Cash and Bank Account Models
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime
from decimal import Decimal

from app.database.base import Base


class CashAccount(Base):
    """Cash Account model for petty cash and cash boxes"""
    __tablename__ = "cash_accounts"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    code = Column(String(20), nullable=False)
    name = Column(String(100), nullable=False)
    name_ar = Column(String(100))  # Arabic name
    name_en = Column(String(100))  # English name
    account_id = Column(Integer, ForeignKey("accounts.id"))  # Linked GL account
    opening_balance = Column(Numeric(19, 4), default=Decimal("0.00"))
    current_balance = Column(Numeric(19, 4), default=Decimal("0.00"))
    currency = Column(String(3), default="EGP")
    location = Column(String(200))  # Physical location
    custodian = Column(String(100))  # Person responsible
    max_balance = Column(Numeric(19, 4))  # Maximum allowed balance
    notes = Column(Text)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    company = relationship("Company", back_populates="cash_accounts")
    account = relationship("Account")
    
    def __repr__(self):
        return f"<CashAccount(id={self.id}, code='{self.code}', name='{self.name}')>"


class BankAccount(Base):
    """Bank Account model"""
    __tablename__ = "bank_accounts"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    code = Column(String(20), nullable=False)
    name = Column(String(100), nullable=False)
    name_ar = Column(String(100))  # Arabic name
    name_en = Column(String(100))  # English name
    account_id = Column(Integer, ForeignKey("accounts.id"))  # Linked GL account
    bank_name = Column(String(200))
    branch_name = Column(String(200))
    account_number = Column(String(50))
    iban = Column(String(34))  # International Bank Account Number
    swift_code = Column(String(11))
    opening_balance = Column(Numeric(19, 4), default=Decimal("0.00"))
    current_balance = Column(Numeric(19, 4), default=Decimal("0.00"))
    currency = Column(String(3), default="EGP")
    account_type = Column(String(50))  # Current, Savings, etc.
    notes = Column(Text)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    company = relationship("Company", back_populates="bank_accounts")
    account = relationship("Account")
    
    def __repr__(self):
        return f"<BankAccount(id={self.id}, code='{self.code}', name='{self.name}')>"
