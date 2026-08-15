# Finovate Journal AI - Cost Center Model

"""
Cost Center model for dimensional accounting.
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base


class CostCenter(Base):
    """Cost Center model for tracking expenses/revenues by department."""
    
    __tablename__ = "cost_centers"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    
    code = Column(String(50), nullable=False, index=True)
    name_ar = Column(String(255), nullable=False)
    name_en = Column(String(255), default="")
    description_ar = Column(Text, default="")
    description_en = Column(Text, default="")
    
    parent_id = Column(Integer, ForeignKey("cost_centers.id"), nullable=True)
    level = Column(Integer, default=1)
    
    is_active = Column(Boolean, default=True)
    notes = Column(Text, default="")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    company = relationship("Company", back_populates="cost_centers")
    parent = relationship("CostCenter", remote_side=[id], backref="children")
    
    def __repr__(self):
        return f"<CostCenter(id={self.id}, code='{self.code}', name='{self.name_ar}')>"
    
    @property
    def name(self) -> str:
        """Get cost center name based on context."""
        return self.name_ar or self.name_en
