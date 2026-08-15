# Finovate Journal AI - Company Model

"""
Company model for multi-company support.
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base


class Company(Base):
    """Company model for multi-company support."""
    
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    address = Column(Text, default="")
    tax_number = Column(String(50), default="")
    phone = Column(String(20), default="")
    email = Column(String(100), default="")
    logo_path = Column(String(500), default="")
    
    # Settings
    currency = Column(String(3), default="EGP")
    language = Column(String(2), default="ar")
    fiscal_year_start_month = Column(Integer, default=1)  # January
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    fiscal_years = relationship("FiscalYear", back_populates="company", cascade="all, delete-orphan")
    account_groups = relationship("AccountGroup", back_populates="company", cascade="all, delete-orphan")
    journal_entries = relationship("JournalEntry", back_populates="company", cascade="all, delete-orphan")
    customers = relationship("Customer", back_populates="company", cascade="all, delete-orphan")
    suppliers = relationship("Supplier", back_populates="company", cascade="all, delete-orphan")
    cash_accounts = relationship("CashAccount", back_populates="company", cascade="all, delete-orphan")
    bank_accounts = relationship("BankAccount", back_populates="company", cascade="all, delete-orphan")
    taxes = relationship("Tax", back_populates="company", cascade="all, delete-orphan")
    cost_centers = relationship("CostCenter", back_populates="company", cascade="all, delete-orphan")
    projects = relationship("Project", back_populates="company", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Company(id={self.id}, name='{self.name}', code='{self.code}')>"
    
    @property
    def display_name(self) -> str:
        """Get company display name."""
        return f"{self.name} ({self.code})"
