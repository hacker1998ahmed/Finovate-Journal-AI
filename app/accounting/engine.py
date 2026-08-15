"""
Accounting Engine - Core accounting logic and validation
"""
from decimal import Decimal
from typing import List, Dict, Tuple, Optional
from datetime import date
from dataclasses import dataclass, field
import logging
import re

logger = logging.getLogger(__name__)


@dataclass
class JournalLineData:
    """Data class for journal line."""
    account_id: int
    account_name: str
    description: str
    debit: Decimal = Decimal('0.00')
    credit: Decimal = Decimal('0.00')
    cost_center_id: Optional[int] = None
    project_id: Optional[int] = None
    tax_id: Optional[int] = None
    tax_amount: Decimal = Decimal('0.00')


@dataclass
class JournalEntryData:
    """Data class for journal entry."""
    description: str
    entry_date: date
    lines: List[JournalLineData] = field(default_factory=list)
    reference: Optional[str] = None
    currency: str = "EGP"
    exchange_rate: Decimal = Decimal('1.00')
    cost_center_id: Optional[int] = None
    project_id: Optional[int] = None
    source: str = "manual"
    
    @property
    def total_debit(self) -> Decimal:
        return sum(line.debit for line in self.lines)
    
    @property
    def total_credit(self) -> Decimal:
        return sum(line.credit for line in self.lines)
    
    @property
    def is_balanced(self) -> bool:
        return self.total_debit == self.total_credit
    
    @property
    def difference(self) -> Decimal:
        return abs(self.total_debit - self.total_credit)


