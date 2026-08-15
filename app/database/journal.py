"""Journal Entry and Journal Line models."""

import enum
from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey, Enum as SQLEnum, Numeric, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, date
from decimal import Decimal

from .base import Base


class EntryStatus(str, enum.Enum):
    """Journal entry status enumeration."""

    DRAFT = "draft"
    AI_SUGGESTED = "ai_suggested"
    USER_EDITED = "user_edited"
    REVIEWED = "reviewed"
    POSTED = "posted"
    CANCELLED = "cancelled"


class JournalEntry(Base):
    """Journal Entry model (header)."""

    __tablename__ = "journal_entries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False, index=True)
    fiscal_year_id = Column(Integer, ForeignKey("fiscal_years.id"), nullable=True)
    entry_number = Column(String(50), unique=True, nullable=False, index=True)  # e.g., JE-2025-000001
    entry_date = Column(Date, nullable=False, default=date.today)
    reference = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    status = Column(SQLEnum(EntryStatus), default=EntryStatus.DRAFT, nullable=False)
    total_debit = Column(Numeric(15, 3), default=Decimal("0.00"), nullable=False)
    total_credit = Column(Numeric(15, 3), default=Decimal("0.00"), nullable=False)
    is_balanced = Column(Boolean, default=False, nullable=False)
    currency = Column(String(3), default="EGP", nullable=False)
    exchange_rate = Column(Numeric(10, 6), default=Decimal("1.000000"))
    cost_center_id = Column(Integer, ForeignKey("cost_centers.id"), nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    attachment_path = Column(String(500), nullable=True)
    notes = Column(Text, nullable=True)
    ai_confidence = Column(Integer, nullable=True)  # 0-100
    ai_provider = Column(String(50), nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    reviewed_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    posted_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    posted_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    company = relationship("Company", back_populates="journal_entries")
    created_by_user = relationship("User", foreign_keys=[created_by], back_populates="journal_entries")
    reviewed_by_user = relationship("User", foreign_keys=[reviewed_by])
    posted_by_user = relationship("User", foreign_keys=[posted_by])
    lines = relationship("JournalLine", back_populates="entry", cascade="all, delete-orphan")
    cost_center = relationship("CostCenter", back_populates="journal_entries")
    project = relationship("Project", back_populates="journal_entries")
    audit_logs = relationship("AuditLog", back_populates="journal_entry")

    def __repr__(self) -> str:
        return f"<JournalEntry(id={self.id}, number='{self.entry_number}', status='{self.status.value}')>"

    @property
    def balance_difference(self) -> Decimal:
        """Calculate the difference between debit and credit."""
        return abs(self.total_debit - self.total_credit)

    @property
    def can_post(self) -> bool:
        """Check if entry can be posted."""
        return self.is_balanced and self.status in [EntryStatus.REVIEWED, EntryStatus.USER_EDITED]


class JournalLine(Base):
    """Journal Line model (individual debit/credit entries)."""

    __tablename__ = "journal_lines"

    id = Column(Integer, primary_key=True, autoincrement=True)
    entry_id = Column(Integer, ForeignKey("journal_entries.id"), nullable=False, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False, index=True)
    line_number = Column(Integer, nullable=False)
    description = Column(String(500), nullable=True)
    debit = Column(Numeric(15, 3), default=Decimal("0.00"), nullable=False)
    credit = Column(Numeric(15, 3), default=Decimal("0.00"), nullable=False)
    cost_center_id = Column(Integer, ForeignKey("cost_centers.id"), nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    tax_id = Column(Integer, ForeignKey("taxes.id"), nullable=True)
    tax_amount = Column(Numeric(15, 3), default=Decimal("0.00"), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    entry = relationship("JournalEntry", back_populates="lines")
    account = relationship("Account", back_populates="journal_lines")
    cost_center = relationship("CostCenter")
    project = relationship("Project")
    tax = relationship("Tax")

    def __repr__(self) -> str:
        return f"<JournalLine(id={self.id}, entry_id={self.entry_id}, account_id={self.account_id}, debit={self.debit}, credit={self.credit})>"

    @property
    def amount(self) -> Decimal:
        """Get the amount (either debit or credit)."""
        return self.debit if self.debit > 0 else self.credit
