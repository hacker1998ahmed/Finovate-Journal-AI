"""
Finovate Journal AI - Tax, Cost Center, Project, Audit Models

Developer: Ahmed Mostafa Ibrahim
Brand: Finovate – AHMED EG
"""

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, Numeric, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from decimal import Decimal

from .base import Base


class Tax(Base):
    """Tax configuration model."""

    __tablename__ = "taxes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    
    name_ar = Column(String(100), nullable=False)
    name_en = Column(String(100), nullable=False)
    code = Column(String(20), nullable=False)
    rate = Column(Numeric(10, 3), nullable=False)  # e.g., 14.000 for 14%
    
    # Tax type
    tax_type = Column(String(20), default="vat")  # vat, withholding, etc.
    is_sales_tax = Column(Boolean, default=True)
    is_purchase_tax = Column(Boolean, default=True)
    
    # Accounts
    output_account_id = Column(Integer, ForeignKey("accounts.id"), nullable=True)
    input_account_id = Column(Integer, ForeignKey("accounts.id"), nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    effective_date = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    company = relationship("Company")
    output_account = relationship("Account", foreign_keys=[output_account_id])
    input_account = relationship("Account", foreign_keys=[input_account_id])

    def __repr__(self):
        return f"<Tax(id={self.id}, code='{self.code}', rate={self.rate})>"


class CostCenter(Base):
    """Cost Center model."""

    __tablename__ = "cost_centers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    
    code = Column(String(50), unique=True, nullable=False)
    name_ar = Column(String(200), nullable=False)
    name_en = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    company = relationship("Company")

    def __repr__(self):
        return f"<CostCenter(id={self.id}, code='{self.code}')>"


class Project(Base):
    """Project model for project accounting."""

    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True)
    
    code = Column(String(50), unique=True, nullable=False)
    name_ar = Column(String(200), nullable=False)
    name_en = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    
    # Budget
    budget_amount = Column(Numeric(20, 3), default=Decimal("0.00"))
    actual_cost = Column(Numeric(20, 3), default=Decimal("0.00"))
    
    # Dates
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    
    # Status
    status = Column(String(20), default="active")  # active, completed, on_hold, cancelled
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    company = relationship("Company")
    customer = relationship("Customer")

    def __repr__(self):
        return f"<Project(id={self.id}, code='{self.code}')>"


class AuditLog(Base):
    """Audit Log model for tracking changes."""

    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Action details
    action = Column(String(100), nullable=False)  # CREATE, UPDATE, DELETE, POST, etc.
    entity_type = Column(String(50), nullable=False)  # JournalEntry, Account, etc.
    entity_id = Column(Integer, nullable=True)
    
    # Changes
    old_value = Column(Text, nullable=True)  # JSON string
    new_value = Column(Text, nullable=True)  # JSON string
    
    # Context
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(String(500), nullable=True)
    notes = Column(Text, nullable=True)
    
    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    user = relationship("User", back_populates="audit_logs")

    def __repr__(self):
        return f"<AuditLog(id={self.id}, action='{self.action}', entity='{self.entity_type}')>"


class Settings(Base):
    """Application settings stored in database."""

    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True)
    
    key = Column(String(100), nullable=False, unique=True)
    value = Column(Text, nullable=True)
    value_type = Column(String(20), default="string")  # string, int, float, bool, json
    
    description = Column(Text, nullable=True)
    is_system = Column(Boolean, default=False)
    
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    company = relationship("Company")

    def __repr__(self):
        return f"<Settings(id={self.id}, key='{self.key}')>"
