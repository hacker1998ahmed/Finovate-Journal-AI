"""
Finovate Journal AI - Party Models (Customers & Suppliers)

Developer: Ahmed Mostafa Ibrahim
Brand: Finovate – AHMED EG
"""

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, Numeric, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from decimal import Decimal

from .base import Base


class Customer(Base):
    """Customer model."""

    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    
    # Customer identification
    code = Column(String(50), unique=True, nullable=False, index=True)
    name_ar = Column(String(200), nullable=False)
    name_en = Column(String(200), nullable=False)
    
    # Contact info
    address = Column(Text, nullable=True)
    phone = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    tax_number = Column(String(50), nullable=True)
    national_id = Column(String(20), nullable=True)
    
    # Financial
    opening_balance = Column(Numeric(20, 3), default=Decimal("0.00"))
    current_balance = Column(Numeric(20, 3), default=Decimal("0.00"))
    credit_limit = Column(Numeric(20, 3), nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Additional info
    notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    company = relationship("Company", back_populates="customers")

    def __repr__(self):
        return f"<Customer(id={self.id}, code='{self.code}', name_ar='{self.name_ar}')>"

    def to_dict(self):
        """Convert customer to dictionary."""
        return {
            "id": self.id,
            "company_id": self.company_id,
            "code": self.code,
            "name_ar": self.name_ar,
            "name_en": self.name_en,
            "address": self.address,
            "phone": self.phone,
            "email": self.email,
            "tax_number": self.tax_number,
            "opening_balance": str(self.opening_balance) if self.opening_balance else "0.00",
            "current_balance": str(self.current_balance) if self.current_balance else "0.00",
            "credit_limit": str(self.credit_limit) if self.credit_limit else None,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class Supplier(Base):
    """Supplier model."""

    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    
    # Supplier identification
    code = Column(String(50), unique=True, nullable=False, index=True)
    name_ar = Column(String(200), nullable=False)
    name_en = Column(String(200), nullable=False)
    
    # Contact info
    address = Column(Text, nullable=True)
    phone = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    tax_number = Column(String(50), nullable=True)
    national_id = Column(String(20), nullable=True)
    
    # Financial
    opening_balance = Column(Numeric(20, 3), default=Decimal("0.00"))
    current_balance = Column(Numeric(20, 3), default=Decimal("0.00"))
    credit_limit = Column(Numeric(20, 3), nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Additional info
    notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    company = relationship("Company", back_populates="suppliers")

    def __repr__(self):
        return f"<Supplier(id={self.id}, code='{self.code}', name_ar='{self.name_ar}')>"

    def to_dict(self):
        """Convert supplier to dictionary."""
        return {
            "id": self.id,
            "company_id": self.company_id,
            "code": self.code,
            "name_ar": self.name_ar,
            "name_en": self.name_en,
            "address": self.address,
            "phone": self.phone,
            "email": self.email,
            "tax_number": self.tax_number,
            "opening_balance": str(self.opening_balance) if self.opening_balance else "0.00",
            "current_balance": str(self.current_balance) if self.current_balance else "0.00",
            "credit_limit": str(self.credit_limit) if self.credit_limit else None,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
