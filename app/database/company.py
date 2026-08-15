"""Company and Fiscal Year models."""

from sqlalchemy import Column, Integer, String, Text, Date, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, date

from .base import Base


class Company(Base):
    """Company model for multi-company support."""

    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    code = Column(String(50), unique=True, nullable=False, index=True)
    address = Column(Text, nullable=True)
    tax_number = Column(String(50), nullable=True)
    commercial_registration = Column(String(100), nullable=True)
    phone = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    logo_path = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    fiscal_years = relationship("FiscalYear", back_populates="company", cascade="all, delete-orphan")
    accounts = relationship("Account", back_populates="company", cascade="all, delete-orphan")
    journal_entries = relationship("JournalEntry", back_populates="company", cascade="all, delete-orphan")
    customers = relationship("Customer", back_populates="company", cascade="all, delete-orphan")
    suppliers = relationship("Supplier", back_populates="company", cascade="all, delete-orphan")
    cash_accounts = relationship("CashAccount", back_populates="company", cascade="all, delete-orphan")
    bank_accounts = relationship("BankAccount", back_populates="company", cascade="all, delete-orphan")
    taxes = relationship("Tax", back_populates="company", cascade="all, delete-orphan")
    cost_centers = relationship("CostCenter", back_populates="company", cascade="all, delete-orphan")
    projects = relationship("Project", back_populates="company", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Company(id={self.id}, name='{self.name}', code='{self.code}')>"


class FiscalYear(Base):
    """Fiscal Year model for accounting periods."""

    __tablename__ = "fiscal_years"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False, index=True)
    name = Column(String(50), nullable=False)  # e.g., "2025"
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    is_open = Column(Boolean, default=True, nullable=False)
    is_closed = Column(Boolean, default=False, nullable=False)
    closing_date = Column(Date, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    company = relationship("Company", back_populates="fiscal_years")

    def __repr__(self) -> str:
        return f"<FiscalYear(id={self.id}, name='{self.name}', company_id={self.company_id})>"

    @property
    def can_post(self) -> bool:
        """Check if entries can be posted in this fiscal year."""
        return self.is_open and not self.is_closed
