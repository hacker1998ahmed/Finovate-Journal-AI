"""NLP Parser for natural language accounting entries."""

from typing import Dict, Any, Optional, List, Tuple
from decimal import Decimal, InvalidOperation
import re
from datetime import datetime

from ..config.constants import DEFAULT_CURRENCY, CURRENCY_SYMBOLS
from .rules import RulesEngine, AccountingRule


class NLPParser:
    """Natural Language Parser for accounting transactions."""

    def __init__(self):
        self.rules_engine = RulesEngine()
        
        # Arabic number words mapping (simplified)
        self.arabic_numbers = {
            'صفر': 0, 'واحد': 1, 'اثنين': 2, 'ثلاثة': 3, 'أربعة': 4,
            'خمسة': 5, 'ستة': 6, 'سبعة': 7, 'ثمانية': 8, 'تسعة': 9,
            'عشرة': 10, 'مائة': 100, 'ألف': 1000,
        }
        
        # Currency patterns
        self.currency_patterns = [
            r'(\d+(?:,\d{3})*(?:\.\d+)?)\s*(جنيه|ج.م|EGP|LE|ريال|درهم|دولار)',
            r'(جنيه|ج.م|EGP|LE)\s*(\d+(?:,\d{3})*(?:\.\d+)?)',
        ]
        
        # Amount extraction patterns
        self.amount_patterns = [
            r'(\d+(?:,\d{3})*(?:\.\d+)?)',  # Numbers with commas and decimals
            r'(\d+)',  # Simple numbers
        ]

    def parse(self, text: str, language: Optional[str] = None) -> Dict[str, Any]:
        """
        Parse natural language text into structured accounting data.
        
        Returns:
            Dictionary with parsed transaction data
        """
        if language is None:
            language = self._detect_language(text)
        
        result = {
            "success": False,
            "language": language,
            "original_text": text,
            "transaction_type": None,
            "amount": None,
            "currency": DEFAULT_CURRENCY,
            "debit_account": None,
            "credit_account": None,
            "party": None,
            "payment_method": None,
            "tax_amount": None,
            "tax_rate": None,
            "confidence": 0,
            "ambiguities": [],
            "explanation": "",
            "explanation_ar": "",
            "rule_matched": None,
        }
        
        # Extract amount
        amount = self._extract_amount(text, language)
        if amount:
            result["amount"] = amount
            result["success"] = True
        
        # Extract currency
        currency = self._extract_currency(text, language)
        if currency:
            result["currency"] = currency
        
        # Find matching rule
        rule = self.rules_engine.find_matching_rule(text, language)
        if rule:
            result["rule_matched"] = rule.name
            result["debit_account"] = rule.debit_account
            result["credit_account"] = rule.credit_account
            result["transaction_type"] = rule.name
            result["explanation"] = rule.description
            result["explanation_ar"] = rule.description_ar
            result["confidence"] = min(95, 70 + len(rule.patterns_ar) * 5)
            result["success"] = True
            
            # Determine payment method
            result["payment_method"] = self._detect_payment_method(text, language)
            
            # Check for tax indicators
            tax_info = self._detect_tax(text, language, amount)
            if tax_info:
                result["tax_amount"] = tax_info.get("amount")
                result["tax_rate"] = tax_info.get("rate")
        else:
            # No rule matched - identify ambiguities
            result["confidence"] = 30
            result["ambiguities"].append("no_rule_matched")
            
            if not amount:
                result["ambiguities"].append("amount_not_found")
            
            result["explanation"] = "No matching accounting rule found. Please clarify the transaction."
            result["explanation_ar"] = "لم يتم العثور على قاعدة محاسبية مطابقة. يرجى توضيح العملية."
        
        return result

    def _detect_language(self, text: str) -> str:
        """Detect if text is Arabic or English."""
        arabic_chars = re.compile(r'[\u0600-\u06FF]')
        if arabic_chars.search(text):
            return "ar"
        return "en"

    def _extract_amount(self, text: str, language: str) -> Optional[Decimal]:
        """Extract monetary amount from text."""
        # Try to find numbers in the text
        for pattern in self.amount_patterns:
            matches = re.findall(pattern, text)
            if matches:
                for match in matches:
                    try:
                        # Remove commas and convert to Decimal
                        number_str = match.replace(',', '')
                        amount = Decimal(number_str)
                        if amount > 0:
                            return amount
                    except (InvalidOperation, ValueError):
                        continue
        return None

    def _extract_currency(self, text: str, language: str) -> Optional[str]:
        """Extract currency from text."""
        text_lower = text.lower()
        
        currency_map = {
            'جنيه': 'EGP',
            'ج.م': 'EGP',
            'egp': 'EGP',
            'le': 'EGP',
            'ريال': 'SAR',
            'درهم': 'AED',
            'دولار': 'USD',
            'dollar': 'USD',
            'euro': 'EUR',
            'يورو': 'EUR',
            'pound': 'GBP',
            'جنيه استرليني': 'GBP',
        }
        
        for key, value in currency_map.items():
            if key in text_lower:
                return value
        
        return DEFAULT_CURRENCY

    def _detect_payment_method(self, text: str, language: str) -> Optional[str]:
        """Detect payment method from text."""
        text_lower = text.lower()
        
        if language == "ar":
            if any(word in text_lower for word in ['نقدًا', 'نقد', 'كاش']):
                return "cash"
            elif any(word in text_lower for word in ['آجل', 'على الحساب', 'شيك', 'شوكة']):
                return "credit"
            elif any(word in text_lower for word in ['بنك', 'تحويل', 'شبكة']):
                return "bank"
        else:
            if any(word in text_lower for word in ['cash', 'immediate']):
                return "cash"
            elif any(word in text_lower for word in ['credit', 'on account', 'later']):
                return "credit"
            elif any(word in text_lower for word in ['bank', 'transfer', 'check']):
                return "bank"
        
        return None

    def _detect_tax(self, text: str, language: str, amount: Optional[Decimal]) -> Optional[Dict[str, Any]]:
        """Detect tax information from text."""
        text_lower = text.lower()
        
        tax_indicators_ar = ['شامل ضريبة', ' شامل الضريبة', 'مع الضريبة', 'ضريبة قيمة مضافة']
        tax_indicators_en = ['including tax', 'incl. VAT', 'with tax', 'VAT included']
        
        has_tax = False
        if language == "ar":
            has_tax = any(indicator in text_lower for indicator in tax_indicators_ar)
        else:
            has_tax = any(indicator in text_lower for indicator in tax_indicators_en)
        
        if has_tax and amount:
            # Default VAT rate (Egypt)
            default_rate = Decimal("14.0")
            tax_amount = amount - (amount / (1 + default_rate / 100))
            
            return {
                "rate": default_rate,
                "amount": tax_amount.quantize(Decimal("0.001")),
            }
        
        return None

    def get_suggestions(self, partial_text: str, language: str = "ar") -> List[str]:
        """Get suggestions for completing partial text."""
        suggestions = []
        
        if language == "ar":
            if partial_text.startswith("شراء"):
                suggestions = [
                    "شراء بضاعة نقدًا",
                    "شراء بضاعة آجل",
                    "شراء أصل ثابت",
                    "شراء مستلزمات",
                ]
            elif partial_text.startswith("بيع"):
                suggestions = [
                    "بيع بضاعة نقدًا",
                    "بيع بضاعة آجل",
                ]
            elif partial_text.startswith("دفعت"):
                suggestions = [
                    "دفعت إيجار",
                    "دفعت رواتب",
                    "دفعت مصروف كهرباء",
                    "دفعت لمورد",
                ]
            elif partial_text.startswith("استلمت"):
                suggestions = [
                    "استلمت من العميل",
                    "استلمت دفعة نقدًا",
                ]
        else:
            if partial_text.startswith("purchase"):
                suggestions = [
                    "Purchase goods for cash",
                    "Purchase goods on credit",
                ]
            elif partial_text.startswith("sale"):
                suggestions = [
                    "Sale for cash",
                    "Sale on credit",
                ]
        
        return suggestions
