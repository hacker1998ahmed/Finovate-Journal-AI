"""
Finovate Journal AI - Customer and Supplier Models
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime
from decimal import Decimal

from app.database.base import Base


class Customer(Base):
    """Customer model for Accounts Receivable"""
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    code = Column(String(20), nullable=False)  # Customer code
    name = Column(String(200), nullable=False)
    name_ar = Column(String(200))  # Arabic name
    name_en = Column(String(200))  # English name
    tax_number = Column(String(50))
    national_id = Column(String(20))
    phone = Column(String(20))
    mobile = Column(String(20))
    email = Column(String(100))
    address = Column(Text)
    city = Column(String(100))
    country = Column(String(100), default="Egypt")
    opening_balance = Column(Numeric(19, 4), default=Decimal("0.00"))
    current_balance = Column(Numeric(19, 4), default=Decimal("0.00"))
    credit_limit = Column(Numeric(19, 4))
    payment_terms = Column(String(100))  # e.g., "Net 30"
    account_id = Column(Integer, ForeignKey("accounts.id"))  # Control account
    notes = Column(Text)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    company = relationship("Company", back_populates="customers")
    account = relationship("Account")
    journal_lines = relationship("JournalLine", back_populates="customer")
    
    def __repr__(self):
        return f"<Customer(id={self.id}, code='{self.code}', name='{self.name}')>"


class Supplier(Base):
    """Supplier model for Accounts Payable"""
    __tablename__ = "suppliers"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    code = Column(String(20), nullable=False)  # Supplier code
    name = Column(String(200), nullable=False)
    name_ar = Column(String(200))  # Arabic name
    name_en = Column(String(200))  # English name
    tax_number = Column(String(50))
    commercial_registration = Column(String(50))
    phone = Column(String(20))
    mobile = Column(String(20))
    email = Column(String(100))
    address = Column(Text)
    city = Column(String(100))
    country = Column(String(100), default="Egypt")
    opening_balance = Column(Numeric(19, 4), default=Decimal("0.00"))
    current_balance = Column(Numeric(19, 4), default=Decimal("0.00"))
    credit_limit = Column(Numeric(19, 4))
    payment_terms = Column(String(100))  # e.g., "Net 30"
    account_id = Column(Integer, ForeignKey("accounts.id"))  # Control account
    notes = Column(Text)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    company = relationship("Company", back_populates="suppliers")
    account = relationship("Account")
    journal_lines = relationship("JournalLine", back_populates="supplier")
    
    def __repr__(self):
        return f"<Supplier(id={self.id}, code='{self.code}', name='{self.name}')>"
