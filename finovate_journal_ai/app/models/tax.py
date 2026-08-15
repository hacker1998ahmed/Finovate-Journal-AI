"""
Finovate Journal AI - Tax Model
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime
from decimal import Decimal

from app.database.base import Base


class Tax(Base):
    """Tax configuration model"""
    __tablename__ = "taxes"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    code = Column(String(20), nullable=False)  # Tax code
    name = Column(String(100), nullable=False)
    name_ar = Column(String(100))  # Arabic name
    name_en = Column(String(100))  # English name
    rate = Column(Numeric(5, 2), nullable=False)  # Tax rate percentage
    tax_type = Column(String(20), default="VAT")  # VAT, WHT, etc.
    is_input_tax = Column(Boolean, default=False)  # Input VAT / Purchase tax
    is_output_tax = Column(Boolean, default=False)  # Output VAT / Sales tax
    input_account_id = Column(Integer, ForeignKey("accounts.id"))  # Input VAT account
    output_account_id = Column(Integer, ForeignKey("accounts.id"))  # Output VAT account
    effective_date = Column(DateTime)
    expiry_date = Column(DateTime)
    description = Column(Text)
    notes = Column(Text)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    company = relationship("Company", back_populates="taxes")
    input_account = relationship("Account", foreign_keys=[input_account_id])
    output_account = relationship("Account", foreign_keys=[output_account_id])
    journal_lines = relationship("JournalLine", back_populates="tax")
    
    def __repr__(self):
        return f"<Tax(id={self.id}, code='{self.code}', rate={self.rate}%)>"
    
    @property
    def rate_decimal(self) -> Decimal:
        """Get tax rate as decimal (e.g., 14% -> 0.14)"""
        return Decimal(str(self.rate)) / Decimal("100")
