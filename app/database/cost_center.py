"""Cost Center model."""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from .base import Base


class CostCenter(Base):
    """Cost Center model for cost allocation."""

    __tablename__ = "cost_centers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False, index=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    name_ar = Column(String(200), nullable=False)
    name_en = Column(String(200), nullable=True)
    description = Column(Text, nullable=True)
    parent_id = Column(Integer, ForeignKey("cost_centers.id"), nullable=True)
    level = Column(Integer, default=1, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    manager_name = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    company = relationship("Company", back_populates="cost_centers")
    parent = relationship("CostCenter", remote_side=[id], backref="children")
    journal_entries = relationship("JournalEntry", back_populates="cost_center")

    def __repr__(self) -> str:
        return f"<CostCenter(id={self.id}, code='{self.code}', name='{self.name_ar}')>"
