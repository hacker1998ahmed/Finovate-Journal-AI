# Finovate Journal AI - Excel Export/Import Service

"""
Excel export and import service for Finovate Journal AI.
Supports openpyxl for reading and writing Excel files.
"""

from typing import List, Dict, Any, Optional
from decimal import Decimal
from pathlib import Path
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

try:
    from openpyxl import Workbook, load_workbook
    from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
    from openpyxl.utils import get_column_letter
    EXCEL_AVAILABLE = True
except ImportError:
    EXCEL_AVAILABLE = False
    logger.warning("openpyxl not installed. Excel features disabled.")


class ExcelService:
    """Service for Excel export and import operations."""
    
    # Style definitions
    HEADER_FONT = Font(bold=True, color="FFFFFF", size=12)
    HEADER_FILL = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
    HEADER_ALIGNMENT = Alignment(horizontal="center", vertical="center")
    
    CELL_ALIGNMENT = Alignment(horizontal="right", vertical="center")
    RTL_ALIGNMENT = Alignment(horizontal="left", vertical="center")
    
    THIN_BORDER = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )
    
    @staticmethod
    def export_journal_entries(entries: List[Dict[str, Any]], 
                               filepath: str,
                               rtl: bool = False) -> bool:
        """Export journal entries to Excel file."""
        
        if not EXCEL_AVAILABLE:
            logger.error("openpyxl not available")
            return False
        
        try:
            wb = Workbook()
            ws = wb.active
            ws.title = "Journal Entries"
            
            # Headers
            headers = [
                "Entry No", "Date", "Description", "Account Code", 
                "Account Name", "Debit", "Credit", "User", "Status"
            ]
            
            # Write headers
            for col, header in enumerate(headers, 1):
                cell = ws.cell(row=1, column=col, value=header)
                cell.font = ExcelService.HEADER_FONT
                cell.fill = ExcelService.HEADER_FILL
                cell.alignment = ExcelService.HEADER_ALIGNMENT
                cell.border = ExcelService.THIN_BORDER
            
            # Write data
            for row_idx, entry in enumerate(entries, 2):
                ws.cell(row=row_idx, column=1, value=entry.get('entry_no', ''))
                ws.cell(row=row_idx, column=2, value=entry.get('date', ''))
                ws.cell(row=row_idx, column=3, value=entry.get('description', ''))
                ws.cell(row=row_idx, column=4, value=entry.get('account_code', ''))
                ws.cell(row=row_idx, column=5, value=entry.get('account_name', ''))
                
                # Format amounts
                debit = entry.get('debit', Decimal('0'))
                credit = entry.get('credit', Decimal('0'))
                ws.cell(row=row_idx, column=6, value=float(debit) if isinstance(debit, Decimal) else debit)
                ws.cell(row=row_idx, column=7, value=float(credit) if isinstance(credit, Decimal) else credit)
                
                ws.cell(row=row_idx, column=8, value=entry.get('user', ''))
                ws.cell(row=row_idx, column=9, value=entry.get('status', ''))
                
                # Apply styles
                for col in range(1, 10):
                    cell = ws.cell(row=row_idx, column=col)
                    cell.alignment = ExcelService.RTL_ALIGNMENT if rtl else ExcelService.CELL_ALIGNMENT
                    cell.border = ExcelService.THIN_BORDER
                    
                    # Format currency columns
                    if col in [6, 7]:
                        cell.number_format = '#,##0.00'
            
            # Auto-adjust column widths
            for col in ws.columns:
                max_length = 0
                column = col[0].column_letter
                for cell in col:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                ws.column_dimensions[column].width = adjusted_width
            
            # Save workbook
            wb.save(filepath)
            logger.info(f"Exported {len(entries)} entries to {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Excel export failed: {e}")
            return False
    
    @staticmethod
    def export_trial_balance(accounts: List[Dict[str, Any]], 
                             filepath: str,
                             rtl: bool = False) -> bool:
        """Export trial balance to Excel file."""
        
        if not EXCEL_AVAILABLE:
            return False
        
        try:
            wb = Workbook()
            ws = wb.active
            ws.title = "Trial Balance"
            
            # Headers
            headers = ["Account Code", "Account Name", "Debit", "Credit"]
            
            # Write headers
            for col, header in enumerate(headers, 1):
                cell = ws.cell(row=1, column=col, value=header)
                cell.font = ExcelService.HEADER_FONT
                cell.fill = ExcelService.HEADER_FILL
                cell.alignment = ExcelService.HEADER_ALIGNMENT
                cell.border = ExcelService.THIN_BORDER
            
            # Write data
            total_debit = Decimal('0')
            total_credit = Decimal('0')
            
            for row_idx, account in enumerate(accounts, 2):
                ws.cell(row=row_idx, column=1, value=account.get('code', ''))
                ws.cell(row=row_idx, column=2, value=account.get('name', ''))
                
                debit = account.get('debit', Decimal('0'))
                credit = account.get('credit', Decimal('0'))
                
                ws.cell(row=row_idx, column=3, value=float(debit) if isinstance(debit, Decimal) else debit)
                ws.cell(row=row_idx, column=4, value=float(credit) if isinstance(credit, Decimal) else credit)
                
                total_debit += debit if isinstance(debit, Decimal) else Decimal(str(debit))
                total_credit += credit if isinstance(credit, Decimal) else Decimal(str(credit))
                
                # Apply styles
                for col in range(1, 5):
                    cell = ws.cell(row=row_idx, column=col)
                    cell.alignment = ExcelService.RTL_ALIGNMENT if rtl else ExcelService.CELL_ALIGNMENT
                    cell.border = ExcelService.THIN_BORDER
                    if col in [3, 4]:
                        cell.number_format = '#,##0.00'
            
            # Totals row
            total_row = len(accounts) + 2
            ws.cell(row=total_row, column=2, value="Totals")
            ws.cell(row=total_row, column=3, value=float(total_debit))
            ws.cell(row=total_row, column=4, value=float(total_credit))
            
            for col in range(2, 5):
                cell = ws.cell(row=total_row, column=col)
                cell.font = Font(bold=True)
                cell.border = ExcelService.THIN_BORDER
                if col in [3, 4]:
                    cell.number_format = '#,##0.00'
            
            # Balance check
            balance_row = total_row + 1
            is_balanced = total_debit == total_credit
            ws.cell(row=balance_row, column=2, value="Balance Check:")
            ws.cell(row=balance_row, column=3, value="✓ Balanced" if is_balanced else "✗ Not Balanced")
            
            wb.save(filepath)
            logger.info(f"Exported trial balance to {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Trial balance export failed: {e}")
            return False
    
    @staticmethod
    def export_accounts(accounts: List[Dict[str, Any]], 
                        filepath: str,
                        rtl: bool = False) -> bool:
        """Export chart of accounts to Excel file."""
        
        if not EXCEL_AVAILABLE:
            return False
        
        try:
            wb = Workbook()
            ws = wb.active
            ws.title = "Chart of Accounts"
            
            # Headers
            headers = ["Code", "Name (Arabic)", "Name (English)", "Type", 
                      "Parent Code", "Level", "Normal Balance", "Active"]
            
            # Write headers
            for col, header in enumerate(headers, 1):
                cell = ws.cell(row=1, column=col, value=header)
                cell.font = ExcelService.HEADER_FONT
                cell.fill = ExcelService.HEADER_FILL
                cell.alignment = ExcelService.HEADER_ALIGNMENT
                cell.border = ExcelService.THIN_BORDER
            
            # Write data
            for row_idx, account in enumerate(accounts, 2):
                ws.cell(row=row_idx, column=1, value=account.get('code', ''))
                ws.cell(row=row_idx, column=2, value=account.get('name_ar', ''))
                ws.cell(row=row_idx, column=3, value=account.get('name_en', ''))
                ws.cell(row=row_idx, column=4, value=account.get('type', ''))
                ws.cell(row=row_idx, column=5, value=account.get('parent_code', ''))
                ws.cell(row=row_idx, column=6, value=account.get('level', 1))
                ws.cell(row=row_idx, column=7, value=account.get('normal_balance', 'Debit'))
                ws.cell(row=row_idx, column=8, value="Yes" if account.get('active', True) else "No")
                
                # Apply styles
                for col in range(1, 9):
                    cell = ws.cell(row=row_idx, column=col)
                    cell.alignment = ExcelService.RTL_ALIGNMENT if rtl else ExcelService.CELL_ALIGNMENT
                    cell.border = ExcelService.THIN_BORDER
            
            # Auto-adjust column widths
            for col in ws.columns:
                max_length = 0
                column = col[0].column_letter
                for cell in col:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                ws.column_dimensions[column].width = adjusted_width
            
            wb.save(filepath)
            logger.info(f"Exported {len(accounts)} accounts to {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Accounts export failed: {e}")
            return False
    
    @staticmethod
    def import_accounts(filepath: str) -> Optional[List[Dict[str, Any]]]:
        """Import chart of accounts from Excel file."""
        
        if not EXCEL_AVAILABLE:
            logger.error("openpyxl not available")
            return None
        
        if not Path(filepath).exists():
            logger.error(f"File not found: {filepath}")
            return None
        
        try:
            wb = load_workbook(filepath, read_only=True)
            ws = wb.active
            
            accounts = []
            headers = None
            
            for row_idx, row in enumerate(ws.iter_rows(values_only=True), 1):
                if row_idx == 1:
                    headers = row
                    continue
                
                if not any(row):  # Skip empty rows
                    continue
                
                account = {
                    'code': str(row[0]) if row[0] else '',
                    'name_ar': row[1] if len(row) > 1 and row[1] else '',
                    'name_en': row[2] if len(row) > 2 and row[2] else '',
                    'type': row[3] if len(row) > 3 and row[3] else 'Asset',
                    'parent_code': str(row[4]) if len(row) > 4 and row[4] else None,
                    'level': int(row[5]) if len(row) > 5 and row[5] else 1,
                    'normal_balance': row[6] if len(row) > 6 and row[6] else 'Debit',
                    'active': row[7] != 'No' if len(row) > 7 else True
                }
                
                accounts.append(account)
            
            logger.info(f"Imported {len(accounts)} accounts from {filepath}")
            return accounts
            
        except Exception as e:
            logger.error(f"Accounts import failed: {e}")
            return None
    
    @staticmethod
    def create_template(template_type: str, filepath: str) -> bool:
        """Create an Excel template for import."""
        
        if not EXCEL_AVAILABLE:
            return False
        
        templates = {
            'accounts': {
                'headers': ['Code', 'Name (Arabic)', 'Name (English)', 'Type', 
                           'Parent Code', 'Level', 'Normal Balance', 'Active'],
                'example': ['1101', 'الصندوق', 'Cash', 'Asset', '', '3', 'Debit', 'Yes']
            },
            'customers': {
                'headers': ['Code', 'Name', 'Phone', 'Address', 'Tax Number', 
                           'Opening Balance', 'Credit Limit', 'Notes'],
                'example': ['C001', 'أحمد محمد', '0123456789', 'القاهرة', '123-456-789', 
                           '0', '50000', '']
            },
            'suppliers': {
                'headers': ['Code', 'Name', 'Phone', 'Address', 'Tax Number', 
                           'Opening Balance', 'Credit Limit', 'Notes'],
                'example': ['S001', 'شركة النور', '0123456789', 'الإسكندرية', '987-654-321', 
                           '0', '100000', '']
            }
        }
        
        if template_type not in templates:
            logger.error(f"Unknown template type: {template_type}")
            return False
        
        try:
            wb = Workbook()
            ws = wb.active
            ws.title = template_type.capitalize()
            
            template = templates[template_type]
            
            # Write headers
            for col, header in enumerate(template['headers'], 1):
                cell = ws.cell(row=1, column=col, value=header)
                cell.font = ExcelService.HEADER_FONT
                cell.fill = ExcelService.HEADER_FILL
                cell.alignment = ExcelService.HEADER_ALIGNMENT
                cell.border = ExcelService.THIN_BORDER
            
            # Write example row
            for col, value in enumerate(template['example'], 1):
                cell = ws.cell(row=2, column=col, value=value)
                cell.border = ExcelService.THIN_BORDER
            
            # Add instructions
            instruction_row = len(template['headers']) + 4
            ws.cell(row=instruction_row, column=1, value="Instructions:")
            ws.cell(row=instruction_row + 1, column=1, value="1. Do not modify the header row")
            ws.cell(row=instruction_row + 2, column=1, value="2. Fill in your data starting from row 3")
            ws.cell(row=instruction_row + 3, column=1, value="3. Save and import back to the system")
            
            wb.save(filepath)
            logger.info(f"Created {template_type} template at {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Template creation failed: {e}")
            return False
