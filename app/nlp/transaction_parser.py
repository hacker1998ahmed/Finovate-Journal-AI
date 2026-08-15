# Finovate Journal AI - Transaction Parser

"""
NLP-based transaction parser for Arabic and English accounting text.
Extracts amounts, currencies, payment methods, and suggests accounts.
"""

import re
from decimal import Decimal
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from ..accounting.rules_engine import rules_engine


@dataclass
class ParsedTransaction:
    """Result of parsing a transaction text."""
    original_text: str
    transaction_type: str = ""
    amount: Optional[Decimal] = None
    currency: str = "EGP"
    party: str = ""  # Customer or supplier name
    payment_method: str = ""  # Cash, Bank, etc.
    debit_account_code: Optional[str] = None
    credit_account_code: Optional[str] = None
    tax_amount: Optional[Decimal] = None
    is_tax_inclusive: bool = False
    confidence: int = 0
    ambiguities: List[str] = None
    explanation: str = ""
    
    def __post_init__(self):
        if self.ambiguities is None:
            self.ambiguities = []


class TransactionParser:
    """Parser for extracting accounting information from natural language."""
    
    # Currency patterns
    CURRENCY_PATTERNS = {
        'EGP': [r'جنيه', r'ج.م', r'مصري', r'egp', r'LE'],
        'USD': [r'دولار', r'$', r'usd', r'dollar'],
        'EUR': [r'يورو', r'€', r'eur', r'euro'],
        'SAR': [r'ريال', r'سعودي', r'sar', r'riyal'],
        'AED': [r'درهم', r'اماراتي', r'aed', r'dirham'],
    }
    
    # Payment method patterns
    PAYMENT_PATTERNS = {
        'cash': [r'نقد', r'nqd', r'كاش', r'cash', r'حاضر'],
        'bank': [r'بنك', r'bank', r'transfer', r'transfer', r'تحويل', r'شيك', r'check'],
        'credit': [r'آجل', r'أجل', r'credit', r'on account', r'على الحساب'],
    }
    
    # Amount patterns (Arabic and English numbers)
    AMOUNT_PATTERNS = [
        r'(\d{4,})',  # Match 4+ digit numbers first (like 10000, 15000)
        r'(\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?)',  # 1,000.00 format
        r'(\d+\.\d{2})',  # Decimal numbers like 100.50
    ]
    
    # Tax indicators
    TAX_INDICATORS_AR = ['شامل الضريبة', 'شامل VAT', 'شامل ضريبة القيمة المضافة']
    TAX_INDICATORS_EN = ['including VAT', 'incl. tax', 'tax included', 'VAT inclusive']
    
    def __init__(self):
        self.rules_engine = rules_engine
    
    def parse(self, text: str, language: str = "ar") -> ParsedTransaction:
        """Parse transaction text and extract accounting information."""
        result = ParsedTransaction(original_text=text)
        
        # Detect language if not specified
        if language == "auto":
            language = self._detect_language(text)
        
        # Extract amount
        result.amount = self._extract_amount(text)
        
        # Extract currency
        result.currency = self._extract_currency(text)
        
        # Extract payment method
        result.payment_method = self._extract_payment_method(text, language)
        
        # Extract party (customer/supplier name)
        result.party = self._extract_party(text, language)
        
        # Determine transaction type and suggest accounts
        rule = self.rules_engine.get_best_rule(text, language)
        if rule:
            result.transaction_type = rule.name_ar if language == "ar" else rule.name_en
            result.debit_account_code = rule.debit_account_code
            result.credit_account_code = rule.credit_account_code
            result.explanation = rule.description_ar if language == "ar" else rule.description_en
            
            # Check tax applicability
            if rule.tax_applicable and self._is_tax_indicated(text, language):
                result.tax_amount = self._calculate_tax(result.amount, result.is_tax_inclusive)
        
        # Calculate confidence score
        result.confidence = self._calculate_confidence(result, language)
        
        # Identify ambiguities
        result.ambiguities = self._identify_ambiguities(result, text, language)
        
        return result
    
    def _detect_language(self, text: str) -> str:
        """Detect if text is Arabic or English."""
        arabic_chars = re.findall(r'[\u0600-\u06FF]', text)
        return "ar" if len(arabic_chars) > len(text) * 0.3 else "en"
    
    def _extract_amount(self, text: str) -> Optional[Decimal]:
        """Extract monetary amount from text."""
        # Remove commas used as thousand separators
        cleaned = text.replace(',', '')
        
        for pattern in self.AMOUNT_PATTERNS:
            match = re.search(pattern, cleaned)
            if match:
                try:
                    return Decimal(match.group(1))
                except:
                    continue
        return None
    
    def _extract_currency(self, text: str) -> str:
        """Extract currency from text."""
        text_lower = text.lower()
        for currency, patterns in self.CURRENCY_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    return currency
        return "EGP"  # Default to Egyptian Pound
    
    def _extract_payment_method(self, text: str, language: str = "ar") -> str:
        """Extract payment method from text."""
        text_lower = text.lower()
        for method, patterns in self.PAYMENT_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    return method
        
        # Infer from context
        if language == "ar":
            if "نقد" in text:
                return "cash"
            elif "آجل" in text or "الحساب" in text:
                return "credit"
        else:
            if "cash" in text:
                return "cash"
            elif "credit" in text or "account" in text:
                return "credit"
        
        return ""
    
    def _extract_party(self, text: str, language: str = "ar") -> str:
        """Extract customer or supplier name from text."""
        # Look for patterns like "من العميل X" or "إلى المورد Y"
        patterns_ar = [
            r'من العميل\s+([\w\s]+?)(?:بمبلغ|بقيمة|على|$)',
            r'للمورد\s+([\w\s]+?)(?:بمبلغ|بقيمة|على|$)',
            r'من\s+([\w\s]+?)(?:بمبلغ|بقيمة|على|$)',
            r'إلى\s+([\w\s]+?)(?:بمبلغ|بقيمة|على|$)',
        ]
        
        patterns_en = [
            r'from customer\s+([\w\s]+?)(?:for|of|amount|$)',
            r'to supplier\s+([\w\s]+?)(?:for|of|amount|$)',
            r'from\s+([\w\s]+?)(?:for|of|amount|$)',
            r'to\s+([\w\s]+?)(?:for|of|amount|$)',
        ]
        
        patterns = patterns_ar if language == "ar" else patterns_en
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return ""
    
    def _is_tax_indicated(self, text: str, language: str = "ar") -> bool:
        """Check if tax is indicated in the text."""
        text_lower = text.lower()
        indicators = self.TAX_INDICATORS_AR if language == "ar" else self.TAX_INDICATORS_EN
        return any(ind in text_lower for ind in indicators)
    
    def _calculate_tax(self, amount: Optional[Decimal], inclusive: bool = False) -> Optional[Decimal]:
        """Calculate tax amount assuming default VAT rate."""
        if amount is None:
            return None
        
        vat_rate = Decimal("0.14")  # 14% Egypt VAT
        
        if inclusive:
            return amount - (amount / (1 + vat_rate))
        else:
            return amount * vat_rate
    
    def _calculate_confidence(self, result: ParsedTransaction, language: str) -> int:
        """Calculate confidence score based on extracted information."""
        score = 0
        
        # Amount clarity (30 points)
        if result.amount is not None:
            score += 30
        
        # Currency clarity (10 points)
        if result.currency != "EGP" or "جنيه" in result.original_text or "EGP" in result.original_text:
            score += 10
        
        # Payment method clarity (15 points)
        if result.payment_method:
            score += 15
        
        # Account matching (25 points)
        if result.debit_account_code and result.credit_account_code:
            score += 25
        
        # Party identification (10 points)
        if result.party:
            score += 10
        
        # No ambiguities (10 points)
        if not result.ambiguities:
            score += 10
        
        return min(score, 100)
    
    def _identify_ambiguities(self, result: ParsedTransaction, text: str, language: str) -> List[str]:
        """Identify potential ambiguities in the transaction."""
        ambiguities = []
        
        if result.amount is None:
            ambiguities.append("لم يتم تحديد المبلغ" if language == "ar" else "Amount not specified")
        
        if not result.payment_method:
            ambiguities.append("طريقة الدفع غير واضحة" if language == "ar" else "Payment method unclear")
        
        if not result.debit_account_code or not result.credit_account_code:
            ambiguities.append("لا يمكن تحديد الحسابات المناسبة" if language == "ar" else "Cannot determine appropriate accounts")
        
        if not result.transaction_type:
            ambiguities.append("نوع العملية غير واضح" if language == "ar" else "Transaction type unclear")
        
        return ambiguities


# Global instance
transaction_parser = TransactionParser()
