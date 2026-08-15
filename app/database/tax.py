"""Tax model."""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Numeric, Date
from sqlalchemy.orm import relationship
from datetime import datetime, date
from decimal import Decimal

from .base import Base


class Tax(Base):
    """Tax model for VAT and other taxes."""

    __tablename__ = "taxes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False, index=True)
    code = Column(String(20), unique=True, nullable=False, index=True)
    name_ar = Column(String(100), nullable=False)
    name_en = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    rate = Column(Numeric(5, 2), nullable=False)  # e.g., 14.00 for 14%
    tax_type = Column(String(50), default="VAT", nullable=False)  # VAT, Withholding, etc.
    is_compound = Column(Boolean, default=False, nullable=False)
    effective_date = Column(Date, default=date.today, nullable=False)
    expiry_date = Column(Date, nullable=True)
    input_account_id = Column(Integer, ForeignKey("accounts.id"), nullable=True)  # Input VAT account
    output_account_id = Column(Integer, ForeignKey("accounts.id"), nullable=True)  # Output VAT account
    is_active = Column(Boolean, default=True, nullable=False)
    is_default = Column(Boolean, default=False, nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    company = relationship("Company", back_populates="taxes")

    def __repr__(self) -> str:
        return f"<Tax(id={self.id}, code='{self.code}', rate={self.rate})>"

    @property
    def rate_percentage(self) -> str:
        """Get rate as percentage string."""
        return f"{self.rate}%"
