"""
Finovate Journal AI - Additional Models (Cost Center, Project, Item, Invoice)
Foundation models for future expansion
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime
from decimal import Decimal

from app.database.base import Base


class CostCenter(Base):
    """Cost Center model for cost accounting"""
    __tablename__ = "cost_centers"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    code = Column(String(20), nullable=False)
    name = Column(String(100), nullable=False)
    name_ar = Column(String(100))
    name_en = Column(String(100))
    parent_id = Column(Integer, ForeignKey("cost_centers.id"))
    manager = Column(String(100))
    budget = Column(Numeric(19, 4))
    notes = Column(Text)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    company = relationship("Company")
    parent = relationship("CostCenter", remote_side=[id], backref="children")
    journal_lines = relationship("JournalLine", back_populates="cost_center")
    
    def __repr__(self):
        return f"<CostCenter(id={self.id}, code='{self.code}')>"


class Project(Base):
    """Project model for project accounting"""
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    code = Column(String(20), nullable=False)
    name = Column(String(200), nullable=False)
    name_ar = Column(String(200))
    name_en = Column(String(200))
    customer_id = Column(Integer, ForeignKey("customers.id"))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    budget = Column(Numeric(19, 4))
    actual_cost = Column(Numeric(19, 4), default=Decimal("0.00"))
    revenue = Column(Numeric(19, 4), default=Decimal("0.00"))
    status = Column(String(20), default="Active")  # Active, Completed, On Hold, Cancelled
    manager = Column(String(100))
    notes = Column(Text)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    company = relationship("Company")
    customer = relationship("Customer")
    journal_lines = relationship("JournalLine", back_populates="project")
    
    def __repr__(self):
        return f"<Project(id={self.id}, code='{self.code}')>"


class Item(Base):
    """Item model for inventory (foundation)"""
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    code = Column(String(50), nullable=False)
    name = Column(String(200), nullable=False)
    name_ar = Column(String(200))
    name_en = Column(String(200))
    description = Column(Text)
    unit = Column(String(20))  # Unit of measure
    cost_price = Column(Numeric(19, 4), default=Decimal("0.00"))
    selling_price = Column(Numeric(19, 4), default=Decimal("0.00"))
    quantity_on_hand = Column(Numeric(19, 2), default=Decimal("0.00"))
    reorder_level = Column(Numeric(19, 2))
    category = Column(String(100))
    tax_id = Column(Integer, ForeignKey("taxes.id"))
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    company = relationship("Company")
    tax = relationship("Tax")
    
    def __repr__(self):
        return f"<Item(id={self.id}, code='{self.code}')>"


class Invoice(Base):
    """Invoice model (foundation for future invoicing module)"""
    __tablename__ = "invoices"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    invoice_number = Column(String(50), nullable=False)
    invoice_type = Column(String(20), nullable=False)  # Sales, Purchase
    date = Column(DateTime, nullable=False)
    due_date = Column(DateTime)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    supplier_id = Column(Integer, ForeignKey("suppliers.id"))
    subtotal = Column(Numeric(19, 4), default=Decimal("0.00"))
    discount = Column(Numeric(19, 4), default=Decimal("0.00"))
    tax_amount = Column(Numeric(19, 4), default=Decimal("0.00"))
    total = Column(Numeric(19, 4), default=Decimal("0.00"))
    paid_amount = Column(Numeric(19, 4), default=Decimal("0.00"))
    balance = Column(Numeric(19, 4), default=Decimal("0.00"))
    status = Column(String(20), default="Draft")  # Draft, Posted, Paid, Cancelled
    notes = Column(Text)
    journal_entry_id = Column(Integer, ForeignKey("journal_entries.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    company = relationship("Company")
    customer = relationship("Customer")
    supplier = relationship("Supplier")
    lines = relationship("InvoiceLine", back_populates="invoice", cascade="all, delete-orphan")
    journal_entry = relationship("JournalEntry")
    
    def __repr__(self):
        return f"<Invoice(id={self.id}, number='{self.invoice_number}')>"


class InvoiceLine(Base):
    """Invoice Line model"""
    __tablename__ = "invoice_lines"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=False)
    line_number = Column(Integer, default=1)
    item_id = Column(Integer, ForeignKey("items.id"))
    description = Column(Text)
    quantity = Column(Numeric(19, 2), default=Decimal("1.00"))
    unit_price = Column(Numeric(19, 4), default=Decimal("0.00"))
    discount = Column(Numeric(19, 4), default=Decimal("0.00"))
    tax_id = Column(Integer, ForeignKey("taxes.id"))
    tax_amount = Column(Numeric(19, 4), default=Decimal("0.00"))
    line_total = Column(Numeric(19, 4), default=Decimal("0.00"))
    notes = Column(Text)
    
    # Relationships
    invoice = relationship("Invoice", back_populates="lines")
    item = relationship("Item")
    tax = relationship("Tax")
    
    def __repr__(self):
        return f"<InvoiceLine(id={self.id}, invoice_id={self.invoice_id})>"
