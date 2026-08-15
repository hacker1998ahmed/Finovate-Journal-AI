# Finovate Journal AI - Journal Entry Models

"""
Journal Entry and Journal Line models for accounting transactions.
Uses Decimal for precise financial calculations.
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, Numeric, DateTime, ForeignKey, Enum as SQLEnum, Date
from sqlalchemy.orm import relationship, validates
from datetime import datetime, date
from decimal import Decimal
import enum
from .base import Base


class JournalStatus(enum.Enum):
    """Journal entry status workflow."""
    DRAFT = "Draft"
    AI_SUGGESTED = "AI Suggested"
    USER_EDITED = "User Edited"
    REVIEWED = "Reviewed"
    POSTED = "Posted"
    CANCELLED = "Cancelled"


class JournalEntry(Base):
    """Journal Entry model representing a complete accounting transaction."""
    
    __tablename__ = "journal_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    fiscal_year_id = Column(Integer, ForeignKey("fiscal_years.id"), nullable=False)
    
    # Journal number (auto-generated)
    journal_number = Column(String(50), unique=True, nullable=False, index=True)
    
    # Transaction details
    transaction_date = Column(Date, nullable=False, index=True)
    reference = Column(String(100), default="")  # External reference number
    description_ar = Column(Text, nullable=False)  # Main description in Arabic
    description_en = Column(Text, default="")  # Optional English description
    
    # Status
    status = Column(SQLEnum(JournalStatus), default=JournalStatus.DRAFT)
    
    # Totals (for quick access, calculated from lines)
    total_debit = Column(Numeric(20, 6), default=Decimal("0.00"))
    total_credit = Column(Numeric(20, 6), default=Decimal("0.00"))
    is_balanced = Column(Boolean, default=False)
    
    # Additional info
    cost_center_id = Column(Integer, ForeignKey("cost_centers.id"), nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    attachment_path = Column(String(500), default="")
    
    # Audit
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    reviewed_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    posted_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    posted_at = Column(DateTime, nullable=True)
    
    notes = Column(Text, default="")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    company = relationship("Company", back_populates="journal_entries")
    fiscal_year = relationship("FiscalYear", back_populates="journal_entries")
    lines = relationship("JournalLine", back_populates="entry", cascade="all, delete-orphan", lazy="dynamic")
    cost_center = relationship("CostCenter", backref="journal_entries")
    project = relationship("Project", backref="journal_entries")
    creator = relationship("User", foreign_keys=[created_by], backref="created_journal_entries")
    reviewer = relationship("User", foreign_keys=[reviewed_by], backref="reviewed_journal_entries")
    poster = relationship("User", foreign_keys=[posted_by], backref="posted_journal_entries")
    
    def __repr__(self):
        return f"<JournalEntry(id={self.id}, number='{self.journal_number}', date={self.transaction_date})>"
    
    @property
    def description(self) -> str:
        """Get description based on context (default Arabic)."""
        return self.description_ar or self.description_en
    
    def calculate_totals(self) -> tuple:
        """Calculate total debit and credit from lines."""
        total_debit = Decimal("0.00")
        total_credit = Decimal("0.00")
        
        for line in self.lines:
            if line.debit_amount:
                total_debit += line.debit_amount
            if line.credit_amount:
                total_credit += line.credit_amount
        
        return total_debit, total_credit
    
    def update_totals(self):
        """Update totals and balanced status."""
        total_debit, total_credit = self.calculate_totals()
        self.total_debit = total_debit
        self.total_credit = total_credit
        self.is_balanced = (total_debit == total_credit)
    
    def is_postable(self) -> bool:
        """Check if entry can be posted."""
        return self.is_balanced and self.status in [JournalStatus.REVIEWED, JournalStatus.USER_EDITED]


class JournalLine(Base):
    """Journal Line model representing individual debit/credit entries."""
    
    __tablename__ = "journal_lines"
    
    id = Column(Integer, primary_key=True, index=True)
    entry_id = Column(Integer, ForeignKey("journal_entries.id"), nullable=False)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    
    # Amounts - only one should be non-zero per line
    debit_amount = Column(Numeric(20, 6), default=Decimal("0.00"))
    credit_amount = Column(Numeric(20, 6), default=Decimal("0.00"))
    
    # Line description (optional, inherits from entry if not provided)
    description_ar = Column(Text, default="")
    description_en = Column(Text, default="")
    
    # Additional dimensions
    cost_center_id = Column(Integer, ForeignKey("cost_centers.id"), nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    
    # Tax info (if applicable)
    tax_amount = Column(Numeric(20, 6), default=Decimal("0.00"))
    tax_id = Column(Integer, ForeignKey("taxes.id"), nullable=True)
    
    line_order = Column(Integer, default=0)  # For display ordering
    notes = Column(Text, default="")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    entry = relationship("JournalEntry", back_populates="lines")
    account = relationship("Account", back_populates="journal_lines")
    cost_center = relationship("CostCenter", backref="journal_lines")
    project = relationship("Project", backref="journal_lines")
    tax = relationship("Tax", backref="journal_lines")
    
    def __repr__(self):
        return f"<JournalLine(id={self.id}, account_id={self.account_id}, debit={self.debit_amount}, credit={self.credit_amount})>"
    
    @property
    def description(self) -> str:
        """Get line description based on context."""
        return self.description_ar or self.description_en or self.entry.description
    
    @property
    def amount(self) -> Decimal:
        """Get the non-zero amount (debit or credit)."""
        return self.debit_amount or self.credit_amount
    
    @validates('debit_amount', 'credit_amount')
    def validate_amounts(self, key, value):
        """Ensure amounts are non-negative."""
        if value is not None and value < 0:
            raise ValueError(f"{key} cannot be negative")
        return value
