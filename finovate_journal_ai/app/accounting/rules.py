"""
Finovate Journal AI - Accounting Rules Engine

This module implements the rule-based accounting engine that maps
transaction types to journal entries without requiring AI.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from decimal import Decimal
import logging

from app.utils.logging_config import get_logger

logger = get_logger(__name__)


@dataclass
class JournalEntryLine:
    """Represents a single line in a journal entry"""
    account_code: str
    account_name: str
    debit: Decimal = Decimal("0.00")
    credit: Decimal = Decimal("0.00")
    description: str = ""


@dataclass
class AccountingRule:
    """
    Represents an accounting rule for transaction classification
    
    Attributes:
        id: Unique rule identifier
        name: Rule name
        keywords: Keywords that trigger this rule (Arabic and English)
        transaction_type: Type of transaction
        debit_account: Account to debit
        credit_account: Account to credit
        priority: Rule priority (higher = checked first)
        enabled: Whether rule is active
    """
    id: str
    name: str
    keywords: List[str]
    transaction_type: str
    debit_account: str  # Account code
    credit_account: str  # Account code
    priority: int = 100
    enabled: bool = True
    tax_applicable: bool = False
    tax_account: Optional[str] = None
    description: str = ""
    
    def matches(self, text: str) -> bool:
        """Check if the input text matches this rule's keywords"""
        text_lower = text.lower()
        for keyword in self.keywords:
            if keyword.lower() in text_lower:
                return True
        return False


