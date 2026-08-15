"""
Database Models - SQLAlchemy ORM Classes
"""
from sqlalchemy import (
    Column, Integer, String, Text, Float, DateTime, Boolean, 
    ForeignKey, Enum, DECIMAL, UniqueConstraint, Index, Date
)
from sqlalchemy.orm import relationship
from datetime import datetime
from decimal import Decimal
import enum

from . import Base


# ============== Enums ==============

class AccountType(enum.Enum):
    """Account types for chart of accounts."""
    ASSET = "asset"
    LIABILITY = "liability"
    EQUITY = "equity"
    REVENUE = "revenue"
    EXPENSE = "expense"


class NormalBalance(enum.Enum):
    """Normal balance side for accounts."""
    DEBIT = "debit"
    CREDIT = "credit"


class JournalStatus(enum.Enum):
    """Journal entry status."""
    DRAFT = "draft"
    REVIEWED = "reviewed"
    POSTED = "posted"
    CANCELLED = "cancelled"


class UserRole(enum.Enum):
    """User roles for access control."""
    ADMIN = "admin"
    ACCOUNTANT = "accountant"
    REVIEWER = "reviewer"
    VIEWER = "viewer"


class Currency(enum.Enum):
    """Supported currencies."""
    EGP = "EGP"
    USD = "USD"
    EUR = "EUR"
    SAR = "SAR"
    AED = "AED"
    GBP = "GBP"


# ============== Core Models ==============

class Company(Base):
    """Company entity for multi-company support."""
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    name_ar = Column(String(200))
    tax_number = Column(String(50))
    commercial_registration = Column(String(50))
    address = Column(Text)
    phone = Column(String(20))
    email = Column(String(100))
    logo_path = Column(String(500))
    currency = Column(Enum(Currency), default=Currency.EGP)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    fiscal_years = relationship("FiscalYear", back_populates="company", cascade="all, delete-orphan")
    accounts = relationship("Account", back_populates="company", cascade="all, delete-orphan")
    journal_entries = relationship("JournalEntry", back_populates="company")
    customers = relationship("Customer", back_populates="company", cascade="all, delete-orphan")
    suppliers = relationship("Supplier", back_populates="company", cascade="all, delete-orphan")
    cash_accounts = relationship("CashAccount", back_populates="company", cascade="all, delete-orphan")
    bank_accounts = relationship("BankAccount", back_populates="company", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index('ix_companies_name', 'name'),
        Index('ix_companies_tax_number', 'tax_number'),
    )


