"""
NLP Parser - Natural Language Processing for accounting transactions
Supports Arabic and English transaction parsing
"""
import re
from decimal import Decimal
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import date
import logging

logger = logging.getLogger(__name__)


@dataclass
class ParsedTransaction:
    """Result of parsing a natural language transaction."""
    original_text: str
    language: str  # 'ar' or 'en'
    transaction_type: Optional[str] = None
    amount: Optional[Decimal] = None
    currency: str = "EGP"
    payment_method: Optional[str] = None  # cash, bank, credit
    party: Optional[str] = None  # customer, supplier name
    debit_accounts: List[Dict] = field(default_factory=list)
    credit_accounts: List[Dict] = field(default_factory=list)
    tax_amount: Optional[Decimal] = None
    tax_rate: Optional[Decimal] = None
    is_tax_inclusive: bool = False
    confidence: float = 0.0
    ambiguities: List[str] = field(default_factory=list)
    explanation: str = ""
    rule_matched: Optional[str] = None


class TransactionParser:
    """
    Parse natural language text into structured accounting transactions.
    Supports both Arabic and English input.
    """
    
    # Currency patterns
    CURRENCY_PATTERNS = {
        'ar': {
            'EGP': ['جنيه', 'جنيهات', 'ج.م', 'مصرى', 'مصري'],
            'USD': ['دولار', 'دولارات', '$'],
            'EUR': ['يورو', '€'],
            'SAR': ['ريال', 'ريالات', 'ر.س'],
            'AED': ['درهم', 'درهمات', 'د.إ'],
            'GBP': ['جنيه استرليني', '£']
        },
        'en': {
            'EGP': ['EGP', 'Egyptian pound', 'LE'],
            'USD': ['USD', 'dollar', 'dollars', '$'],
            'EUR': ['EUR', 'euro', '€'],
            'SAR': ['SAR', 'Saudi riyal', '﷼'],
            'AED': ['AED', 'UAE dirham', 'DH'],
            'GBP': ['GBP', 'British pound', '£']
        }
    }
    
    # Payment method patterns
    PAYMENT_PATTERNS = {
        'ar': {
            'cash': ['نقد', 'نقدا', 'كاش', 'كاشة'],
            'bank': ['بنك', 'من البنك', 'تحويل', 'شيك', 'شيكة'],
            'credit': ['آجل', 'على الحساب', 'دين', 'قروض']
        },
        'en': {
            'cash': ['cash', 'cashy'],
            'bank': ['bank', 'from bank', 'transfer', 'check', 'cheque'],
            'credit': ['credit', 'on account', 'on credit', 'deferred']
        }
    }
    
    # Amount patterns (Arabic and English numerals)
    AMOUNT_PATTERN_AR = r'(\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?)|\b(\d+)\b'
    AMOUNT_PATTERN_EN = r'(\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?)|\b(\d+)\b'
    
    # Tax patterns
    TAX_PATTERNS = {
        'ar': ['ضريبة', 'ض.ق.م', 'vat', 'قيمة مضافة', 'شامل الضريبة', ' شامل ضريبة'],
        'en': ['tax', 'VAT', 'value added', 'including tax', 'tax inclusive']
    }
    
    def __init__(self):
        self.amount_pattern_ar = re.compile(self.AMOUNT_PATTERN_AR)
        self.amount_pattern_en = re.compile(self.AMOUNT_PATTERN_EN)
    
    def detect_language(self, text: str) -> str:
        """Detect if text is Arabic or English."""
        # Check for Arabic characters
        arabic_chars = re.findall(r'[\u0600-\u06FF]', text)
        if len(arabic_chars) > len(text) * 0.3:  # More than 30% Arabic chars
            return 'ar'
        return 'en'
    
    def extract_amount(self, text: str, language: str) -> Optional[Decimal]:
        """Extract monetary amount from text."""
        pattern = self.amount_pattern_ar if language == 'ar' else self.amount_pattern_en
        
        # Find all number matches
        matches = pattern.findall(text)
        
        for match in matches:
            # match is a tuple due to groups in regex
            num_str = match[0] if match[0] else match[1] if len(match) > 1 else None
            
            if num_str:
                try:
                    # Remove commas and convert to Decimal
                    num_str = num_str.replace(',', '')
                    amount = Decimal(num_str)
                    if amount > 0:
                        logger.debug(f"Extracted amount: {amount}")
                        return amount
                except Exception as e:
                    logger.warning(f"Failed to parse amount '{num_str}': {e}")
        
        return None
    
    def extract_currency(self, text: str, language: str) -> str:
        """Detect currency from text."""
        text_lower = text.lower()
        
        for currency, patterns in self.CURRENCY_PATTERNS[language].items():
            for pattern in patterns:
                if pattern.lower() in text_lower:
                    logger.debug(f"Detected currency: {currency}")
                    return currency
        
        # Default to EGP for Egyptian context
        return 'EGP'
    
    def extract_payment_method(self, text: str, language: str) -> Optional[str]:
        """Detect payment method (cash, bank, credit)."""
        text_lower = text.lower()
        
        for method, patterns in self.PAYMENT_PATTERNS[language].items():
            for pattern in patterns:
                if pattern.lower() in text_lower:
                    logger.debug(f"Detected payment method: {method}")
                    return method
        
        return None
    
    def extract_tax_info(self, text: str, language: str) -> Tuple[bool, Optional[Decimal]]:
        """
        Extract tax information from text.
        
        Returns:
            Tuple of (is_tax_inclusive, tax_rate)
        """
        text_lower = text.lower()
        is_inclusive = False
        rate = None
        
        # Check for tax keywords
        for pattern in self.TAX_PATTERNS[language]:
            if pattern.lower() in text_lower:
                is_inclusive = True
                
                # Try to extract tax rate
                rate_match = re.search(r'(\d+(?:\.\d+)?)\s*%', text)
                if rate_match:
                    rate = Decimal(rate_match.group(1)) / 100
                else:
                    # Default VAT rate for Egypt
                    rate = Decimal('0.14')
                
                break
        
        logger.debug(f"Tax info: inclusive={is_inclusive}, rate={rate}")
        return is_inclusive, rate
    
    def extract_party(self, text: str, language: str) -> Optional[str]:
        """Extract party name (customer/supplier) from text."""
        # Simple extraction - look for names after certain keywords
        if language == 'ar':
            patterns = [r'من\s+(\w+)', r'لـ?\s*(\w+)', r'شركة\s+(\w+)']
        else:
            patterns = [r'from\s+(\w+)', r'to\s+(\w+)', r'company\s+(\w+)']
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return None
    
    def identify_transaction_type(self, text: str, language: str) -> Optional[str]:
        """Identify the type of transaction from text."""
        text_lower = text.lower()
        
        if language == 'ar':
            if any(word in text_lower for word in ['شراء', 'اشتريت', 'اشتروا']):
                return 'purchase'
            elif any(word in text_lower for word in ['بيع', 'بعنا', 'باع']):
                return 'sale'
            elif any(word in text_lower for word in ['دفع', 'دفعت', 'دفعوا', 'مصروف']):
                return 'expense_payment'
            elif any(word in text_lower for word in ['استلمت', 'استلام', 'قبض', 'تحصيل']):
                return 'collection'
            elif any(word in text_lower for word in ['سددت', 'سداد', 'دفع لمورد']):
                return 'supplier_payment'
        else:
            if any(word in text_lower for word in ['buy', 'bought', 'purchase']):
                return 'purchase'
            elif any(word in text_lower for word in ['sell', 'sold', 'sale']):
                return 'sale'
            elif any(word in text_lower for word in ['paid', 'pay', 'expense']):
                return 'expense_payment'
            elif any(word in text_lower for word in ['received', 'receive', 'collect']):
                return 'collection'
            elif any(word in text_lower for word in ['settle', 'payment to supplier']):
                return 'supplier_payment'
        
        return None
    
    def calculate_confidence(
        self,
        has_amount: bool,
        has_currency: bool,
        has_payment_method: bool,
        has_transaction_type: bool,
        has_party: bool,
        ambiguity_count: int
    ) -> float:
        """
        Calculate confidence score based on extracted information.
        
        Returns:
            Confidence score 0-100
        """
        score = 0
        
        # Base scores for each element
        if has_amount:
            score += 25
        if has_currency:
            score += 10
        if has_payment_method:
            score += 20
        if has_transaction_type:
            score += 25
        if has_party:
            score += 10
        
        # Penalty for ambiguities
        score -= ambiguity_count * 10
        
        # Ensure score is between 0 and 100
        return max(0, min(100, score))
    
    def parse(self, text: str) -> ParsedTransaction:
        """
        Parse natural language text into structured transaction.
        
        Args:
            text: Natural language description of transaction
            
        Returns:
            ParsedTransaction object with extracted information
        """
        logger.info(f"Parsing transaction: {text}")
        
        # Detect language
        language = self.detect_language(text)
        logger.debug(f"Detected language: {language}")
        
        # Extract components
        amount = self.extract_amount(text, language)
        currency = self.extract_currency(text, language)
        payment_method = self.extract_payment_method(text, language)
        is_tax_inclusive, tax_rate = self.extract_tax_info(text, language)
        party = self.extract_party(text, language)
        transaction_type = self.identify_transaction_type(text, language)
        
        # Track ambiguities
        ambiguities = []
        
        if not amount:
            ambiguities.append("Amount not detected")
        
        if not transaction_type:
            ambiguities.append("Transaction type unclear")
        
        if not payment_method:
            ambiguities.append("Payment method not specified")
        
        # Calculate confidence
        confidence = self.calculate_confidence(
            has_amount=(amount is not None),
            has_currency=(currency != 'EGP' or 'جنيه' in text or 'EGP' in text),
            has_payment_method=(payment_method is not None),
            has_transaction_type=(transaction_type is not None),
            has_party=(party is not None),
            ambiguity_count=len(ambiguities)
        )
        
        # Generate explanation
        explanation = self._generate_explanation(
            transaction_type=transaction_type,
            amount=amount,
            currency=currency,
            payment_method=payment_method,
            language=language
        )
        
        result = ParsedTransaction(
            original_text=text,
            language=language,
            transaction_type=transaction_type,
            amount=amount,
            currency=currency,
            payment_method=payment_method,
            party=party,
            tax_amount=None,  # Will be calculated later
            tax_rate=tax_rate,
            is_tax_inclusive=is_tax_inclusive,
            confidence=confidence,
            ambiguities=ambiguities,
            explanation=explanation
        )
        
        logger.info(f"Parsed transaction: type={transaction_type}, amount={amount}, confidence={confidence}")
        return result
    
    def _generate_explanation(
        self,
        transaction_type: Optional[str],
        amount: Optional[Decimal],
        currency: str,
        payment_method: Optional[str],
        language: str
    ) -> str:
        """Generate human-readable explanation of the parsed transaction."""
        if language == 'ar':
            parts = []
            if transaction_type:
                type_map = {
                    'purchase': 'شراء',
                    'sale': 'بيع',
                    'expense_payment': 'دفع مصروف',
                    'collection': 'تحصيل',
                    'supplier_payment': 'سداد مورد'
                }
                parts.append(f"نوع العملية: {type_map.get(transaction_type, transaction_type)}")
            
            if amount:
                parts.append(f"المبلغ: {amount:,} {currency}")
            
            if payment_method:
                method_map = {'cash': 'نقدي', 'bank': 'بنكي', 'credit': 'آجل'}
                parts.append(f"طريقة الدفع: {method_map.get(payment_method, payment_method)}")
            
            return ' | '.join(parts) if parts else "تعذر تحليل العملية بالكامل"
        else:
            parts = []
            if transaction_type:
                parts.append(f"Type: {transaction_type.replace('_', ' ').title()}")
            
            if amount:
                parts.append(f"Amount: {amount:,.2f} {currency}")
            
            if payment_method:
                parts.append(f"Payment: {payment_method.title()}")
            
            return ' | '.join(parts) if parts else "Could not fully parse transaction"


# Global parser instance
parser = TransactionParser()


def parse_transaction(text: str) -> ParsedTransaction:
    """Convenience function to parse a transaction."""
    return parser.parse(text)