class RuleEngine:
    """
    Rule-based accounting engine that matches transactions to accounts
    
    This engine uses predefined rules to determine the appropriate
    debit and credit accounts for common accounting transactions.
    """
    
    def __init__(self):
        self.rules: List[AccountingRule] = []
        self._initialize_default_rules()
        logger.info("RuleEngine initialized with %d default rules", len(self.rules))
    
    def _initialize_default_rules(self) -> None:
        """Initialize with default accounting rules for Egyptian accounting"""
        
        # Purchase Rules / قواعد المشتريات
        self.add_rule(AccountingRule(
            id="PURCHASE_CASH",
            name="Cash Purchase",
            keywords=[
                "شراء بضاعة نقدًا", "شراء بضاعة نقدا", "شراء نقدًا", "شراء نقدا",
                "purchased goods for cash", "cash purchase", "bought for cash"
            ],
            transaction_type="purchase_cash",
            debit_account="5101",  # Purchases / المشتريات
            credit_account="1101",  # Cash / الصندوق
            priority=10,
            tax_applicable=True,
            tax_account="1106",  # Input VAT / ضريبة قيمة مضافة مدخلة
            description="شراء بضاعة ودفع نقدًا"
        ))
        
        self.add_rule(AccountingRule(
            id="PURCHASE_CREDIT",
            name="Credit Purchase",
            keywords=[
                "شراء بضاعة آجل", "شراء بضاعة اجل", "شراء من مورد", "اشترى من",
                "purchased on credit", "credit purchase", "bought from supplier"
            ],
            transaction_type="purchase_credit",
            debit_account="5101",  # Purchases
            credit_account="2101",  # Suppliers / الموردون
            priority=10,
            tax_applicable=True,
            tax_account="1106",
            description="شراء بضاعة على الحساب"
        ))
        
        # Sales Rules / قواعد المبيعات
        self.add_rule(AccountingRule(
            id="SALE_CASH",
            name="Cash Sale",
            keywords=[
                "بيع بضاعة نقدًا", "بيع بضاعة نقدا", "بيع نقدًا", "بيع نقدا",
                "sold goods for cash", "cash sale", "sale for cash"
            ],
            transaction_type="sale_cash",
            debit_account="1101",  # Cash
            credit_account="4101",  # Sales / المبيعات
            priority=10,
            tax_applicable=True,
            tax_account="2103",  # Output VAT / ضريبة قيمة مضافة خرجة
            description="بيع بضاعة مقابل نقد"
        ))
        
        self.add_rule(AccountingRule(
            id="SALE_CREDIT",
            name="Credit Sale",
            keywords=[
                "بيع بضاعة آجل", "بيع بضاعة اجل", "بيع للعميل", "باع للعميل",
                "sold on credit", "credit sale", "sale to customer"
            ],
            transaction_type="sale_credit",
            debit_account="1103",  # Customers / العملاء
            credit_account="4101",  # Sales
            priority=10,
            tax_applicable=True,
            tax_account="2103",
            description="بيع بضاعة على الحساب"
        ))
        
        # Payment Rules / قواعد الدفع
        self.add_rule(AccountingRule(
            id="PAY_RENT",
            name="Rent Payment",
            keywords=[
                "دفع إيجار", "دفع ايجار", "سداد إيجار", "سداد ايجار",
                "paid rent", "rent payment", "pay rent"
            ],
            transaction_type="expense_rent",
            debit_account="5201",  # Rent Expense / مصروف إيجار
            credit_account="1101",  # Cash (default, can be bank)
            priority=20,
            description="دفع مصروف إيجار"
        ))
        
        self.add_rule(AccountingRule(
            id="PAY_SALARY",
            name="Salary Payment",
            keywords=[
                "دفع رواتب", "دفع راتب", "سداد رواتب", "صرف رواتب",
                "paid salaries", "salary payment", "payroll"
            ],
            transaction_type="expense_salary",
            debit_account="5301",  # Salaries Expense / مصروف رواتب
            credit_account="1101",  # Cash
            priority=20,
            description="دفع مصروف رواتب"
        ))
        
        self.add_rule(AccountingRule(
            id="PAY_SUPPLIER",
            name="Supplier Payment",
            keywords=[
                "سداد مورد", "دفع لمورد", "تحويل للمورد", "دفع لشركة",
                "paid supplier", "supplier payment", "settle supplier"
            ],
            transaction_type="supplier_payment",
            debit_account="2101",  # Suppliers
            credit_account="1101",  # Cash (or bank)
            priority=15,
            description="سداد مستحقات مورد"
        ))
        
        # Collection Rules / قواعد التحصيل
        self.add_rule(AccountingRule(
            id="COLLECT_CUSTOMER",
            name="Customer Collection",
            keywords=[
                "استلم من عميل", "تحصيل من عميل", "قبض من عميل", "استلام من",
                "استلمت من العميل", "تحصيل مستحقات",
                "received from customer", "customer collection", "collected from"
            ],
            transaction_type="customer_collection",
            debit_account="1101",  # Cash
            credit_account="1103",  # Customers
            priority=15,
            description="تحصيل مستحقات من عميل"
        ))
        
        # Bank Rules / قواعد البنك
        self.add_rule(AccountingRule(
            id="DEPOSIT_BANK",
            name="Bank Deposit",
            keywords=[
                "إيداع في البنك", "ايداع في البنك", "تحويل للبنك", "إيداع بنكي",
                "bank deposit", "deposited to bank", "transfer to bank"
            ],
            transaction_type="bank_deposit",
            debit_account="1102",  # Bank / البنك
            credit_account="1101",  # Cash
            priority=25,
            description="إيداع نقدي في البنك"
        ))
        
        self.add_rule(AccountingRule(
            id="WITHDRAW_BANK",
            name="Bank Withdrawal",
            keywords=[
                "سحب من البنك", "سحب بنكي", "تحويل من البنك",
                "bank withdrawal", "withdrew from bank", "transfer from bank"
            ],
            transaction_type="bank_withdrawal",
            debit_account="1101",  # Cash
            credit_account="1102",  # Bank
            priority=25,
            description="سحب نقدي من البنك"
        ))
        
        # Utility Rules / قواعد المصروفات
        self.add_rule(AccountingRule(
            id="PAY_UTILITY",
            name="Utility Payment",
            keywords=[
                "دفع كهرباء", "سداد كهرباء", "فاتورة كهرباء",
                "دفع مياه", "دفع غاز", "دفع هاتف", "دفع انترنت",
                "paid electricity", "utility payment", "phone bill", "internet bill"
            ],
            transaction_type="expense_utility",
            debit_account="5202",  # Utilities Expense / مصروف مرافق
            credit_account="1101",  # Cash
            priority=30,
            description="دفع مصروف مرافق"
        ))
        
        # Fixed Asset Rules / قواعد الأصول الثابتة
        self.add_rule(AccountingRule(
            id="PURCHASE_ASSET",
            name="Fixed Asset Purchase",
            keywords=[
                "شراء أصل ثابت", "شراء جهاز", "شراء أثاث", "شراء سيارة",
                "شراء كمبيوتر", "شراء معدات",
                "purchased asset", "bought equipment", "fixed asset"
            ],
            transaction_type="asset_purchase",
            debit_account="1301",  # Fixed Assets / أصول ثابتة
            credit_account="1101",  # Cash
            priority=35,
            tax_applicable=True,
            tax_account="1106",
            description="شراء أصل ثابت"
        ))
        
        # Capital Rules / قواعد رأس المال
        self.add_rule(AccountingRule(
            id="CAPITAL_INJECTION",
            name="Capital Injection",
            keywords=[
                "إيداع رأس مال", "ايداع رأس مال", "زيادة رأس المال",
                "capital injection", "owner investment", "capital contribution"
            ],
            transaction_type="capital_injection",
            debit_account="1101",  # Cash
            credit_account="3101",  # Capital / رأس المال
            priority=40,
            description="إيداع رأس مال"
        ))
        
        logger.debug("Initialized %d default accounting rules", len(self.rules))
    
    def add_rule(self, rule: AccountingRule) -> None:
        """Add a new accounting rule"""
        self.rules.append(rule)
        # Sort by priority (lower number = higher priority)
        self.rules.sort(key=lambda r: r.priority)
        logger.debug("Added rule: %s", rule.id)
    
    def remove_rule(self, rule_id: str) -> bool:
        """Remove a rule by ID"""
        for i, rule in enumerate(self.rules):
            if rule.id == rule_id:
                self.rules.pop(i)
                logger.debug("Removed rule: %s", rule_id)
                return True
        return False
    
    def match_transaction(self, text: str) -> Optional[AccountingRule]:
        """
        Find the best matching rule for a transaction description
        
        Args:
            text: Transaction description in Arabic or English
            
        Returns:
            Best matching AccountingRule or None if no match
        """
        for rule in self.rules:
            if rule.enabled and rule.matches(text):
                logger.debug("Matched rule '%s' for text: %s", rule.id, text[:50])
                return rule
        
        logger.debug("No matching rule found for text: %s", text[:50])
        return None
    
    def get_all_rules(self) -> List[AccountingRule]:
        """Get all accounting rules"""
        return self.rules.copy()
    
    def get_enabled_rules(self) -> List[AccountingRule]:
        """Get only enabled rules"""
        return [r for r in self.rules if r.enabled]
    
    def suggest_accounts(
        self, 
        text: str, 
        amount: Decimal
    ) -> Tuple[Optional[AccountingRule], List[JournalEntryLine]]:
        """
        Suggest journal entry lines based on transaction text
        
        Args:
            text: Transaction description
            amount: Transaction amount
            
        Returns:
            Tuple of (matched_rule, journal_lines)
        """
        rule = self.match_transaction(text)
        
        if not rule:
            return None, []
        
        lines = []
        
        # Handle tax if applicable
        if rule.tax_applicable and rule.tax_account:
            # Assume amount includes tax, calculate base and tax
            tax_rate = Decimal("0.14")  # Default 14% VAT
            base_amount = amount / (1 + tax_rate)
            tax_amount = amount - base_amount
            
            # Debit: Main account (e.g., Purchases)
            lines.append(JournalEntryLine(
                account_code=rule.debit_account,
                account_name=f"Account {rule.debit_account}",
                debit=base_amount,
                credit=Decimal("0.00"),
                description=rule.description
            ))
            
            # Debit: Tax account
            lines.append(JournalEntryLine(
                account_code=rule.tax_account,
                account_name=f"Tax Account {rule.tax_account}",
                debit=tax_amount,
                credit=Decimal("0.00"),
                description="VAT"
            ))
            
            # Credit: Payment account
            lines.append(JournalEntryLine(
                account_code=rule.credit_account,
                account_name=f"Account {rule.credit_account}",
                debit=Decimal("0.00"),
                credit=amount,
                description=rule.description
            ))
        else:
            # Simple entry without tax
            lines.append(JournalEntryLine(
                account_code=rule.debit_account,
                account_name=f"Account {rule.debit_account}",
                debit=amount,
                credit=Decimal("0.00"),
                description=rule.description
            ))
            
            lines.append(JournalEntryLine(
                account_code=rule.credit_account,
                account_name=f"Account {rule.credit_account}",
                debit=Decimal("0.00"),
                credit=amount,
                description=rule.description
            ))
        
        return rule, lines


# Global rule engine instance
_rule_engine: Optional[RuleEngine] = None


def get_rule_engine() -> RuleEngine:
    """Get or create the global rule engine instance"""
    global _rule_engine
    if _rule_engine is None:
        _rule_engine = RuleEngine()
    return _rule_engine
