# Finovate Journal AI - Rules Engine

"""
Accounting Rules Engine for automatic journal entry generation.
Implements hybrid accounting logic without relying solely on AI.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from decimal import Decimal
import re


@dataclass
class AccountingRule:
    """Represents an accounting rule for transaction classification."""
    id: str
    name_ar: str
    name_en: str
    keywords_ar: List[str]
    keywords_en: List[str]
    debit_account_code: str
    credit_account_code: str
    description_ar: str = ""
    description_en: str = ""
    priority: int = 1
    tax_applicable: bool = False
    
    def matches(self, text: str, language: str = "ar") -> bool:
        """Check if text matches rule keywords."""
        keywords = self.keywords_ar if language == "ar" else self.keywords_en
        text_lower = text.lower()
        return any(kw.lower() in text_lower for kw in keywords)


class RulesEngine:
    """Engine for applying accounting rules to transactions."""
    
    def __init__(self):
        self.rules: List[AccountingRule] = []
        self._load_default_rules()
    
    def _load_default_rules(self):
        """Load default accounting rules for Egyptian accounting."""
        
        # Purchase rules
        self.rules.append(AccountingRule(
            id="PURCHASE_CASH",
            name_ar="شراء نقدي",
            name_en="Cash Purchase",
            keywords_ar=["شراء", "اشتريت", "اشترى", "مشتريات", "بضاعة"],
            keywords_en=["purchase", "bought", "buy", "purchases", "goods"],
            debit_account_code="5101",  # Purchases
            credit_account_code="1101",  # Cash
            description_ar="شراء بضاعة نقدًا",
            description_en="Cash purchase of goods",
            priority=10,
            tax_applicable=True
        ))
        
        self.rules.append(AccountingRule(
            id="PURCHASE_CREDIT",
            name_ar="شراء آجل",
            name_en="Credit Purchase",
            keywords_ar=["شراء", "اشتريت", "آجل", "أجل", "على الحساب"],
            keywords_en=["purchase", "bought", "credit", "on account"],
            debit_account_code="5101",  # Purchases
            credit_account_code="2101",  # Suppliers
            description_ar="شراء بضاعة على الحساب",
            description_en="Credit purchase of goods",
            priority=10,
            tax_applicable=True
        ))
        
        # Sales rules
        self.rules.append(AccountingRule(
            id="SALE_CASH",
            name_ar="بيع نقدي",
            name_en="Cash Sale",
            keywords_ar=["بيع", "بعت", "باع", "مبيعات"],
            keywords_en=["sale", "sold", "sell", "sales"],
            debit_account_code="1101",  # Cash
            credit_account_code="4101",  # Sales
            description_ar="بيع بضاعة نقدًا",
            description_en="Cash sale of goods",
            priority=10,
            tax_applicable=True
        ))
        
        self.rules.append(AccountingRule(
            id="SALE_CREDIT",
            name_ar="بيع آجل",
            name_en="Credit Sale",
            keywords_ar=["بيع", "بعت", "آجل", "أجل", "على الحساب", "للعميل"],
            keywords_en=["sale", "sold", "credit", "on account", "to customer"],
            debit_account_code="1103",  # Customers
            credit_account_code="4101",  # Sales
            description_ar="بيع بضاعة على الحساب",
            description_en="Credit sale of goods",
            priority=10,
            tax_applicable=True
        ))
        
        # Payment rules
        self.rules.append(AccountingRule(
            id="PAY_RENT",
            name_ar="دفع إيجار",
            name_en="Pay Rent",
            keywords_ar=["إيجار", "كراء", "دفعت إيجار", "سددت إيجار"],
            keywords_en=["rent", "paid rent", "lease"],
            debit_account_code="5201",  # Rent Expense
            credit_account_code="1101",  # Cash or 1102 Bank
            description_ar="دفع مصروف الإيجار",
            description_en="Payment of rent expense",
            priority=8
        ))
        
        self.rules.append(AccountingRule(
            id="PAY_SALARIES",
            name_ar="دفع رواتب",
            name_en="Pay Salaries",
            keywords_ar=["رواتب", "أجور", "مرتبات", "مصروف الرواتب"],
            keywords_en=["salaries", "wages", "payroll", "salary expense"],
            debit_account_code="5301",  # Salaries Expense
            credit_account_code="1101",  # Cash or 1102 Bank
            description_ar="دفع مصروف الرواتب",
            description_en="Payment of salaries expense",
            priority=8
        ))
        
        self.rules.append(AccountingRule(
            id="PAY_SUPPLIER",
            name_ar="سداد مورد",
            name_en="Pay Supplier",
            keywords_ar=["سددت للمورد", "دفعت للمورد", "سداد مورد", "تسوية مورد"],
            keywords_en=["paid supplier", "settle supplier", "pay vendor"],
            debit_account_code="2101",  # Suppliers
            credit_account_code="1101",  # Cash or 1102 Bank
            description_ar="سداد حساب المورد",
            description_en="Payment to supplier",
            priority=7
        ))
        
        # Collection rules
        self.rules.append(AccountingRule(
            id="COLLECT_CUSTOMER",
            name_ar="تحصيل من عميل",
            name_en="Collect from Customer",
            keywords_ar=["استلمت من العميل", "تحصيل من عميل", "قبض من العميل"],
            keywords_en=["received from customer", "collect from customer", "customer payment"],
            debit_account_code="1101",  # Cash or 1102 Bank
            credit_account_code="1103",  # Customers
            description_ar="تحصيل مستحقات من العميل",
            description_en="Collection from customer",
            priority=7
        ))
        
        # Fixed Asset rules
        self.rules.append(AccountingRule(
            id="BUY_FIXED_ASSET",
            name_ar="شراء أصل ثابت",
            name_en="Buy Fixed Asset",
            keywords_ar=["أصل ثابت", "جهاز", "كمبيوتر", "سيارة", "أثاث", "معدات"],
            keywords_en=["fixed asset", "computer", "car", "furniture", "equipment", "asset"],
            debit_account_code="1301",  # Fixed Assets
            credit_account_code="1101",  # Cash or 1102 Bank
            description_ar="شراء أصل ثابت",
            description_en="Purchase of fixed asset",
            priority=5,
            tax_applicable=True
        ))
        
        # Utility expenses
        self.rules.append(AccountingRule(
            id="PAY_UTILITIES",
            name_ar="دفع مرافق",
            name_en="Pay Utilities",
            keywords_ar=["كهرباء", "ماء", "غاز", "اتصالات", "إنترنت", "تليفون"],
            keywords_en=["electricity", "water", "gas", "utilities", "phone", "internet"],
            debit_account_code="5202",  # Utilities Expense
            credit_account_code="1101",  # Cash or 1102 Bank
            description_ar="دفع مصروف المرافق",
            description_en="Payment of utilities expense",
            priority=6
        ))
    
    def find_matching_rules(self, text: str, language: str = "ar") -> List[AccountingRule]:
        """Find all rules that match the given text."""
        matching = []
        for rule in sorted(self.rules, key=lambda r: r.priority, reverse=True):
            if rule.matches(text, language):
                matching.append(rule)
        return matching
    
    def get_best_rule(self, text: str, language: str = "ar") -> Optional[AccountingRule]:
        """Get the best matching rule for the given text."""
        matching = self.find_matching_rules(text, language)
        return matching[0] if matching else None
    
    def suggest_accounts(self, text: str, language: str = "ar") -> Tuple[Optional[str], Optional[str]]:
        """Suggest debit and credit account codes based on text."""
        rule = self.get_best_rule(text, language)
        if rule:
            return rule.debit_account_code, rule.credit_account_code
        return None, None
    
    def is_tax_applicable(self, text: str, language: str = "ar") -> bool:
        """Check if tax should be applied to this transaction."""
        rule = self.get_best_rule(text, language)
        return rule.tax_applicable if rule else False


# Global instance
rules_engine = RulesEngine()
