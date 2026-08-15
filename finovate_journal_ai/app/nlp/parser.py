"""
Finovate Journal AI - NLP Parser for Arabic and English accounting transactions
"""
import re
from decimal import Decimal
from typing import Optional, Dict, List, Any, Tuple
from dataclasses import dataclass
import logging

from app.utils.logging_config import get_logger

logger = get_logger(__name__)


@dataclass
class ParsedTransaction:
    """Represents a parsed accounting transaction"""
    transaction_type: str = ""
    amount: Optional[Decimal] = None
    currency: str = "EGP"
    party: Optional[str] = None
    payment_method: str = "cash"  # cash, bank, credit
    tax_detected: bool = False
    tax_amount: Optional[Decimal] = None
    confidence: float = 0.0
    ambiguities: List[str] = None
    explanation: str = ""
    raw_text: str = ""
    
    def __post_init__(self):
        if self.ambiguities is None:
            self.ambiguities = []


class NLParser:
    """
    Natural Language Parser for accounting transactions
    
    Supports Arabic and English transaction descriptions
    """
    
    # Arabic number words mapping
    ARABIC_NUMBERS = {
        'صفر': 0, 'واحد': 1, 'اثنين': 2, 'ثلاثة': 3, 'أربعة': 4,
        'خمسة': 5, 'ستة': 6, 'سبعة': 7, 'ثمانية': 8, 'تسعة': 9,
        'عشرة': 10, 'عشرين': 20, 'ثلاثين': 30, 'أربعين': 40,
        'خمسين': 50, 'ستين': 60, 'سبعين': 70, 'ثمانين': 80, 'تسعين': 90,
        'مائة': 100, 'مئة': 100, 'ألف': 1000, 'آلاف': 1000,
        'مليون': 1000000, 'مليار': 1000000000
    }
    
    # Currency patterns
    CURRENCY_PATTERNS = {
        'EGP': ['جنيه', 'جنيهات', 'ج.م', 'EGP', 'LE'],
        'USD': ['دولار', 'دولارات', '$', 'USD'],
        'EUR': ['يورو', '€', 'EUR'],
        'SAR': ['ريال', 'ريالات', 'SAR'],
        'AED': ['درهم', 'درامهم', 'AED']
    }
    
    # Payment method keywords
    PAYMENT_METHODS = {
        'cash': ['نقدًا', 'نقدا', 'كاش', 'cash', 'ready money'],
        'bank': ['بنك', 'تحوييل', 'شيك', 'check', 'transfer', 'من البنك'],
        'credit': ['آجل', 'اجل', 'على الحساب', 'credit', 'on account']
    }
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def parse(self, text: str) -> ParsedTransaction:
        """
        Parse a transaction description
        
        Args:
            text: Transaction description in Arabic or English
            
        Returns:
            ParsedTransaction object
        """
        result = ParsedTransaction(raw_text=text)
        
        if not text or not text.strip():
            result.ambiguities.append("Empty transaction description")
            return result
        
        text = text.strip()
        self.logger.debug("Parsing transaction: %s", text[:100])
        
        # Extract amount
        amount, currency = self._extract_amount(text)
        result.amount = amount
        result.currency = currency
        
        # Detect payment method
        result.payment_method = self._detect_payment_method(text)
        
        # Detect party (customer/supplier name)
        result.party = self._detect_party(text)
        
        # Detect tax
        tax_detected, tax_amount = self._detect_tax(text, amount)
        result.tax_detected = tax_detected
        result.tax_amount = tax_amount
        
        # Determine transaction type
        result.transaction_type = self._determine_transaction_type(text)
        
        # Calculate confidence
        result.confidence = self._calculate_confidence(result)
        
        # Generate explanation
        result.explanation = self._generate_explanation(result)
        
        # Check for ambiguities
        self._check_ambiguities(result, text)
        
        return result
    
    def _extract_amount(self, text: str) -> Tuple[Optional[Decimal], str]:
        """Extract monetary amount from text"""
        currency = "EGP"
        
        # Pattern for numbers - try to find any numeric value
        pattern = r'(\d+(?:\.\d{1,2})?)'
        
        matches = re.findall(pattern, text)
        amount = None
        
        if matches:
            try:
                # Get the last match (usually the amount appears after description)
                amount_str = matches[-1]
                amount = Decimal(amount_str)
            except Exception:
                pass
        
        # Detect currency
        text_lower = text.lower()
        for curr, symbols in self.CURRENCY_PATTERNS.items():
            for symbol in symbols:
                if symbol.lower() in text_lower:
                    currency = curr
                    break
        
        return amount, currency
    
    def _detect_payment_method(self, text: str) -> str:
        """Detect payment method from text"""
        text_lower = text.lower()
        
        for method, keywords in self.PAYMENT_METHODS.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return method
        
        return "cash"  # Default to cash
    
    def _detect_party(self, text: str) -> Optional[str]:
        """Detect customer or supplier name"""
        # Look for common patterns
        patterns = [
            r'(?:من|from)\s+([^\s,]+(?:\s+[^\s,]+)*)',
            r'(?:العميل|customer)\s+([^\s,]+)',
            r'(?:شركة|company|supplier)\s+([^\s,]+)',
            r'(?:مورد|supplier)\s+([^\s,]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return None
    
    def _detect_tax(self, text: str, amount: Optional[Decimal]) -> Tuple[bool, Optional[Decimal]]:
        """Detect if tax is mentioned and calculate tax amount"""
        if amount is None:
            return False, None
        
        text_lower = text.lower()
        
        # Check for tax keywords
        tax_keywords = ['ضريبة', 'vat', 'tax', 'قيمة مضافة', 'شامل الضريبة']
        has_tax = any(keyword in text_lower for keyword in tax_keywords)
        
        if not has_tax:
            return False, None
        
        # Try to extract tax rate
        rate_patterns = [
            r'(\d+(?:\.\d+)?)\s*%',
            r'ضريبة\s+(\d+(?:\.\d+)?)',
        ]
        
        tax_rate = Decimal("0.14")  # Default 14% VAT
        for pattern in rate_patterns:
            match = re.search(pattern, text_lower)
            if match:
                try:
                    tax_rate = Decimal(match.group(1)) / Decimal("100")
                    break
                except Exception:
                    continue
        
        # Calculate tax amount (assuming amount includes tax)
        if "شامل" in text_lower or "inclusive" in text_lower:
            base_amount = amount / (1 + tax_rate)
            tax_amount = amount - base_amount
        else:
            tax_amount = amount * tax_rate
        
        return True, tax_amount.quantize(Decimal("0.01"))
    
    def _determine_transaction_type(self, text: str) -> str:
        """Determine transaction type from keywords"""
        text_lower = text.lower()
        
        type_keywords = {
            'purchase': ['شراء', 'buy', 'purchased', 'bought'],
            'sale': ['بيع', 'sell', 'sold', 'sale'],
            'payment': ['دفع', 'pay', 'paid', 'payment', 'سداد'],
            'receipt': ['استلم', 'receive', 'received', 'collection', 'تحصيل'],
            'expense': ['مصروف', 'expense', 'cost'],
            'deposit': ['إيداع', 'deposit', 'ايداع'],
            'withdrawal': ['سحب', 'withdraw', 'withdrawal'],
        }
        
        for trans_type, keywords in type_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                return trans_type
        
        return "general"
    
    def _calculate_confidence(self, result: ParsedTransaction) -> float:
        """Calculate confidence score based on extracted information"""
        confidence = 0.0
        
        if result.amount is not None:
            confidence += 30
        else:
            result.ambiguities.append("Amount not detected")
        
        if result.transaction_type != "general":
            confidence += 25
        else:
            result.ambiguities.append("Transaction type unclear")
        
        if result.payment_method:
            confidence += 15
        
        if result.party:
            confidence += 15
        
        if not result.ambiguities:
            confidence += 15
        
        # Penalize for ambiguities
        confidence -= len(result.ambiguities) * 5
        
        return max(0.0, min(100.0, confidence))
    
    def _generate_explanation(self, result: ParsedTransaction) -> str:
        """Generate human-readable explanation of the parsing"""
        parts = []
        
        if result.transaction_type:
            parts.append(f"نوع العملية: {result.transaction_type}")
        
        if result.amount:
            parts.append(f"المبلغ: {result.amount:.2f} {result.currency}")
        
        if result.payment_method:
            method_ar = {'cash': 'نقدي', 'bank': 'بنكي', 'credit': 'آجل'}
            parts.append(f"طريقة الدفع: {method_ar.get(result.payment_method, result.payment_method)}")
        
        if result.party:
            parts.append(f"الطرف: {result.party}")
        
        if result.tax_detected:
            parts.append(f"ضريبة مكتشفة: {result.tax_amount}")
        
        return " | ".join(parts) if parts else "لا توجد معلومات كافية"
    
    def _check_ambiguities(self, result: ParsedTransaction, text: str) -> None:
        """Check for common ambiguities in the transaction"""
        text_lower = text.lower()
        
        # Check for vague payment descriptions
        if result.amount and not result.transaction_type:
            result.ambiguities.append("لم يتم تحديد سبب الدفع/الاستلام")
        
        # Check for missing accounts
        vague_terms = ['دفع', 'استلم', 'مصروف']
        if any(term in text_lower for term in vague_terms) and result.confidence < 70:
            result.ambiguities.append("يحتاج إلى تحديد الحساب المناسب")


# Global parser instance
_parser: Optional[NLParser] = None


def get_parser() -> NLParser:
    """Get or create the global NLP parser instance"""
    global _parser
    if _parser is None:
        _parser = NLParser()
    return _parser
