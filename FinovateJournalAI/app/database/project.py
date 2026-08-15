# Finovate Journal AI - Project Model

"""
Project model for project accounting.
"""

from sqlalchemy import Column, Integer, String, Text, Numeric, Boolean, DateTime, ForeignKey, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from decimal import Decimal
from .base import Base


class Project(Base):
    """Project model for tracking costs and revenues by project."""
    
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True)
    
    code = Column(String(50), nullable=False, index=True)
    name_ar = Column(String(255), nullable=False)
    name_en = Column(String(255), default="")
    description_ar = Column(Text, default="")
    description_en = Column(Text, default="")
    
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    
    budget = Column(Numeric(20, 6), default=Decimal("0.00"))
    actual_cost = Column(Numeric(20, 6), default=Decimal("0.00"))
    
    is_active = Column(Boolean, default=True)
    is_completed = Column(Boolean, default=False)
    notes = Column(Text, default="")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    company = relationship("Company", back_populates="projects")
    customer = relationship("Customer", backref="projects")
    
    def __repr__(self):
        return f"<Project(id={self.id}, code='{self.code}', name='{self.name_ar}')>"
    
    @property
    def name(self) -> str:
        """Get project name based on context."""
        return self.name_ar or self.name_en
    
    @property
    def profit(self) -> Decimal:
        """Calculate project profit (placeholder)."""
        return Decimal("0.00")  # To be calculated from journal entries
