# Finovate Journal AI - Fiscal Year Model

"""
Fiscal Year model for managing accounting periods.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Date
from sqlalchemy.orm import relationship
from datetime import datetime, date
from .base import Base


class FiscalYear(Base):
    """Fiscal Year model for accounting periods."""
    
    __tablename__ = "fiscal_years"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    
    name = Column(String(50), nullable=False)  # e.g., "2025", "FY2025"
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    
    is_current = Column(Boolean, default=False)
    is_closed = Column(Boolean, default=False)
    is_opening_balance_entered = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    company = relationship("Company", back_populates="fiscal_years")
    journal_entries = relationship("JournalEntry", back_populates="fiscal_year")
    
    def __repr__(self):
        return f"<FiscalYear(id={self.id}, name='{self.name}', company_id={self.company_id})>"
    
    @property
    def can_post(self) -> bool:
        """Check if entries can be posted to this fiscal year."""
        return not self.is_closed and self.is_current
    
    @staticmethod
    def get_fiscal_year_for_date(db_session, target_date: date, company_id: int):
        """Get the fiscal year that contains the given date."""
        return db_session.query(FiscalYear).filter(
            FiscalYear.company_id == company_id,
            FiscalYear.start_date <= target_date,
            FiscalYear.end_date >= target_date
        ).first()
    
    @staticmethod
    def create_fiscal_year(db_session, company_id: int, year: int, start_month: int = 1):
        """Create a fiscal year for the given calendar year."""
        start_date = date(year, start_month, 1)
        
        # End date is last day of month before start_month in next year
        if start_month == 1:
            end_date = date(year, 12, 31)
        else:
            end_date = date(year + 1, start_month - 1, 1)
            # Get last day of previous month
            from datetime import timedelta
            end_date = end_date - timedelta(days=1)
        
        fiscal_year = FiscalYear(
            company_id=company_id,
            name=str(year),
            start_date=start_date,
            end_date=end_date,
            is_current=False,
            is_closed=False
        )
        
        db_session.add(fiscal_year)
        return fiscal_year
