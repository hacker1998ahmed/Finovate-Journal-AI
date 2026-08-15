"""
Finovate Journal AI - Company and Fiscal Year Models
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from decimal import Decimal

from app.database.base import Base


class Company(Base):
    """Company model for multi-company support"""
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    name_ar = Column(String(200))  # Arabic name
    name_en = Column(String(200))  # English name
    tax_number = Column(String(50))
    commercial_registration = Column(String(50))
    address = Column(Text)
    phone = Column(String(20))
    email = Column(String(100))
    logo_path = Column(String(500))
    currency = Column(String(3), default="EGP")
    currency_symbol = Column(String(10), default="ج.م")
    language = Column(String(2), default="ar")  # ar or en
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    fiscal_years = relationship("FiscalYear", back_populates="company", cascade="all, delete-orphan")
    accounts = relationship("Account", back_populates="company", cascade="all, delete-orphan")
    journal_entries = relationship("JournalEntry", back_populates="company", cascade="all, delete-orphan")
    customers = relationship("Customer", back_populates="company", cascade="all, delete-orphan")
    suppliers = relationship("Supplier", back_populates="company", cascade="all, delete-orphan")
    cash_accounts = relationship("CashAccount", back_populates="company", cascade="all, delete-orphan")
    bank_accounts = relationship("BankAccount", back_populates="company", cascade="all, delete-orphan")
    taxes = relationship("Tax", back_populates="company", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Company(id={self.id}, name='{self.name}')>"


class FiscalYear(Base):
    """Fiscal Year model"""
    __tablename__ = "fiscal_years"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    name = Column(String(100), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    is_open = Column(Boolean, default=False)  # Whether year is open for posting
    is_closed = Column(Boolean, default=False)  # Whether year is closed
    closing_date = Column(DateTime)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    company = relationship("Company", back_populates="fiscal_years")
    
    def __repr__(self):
        return f"<FiscalYear(id={self.id}, name='{self.name}')>"
