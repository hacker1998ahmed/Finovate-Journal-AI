"""
Finovate Journal AI - Financial Calculator

Developer: Ahmed Mostafa Ibrahim
Brand: Finovate – AHMED EG
"""

from decimal import Decimal, ROUND_HALF_UP
from typing import Tuple


def calculate_tax(amount: Decimal, tax_rate: Decimal, 
                  inclusive: bool = False) -> Tuple[Decimal, Decimal]:
    """
    Calculate tax amount and net/gross amount.
    
    Args:
        amount: The amount (either net or gross depending on 'inclusive')
        tax_rate: Tax rate as percentage (e.g., 14.0 for 14%)
        inclusive: If True, amount includes tax; if False, amount excludes tax
    
    Returns:
        Tuple of (tax_amount, base_amount)
    """
    if tax_rate <= 0:
        return Decimal("0.00"), amount
    
    if inclusive:
        # Amount includes tax, extract base and tax
        # Gross = Base + (Base * Rate/100)
        # Gross = Base * (1 + Rate/100)
        # Base = Gross / (1 + Rate/100)
        multiplier = Decimal("1") + (tax_rate / Decimal("100"))
        base_amount = amount / multiplier
        tax_amount = amount - base_amount
    else:
        # Amount excludes tax, calculate tax
        base_amount = amount
        tax_amount = amount * (tax_rate / Decimal("100"))
    
    # Round to 3 decimal places
    tax_amount = tax_amount.quantize(Decimal("0.001"), rounding=ROUND_HALF_UP)
    base_amount = base_amount.quantize(Decimal("0.001"), rounding=ROUND_HALF_UP)
    
    return tax_amount, base_amount


def calculate_net_amount(gross_amount: Decimal, tax_rate: Decimal) -> Decimal:
    """
    Calculate net amount from gross amount (amount including tax).
    
    Args:
        gross_amount: Amount including tax
        tax_rate: Tax rate as percentage
    
    Returns:
        Net amount (excluding tax)
    """
    _, net = calculate_tax(gross_amount, tax_rate, inclusive=True)
    return net


def calculate_gross_amount(net_amount: Decimal, tax_rate: Decimal) -> Decimal:
    """
    Calculate gross amount from net amount (amount excluding tax).
    
    Args:
        net_amount: Amount excluding tax
        tax_rate: Tax rate as percentage
    
    Returns:
        Gross amount (including tax)
    """
    tax, _ = calculate_tax(net_amount, tax_rate, inclusive=False)
    return net_amount + tax


def format_currency(amount: Decimal, currency: str = "EGP", 
                    locale: str = "ar") -> str:
    """
    Format amount as currency string.
    
    Args:
        amount: The amount to format
        currency: Currency code (EGP, USD, etc.)
        locale: Locale for formatting ('ar' or 'en')
    
    Returns:
        Formatted currency string
    """
    # Round to 3 decimal places
    amount = amount.quantize(Decimal("0.001"), rounding=ROUND_HALF_UP)
    
    # Convert to string with thousands separator
    if locale == "ar":
        # Arabic formatting (RTL)
        amount_str = f"{amount:,.3f}"
        # Convert to Arabic-Indic digits if needed
        arabic_digits = {
            '0': '٠', '1': '١', '2': '٢', '3': '٣', '4': '٤',
            '5': '٥', '6': '٦', '7': '٧', '8': '٨', '9': '٩'
        }
        # Optional: Convert to Arabic-Indic digits
        # amount_str = ''.join(arabic_digits.get(c, c) for c in amount_str)
        
        currency_symbols = {
            "EGP": "ج.م",
            "USD": "$",
            "EUR": "€",
            "SAR": "ر.س",
            "AED": "د.إ",
            "GBP": "£",
        }
        symbol = currency_symbols.get(currency, currency)
        return f"{amount_str} {symbol}"
    else:
        # English formatting (LTR)
        amount_str = f"{amount:,.3f}"
        
        currency_symbols = {
            "EGP": "EGP",
            "USD": "$",
            "EUR": "€",
            "SAR": "SAR",
            "AED": "AED",
            "GBP": "£",
        }
        symbol = currency_symbols.get(currency, currency)
        
        if symbol in ["$", "€", "£"]:
            return f"{symbol}{amount_str}"
        else:
            return f"{amount_str} {symbol}"


def parse_amount_string(amount_str: str) -> Decimal:
    """
    Parse amount from string, handling various formats.
    
    Supports:
    - "1,000.00"
    - "1.000,00"
    - "1000"
    - "1000.5"
    - Arabic-Indic digits
    
    Args:
        amount_str: String representation of amount
    
    Returns:
        Decimal amount
    """
    if not amount_str:
        return Decimal("0.00")
    
    # Convert Arabic-Indic digits to Western digits
    arabic_to_western = {
        '٠': '0', '١': '1', '٢': '2', '٣': '3', '٤': '4',
        '٥': '5', '٦': '6', '٧': '7', '٨': '8', '٩': '9'
    }
    amount_str = ''.join(arabic_to_western.get(c, c) for c in amount_str.strip())
    
    # Remove currency symbols and whitespace
    cleaned = amount_str.strip()
    for char in ['$', '€', '£', 'ج', '.', 'م', 'ر', 'س', 'د', 'إ', 'EGP', 'USD', 'EUR']:
        cleaned = cleaned.replace(char, '')
    cleaned = cleaned.strip()
    
    # Handle different decimal/thousand separators
    if ',' in cleaned and '.' in cleaned:
        # Determine which is the decimal separator
        last_comma = cleaned.rfind(',')
        last_dot = cleaned.rfind('.')
        
        if last_comma > last_dot:
            # European format: 1.000,00
            cleaned = cleaned.replace('.', '').replace(',', '.')
        else:
            # US format: 1,000.00
            cleaned = cleaned.replace(',', '')
    elif ',' in cleaned:
        # Could be thousand separator or decimal separator
        parts = cleaned.split(',')
        if len(parts) == 2 and len(parts[1]) <= 2:
            # Likely decimal separator: 100,50
            cleaned = cleaned.replace(',', '.')
        else:
            # Likely thousand separator: 1,000
            cleaned = cleaned.replace(',', '')
    
    try:
        return Decimal(cleaned)
    except Exception:
        return Decimal("0.00")


def round_decimal(value: Decimal, places: int = 3) -> Decimal:
    """
    Round decimal to specified places.
    
    Args:
        value: Decimal value to round
        places: Number of decimal places
    
    Returns:
        Rounded Decimal
    """
    quantizer = Decimal(10) ** -places
    return value.quantize(quantizer, rounding=ROUND_HALF_UP)


def validate_decimal_range(value: Decimal, min_val: Decimal = None, 
                           max_val: Decimal = None) -> bool:
    """
    Validate that a decimal is within range.
    
    Args:
        value: Value to validate
        min_val: Minimum allowed value (inclusive)
        max_val: Maximum allowed value (inclusive)
    
    Returns:
        True if valid, False otherwise
    """
    if min_val is not None and value < min_val:
        return False
    if max_val is not None and value > max_val:
        return False
    return True
