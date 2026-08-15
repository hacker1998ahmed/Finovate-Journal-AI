"""
Finovate Journal AI - Company and Fiscal Year Models

Developer: Ahmed Mostafa Ibrahim
Brand: Finovate – AHMED EG
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from .base import Base


class Company(Base):
    """Company model for multi-company support."""

    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    code = Column(String(50), unique=True, nullable=False, index=True)
    address = Column(Text, nullable=True)
    tax_number = Column(String(50), nullable=True)
    phone = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    
    # Settings
    currency = Column(String(3), default="EGP")
    language = Column(String(2), default="ar")
    fiscal_year_start_month = Column(Integer, default=1)
    fiscal_year_start_day = Column(Integer, default=1)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
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

    def __repr__(self):
        return f"<Company(id={self.id}, code='{self.code}', name='{self.name}')>"

    def to_dict(self):
        """Convert company to dictionary."""
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "address": self.address,
            "tax_number": self.tax_number,
            "phone": self.phone,
            "email": self.email,
            "currency": self.currency,
            "language": self.language,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class FiscalYear(Base):
    """Fiscal Year model."""

    __tablename__ = "fiscal_years"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    year = Column(Integer, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    
    # Status
    is_open = Column(Boolean, default=True)
    is_closed = Column(Boolean, default=False)
    closed_at = Column(DateTime, nullable=True)
    closed_by = Column(String(50), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    company = relationship("Company", back_populates="fiscal_years")

    def __repr__(self):
        return f"<FiscalYear(id={self.id}, year={self.year}, company_id={self.company_id})>"

    def to_dict(self):
        """Convert fiscal year to dictionary."""
        return {
            "id": self.id,
            "company_id": self.company_id,
            "year": self.year,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "is_open": self.is_open,
            "is_closed": self.is_closed,
            "closed_at": self.closed_at.isoformat() if self.closed_at else None,
            "closed_by": self.closed_by,
        }