class AccountingValidator:
    """Validates accounting entries according to double-entry principles."""
    
    @staticmethod
    def validate_entry(entry: JournalEntryData) -> Tuple[bool, List[str]]:
        """
        Validate a journal entry.
        
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        # Check if entry has lines
        if not entry.lines:
            errors.append("Entry must have at least two lines")
            return False, errors
        
        if len(entry.lines) < 2:
            errors.append("Entry must have at least two lines (debit and credit)")
        
        # Check amounts
        for i, line in enumerate(entry.lines):
            if line.debit <= 0 and line.credit <= 0:
                errors.append(f"Line {i+1}: Must have either debit or credit amount")
            
            if line.debit > 0 and line.credit > 0:
                errors.append(f"Line {i+1}: Cannot have both debit and credit")
        
        # Check balance
        if not entry.is_balanced:
            errors.append(
                f"Entry is not balanced. Debit: {entry.total_debit}, "
                f"Credit: {entry.total_credit}, Difference: {entry.difference}"
            )
        
        # Check for zero amounts
        if entry.total_debit == 0:
            errors.append("Total debit cannot be zero")
        
        if entry.total_credit == 0:
            errors.append("Total credit cannot be zero")
        
        is_valid = len(errors) == 0
        if is_valid:
            logger.debug(f"Entry validated successfully: {entry.description}")
        else:
            logger.warning(f"Entry validation failed: {errors}")
        
        return is_valid, errors
    
    @staticmethod
    def validate_account_type(account_type: str, is_debit: bool) -> Tuple[bool, Optional[str]]:
        """
        Validate that the account type matches the expected normal balance.
        
        Normal balances:
        - Assets: Debit
        - Expenses: Debit
        - Liabilities: Credit
        - Equity: Credit
        - Revenue: Credit
        """
        normal_debit_accounts = ["asset", "expense"]
        normal_credit_accounts = ["liability", "equity", "revenue"]
        
        if account_type.lower() in normal_debit_accounts and is_debit:
            return True, None
        elif account_type.lower() in normal_credit_accounts and not is_debit:
            return True, None
        else:
            warning = (
                f"Unusual entry: {account_type} account used as {'debit' if is_debit else 'credit'}. "
                f"Normal balance is {'debit' if account_type in normal_debit_accounts else 'credit'}."
            )
            return True, warning  # Not an error, just a warning


class TaxCalculator:
    """Calculate tax amounts for transactions."""
    
    def __init__(self, tax_rate: Decimal):
        """Initialize with tax rate (e.g., Decimal('0.14') for 14%)."""
        self.tax_rate = tax_rate
    
    def calculate_tax_from_base(self, base_amount: Decimal) -> Decimal:
        """Calculate tax from base amount (before tax)."""
        return (base_amount * self.tax_rate).quantize(Decimal('0.01'))
    
    def calculate_tax_from_total(self, total_amount: Decimal) -> Decimal:
        """Extract tax from total amount (including tax)."""
        base = total_amount / (1 + self.tax_rate)
        tax = total_amount - base
        return tax.quantize(Decimal('0.01'))
    
    def get_base_and_tax(self, amount: Decimal, is_inclusive: bool) -> Tuple[Decimal, Decimal]:
        """
        Get base amount and tax from given amount.
        
        Args:
            amount: The amount
            is_inclusive: True if amount includes tax
            
        Returns:
            Tuple of (base_amount, tax_amount)
        """
        if is_inclusive:
            tax = self.calculate_tax_from_total(amount)
            base = amount - tax
        else:
            base = amount
            tax = self.calculate_tax_from_base(amount)
        
        return base, tax


class RulesEngine:
    """
    Rule-based accounting engine for common transaction types.
    Provides default account mappings for standard transactions.
    """
    
    def __init__(self):
        self.rules = self._initialize_rules()
    
    def _initialize_rules(self) -> Dict[str, Dict]:
        """Initialize accounting rules for common transactions."""
        return {
            "cash_purchase": {
                "name": "Cash Purchase",
                "name_ar": "شراء نقدي",
                "pattern_ar": ["شراء.*نقد", "اشتريت.*نقد"],
                "pattern_en": ["buy.*cash", "purchase.*cash", "paid.*cash"],
                "entries": [
                    {"type": "debit", "account_key": "purchases"},
                    {"type": "credit", "account_key": "cash"}
                ]
            },
            "credit_purchase": {
                "name": "Credit Purchase",
                "name_ar": "شراء آجل",
                "pattern_ar": ["شراء.*آجل", "شراء.*من.*شركة", "اشتريت.*على الحساب"],
                "pattern_en": ["buy.*credit", "purchase.*on account", "bought.*from"],
                "entries": [
                    {"type": "debit", "account_key": "purchases"},
                    {"type": "credit", "account_key": "suppliers"}
                ]
            },
            "cash_sale": {
                "name": "Cash Sale",
                "name_ar": "بيع نقدي",
                "pattern_ar": ["بيع.*نقد", "بعنا.*نقد", "استلمت.*نقد"],
                "pattern_en": ["sell.*cash", "sale.*cash", "received.*cash"],
                "entries": [
                    {"type": "debit", "account_key": "cash"},
                    {"type": "credit", "account_key": "sales"}
                ]
            },
            "credit_sale": {
                "name": "Credit Sale",
                "name_ar": "بيع آجل",
                "pattern_ar": ["بيع.*آجل", "بعنا.*للعميل", "بيع.*على الحساب"],
                "pattern_en": ["sell.*credit", "sale.*on account", "sold.*to"],
                "entries": [
                    {"type": "debit", "account_key": "customers"},
                    {"type": "credit", "account_key": "sales"}
                ]
            },
            "rent_payment": {
                "name": "Rent Payment",
                "name_ar": "دفع إيجار",
                "pattern_ar": ["دفع.*إيجار", "دفعت.*إيجار", "مصروف.*إيجار"],
                "pattern_en": ["paid.*rent", "pay.*rent", "rent expense"],
                "entries": [
                    {"type": "debit", "account_key": "rent_expense"},
                    {"type": "credit", "account_key": "cash_or_bank"}
                ]
            },
            "salary_payment": {
                "name": "Salary Payment",
                "name_ar": "دفع رواتب",
                "pattern_ar": ["دفع.*رواتب", "دفعت.*رواتب", "مصروف.*رواتب", "صرف.*رواتب"],
                "pattern_en": ["paid.*salary", "pay.*salaries", "salary expense"],
                "entries": [
                    {"type": "debit", "account_key": "salaries_expense"},
                    {"type": "credit", "account_key": "cash_or_bank"}
                ]
            },
            "customer_collection": {
                "name": "Customer Collection",
                "name_ar": "تحصيل من عميل",
                "pattern_ar": ["استلمت.*من.*عميل", "تحصيل.*من", "قبض.*من"],
                "pattern_en": ["received.*from customer", "collect.*from", "collection"],
                "entries": [
                    {"type": "debit", "account_key": "cash_or_bank"},
                    {"type": "credit", "account_key": "customers"}
                ]
            },
            "supplier_payment": {
                "name": "Supplier Payment",
                "name_ar": "سداد مورد",
                "pattern_ar": ["سددت.*لمورد", "دفعت.*لمورد", "دفع.*لمورد"],
                "pattern_en": ["paid.*supplier", "payment.*to supplier", "settle.*supplier"],
                "entries": [
                    {"type": "debit", "account_key": "suppliers"},
                    {"type": "credit", "account_key": "cash_or_bank"}
                ]
            },
            "fixed_asset_purchase": {
                "name": "Fixed Asset Purchase",
                "name_ar": "شراء أصل ثابت",
                "pattern_ar": ["اشتريت.*أصل", "شراء.*جهاز", "شراء.*معدات", "شراء.*أثاث"],
                "pattern_en": ["bought.*asset", "purchase.*equipment", "bought.*machine"],
                "entries": [
                    {"type": "debit", "account_key": "fixed_assets"},
                    {"type": "credit", "account_key": "cash_or_bank"}
                ]
            },
            "utility_payment": {
                "name": "Utility Payment",
                "name_ar": "دفع مرافق",
                "pattern_ar": ["دفع.*كهرباء", "دفع.*مياه", "دفع.*غاز", "مصروف.*مرافق"],
                "pattern_en": ["paid.*electricity", "paid.*utilities", "utility bill"],
                "entries": [
                    {"type": "debit", "account_key": "utilities_expense"},
                    {"type": "credit", "account_key": "cash_or_bank"}
                ]
            }
        }
    
    def match_transaction(self, text: str, language: str = "ar") -> Optional[Dict]:
        """
        Match transaction text against rules.
        
        Args:
            text: Transaction description
            language: 'ar' or 'en'
            
        Returns:
            Matching rule or None
        """
        text_lower = text.lower()
        
        for rule_key, rule_data in self.rules.items():
            patterns = rule_data.get(f"pattern_{language}", [])
            for pattern in patterns:
                # Use regex matching for patterns with special chars
                if '.*' in pattern or '+' in pattern:
                    if re.search(pattern, text_lower):
                        return {
                            "rule_key": rule_key,
                            "name": rule_data["name"],
                            "name_ar": rule_data["name_ar"],
                            "entries": rule_data["entries"]
                        }
                else:
                    # Simple substring match
                    if pattern in text_lower:
                        return {
                            "rule_key": rule_key,
                            "name": rule_data["name"],
                            "name_ar": rule_data["name_ar"],
                            "entries": rule_data["entries"]
                        }
        
        return None
    
    def get_default_accounts(self, rule_key: str) -> List[Dict]:
        """Get default account mappings for a rule."""
        rule = self.rules.get(rule_key)
        if rule:
            return rule["entries"]
        return []


# Global instances
validator = AccountingValidator()
rules_engine = RulesEngine()


def create_journal_entry(
    description: str,
    entry_date: date,
    lines: List[JournalLineData],
    reference: Optional[str] = None,
    **kwargs
) -> Tuple[Optional[JournalEntryData], List[str]]:
    """
    Create and validate a journal entry.
    
    Returns:
        Tuple of (JournalEntryData or None, list of errors)
    """
    entry = JournalEntryData(
        description=description,
        entry_date=entry_date,
        lines=lines,
        reference=reference,
        **kwargs
    )
    
    is_valid, errors = validator.validate_entry(entry)
    
    if is_valid:
        return entry, []
    else:
        return None, errors
