"""
Finovate Journal AI - Accounting Rules Engine

Developer: Ahmed Mostafa Ibrahim
Brand: Finovate – AHMED EG
"""

from decimal import Decimal
from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass, field


@dataclass
class AccountingRule:
    """Represents an accounting rule."""
    id: str
    name_ar: str
    name_en: str
    description_ar: str
    description_en: str
    pattern_keywords_ar: List[str]
    pattern_keywords_en: List[str]
    debit_account_type: str  # e.g., "expense", "asset"
    credit_account_type: str  # e.g., "cash", "liability"
    default_debit_account: Optional[str] = None  # Account code or name
    default_credit_account: Optional[str] = None
    tax_applicable: bool = False
    priority: int = 1
    
    def matches(self, text_ar: str, text_en: str) -> bool:
        """Check if the rule matches the given text."""
        text_combined = f"{text_ar} {text_en}".lower()
        
        # Check Arabic keywords
        for keyword in self.pattern_keywords_ar:
            if keyword.lower() in text_combined:
                return True
        
        # Check English keywords
        for keyword in self.pattern_keywords_en:
            if keyword.lower() in text_combined:
                return True
        
        return False


def get_default_rules() -> List[AccountingRule]:
    """Get the default set of accounting rules."""
    
    rules = [
        # Cash Purchase
        AccountingRule(
            id="CASH_PURCHASE",
            name_ar="شراء نقدي",
            name_en="Cash Purchase",
            description_ar="شراء بضاعة أو مصروفات نقدًا",
            description_en="Purchase of goods or expenses paid in cash",
            pattern_keywords_ar=["شراء", "اشتريت", "مشتريات"],
            pattern_keywords_en=["purchase", "bought", "buy"],
            debit_account_type="expense",
            credit_account_type="asset",
            default_debit_account="5101",  # Purchases
            default_credit_account="1101",  # Cash
            tax_applicable=True,
            priority=10,
        ),
        
        # Credit Purchase
        AccountingRule(
            id="CREDIT_PURCHASE",
            name_ar="شراء آجل",
            name_en="Credit Purchase",
            description_ar="شراء بضاعة أو مصروفات على الحساب",
            description_en="Purchase of goods or expenses on credit",
            pattern_keywords_ar=["آجل", "على الحساب", "ذمم"],
            pattern_keywords_en=["credit", "on account", "payable"],
            debit_account_type="expense",
            credit_account_type="liability",
            default_debit_account="5101",  # Purchases
            default_credit_account="2101",  # Suppliers
            tax_applicable=True,
            priority=9,
        ),
        
        # Cash Sale
        AccountingRule(
            id="CASH_SALE",
            name_ar="بيع نقدي",
            name_en="Cash Sale",
            description_ar="بيع بضاعة أو إيرادات نقدًا",
            description_en="Sale of goods or revenue received in cash",
            pattern_keywords_ar=["بيع", "بعت", "مبيعات", "استلمت نقدًا"],
            pattern_keywords_en=["sale", "sold", "sell", "received cash"],
            debit_account_type="asset",
            credit_account_type="revenue",
            default_debit_account="1101",  # Cash
            default_credit_account="4101",  # Sales
            tax_applicable=True,
            priority=10,
        ),
        
        # Credit Sale
        AccountingRule(
            id="CREDIT_SALE",
            name_ar="بيع آجل",
            name_en="Credit Sale",
            description_ar="بيع بضاعة أو إيرادات على الحساب",
            description_en="Sale of goods or revenue on credit",
            pattern_keywords_ar=["بيع آجل", "على الحساب", "عملاء"],
            pattern_keywords_en=["credit sale", "on account", "receivable"],
            debit_account_type="asset",
            credit_account_type="revenue",
            default_debit_account="1103",  # Customers
            default_credit_account="4101",  # Sales
            tax_applicable=True,
            priority=9,
        ),
        
        # Cash Payment (Expense)
        AccountingRule(
            id="CASH_PAYMENT",
            name_ar="دفع نقدي",
            name_en="Cash Payment",
            description_ar="دفع مصروف نقدًا",
            description_en="Payment of expense in cash",
            pattern_keywords_ar=["دفعت", "دفع", "مصروف", "صرف"],
            pattern_keywords_en=["paid", "payment", "expense", "pay"],
            debit_account_type="expense",
            credit_account_type="asset",
            default_debit_account="5901",  # General Expense
            default_credit_account="1101",  # Cash
            tax_applicable=False,
            priority=8,
        ),
        
        # Bank Payment
        AccountingRule(
            id="BANK_PAYMENT",
            name_ar="دفع بنكي",
            name_en="Bank Payment",
            description_ar="دفع من البنك",
            description_en="Payment from bank",
            pattern_keywords_ar=["من البنك", "تحويل بنكي", "شيك"],
            pattern_keywords_en=["bank", "transfer", "check", "cheque"],
            debit_account_type="expense",
            credit_account_type="asset",
            default_debit_account="5901",  # General Expense
            default_credit_account="1102",  # Bank
            tax_applicable=False,
            priority=8,
        ),
        
        # Cash Receipt from Customer
        AccountingRule(
            id="CASH_RECEIPT",
            name_ar="قبض نقدي",
            name_en="Cash Receipt",
            description_ar="استلام نقدًا من عميل",
            description_en="Cash receipt from customer",
            pattern_keywords_ar=["استلمت", "قبض", "تحصيل"],
            pattern_keywords_en=["received", "receipt", "collect", "collection"],
            debit_account_type="asset",
            credit_account_type="asset",
            default_debit_account="1101",  # Cash
            default_credit_account="1103",  # Customers
            tax_applicable=False,
            priority=9,
        ),
        
        # Rent Payment
        AccountingRule(
            id="RENT_PAYMENT",
            name_ar="دفع إيجار",
            name_en="Rent Payment",
            description_ar="دفع إيجار المكتب أو المقر",
            description_en="Payment of office rent",
            pattern_keywords_ar=["إيجار", "كراء", "ايجار"],
            pattern_keywords_en=["rent", "lease"],
            debit_account_type="expense",
            credit_account_type="asset",
            default_debit_account="5201",  # Rent Expense
            default_credit_account="1101",  # Cash
            tax_applicable=False,
            priority=10,
        ),
        
        # Salary Payment
        AccountingRule(
            id="SALARY_PAYMENT",
            name_ar="دفع رواتب",
            name_en="Salary Payment",
            description_ar="دفع رواتب الموظفين",
            description_en="Payment of employee salaries",
            pattern_keywords_ar=["راتب", "رواتب", "أجور", "مرتبات"],
            pattern_keywords_en=["salary", "salaries", "wages", "payroll"],
            debit_account_type="expense",
            credit_account_type="asset",
            default_debit_account="5301",  # Salaries Expense
            default_credit_account="1101",  # Cash
            tax_applicable=False,
            priority=10,
        ),
        
        # Fixed Asset Purchase
        AccountingRule(
            id="FIXED_ASSET_PURCHASE",
            name_ar="شراء أصل ثابت",
            name_en="Fixed Asset Purchase",
            description_ar="شراء جهاز أو أثاث أو سيارة",
            description_en="Purchase of fixed asset",
            pattern_keywords_ar=["جهاز", "كمبيوتر", "أثاث", "سيارة", "أصل ثابت"],
            pattern_keywords_en=["computer", "furniture", "car", "vehicle", "fixed asset", "equipment"],
            debit_account_type="asset",
            credit_account_type="asset",
            default_debit_account="1601",  # Fixed Assets
            default_credit_account="1101",  # Cash
            tax_applicable=True,
            priority=7,
        ),
        
        # Supplier Payment
        AccountingRule(
            id="SUPPLIER_PAYMENT",
            name_ar="سداد مورد",
            name_en="Supplier Payment",
            description_ar="سداد مستحقات مورد",
            description_en="Payment to supplier",
            pattern_keywords_ar=["سددت للمورد", "دفعت للمورد", "سداد مورد"],
            pattern_keywords_en=["paid supplier", "supplier payment", "vendor payment"],
            debit_account_type="liability",
            credit_account_type="asset",
            default_debit_account="2101",  # Suppliers
            default_credit_account="1101",  # Cash
            tax_applicable=False,
            priority=9,
        ),
    ]
    
    # Sort by priority (higher priority first)
    rules.sort(key=lambda r: r.priority, reverse=True)
    
    return rules