class FiscalYear(Base):
    """Fiscal year definition."""
    __tablename__ = "fiscal_years"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    name = Column(String(50), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    is_open = Column(Boolean, default=True)
    is_closed = Column(Boolean, default=False)
    closed_at = Column(DateTime)
    closed_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    company = relationship("Company", back_populates="fiscal_years")
    journal_entries = relationship("JournalEntry", back_populates="fiscal_year")
    
    __table_args__ = (
        UniqueConstraint('company_id', 'start_date', 'end_date', name='uq_fiscal_year_dates'),
        Index('ix_fiscal_years_company', 'company_id'),
        Index('ix_fiscal_years_dates', 'start_date', 'end_date'),
    )


class User(Base):
    """System users with role-based access."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100))
    phone = Column(String(20))
    role = Column(Enum(UserRole), default=UserRole.VIEWER)
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime)
    failed_login_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    journal_entries = relationship("JournalEntry", back_populates="created_by_user")
    
    __table_args__ = (
        Index('ix_users_username', 'username'),
        Index('ix_users_role', 'role'),
    )


# ============== Accounting Models ==============

class AccountGroup(Base):
    """Account groups for hierarchical structure."""
    __tablename__ = "account_groups"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(20), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    name_ar = Column(String(100))
    parent_id = Column(Integer, ForeignKey("account_groups.id"))
    level = Column(Integer, default=1)
    account_type = Column(Enum(AccountType), nullable=False)
    normal_balance = Column(Enum(NormalBalance), default=NormalBalance.DEBIT)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    parent = relationship("AccountGroup", remote_side=[id], backref="children")
    accounts = relationship("Account", back_populates="group", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index('ix_account_groups_code', 'code'),
        Index('ix_account_groups_parent', 'parent_id'),
    )


class Account(Base):
    """Chart of accounts."""
    __tablename__ = "accounts"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    group_id = Column(Integer, ForeignKey("account_groups.id"))
    code = Column(String(20), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    name_ar = Column(String(100))
    account_type = Column(Enum(AccountType), nullable=False)
    normal_balance = Column(Enum(NormalBalance), default=NormalBalance.DEBIT)
    parent_id = Column(Integer, ForeignKey("accounts.id"))
    level = Column(Integer, default=1)
    is_active = Column(Boolean, default=True)
    is_control_account = Column(Boolean, default=False)
    tax_account_id = Column(Integer, ForeignKey("taxes.id"))
    opening_balance = Column(DECIMAL(20, 4), default=Decimal('0.0000'))
    current_balance = Column(DECIMAL(20, 4), default=Decimal('0.0000'))
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    company = relationship("Company", back_populates="accounts")
    group = relationship("AccountGroup", back_populates="accounts")
    parent = relationship("Account", remote_side=[id], backref="children")
    tax_account = relationship("Tax", back_populates="accounts")
    journal_lines = relationship("JournalLine", back_populates="account")
    
    __table_args__ = (
        UniqueConstraint('company_id', 'code', name='uq_account_company_code'),
        Index('ix_accounts_code', 'code'),
        Index('ix_accounts_company', 'company_id'),
        Index('ix_accounts_type', 'account_type'),
    )


class JournalEntry(Base):
    """Journal entry header."""
    __tablename__ = "journal_entries"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    fiscal_year_id = Column(Integer, ForeignKey("fiscal_years.id"))
    entry_number = Column(String(50), unique=True, nullable=False, index=True)
    entry_date = Column(Date, nullable=False, index=True)
    reference = Column(String(50))
    description = Column(Text, nullable=False)
    description_ar = Column(Text)
    status = Column(Enum(JournalStatus), default=JournalStatus.DRAFT)
    total_debit = Column(DECIMAL(20, 4), default=Decimal('0.0000'))
    total_credit = Column(DECIMAL(20, 4), default=Decimal('0.0000'))
    is_balanced = Column(Boolean, default=False)
    currency = Column(Enum(Currency), default=Currency.EGP)
    exchange_rate = Column(DECIMAL(18, 6), default=Decimal('1.000000'))
    cost_center_id = Column(Integer, ForeignKey("cost_centers.id"))
    project_id = Column(Integer, ForeignKey("projects.id"))
    source = Column(String(50))  # manual, smart_journal, ai, invoice, etc.
    attachment_path = Column(String(500))
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(Integer, ForeignKey("users.id"))
    reviewed_at = Column(DateTime)
    reviewed_by = Column(Integer, ForeignKey("users.id"))
    posted_at = Column(DateTime)
    posted_by = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    company = relationship("Company", back_populates="journal_entries")
    fiscal_year = relationship("FiscalYear", back_populates="journal_entries")
    created_by_user = relationship("User", foreign_keys=[created_by])
    reviewed_by_user = relationship("User", foreign_keys=[reviewed_by])
    posted_by_user = relationship("User", foreign_keys=[posted_by])
    lines = relationship("JournalLine", back_populates="entry", cascade="all, delete-orphan")
    cost_center = relationship("CostCenter", back_populates="journal_entries")
    project = relationship("Project", back_populates="journal_entries")
    
    __table_args__ = (
        Index('ix_journal_entries_date', 'entry_date'),
        Index('ix_journal_entries_status', 'status'),
        Index('ix_journal_entries_company', 'company_id'),
    )


class JournalLine(Base):
    """Journal entry lines (debit/credit)."""
    __tablename__ = "journal_lines"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    entry_id = Column(Integer, ForeignKey("journal_entries.id"), nullable=False)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    line_number = Column(Integer, nullable=False)
    description = Column(String(200))
    debit_amount = Column(DECIMAL(20, 4), default=Decimal('0.0000'))
    credit_amount = Column(DECIMAL(20, 4), default=Decimal('0.0000'))
    cost_center_id = Column(Integer, ForeignKey("cost_centers.id"))
    project_id = Column(Integer, ForeignKey("projects.id"))
    tax_id = Column(Integer, ForeignKey("taxes.id"))
    tax_amount = Column(DECIMAL(20, 4), default=Decimal('0.0000'))
    is_tax_inclusive = Column(Boolean, default=False)
    notes = Column(Text)
    
    # Relationships
    entry = relationship("JournalEntry", back_populates="lines")
    account = relationship("Account", back_populates="journal_lines")
    cost_center = relationship("CostCenter", back_populates="journal_lines")
    project = relationship("Project", back_populates="journal_lines")
    tax = relationship("Tax", back_populates="journal_lines")
    
    __table_args__ = (
        Index('ix_journal_lines_entry', 'entry_id'),
        Index('ix_journal_lines_account', 'account_id'),
    )


# ============== Party Models ==============

class Customer(Base):
    """Customer records."""
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    code = Column(String(20), unique=True, nullable=False, index=True)
    name = Column(String(200), nullable=False)
    name_ar = Column(String(200))
    tax_number = Column(String(50))
    national_id = Column(String(20))
    address = Column(Text)
    phone = Column(String(20))
    email = Column(String(100))
    opening_balance = Column(DECIMAL(20, 4), default=Decimal('0.0000'))
    current_balance = Column(DECIMAL(20, 4), default=Decimal('0.0000'))
    credit_limit = Column(DECIMAL(20, 4))
    is_active = Column(Boolean, default=True)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    company = relationship("Company", back_populates="customers")
    
    __table_args__ = (
        Index('ix_customers_company', 'company_id'),
        Index('ix_customers_name', 'name'),
    )


class Supplier(Base):
    """Supplier records."""
    __tablename__ = "suppliers"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    code = Column(String(20), unique=True, nullable=False, index=True)
    name = Column(String(200), nullable=False)
    name_ar = Column(String(200))
    tax_number = Column(String(50))
    national_id = Column(String(20))
    address = Column(Text)
    phone = Column(String(20))
    email = Column(String(100))
    opening_balance = Column(DECIMAL(20, 4), default=Decimal('0.0000'))
    current_balance = Column(DECIMAL(20, 4), default=Decimal('0.0000'))
    credit_limit = Column(DECIMAL(20, 4))
    is_active = Column(Boolean, default=True)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    company = relationship("Company", back_populates="suppliers")
    
    __table_args__ = (
        Index('ix_suppliers_company', 'company_id'),
        Index('ix_suppliers_name', 'name'),
    )


# ============== Cash & Bank Models ==============

class CashAccount(Base):
    """Cash accounts (petty cash, etc.)."""
    __tablename__ = "cash_accounts"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    code = Column(String(20), nullable=False)
    name = Column(String(100), nullable=False)
    name_ar = Column(String(100))
    currency = Column(Enum(Currency), default=Currency.EGP)
    opening_balance = Column(DECIMAL(20, 4), default=Decimal('0.0000'))
    current_balance = Column(DECIMAL(20, 4), default=Decimal('0.0000'))
    account_id = Column(Integer, ForeignKey("accounts.id"))
    is_active = Column(Boolean, default=True)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    company = relationship("Company", back_populates="cash_accounts")
    account = relationship("Account")
    
    __table_args__ = (
        UniqueConstraint('company_id', 'code', name='uq_cash_account_code'),
        Index('ix_cash_accounts_company', 'company_id'),
    )


class BankAccount(Base):
    """Bank accounts."""
    __tablename__ = "bank_accounts"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    code = Column(String(20), nullable=False)
    name = Column(String(100), nullable=False)
    name_ar = Column(String(100))
    bank_name = Column(String(100))
    account_number = Column(String(50))
    iban = Column(String(34))
    swift_code = Column(String(11))
    currency = Column(Enum(Currency), default=Currency.EGP)
    opening_balance = Column(DECIMAL(20, 4), default=Decimal('0.0000'))
    current_balance = Column(DECIMAL(20, 4), default=Decimal('0.0000'))
    account_id = Column(Integer, ForeignKey("accounts.id"))
    is_active = Column(Boolean, default=True)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    company = relationship("Company", back_populates="bank_accounts")
    account = relationship("Account")
    
    __table_args__ = (
        UniqueConstraint('company_id', 'code', name='uq_bank_account_code'),
        Index('ix_bank_accounts_company', 'company_id'),
    )


# ============== Tax Models ==============

class Tax(Base):
    """Tax configuration."""
    __tablename__ = "taxes"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    code = Column(String(20), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    name_ar = Column(String(100))
    rate = Column(DECIMAL(5, 2), nullable=False)  # e.g., 14.00 for 14%
    tax_type = Column(String(20))  # input, output, withholding, etc.
    is_active = Column(Boolean, default=True)
    effective_from = Column(Date)
    effective_to = Column(Date)
    input_account_id = Column(Integer, ForeignKey("accounts.id"))
    output_account_id = Column(Integer, ForeignKey("accounts.id"))
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    company = relationship("Company")
    accounts = relationship("Account", back_populates="tax_account")
    journal_lines = relationship("JournalLine", back_populates="tax")
    
    __table_args__ = (
        Index('ix_taxes_company', 'company_id'),
        Index('ix_taxes_code', 'code'),
    )


# ============== Cost Center & Project Models ==============

class CostCenter(Base):
    """Cost centers for tracking expenses."""
    __tablename__ = "cost_centers"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    code = Column(String(20), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    name_ar = Column(String(100))
    parent_id = Column(Integer, ForeignKey("cost_centers.id"))
    is_active = Column(Boolean, default=True)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    company = relationship("Company")
    parent = relationship("CostCenter", remote_side=[id], backref="children")
    journal_entries = relationship("JournalEntry", back_populates="cost_center")
    journal_lines = relationship("JournalLine", back_populates="cost_center")
    
    __table_args__ = (
        UniqueConstraint('company_id', 'code', name='uq_cost_center_code'),
        Index('ix_cost_centers_company', 'company_id'),
    )


class Project(Base):
    """Projects for project accounting."""
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    code = Column(String(20), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    name_ar = Column(String(100))
    customer_id = Column(Integer, ForeignKey("customers.id"))
    budget = Column(DECIMAL(20, 4))
    actual_cost = Column(DECIMAL(20, 4), default=Decimal('0.0000'))
    revenue = Column(DECIMAL(20, 4), default=Decimal('0.0000'))
    start_date = Column(Date)
    end_date = Column(Date)
    is_active = Column(Boolean, default=True)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    company = relationship("Company")
    customer = relationship("Customer")
    journal_entries = relationship("JournalEntry", back_populates="project")
    journal_lines = relationship("JournalLine", back_populates="project")
    
    __table_args__ = (
        UniqueConstraint('company_id', 'code', name='uq_project_code'),
        Index('ix_projects_company', 'company_id'),
    )


# ============== Audit & Settings Models ==============

class AuditLog(Base):
    """Audit trail for all important operations."""
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String(50), nullable=False, index=True)
    entity_type = Column(String(50), nullable=False)
    entity_id = Column(Integer)
    old_values = Column(Text)  # JSON
    new_values = Column(Text)  # JSON
    ip_address = Column(String(45))
    device_info = Column(String(200))
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    user = relationship("User")
    
    __table_args__ = (
        Index('ix_audit_logs_entity', 'entity_type', 'entity_id'),
        Index('ix_audit_logs_created', 'created_at'),
    )


class Setting(Base):
    """Application settings storage."""
    __tablename__ = "settings"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    key = Column(String(100), nullable=False)
    value = Column(Text)
    value_type = Column(String(20), default="string")
    category = Column(String(50))
    description = Column(Text)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_by = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    company = relationship("Company")
    updated_by_user = relationship("User")
    
    __table_args__ = (
        UniqueConstraint('company_id', 'key', name='uq_setting_company_key'),
        Index('ix_settings_company', 'company_id'),
        Index('ix_settings_key', 'key'),
    )


# Export all models
__all__ = [
    # Enums
    "AccountType",
    "NormalBalance",
    "JournalStatus",
    "UserRole",
    "Currency",
    # Core
    "Company",
    "FiscalYear",
    "User",
    # Accounting
    "AccountGroup",
    "Account",
    "JournalEntry",
    "JournalLine",
    # Parties
    "Customer",
    "Supplier",
    # Cash & Bank
    "CashAccount",
    "BankAccount",
    # Tax
    "Tax",
    # Cost Center & Project
    "CostCenter",
    "Project",
    # Audit & Settings
    "AuditLog",
    "Setting",
]
