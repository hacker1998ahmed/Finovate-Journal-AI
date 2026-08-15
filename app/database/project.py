"""Project model."""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Numeric, Date, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime, date
from decimal import Decimal
import enum

from .base import Base


class ProjectStatus(str, enum.Enum):
    """Project status enumeration."""

    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Project(Base):
    """Project model for project accounting."""

    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False, index=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    name_ar = Column(String(200), nullable=False)
    name_en = Column(String(200), nullable=True)
    description = Column(Text, nullable=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True)
    status = Column(SQLEnum(ProjectStatus), default=ProjectStatus.PLANNED, nullable=False)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    budget_amount = Column(Numeric(15, 3), default=Decimal("0.00"), nullable=True)
    actual_cost = Column(Numeric(15, 3), default=Decimal("0.00"), nullable=True)
    actual_revenue = Column(Numeric(15, 3), default=Decimal("0.00"), nullable=True)
    manager_name = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    company = relationship("Company", back_populates="projects")
    customer = relationship("Customer")
    journal_entries = relationship("JournalEntry", back_populates="project")

    def __repr__(self) -> str:
        return f"<Project(id={self.id}, code='{self.code}', name='{self.name_ar}')>"

    @property
    def profit(self) -> Decimal:
        """Calculate project profit."""
        if self.actual_revenue and self.actual_cost:
            return self.actual_revenue - self.actual_cost
        return Decimal("0.00")