class RuleEngine:
    """
    Accounting Rule Engine.
    
    Matches transaction descriptions against predefined rules
    to suggest appropriate debit and credit accounts.
    """
    
    def __init__(self, custom_rules: Optional[List[AccountingRule]] = None):
        self.rules = custom_rules if custom_rules else get_default_rules()
    
    def add_rule(self, rule: AccountingRule):
        """Add a custom rule."""
        self.rules.append(rule)
        # Re-sort by priority
        self.rules.sort(key=lambda r: r.priority, reverse=True)
    
    def remove_rule(self, rule_id: str):
        """Remove a rule by ID."""
        self.rules = [r for r in self.rules if r.id != rule_id]
    
    def match(self, text_ar: str = "", text_en: str = "") -> Optional[AccountingRule]:
        """
        Find the best matching rule for the given text.
        
        Returns the first matching rule (highest priority).
        """
        for rule in self.rules:
            if rule.matches(text_ar, text_en):
                return rule
        return None
    
    def match_all(self, text_ar: str = "", text_en: str = "") -> List[AccountingRule]:
        """Find all matching rules."""
        return [rule for rule in self.rules if rule.matches(text_ar, text_en)]
    
    def suggest_entry(self, text_ar: str = "", text_en: str = "", 
                     amount: Decimal = Decimal("0.00"),
                     tax_rate: Decimal = Decimal("0.00")) -> Dict[str, Any]:
        """
        Suggest a journal entry based on rules.
        
        Returns a dictionary with suggested accounts and explanation.
        """
        rule = self.match(text_ar, text_en)
        
        if not rule:
            return {
                "matched": False,
                "rule": None,
                "suggestion": None,
                "confidence": 0.0,
                "explanation_ar": "لم يتم العثور على قاعدة محاسبية مطابقة",
                "explanation_en": "No matching accounting rule found",
            }
        
        # Build suggestion
        lines = []
        
        # Calculate amounts
        base_amount = amount
        tax_amount = Decimal("0.00")
        
        if rule.tax_applicable and tax_rate > 0:
            tax_amount = base_amount * (tax_rate / Decimal("100"))
        
        # Debit line
        lines.append({
            "account_type": rule.debit_account_type,
            "account_code": rule.default_debit_account,
            "debit": base_amount,
            "credit": Decimal("0.00"),
            "description_ar": rule.description_ar,
            "description_en": rule.description_en,
        })
        
        # Tax line (if applicable)
        if tax_amount > 0:
            lines.append({
                "account_type": "asset",  # Input VAT
                "account_code": "1151",  # Input VAT
                "debit": tax_amount,
                "credit": Decimal("0.00"),
                "description_ar": "ضريبة قيمة مضافة مدخلة",
                "description_en": "Input VAT",
            })
        
        # Credit line
        total_credit = base_amount + tax_amount
        lines.append({
            "account_type": rule.credit_account_type,
            "account_code": rule.default_credit_account,
            "debit": Decimal("0.00"),
            "credit": total_credit,
            "description_ar": rule.description_ar,
            "description_en": rule.description_en,
        })
        
        return {
            "matched": True,
            "rule": {
                "id": rule.id,
                "name_ar": rule.name_ar,
                "name_en": rule.name_en,
            },
            "suggestion": {
                "lines": lines,
                "total_debit": sum(l["debit"] for l in lines),
                "total_credit": sum(l["credit"] for l in lines),
            },
            "confidence": 0.85,  # Base confidence for rule-based match
            "explanation_ar": f"تم تطبيق قاعدة: {rule.name_ar}. {rule.description_ar}",
            "explanation_en": f"Applied rule: {rule.name_en}. {rule.description_en}",
        }
