# Finovate Journal AI - Tax Model

"""
Tax model for VAT and other tax configurations.
"""

from sqlalchemy import Column, Integer, String, Text, Numeric, Boolean, DateTime, ForeignKey, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from decimal import Decimal
from .base import Base


class Tax(Base):
    """Tax model for VAT and other taxes."""
    
    __tablename__ = "taxes"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    
    code = Column(String(20), nullable=False, index=True)  # e.g., "VAT14"
    name_ar = Column(String(100), nullable=False)
    name_en = Column(String(100), default="")
    
    rate = Column(Numeric(5, 4), nullable=False)  # e.g., 0.14 for 14%
    is_compound = Column(Boolean, default=False)  # Whether tax compounds
    
    effective_date = Column(Date, nullable=False)
    expiry_date = Column(Date, nullable=True)
    
    # Tax accounts
    input_tax_account_id = Column(Integer, ForeignKey("accounts.id"), nullable=True)
    output_tax_account_id = Column(Integer, ForeignKey("accounts.id"), nullable=True)
    
    is_active = Column(Boolean, default=True)
    is_default = Column(Boolean, default=False)
    notes = Column(Text, default="")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    company = relationship("Company", back_populates="taxes")
    
    def __repr__(self):
        return f"<Tax(id={self.id}, code='{self.code}', rate={self.rate})>"
    
    @property
    def name(self) -> str:
        """Get tax name based on context."""
        return self.name_ar or self.name_en
    
    @property
    def rate_percentage(self) -> str:
        """Get tax rate as percentage string."""
        return f"{float(self.rate) * 100:.2f}%"
    
    def calculate_tax(self, amount: Decimal, inclusive: bool = False) -> Decimal:
        """Calculate tax amount from base amount."""
        if inclusive:
            # Amount includes tax, extract tax portion
            return amount - (amount / (1 + self.rate))
        else:
            # Amount excludes tax, calculate tax
            return amount * self.rate
