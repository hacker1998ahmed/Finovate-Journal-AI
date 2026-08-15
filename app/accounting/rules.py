"""Accounting rules engine for Finovate Journal AI."""

from typing import List, Dict, Any, Optional
from decimal import Decimal
import re

from ..config.constants import ACCOUNT_TYPES, NORMAL_BALANCES


class AccountingRule:
    """Represents a single accounting rule."""

    def __init__(
        self,
        name: str,
        name_ar: str,
        patterns: List[str],
        patterns_ar: List[str],
        debit_account: str,
        credit_account: str,
        description: str,
        description_ar: str,
    ):
        self.name = name
        self.name_ar = name_ar
        self.patterns = patterns
        self.patterns_ar = patterns_ar
        self.debit_account = debit_account
        self.credit_account = credit_account
        self.description = description
        self.description_ar = description_ar

    def matches(self, text: str, language: str = "ar") -> bool:
        """Check if the rule matches the given text."""
        patterns = self.patterns_ar if language == "ar" else self.patterns
        text_lower = text.lower()
        
        for pattern in patterns:
            if pattern.lower() in text_lower:
                return True
        return False


class RulesEngine:
    """Accounting rules engine for transaction classification."""

    def __init__(self):
        self.rules: List[AccountingRule] = []
        self._load_default_rules()

    def _load_default_rules(self) -> None:
        """Load default accounting rules."""
        
        # Cash Purchase of Goods
        self.rules.append(AccountingRule(
            name="cash_purchase",
            name_ar="شراء نقدي",
            patterns=["cash purchase", "purchased goods for cash", "bought for cash"],
            patterns_ar=["شراء بضاعة نقدًا", "اشتريت بضاعة نقد", "شراء نقدى"],
            debit_account="purchases",
            credit_account="cash",
            description="Cash purchase of goods",
            description_ar="شراء بضاعة دفع نقد",
        ))

        # Credit Purchase of Goods
        self.rules.append(AccountingRule(
            name="credit_purchase",
            name_ar="شراء آجل",
            patterns=["credit purchase", "purchased on account", "bought on credit"],
            patterns_ar=["شراء بضاعة آجل", "اشتريت بضاعة على الحساب", "شراء أجل"],
            debit_account="purchases",
            credit_account="suppliers",
            description="Credit purchase of goods",
            description_ar="شراء بضاعة على الحساب",
        ))

        # Cash Sale
        self.rules.append(AccountingRule(
            name="cash_sale",
            name_ar="بيع نقدي",
            patterns=["cash sale", "sold for cash", "received cash for sale"],
            patterns_ar=["بيع بضاعة نقدًا", "بعت بضاعة نقد", "بيع نقدى"],
            debit_account="cash",
            credit_account="sales",
            description="Cash sale of goods",
            description_ar="بيع بضاعة قبض نقد",
        ))

        # Credit Sale
        self.rules.append(AccountingRule(
            name="credit_sale",
            name_ar="بيع آجل",
            patterns=["credit sale", "sold on account", "sold on credit"],
            patterns_ar=["بيع بضاعة آجل", "بعت بضاعة على الحساب", "بيع أجل"],
            debit_account="customers",
            credit_account="sales",
            description="Credit sale of goods",
            description_ar="بيع بضاعة على الحساب",
        ))

        # Rent Payment
        self.rules.append(AccountingRule(
            name="rent_payment",
            name_ar="دفع إيجار",
            patterns=["paid rent", "rent payment", "office rent"],
            patterns_ar=["دفعت إيجار", "دفع إيجار", "إيجار المكتب"],
            debit_account="rent_expense",
            credit_account="cash",
            description="Rent payment",
            description_ar="دفع مصروف إيجار",
        ))

        # Salary Payment
        self.rules.append(AccountingRule(
            name="salary_payment",
            name_ar="دفع رواتب",
            patterns=["paid salaries", "salary payment", "wages paid"],
            patterns_ar=["دفعت رواتب", "دفع رواتب", "رواتب الموظفين"],
            debit_account="salaries_expense",
            credit_account="cash",
            description="Salary payment",
            description_ar="دفع مصروف رواتب",
        ))

        # Collection from Customer
        self.rules.append(AccountingRule(
            name="customer_collection",
            name_ar="تحصيل من عميل",
            patterns=["received from customer", "collected from", "customer payment"],
            patterns_ar=["استلمت من العميل", "تحصيل من عميل", "سداد عميل"],
            debit_account="cash",
            credit_account="customers",
            description="Collection from customer",
            description_ar="تحصيل نقد من عميل",
        ))

        # Payment to Supplier
        self.rules.append(AccountingRule(
            name="supplier_payment",
            name_ar="سداد لمورد",
            patterns=["paid to supplier", "payment to vendor", "settled supplier"],
            patterns_ar=["سددت للمورد", "دفع لمورد", "سداد مورد"],
            debit_account="suppliers",
            credit_account="cash",
            description="Payment to supplier",
            description_ar="سداد نقد لمورد",
        ))

        # Fixed Asset Purchase
        self.rules.append(AccountingRule(
            name="fixed_asset_purchase",
            name_ar="شراء أصل ثابت",
            patterns=["purchased equipment", "bought asset", "acquired fixed asset"],
            patterns_ar=["اشتريت جهاز", "شراء أصل ثابت", "شراء معدات"],
            debit_account="fixed_assets",
            credit_account="cash",
            description="Fixed asset purchase",
            description_ar="شراء أصل ثابت نقدًا",
        ))

        # Utility Payment
        self.rules.append(AccountingRule(
            name="utility_payment",
            name_ar="دفع مرافق",
            patterns=["paid electricity", "utilities payment", "water bill"],
            patterns_ar=["دفعت كهرباء", "مصروف كهرباء", "فاتورة مياه"],
            debit_account="utilities_expense",
            credit_account="cash",
            description="Utility payment",
            description_ar="دفع مصروف مرافق",
        ))

    def find_matching_rule(self, text: str, language: str = "ar") -> Optional[AccountingRule]:
        """Find the first matching rule for the given text."""
        for rule in self.rules:
            if rule.matches(text, language):
                return rule
        return None

    def get_all_rules(self) -> List[AccountingRule]:
        """Get all loaded rules."""
        return self.rules

    def add_rule(self, rule: AccountingRule) -> None:
        """Add a custom rule."""
        self.rules.append(rule)
