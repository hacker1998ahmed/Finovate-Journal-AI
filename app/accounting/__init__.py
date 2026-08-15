"""
Finovate Journal AI - Accounting Engine Module

Developer: Ahmed Mostafa Ibrahim
Brand: Finovate – AHMED EG
"""

from .validation import (
    validate_journal_entry,
    validate_debit_credit_balance,
    validate_account_exists,
    validate_fiscal_year_open,
    ValidationRule,
    ValidationError,
    ValidationResult,
)
from .rules import (
    RuleEngine,
    AccountingRule,
    get_default_rules,
)
from .calculator import (
    calculate_tax,
    calculate_net_amount,
    calculate_gross_amount,
    format_currency,
)

__all__ = [
    # Validation
    "validate_journal_entry",
    "validate_debit_credit_balance",
    "validate_account_exists",
    "validate_fiscal_year_open",
    "ValidationRule",
    "ValidationError",
    "ValidationResult",
    # Rules
    "RuleEngine",
    "AccountingRule",
    "get_default_rules",
    # Calculator
    "calculate_tax",
    "calculate_net_amount",
    "calculate_gross_amount",
    "format_currency",
]
