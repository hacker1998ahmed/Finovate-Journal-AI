# Finovate Journal AI - Cash Account Model

"""
Cash Account model for petty cash management.
"""

from sqlalchemy import Column, Integer, String, Text, Numeric, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from decimal import Decimal
from .base import Base


class CashAccount(Base):
    """Cash account model for petty cash funds."""
    
    __tablename__ = "cash_accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    
    code = Column(String(50), nullable=False, index=True)
    name_ar = Column(String(255), nullable=False)
    name_en = Column(String(255), default="")
    
    currency = Column(String(3), default="EGP")
    opening_balance = Column(Numeric(20, 6), default=Decimal("0.00"))
    current_balance = Column(Numeric(20, 6), default=Decimal("0.00"))
    
    is_active = Column(Boolean, default=True)
    notes = Column(Text, default="")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    company = relationship("Company", back_populates="cash_accounts")
    
    def __repr__(self):
        return f"<CashAccount(id={self.id}, code='{self.code}', name='{self.name_ar}')>"
    
    @property
    def name(self) -> str:
        """Get cash account name based on context."""
        return self.name_ar or self.name_en
