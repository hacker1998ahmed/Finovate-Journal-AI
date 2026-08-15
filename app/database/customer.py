# Finovate Journal AI - Customer Model

"""
Customer model for accounts receivable.
"""

from sqlalchemy import Column, Integer, String, Text, Numeric, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from decimal import Decimal
from .base import Base


class Customer(Base):
    """Customer model for managing receivables."""
    
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    
    code = Column(String(50), nullable=False, index=True)
    name_ar = Column(String(255), nullable=False)
    name_en = Column(String(255), default="")
    
    address_ar = Column(Text, default="")
    address_en = Column(Text, default="")
    phone = Column(String(20), default="")
    email = Column(String(100), default="")
    tax_number = Column(String(50), default="")
    
    opening_balance = Column(Numeric(20, 6), default=Decimal("0.00"))
    current_balance = Column(Numeric(20, 6), default=Decimal("0.00"))
    credit_limit = Column(Numeric(20, 6), default=Decimal("0.00"))
    
    is_active = Column(Boolean, default=True)
    notes = Column(Text, default="")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    company = relationship("Company", back_populates="customers")
    
    def __repr__(self):
        return f"<Customer(id={self.id}, code='{self.code}', name='{self.name_ar}')>"
    
    @property
    def name(self) -> str:
        """Get customer name based on context."""
        return self.name_ar or self.name_en
    
    @property
    def display_name(self) -> str:
        """Get formatted display name."""
        return f"{self.code} - {self.name_ar}"
