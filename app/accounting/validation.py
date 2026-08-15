"""
Finovate Journal AI - Validation Engine

Developer: Ahmed Mostafa Ibrahim
Brand: Finovate – AHMED EG
"""

from decimal import Decimal
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class ValidationSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class ValidationError:
    """Represents a validation error."""
    field: str
    message: str
    severity: ValidationSeverity = ValidationSeverity.ERROR
    code: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "field": self.field,
            "message": self.message,
            "severity": self.severity.value,
            "code": self.code,
        }


@dataclass
class ValidationResult:
    """Result of validation process."""
    is_valid: bool = True
    errors: List[ValidationError] = field(default_factory=list)
    warnings: List[ValidationError] = field(default_factory=list)
    
    def add_error(self, field: str, message: str, code: str = "", severity: ValidationSeverity = ValidationSeverity.ERROR):
        error = ValidationError(field=field, message=message, severity=severity, code=code)
        self.errors.append(error)
        self.is_valid = False
    
    def add_warning(self, field: str, message: str, code: str = ""):
        warning = ValidationError(field=field, message=message, severity=ValidationSeverity.WARNING, code=code)
        self.warnings.append(warning)
    
    def merge(self, other: 'ValidationResult'):
        """Merge another validation result into this one."""
        self.errors.extend(other.errors)
        self.warnings.extend(other.warnings)
        if not other.is_valid:
            self.is_valid = False
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_valid": self.is_valid,
            "errors": [e.to_dict() for e in self.errors],
            "warnings": [w.to_dict() for w in self.warnings],
        }


@dataclass
class ValidationRule:
    """A validation rule definition."""
    name: str
    description: str
    enabled: bool = True
    

def validate_debit_credit_balance(debit_total: Decimal, credit_total: Decimal) -> ValidationResult:
    """Validate that debit equals credit."""
    result = ValidationResult()
    
    if debit_total != credit_total:
        difference = abs(debit_total - credit_total)
        result.add_error(
            field="balance",
            message=f"القيد غير متوازن. الفرق: {difference}",
            code="BALANCE_MISMATCH",
            severity=ValidationSeverity.CRITICAL
        )
    
    if debit_total == Decimal("0.00") and credit_total == Decimal("0.00"):
        result.add_error(
            field="amounts",
            message="لا يمكن إنشاء قيد بمبلغ صفر",
            code="ZERO_AMOUNT",
            severity=ValidationSeverity.ERROR
        )
    
    return result


def validate_account_exists(account_id: int, available_accounts: List[int]) -> ValidationResult:
    """Validate that an account exists."""
    result = ValidationResult()
    
    if account_id not in available_accounts:
        result.add_error(
            field="account_id",
            message=f"الحساب رقم {account_id} غير موجود",
            code="ACCOUNT_NOT_FOUND",
            severity=ValidationSeverity.ERROR
        )
    
    return result


def validate_fiscal_year_open(entry_date: datetime, fiscal_years: List[Dict[str, Any]]) -> ValidationResult:
    """Validate that the fiscal year is open for the entry date."""
    result = ValidationResult()
    
    year = entry_date.year
    open_year_found = False
    
    for fy in fiscal_years:
        if fy.get("year") == year and fy.get("is_open", False):
            open_year_found = True
            break
    
    if not open_year_found:
        result.add_error(
            field="entry_date",
            message=f"السنة المالية {year} مغلقة أو غير موجودة",
            code="FISCAL_YEAR_CLOSED",
            severity=ValidationSeverity.ERROR
        )
    
    return result


def validate_journal_entry(lines: List[Dict[str, Any]], 
                          available_accounts: List[int],
                          fiscal_years: List[Dict[str, Any]],
                          entry_date: datetime) -> ValidationResult:
    """
    Complete journal entry validation pipeline.
    
    Validates:
    1. At least 2 lines
    2. Debit/Credit balance
    3. Account existence
    4. Fiscal year status
    5. Amount validity
    """
    result = ValidationResult()
    
    # Rule 1: At least 2 lines
    if len(lines) < 2:
        result.add_error(
            field="lines",
            message="يجب أن يحتوي القيد على سطرین على الأقل",
            code="MIN_LINES",
            severity=ValidationSeverity.ERROR
        )
        return result  # Cannot continue with less than 2 lines
    
    # Rule 2: Calculate totals
    debit_total = Decimal("0.00")
    credit_total = Decimal("0.00")
    
    for i, line in enumerate(lines):
        line_num = i + 1
        
        # Validate amounts
        debit = Decimal(str(line.get("debit_amount", 0)))
        credit = Decimal(str(line.get("credit_amount", 0)))
        
        if debit < 0 or credit < 0:
            result.add_error(
                field=f"line_{line_num}_amount",
                message="المبالغ لا يمكن أن تكون سالبة",
                code="NEGATIVE_AMOUNT",
                severity=ValidationSeverity.ERROR
            )
        
        if debit > 0 and credit > 0:
            result.add_warning(
                field=f"line_{line_num}_amount",
                message="السطر يحتوي على مدين ودائن معًا",
                code="BOTH_DEBIT_CREDIT"
            )
        
        debit_total += debit
        credit_total += credit
        
        # Validate account
        account_id = line.get("account_id")
        if account_id:
            account_result = validate_account_exists(account_id, available_accounts)
            result.merge(account_result)
    
    # Rule 3: Balance validation
    balance_result = validate_debit_credit_balance(debit_total, credit_total)
    result.merge(balance_result)
    
    # Rule 4: Fiscal year validation
    fy_result = validate_fiscal_year_open(entry_date, fiscal_years)
    result.merge(fy_result)
    
    return result
