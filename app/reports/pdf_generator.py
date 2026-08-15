# Finovate Journal AI - PDF Report Generator

"""
PDF report generator for Finovate Journal AI.
Uses ReportLab to create professional PDF reports with Arabic support.
"""

from typing import List, Dict, Any, Optional
from decimal import Decimal
from pathlib import Path
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch, cm
    from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.lib.fonts import addMapping
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    logger.warning("ReportLab not installed. PDF features disabled.")


class PDFReportGenerator:
    """Generate professional PDF reports."""
    
    def __init__(self, language: str = 'ar'):
        self.language = language
        self.rtl = language == 'ar'
        self.styles = None
        self._setup_fonts()
    
    def _setup_fonts(self):
        """Setup fonts for Arabic and English support."""
        if not PDF_AVAILABLE:
            return
        
        try:
            # Try to register Arabic font (if available)
            # Common Arabic fonts: Arial, Traditional Arabic, Simplified Arabic
            font_paths = [
                "/usr/share/fonts/truetype/arabeyes/ae_AlArabiya.ttf",
                "/usr/share/fonts/truetype/kacst/KacstBook.ttf",
                "C:\\Windows\\Fonts\\arial.ttf",
            ]
            
            for font_path in font_paths:
                if Path(font_path).exists():
                    pdfmetrics.registerFont(TTFont('ArabicFont', font_path))
                    addMapping('ArabicFont', 0, 0, 'ArabicFont')
                    break
            else:
                # Use default font
                pass
            
            self.styles = getSampleStyleSheet()
            
            # Custom styles for Arabic
            if self.rtl:
                self.styles.add(ParagraphStyle(
                    name='ArabicHeading',
                    parent=self.styles['Heading1'],
                    alignment=TA_RIGHT,
                    rightIndent=20,
                    leftIndent=20,
                    fontName='Helvetica-Bold'  # Fallback
                ))
                
                self.styles.add(ParagraphStyle(
                    name='ArabicNormal',
                    parent=self.styles['Normal'],
                    alignment=TA_RIGHT,
                    rightIndent=10,
                    leftIndent=10,
                    fontName='Helvetica'
                ))
        
        except Exception as e:
            logger.warning(f"Font setup failed: {e}")
    
    def generate_journal_report(self, entries: List[Dict[str, Any]], 
                                filepath: str,
                                company_name: str = "",
                                period_from: str = "",
                                period_to: str = "") -> bool:
        """Generate Journal Entries PDF report."""
        
        if not PDF_AVAILABLE:
            logger.error("ReportLab not available")
            return False
        
        try:
            doc = SimpleDocTemplate(
                filepath,
                pagesize=landscape(A4),
                rightMargin=1*cm,
                leftMargin=1*cm,
                topMargin=1*cm,
                bottomMargin=1*cm
            )
            
            elements = []
            
            # Title
            title_text = "دفتر اليومية" if self.rtl else "Journal Entries"
            elements.append(Paragraph(title_text, self.styles.get('ArabicHeading' if self.rtl else 'Heading1')))
            elements.append(Spacer(1, 0.3*inch))
            
            # Company info
            if company_name:
                elements.append(Paragraph(company_name, self.styles.get('ArabicNormal' if self.rtl else 'Normal')))
            
            # Period info
            if period_from and period_to:
                period_text = f"من {period_from} إلى {period_to}" if self.rtl else f"From {period_from} To {period_to}"
                elements.append(Paragraph(period_text, self.styles.get('ArabicNormal' if self.rtl else 'Normal')))
            
            elements.append(Spacer(1, 0.3*inch))
            
            # Table data
            headers = [
                "رقم القيد" if self.rtl else "Entry No",
                "التاريخ" if self.rtl else "Date",
                "البيان" if self.rtl else "Description",
                "الحساب" if self.rtl else "Account",
                "مدين" if self.rtl else "Debit",
                "دائن" if self.rtl else "Credit"
            ]
            
            table_data = [headers]
            
            total_debit = Decimal('0')
            total_credit = Decimal('0')
            
            for entry in entries:
                debit = entry.get('debit', Decimal('0'))
                credit = entry.get('credit', Decimal('0'))
                
                row = [
                    str(entry.get('entry_no', '')),
                    str(entry.get('date', '')),
                    str(entry.get('description', '')),
                    str(entry.get('account_name', '')),
                    f"{float(debit):,.2f}" if isinstance(debit, Decimal) else f"{debit:,.2f}",
                    f"{float(credit):,.2f}" if isinstance(credit, Decimal) else f"{credit:,.2f}"
                ]
                
                total_debit += debit if isinstance(debit, Decimal) else Decimal(str(debit))
                total_credit += credit if isinstance(credit, Decimal) else Decimal(str(credit))
                
                table_data.append(row)
            
            # Create table
            table = Table(table_data, colWidths=[1.2*inch, 1*inch, 2.5*inch, 2*inch, 1.2*inch, 1.2*inch])
            
            # Table style
            style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4472C4')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'RIGHT' if self.rtl else 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            ])
            
            # Format amounts columns
            for i in range(len(table_data)):
                style.add('VALIGN', (4, i), (5, i), 'MIDDLE')
            
            table.setStyle(style)
            elements.append(table)
            
            elements.append(Spacer(1, 0.3*inch))
            
            # Totals
            totals_text = "الإجماليات:" if self.rtl else "Totals:"
            elements.append(Paragraph(totals_text, self.styles.get('ArabicNormal' if self.rtl else 'Normal')))
            
            totals_data = [
                ['', '', '', 'الإجمالي' if self.rtl else 'Total:', 
                 f"{float(total_debit):,.2f}", f"{float(total_credit):,.2f}"]
            ]
            
            totals_table = Table(totals_data, colWidths=[1.2*inch, 1*inch, 2.5*inch, 2*inch, 1.2*inch, 1.2*inch])
            totals_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('ALIGN', (0, 0), (-1, 0), 'RIGHT' if self.rtl else 'LEFT'),
                ('GRID', (0, 0), (-1, 0), 1, colors.black),
            ]))
            
            elements.append(totals_table)
            
            # Balance check
            elements.append(Spacer(1, 0.2*inch))
            is_balanced = total_debit == total_credit
            balance_text = "✓ القيد متوازن" if is_balanced else "✗ القيد غير متوازن"
            balance_color = colors.green if is_balanced else colors.red
            balance_para = Paragraph(balance_text, self.styles.get('ArabicNormal' if self.rtl else 'Normal'))
            elements.append(balance_para)
            
            # Footer
            elements.append(Spacer(1, 0.5*inch))
            footer_text = f"تم إنشاء التقرير في {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            elements.append(Paragraph(footer_text, self.styles.get('ArabicNormal' if self.rtl else 'Normal')))
            
            # Build PDF
            doc.build(elements)
            logger.info(f"Generated journal report: {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"PDF generation failed: {e}")
            return False
    
    def generate_trial_balance(self, accounts: List[Dict[str, Any]], 
                               filepath: str,
                               company_name: str = "",
                               period_from: str = "",
                               period_to: str = "") -> bool:
        """Generate Trial Balance PDF report."""
        
        if not PDF_AVAILABLE:
            return False
        
        try:
            doc = SimpleDocTemplate(
                filepath,
                pagesize=A4,
                rightMargin=1*cm,
                leftMargin=1*cm,
                topMargin=1*cm,
                bottomMargin=1*cm
            )
            
            elements = []
            
            # Title
            title_text = "ميزان المراجعة" if self.rtl else "Trial Balance"
            elements.append(Paragraph(title_text, self.styles.get('ArabicHeading' if self.rtl else 'Heading1')))
            elements.append(Spacer(1, 0.3*inch))
            
            # Company info
            if company_name:
                elements.append(Paragraph(company_name, self.styles.get('ArabicNormal' if self.rtl else 'Normal')))
            
            # Period info
            if period_from and period_to:
                period_text = f"من {period_from} إلى {period_to}" if self.rtl else f"From {period_from} To {period_to}"
                elements.append(Paragraph(period_text, self.styles.get('ArabicNormal' if self.rtl else 'Normal')))
            
            elements.append(Spacer(1, 0.3*inch))
            
            # Table data
            headers = [
                "الكود" if self.rtl else "Code",
                "الحساب" if self.rtl else "Account",
                "مدين" if self.rtl else "Debit",
                "دائن" if self.rtl else "Credit"
            ]
            
            table_data = [headers]
            
            total_debit = Decimal('0')
            total_credit = Decimal('0')
            
            for account in accounts:
                debit = account.get('debit', Decimal('0'))
                credit = account.get('credit', Decimal('0'))
                
                row = [
                    str(account.get('code', '')),
                    str(account.get('name_ar' if self.rtl else 'name_en', '')),
                    f"{float(debit):,.2f}" if isinstance(debit, Decimal) else f"{debit:,.2f}",
                    f"{float(credit):,.2f}" if isinstance(credit, Decimal) else f"{credit:,.2f}"
                ]
                
                total_debit += debit if isinstance(debit, Decimal) else Decimal(str(debit))
                total_credit += credit if isinstance(credit, Decimal) else Decimal(str(credit))
                
                table_data.append(row)
            
            # Create table
            table = Table(table_data, colWidths=[0.8*inch, 3*inch, 1.5*inch, 1.5*inch])
            
            # Table style
            style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4472C4')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'RIGHT' if self.rtl else 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            ])
            
            table.setStyle(style)
            elements.append(table)
            
            # Totals
            elements.append(Spacer(1, 0.3*inch))
            
            totals_data = [
                ['', 'الإجمالي' if self.rtl else 'Totals:', 
                 f"{float(total_debit):,.2f}", f"{float(total_credit):,.2f}"]
            ]
            
            totals_table = Table(totals_data, colWidths=[0.8*inch, 3*inch, 1.5*inch, 1.5*inch])
            totals_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('ALIGN', (0, 0), (-1, 0), 'RIGHT' if self.rtl else 'LEFT'),
                ('GRID', (0, 0), (-1, 0), 1, colors.black),
            ]))
            
            elements.append(totals_table)
            
            # Balance check
            elements.append(Spacer(1, 0.2*inch))
            is_balanced = total_debit == total_credit
            balance_text = "✓ متوازن" if is_balanced else "✗ غير متوازن"
            balance_para = Paragraph(balance_text, self.styles.get('ArabicNormal' if self.rtl else 'Normal'))
            elements.append(balance_para)
            
            # Footer
            elements.append(Spacer(1, 0.5*inch))
            footer_text = f"Finovate Journal AI - {datetime.now().strftime('%Y-%m-%d')}"
            elements.append(Paragraph(footer_text, self.styles.get('ArabicNormal' if self.rtl else 'Normal')))
            
            doc.build(elements)
            logger.info(f"Generated trial balance report: {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Trial balance PDF generation failed: {e}")
            return False
