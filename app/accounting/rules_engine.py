"""
Finovate Journal AI - Accounting Rules Engine
Copyright © 2025 Ahmed Mostafa Ibrahim — All Rights Reserved.
"""

from decimal import Decimal
from typing import Dict, Any, List


class RulesEngine:
    """Apply accounting rules to parsed transactions"""
    
    def __init__(self):
        # VAT rate (Egypt)
        self.vat_rate = Decimal('0.14')
    
    def apply_rules(self, parsed: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply accounting rules to parsed transaction
        
        Args:
            parsed: Parsed transaction data
            
        Returns:
            Enhanced transaction data with applied rules
        """
        result = parsed.copy()
        
        # Check for VAT indicators
        if self._has_vat_indicator(parsed['original_text']):
            result = self._apply_vat_rules(result)
        
        # Validate entries balance
        result = self._validate_balance(result)
        
        # Apply account mapping rules
        result = self._apply_account_mappings(result)
        
        return result
    
    def _has_vat_indicator(self, text: str) -> bool:
        """Check if text contains VAT indicators"""
        vat_indicators = [
            'ضريبة', 'قيمة مضافة', 'vat', 'VAT', 
            'شامل الضريبة', 'شامل Vat', '+ ضريبة'
        ]
        return any(indicator in text.lower() for indicator in vat_indicators)
    
    def _apply_vat_rules(self, parsed: Dict[str, Any]) -> Dict[str, Any]:
        """Apply VAT calculation rules"""
        amount = parsed['amount']
        
        # Check if amount includes VAT
        if 'شامل' in parsed['original_text'].lower():
            # Extract VAT from inclusive amount
            net_amount = amount / (1 + self.vat_rate)
            vat_amount = amount - net_amount
            
            # Modify entries to include VAT
            new_entries = []
            for entry in parsed['entries']:
                if entry['debit'] > 0 and entry['account'] == 'المشتريات':
                    # Split purchase entry
                    new_entries.append({
                        'account': 'المشتريات',
                        'description': entry['description'],
                        'debit': net_amount,
                        'credit': Decimal('0')
                    })
                    new_entries.append({
                        'account': 'ضريبة القيمة المضافة (مدخلات)',
                        'description': 'ضريبة قيمة مضافة',
                        'debit': vat_amount,
                        'credit': Decimal('0')
                    })
                else:
                    new_entries.append(entry)
            
            parsed['entries'] = new_entries
            parsed['vat_included'] = True
            parsed['net_amount'] = net_amount
            parsed['vat_amount'] = vat_amount
            parsed['confidence'] += 10
        
        return parsed
    
    def _validate_balance(self, parsed: Dict[str, Any]) -> Dict[str, Any]:
        """Validate that debits equal credits"""
        total_debit = sum(e.get('debit', Decimal('0')) for e in parsed['entries'])
        total_credit = sum(e.get('credit', Decimal('0')) for e in parsed['entries'])
        
        parsed['is_balanced'] = (total_debit == total_credit)
        parsed['total_debit'] = total_debit
        parsed['total_credit'] = total_credit
        
        if not parsed['is_balanced']:
            parsed['confidence'] -= 20
        
        return parsed
    
    def _apply_account_mappings(self, parsed: Dict[str, Any]) -> Dict[str, Any]:
        """Apply standard account mappings"""
        # This can be extended with more sophisticated mapping logic
        return parsed
