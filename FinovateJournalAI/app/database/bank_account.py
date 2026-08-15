# Finovate Journal AI - Bank Account Model

"""
Bank Account model for bank transactions.
"""

from sqlalchemy import Column, Integer, String, Text, Numeric, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from decimal import Decimal
from .base import Base


class BankAccount(Base):
    """Bank account model for bank transactions."""
    
    __tablename__ = "bank_accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    
    code = Column(String(50), nullable=False, index=True)
    name_ar = Column(String(255), nullable=False)
    name_en = Column(String(255), default="")
    
    bank_name_ar = Column(String(255), default="")
    bank_name_en = Column(String(255), default="")
    account_number = Column(String(50), default="")
    iban = Column(String(34), default="")
    swift_code = Column(String(11), default="")
    
    currency = Column(String(3), default="EGP")
    opening_balance = Column(Numeric(20, 6), default=Decimal("0.00"))
    current_balance = Column(Numeric(20, 6), default=Decimal("0.00"))
    
    is_active = Column(Boolean, default=True)
    notes = Column(Text, default="")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    company = relationship("Company", back_populates="bank_accounts")
    
    def __repr__(self):
        return f"<BankAccount(id={self.id}, code='{self.code}', name='{self.name_ar}')>"
    
    @property
    def name(self) -> str:
        """Get bank account name based on context."""
        return self.name_ar or self.name_en
    
    @property
    def bank_name(self) -> str:
        """Get bank name based on context."""
        return self.bank_name_ar or self.bank_name_en
