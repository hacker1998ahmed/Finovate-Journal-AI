"""
Finovate Journal AI - Journal Entry Models

Developer: Ahmed Mostafa Ibrahim
Brand: Finovate – AHMED EG
"""

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, Numeric, DateTime, CheckConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from decimal import Decimal

from .base import Base


class JournalEntry(Base):
    """Journal Entry (Header) model."""

    __tablename__ = "journal_entries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    fiscal_year_id = Column(Integer, ForeignKey("fiscal_years.id"), nullable=True)
    
    # Entry identification
    entry_number = Column(String(50), unique=True, nullable=False, index=True)  # e.g., JE-2025-000001
    reference = Column(String(50), nullable=True)  # External reference
    
    # Entry details
    entry_date = Column(DateTime, nullable=False)
    description_ar = Column(String(500), nullable=True)
    description_en = Column(String(500), nullable=True)
    
    # Status workflow
    status = Column(String(20), nullable=False, default="draft")  # draft, reviewed, posted, cancelled
    is_posted = Column(Boolean, default=False)
    is_reversed = Column(Boolean, default=False)
    reversed_by_id = Column(Integer, ForeignKey("journal_entries.id"), nullable=True)
    
    # Amounts (calculated from lines)
    total_debit = Column(Numeric(20, 3), default=Decimal("0.00"))
    total_credit = Column(Numeric(20, 3), default=Decimal("0.00"))
    is_balanced = Column(Boolean, default=False)
    
    # Additional info
    notes = Column(Text, nullable=True)
    attachment_path = Column(String(500), nullable=True)
    
    # Audit
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    reviewed_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    posted_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    posted_at = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Constraints
    __table_args__ = (
        CheckConstraint("status IN ('draft', 'reviewed', 'posted', 'cancelled')", name="chk_entry_status"),
    )
    
    # Relationships
    company = relationship("Company", back_populates="journal_entries")
    fiscal_year = relationship("FiscalYear")
    creator = relationship("User", foreign_keys=[created_by], back_populates="journal_entries")
    reviewer = relationship("User", foreign_keys=[reviewed_by])
    poster = relationship("User", foreign_keys=[posted_by])
    lines = relationship("JournalLine", back_populates="entry", cascade="all, delete-orphan")
    reversal = relationship("JournalEntry", remote_side=[reversed_by_id])

    def __repr__(self):
        return f"<JournalEntry(id={self.id}, number='{self.entry_number}', status='{self.status}')>"

    def to_dict(self):
        """Convert journal entry to dictionary."""
        return {
            "id": self.id,
            "company_id": self.company_id,
            "entry_number": self.entry_number,
            "reference": self.reference,
            "entry_date": self.entry_date.isoformat() if self.entry_date else None,
            "description_ar": self.description_ar,
            "description_en": self.description_en,
            "status": self.status,
            "is_posted": self.is_posted,
            "total_debit": str(self.total_debit) if self.total_debit else "0.00",
            "total_credit": str(self.total_credit) if self.total_credit else "0.00",
            "is_balanced": self.is_balanced,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "posted_at": self.posted_at.isoformat() if self.posted_at else None,
        }


class JournalLine(Base):
    """Journal Entry Line model."""

    __tablename__ = "journal_lines"

    id = Column(Integer, primary_key=True, autoincrement=True)
    entry_id = Column(Integer, ForeignKey("journal_entries.id"), nullable=False)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    
    # Line details
    line_number = Column(Integer, nullable=False)
    description_ar = Column(String(500), nullable=True)
    description_en = Column(String(500), nullable=True)
    
    # Amounts
    debit_amount = Column(Numeric(20, 3), default=Decimal("0.00"))
    credit_amount = Column(Numeric(20, 3), default=Decimal("0.00"))
    
    # Cost center and project
    cost_center_id = Column(Integer, ForeignKey("cost_centers.id"), nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    
    # Tax
    tax_amount = Column(Numeric(20, 3), default=Decimal("0.00"))
    tax_rate = Column(Numeric(10, 3), nullable=True)
    is_tax_inclusive = Column(Boolean, default=False)
    
    # Additional info
    notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    entry = relationship("JournalEntry", back_populates="lines")
    account = relationship("Account", back_populates="journal_lines")
    cost_center = relationship("CostCenter")
    project = relationship("Project")

    def __repr__(self):
        return f"<JournalLine(id={self.id}, entry_id={self.entry_id}, account_id={self.account_id})>"

    @property
    def amount(self) -> Decimal:
        """Get the amount (debit or credit)."""
        return self.debit_amount if self.debit_amount > 0 else self.credit_amount

    def to_dict(self):
        """Convert journal line to dictionary."""
        return {
            "id": self.id,
            "entry_id": self.entry_id,
            "account_id": self.account_id,
            "line_number": self.line_number,
            "description_ar": self.description_ar,
            "description_en": self.description_en,
            "debit_amount": str(self.debit_amount) if self.debit_amount else "0.00",
            "credit_amount": str(self.credit_amount) if self.credit_amount else "0.00",
            "cost_center_id": self.cost_center_id,
            "project_id": self.project_id,
            "tax_amount": str(self.tax_amount) if self.tax_amount else "0.00",
            "tax_rate": str(self.tax_rate) if self.tax_rate else None,
        }
