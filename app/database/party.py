"""Customer and Supplier models."""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime
from decimal import Decimal

from .base import Base


class Customer(Base):
    """Customer model for accounts receivable."""

    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False, index=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    name_ar = Column(String(200), nullable=False)
    name_en = Column(String(200), nullable=True)
    address = Column(Text, nullable=True)
    phone = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    tax_number = Column(String(50), nullable=True)
    national_id = Column(String(20), nullable=True)
    opening_balance = Column(Numeric(15, 3), default=Decimal("0.00"), nullable=False)
    current_balance = Column(Numeric(15, 3), default=Decimal("0.00"), nullable=False)
    credit_limit = Column(Numeric(15, 3), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    company = relationship("Company", back_populates="customers")

    def __repr__(self) -> str:
        return f"<Customer(id={self.id}, code='{self.code}', name='{self.name_ar}')>"


class Supplier(Base):
    """Supplier model for accounts payable."""

    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False, index=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    name_ar = Column(String(200), nullable=False)
    name_en = Column(String(200), nullable=True)
    address = Column(Text, nullable=True)
    phone = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    tax_number = Column(String(50), nullable=True)
    national_id = Column(String(20), nullable=True)
    opening_balance = Column(Numeric(15, 3), default=Decimal("0.00"), nullable=False)
    current_balance = Column(Numeric(15, 3), default=Decimal("0.00"), nullable=False)
    credit_limit = Column(Numeric(15, 3), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    company = relationship("Company", back_populates="suppliers")

    def __repr__(self) -> str:
        return f"<Supplier(id={self.id}, code='{self.code}', name='{self.name_ar}')>"
