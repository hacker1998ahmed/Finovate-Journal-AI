"""
Finovate Journal AI - Journal Entry and Journal Line Models
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Numeric, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from decimal import Decimal

from app.database.base import Base


class JournalEntry(Base):
    """Journal Entry header model"""
    __tablename__ = "journal_entries"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    entry_number = Column(String(50), nullable=False, unique=True)  # JE-YYYY-NNNNNN
    fiscal_year_id = Column(Integer, ForeignKey("fiscal_years.id"))
    date = Column(DateTime, nullable=False)
    reference = Column(String(100))  # External reference number
    description = Column(Text, nullable=False)  # Main description
    source = Column(String(50), default="Manual")  # Manual, Smart Journal, AI, Import, etc.
    status = Column(String(20), default="Draft")  # Draft, Reviewed, Posted, Cancelled
    created_by = Column(Integer, ForeignKey("users.id"))
    reviewed_by = Column(Integer, ForeignKey("users.id"))
    posted_by = Column(Integer, ForeignKey("users.id"))
    posted_date = Column(DateTime)
    total_debit = Column(Numeric(19, 4), default=Decimal("0.00"))
    total_credit = Column(Numeric(19, 4), default=Decimal("0.00"))
    is_balanced = Column(Boolean, default=False)
    notes = Column(Text)
    attachment_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    company = relationship("Company", back_populates="journal_entries")
    lines = relationship("JournalLine", back_populates="entry", cascade="all, delete-orphan", lazy="joined")
    creator = relationship("User", foreign_keys=[created_by])
    reviewer = relationship("User", foreign_keys=[reviewed_by])
    poster = relationship("User", foreign_keys=[posted_by])
    
    def __repr__(self):
        return f"<JournalEntry(id={self.id}, number='{self.entry_number}')>"
    
    @property
    def balance_difference(self) -> Decimal:
        """Calculate difference between debit and credit"""
        return abs(self.total_debit - self.total_credit)


class JournalLine(Base):
    """Journal Entry Line model"""
    __tablename__ = "journal_lines"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    entry_id = Column(Integer, ForeignKey("journal_entries.id"), nullable=False)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    line_number = Column(Integer, default=1)
    description = Column(Text)  # Line-specific description
    debit = Column(Numeric(19, 4), default=Decimal("0.00"))
    credit = Column(Numeric(19, 4), default=Decimal("0.00"))
    cost_center_id = Column(Integer, ForeignKey("cost_centers.id"))  # Optional cost center
    project_id = Column(Integer, ForeignKey("projects.id"))  # Optional project
    tax_id = Column(Integer, ForeignKey("taxes.id"))  # Optional tax
    tax_amount = Column(Numeric(19, 4), default=Decimal("0.00"))
    customer_id = Column(Integer, ForeignKey("customers.id"))  # For AR transactions
    supplier_id = Column(Integer, ForeignKey("suppliers.id"))  # For AP transactions
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    entry = relationship("JournalEntry", back_populates="lines")
    account = relationship("Account", back_populates="journal_lines")
    cost_center = relationship("CostCenter")
    project = relationship("Project")
    tax = relationship("Tax")
    customer = relationship("Customer")
    supplier = relationship("Supplier")
    
    def __repr__(self):
        return f"<JournalLine(id={self.id}, account_id={self.account_id}, debit={self.debit}, credit={self.credit})>"
    
    __table_args__ = (
        UniqueConstraint('entry_id', 'line_number', name='uq_entry_line_number'),
    )
