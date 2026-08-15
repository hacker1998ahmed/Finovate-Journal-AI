"""
Finovate Journal AI - Models Package

Developer: Ahmed Mostafa Ibrahim
Brand: Finovate – AHMED EG
"""

from pydantic import BaseModel, Field, validator
from decimal import Decimal
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum


class AccountType(str, Enum):
    ASSET = "asset"
    LIABILITY = "liability"
    EQUITY = "equity"
    REVENUE = "revenue"
    EXPENSE = "expense"


class NormalBalance(str, Enum):
    DEBIT = "debit"
    CREDIT = "credit"


class EntryStatus(str, Enum):
    DRAFT = "draft"
    REVIEWED = "reviewed"
    POSTED = "posted"
    CANCELLED = "cancelled"


# Pydantic models for validation and data transfer

class AccountBase(BaseModel):
    code: str
    name_ar: str
    name_en: str
    account_type: AccountType
    normal_balance: NormalBalance
    parent_id: Optional[int] = None
    is_active: bool = True


class AccountCreate(AccountBase):
    company_id: int
    group_id: Optional[int] = None
    description: Optional[str] = None
    opening_balance: Decimal = Field(default=Decimal("0.00"))


class Account(AccountCreate):
    id: int
    level: int = 1
    is_system: bool = False
    current_balance: Decimal = Field(default=Decimal("0.00"))
    created_at: datetime
    
    class Config:
        from_attributes = True


class JournalLineBase(BaseModel):
    account_id: int
    description_ar: Optional[str] = None
    description_en: Optional[str] = None
    debit_amount: Decimal = Field(default=Decimal("0.00"))
    credit_amount: Decimal = Field(default=Decimal("0.00"))
    cost_center_id: Optional[int] = None
    project_id: Optional[int] = None
    tax_amount: Decimal = Field(default=Decimal("0.00"))
    tax_rate: Optional[Decimal] = None


class JournalLineCreate(JournalLineBase):
    line_number: int


class JournalLine(JournalLineCreate):
    id: int
    entry_id: int
    
    class Config:
        from_attributes = True


class JournalEntryBase(BaseModel):
    entry_date: datetime
    description_ar: Optional[str] = None
    description_en: Optional[str] = None
    reference: Optional[str] = None
    notes: Optional[str] = None
    
    @validator('description_ar', 'description_en')
    def validate_description(cls, v):
        if v and len(v) > 500:
            raise ValueError("Description cannot exceed 500 characters")
        return v


class JournalEntryCreate(JournalEntryBase):
    company_id: int
    lines: List[JournalLineCreate]
    
    @validator('lines')
    def validate_lines(cls, lines):
        if len(lines) < 2:
            raise ValueError("Journal entry must have at least 2 lines")
        return lines


class JournalEntry(JournalEntryBase):
    id: int
    entry_number: str
    company_id: int
    status: EntryStatus = EntryStatus.DRAFT
    total_debit: Decimal = Field(default=Decimal("0.00"))
    total_credit: Decimal = Field(default=Decimal("0.00"))
    is_balanced: bool = False
    is_posted: bool = False
    created_by: Optional[int] = None
    created_at: datetime
    lines: List[JournalLine] = []
    
    class Config:
        from_attributes = True
    
    def calculate_totals(self):
        """Calculate debit and credit totals."""
        self.total_debit = sum(line.debit_amount for line in self.lines)
        self.total_credit = sum(line.credit_amount for line in self.lines)
        self.is_balanced = (self.total_debit == self.total_credit)
        return self.is_balanced


class TransactionAnalysis(BaseModel):
    """Result of NLP/AI transaction analysis."""
    transaction_type: Optional[str] = None
    amount: Optional[Decimal] = None
    currency: str = "EGP"
    party: Optional[str] = None
    payment_method: Optional[str] = None  # cash, bank, credit
    tax: Dict[str, Any] = {}
    entries: List[Dict[str, Any]] = []
    confidence: float = Field(ge=0.0, le=100.0)
    ambiguities: List[str] = []
    explanation: str = ""
    suggested_accounts: List[int] = []
    
    class Config:
        from_attributes = True


class ConfidenceLevel(str, Enum):
    VERY_HIGH = "very_high"  # 90-100%
    HIGH = "high"  # 75-89%
    MEDIUM = "medium"  # 50-74%
    LOW = "low"  # Below 50%


def get_confidence_level(confidence: float) -> ConfidenceLevel:
    """Get confidence level from percentage."""
    if confidence >= 90:
        return ConfidenceLevel.VERY_HIGH
    elif confidence >= 75:
        return ConfidenceLevel.HIGH
    elif confidence >= 50:
        return ConfidenceLevel.MEDIUM
    else:
        return ConfidenceLevel.LOW
