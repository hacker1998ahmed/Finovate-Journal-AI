"""
Finovate Journal AI - Account and Account Group Models
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime
from decimal import Decimal

from app.database.base import Base


class AccountGroup(Base):
    """Account Group for hierarchical chart of accounts"""
    __tablename__ = "account_groups"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    name = Column(String(100), nullable=False)
    name_ar = Column(String(100))  # Arabic name
    name_en = Column(String(100))  # English name
    code = Column(String(20))  # Group code
    parent_id = Column(Integer, ForeignKey("account_groups.id"))
    level = Column(Integer, default=1)  # Hierarchy level
    account_type = Column(String(50))  # Asset, Liability, Equity, Revenue, Expense
    normal_balance = Column(String(10))  # Debit or Credit
    description = Column(Text)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    company = relationship("Company")
    parent = relationship("AccountGroup", remote_side=[id], backref="children")
    accounts = relationship("Account", back_populates="group", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<AccountGroup(id={self.id}, name='{self.name}')>"


class Account(Base):
    """Account model for Chart of Accounts"""
    __tablename__ = "accounts"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    group_id = Column(Integer, ForeignKey("account_groups.id"))
    code = Column(String(20), nullable=False)  # Account code
    name = Column(String(200), nullable=False)
    name_ar = Column(String(200))  # Arabic name
    name_en = Column(String(200))  # English name
    account_type = Column(String(50), nullable=False)  # Asset, Liability, Equity, Revenue, Expense
    parent_id = Column(Integer, ForeignKey("accounts.id"))  # For sub-accounts
    level = Column(Integer, default=1)
    normal_balance = Column(String(10), default="Debit")  # Debit or Credit
    opening_balance = Column(Numeric(19, 4), default=Decimal("0.00"))
    current_balance = Column(Numeric(19, 4), default=Decimal("0.00"))
    is_bank_account = Column(Boolean, default=False)
    is_cash_account = Column(Boolean, default=False)
    is_control_account = Column(Boolean, default=False)  # Control account for sub-ledgers
    tax_account = Column(Boolean, default=False)  # Is this a tax account?
    tax_type = Column(String(20))  # Input VAT, Output VAT
    currency = Column(String(3), default="EGP")
    description = Column(Text)
    notes = Column(Text)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    company = relationship("Company", back_populates="accounts")
    group = relationship("AccountGroup", back_populates="accounts")
    parent = relationship("Account", remote_side=[id], backref="children")
    journal_lines = relationship("JournalLine", back_populates="account")
    
    def __repr__(self):
        return f"<Account(id={self.id}, code='{self.code}', name='{self.name}')>"
    
    @property
    def full_name(self) -> str:
        """Get full account name with code"""
        return f"{self.code} - {self.name}"
