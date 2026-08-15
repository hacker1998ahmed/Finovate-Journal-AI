"""
Finovate Journal AI - Transaction Parser
Copyright © 2025 Ahmed Mostafa Ibrahim — All Rights Reserved.
"""

import re
from decimal import Decimal
from typing import Dict, List, Any


class TransactionParser:
    """Parse natural language accounting transactions"""
    
    def __init__(self):
        # Arabic patterns for amounts
        self.amount_patterns = [
            r'(\d+(?:,\d{3})*(?:\.\d+)?)\s*(?:جنيه|ج.م|ريال|دولار|EUR|USD)',
            r'(\d+(?:,\d{3})*(?:\.\d+)?)',
        ]
        
        # Account mappings (Arabic keywords to account names)
        self.account_mappings = {
            'نقد': 'الصندوق',
            'نقدًا': 'الصندوق',
            'كاش': 'الصندوق',
            'بنك': 'البنك',
            'شيك': 'البنك',
            'عميل': 'العملاء',
            'مورد': 'الموردون',
            'بضاعة': 'المشتريات',
            'مشتريات': 'المشتريات',
            'مبيعات': 'المبيعات',
            'بيع': 'المبيعات',
            'إيجار': 'مصروف إيجار',
            'رواتب': 'مصروف رواتب',
            'مرافق': 'مصروف مرافق',
            'كهرباء': 'مصروف كهرباء ومياه',
            'أصل ثابت': 'الأصول الثابتة',
            'سيارة': 'الأصول الثابتة',
            'أثاث': 'الأصول الثابتة',
        }
        
        # Transaction type patterns
        self.transaction_types = {
            'شراء': 'purchase',
            'بيع': 'sale',
            'دفع': 'payment',
            'استلام': 'receipt',
            'سداد': 'payment',
            'تحصيل': 'receipt',
        }
    
    def parse(self, text: str) -> Dict[str, Any]:
        """
        Parse a transaction description and return structured data
        
        Args:
            text: Natural language transaction description
            
        Returns:
            Dictionary with parsed transaction data
        """
        result = {
            'original_text': text,
            'transaction_type': 'general',
            'amount': Decimal('0'),
            'currency': 'EGP',
            'payment_method': 'cash',
            'confidence': 50,
            'entries': [],
        }
        
        # Extract amount
        amount_match = self._extract_amount(text)
        if amount_match:
            result['amount'] = amount_match['amount']
            result['currency'] = amount_match.get('currency', 'EGP')
            result['confidence'] += 20
        
        # Detect transaction type
        trans_type = self._detect_transaction_type(text)
        result['transaction_type'] = trans_type
        result['confidence'] += 10
        
        # Detect payment method
        payment_method = self._detect_payment_method(text)
        result['payment_method'] = payment_method
        result['confidence'] += 10
        
        # Generate journal entries
        entries = self._generate_entries(text, result)
        result['entries'] = entries
        
        # Cap confidence at 95%
        result['confidence'] = min(result['confidence'], 95)
        
        return result
    
    def _extract_amount(self, text: str) -> Dict[str, Any]:
        """Extract amount from text"""
        for pattern in self.amount_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                amount_str = match.group(1).replace(',', '')
                
                # Determine currency
                currency = 'EGP'
                if 'دولار' in text or 'USD' in text:
                    currency = 'USD'
                elif 'ريال' in text:
                    currency = 'SAR'
                elif 'EUR' in text or 'يورو' in text:
                    currency = 'EUR'
                
                return {
                    'amount': Decimal(amount_str),
                    'currency': currency
                }
        
        return {'amount': Decimal('0'), 'currency': 'EGP'}
    
    def _detect_transaction_type(self, text: str) -> str:
        """Detect transaction type from text"""
        text_lower = text.lower()
        
        for keyword, trans_type in self.transaction_types.items():
            if keyword in text_lower:
                return trans_type
        
        return 'general'
    
    def _detect_payment_method(self, text: str) -> str:
        """Detect payment method from text"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['نقد', 'كاش', 'نقدًا']):
            return 'cash'
        elif any(word in text_lower for word in ['بنك', 'تحويل', 'شيك']):
            return 'bank'
        elif 'آجل' in text_lower or 'اجل' in text_lower:
            return 'credit'
        
        return 'cash'
    
    def _generate_entries(self, text: str, parsed: Dict) -> List[Dict]:
        """Generate journal entries based on parsed data"""
        entries = []
        amount = parsed['amount']
        payment_method = parsed['payment_method']
        trans_type = parsed['transaction_type']
        
        # Simple rule-based entry generation
        if trans_type == 'purchase':
            if payment_method == 'cash':
                entries.append({
                    'account': 'المشتريات',
                    'description': f'شراء بضاعة نقدًا',
                    'debit': amount,
                    'credit': Decimal('0')
                })
                entries.append({
                    'account': 'الصندوق',
                    'description': f'دفع نقدًا للمشتريات',
                    'debit': Decimal('0'),
                    'credit': amount
                })
            else:
                entries.append({
                    'account': 'المشتريات',
                    'description': f'شراء بضاعة',
                    'debit': amount,
                    'credit': Decimal('0')
                })
                entries.append({
                    'account': 'البنك' if payment_method == 'bank' else 'الموردون',
                    'description': f'الدفع عن طريق {payment_method}',
                    'debit': Decimal('0'),
                    'credit': amount
                })
        
        elif trans_type == 'sale':
            if payment_method == 'cash':
                entries.append({
                    'account': 'الصندوق',
                    'description': f'قبض نقدًا من المبيعات',
                    'debit': amount,
                    'credit': Decimal('0')
                })
                entries.append({
                    'account': 'المبيعات',
                    'description': f'بيع بضاعة',
                    'debit': Decimal('0'),
                    'credit': amount
                })
            else:
                entries.append({
                    'account': 'البنك' if payment_method == 'bank' else 'العملاء',
                    'description': f'تحصيل من المبيعات',
                    'debit': amount,
                    'credit': Decimal('0')
                })
                entries.append({
                    'account': 'المبيعات',
                    'description': f'بيع بضاعة',
                    'debit': Decimal('0'),
                    'credit': amount
                })
        
        elif trans_type == 'payment':
            expense_account = self._infer_expense_account(text)
            entries.append({
                'account': expense_account,
                'description': f'دفع {expense_account}',
                'debit': amount,
                'credit': Decimal('0')
            })
            entries.append({
                'account': 'البنك' if payment_method == 'bank' else 'الصندوق',
                'description': f'دفع نقدًا/من البنك',
                'debit': Decimal('0'),
                'credit': amount
            })
        
        elif trans_type == 'receipt':
            entries.append({
                'account': 'البنك' if payment_method == 'bank' else 'الصندوق',
                'description': f'قبض نقدًا/في البنك',
                'debit': amount,
                'credit': Decimal('0')
            })
            entries.append({
                'account': 'العملاء',
                'description': f'تحصيل من العملاء',
                'debit': Decimal('0'),
                'credit': amount
            })
        
        else:
            # General entry - placeholder
            entries.append({
                'account': 'حساب عام',
                'description': text[:50],
                'debit': amount,
                'credit': Decimal('0')
            })
            entries.append({
                'account': 'ح مقابل',
                'description': text[:50],
                'debit': Decimal('0'),
                'credit': amount
            })
        
        return entries
    
    def _infer_expense_account(self, text: str) -> str:
        """Infer expense account from text"""
        text_lower = text.lower()
        
        for keyword, account in self.account_mappings.items():
            if keyword in text_lower and 'مصروف' in account:
                return account
        
        return 'مصروفات متنوعة'
