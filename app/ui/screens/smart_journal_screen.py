"""
Finovate Journal AI - Smart Journal Screen
Copyright © 2025 Ahmed Mostafa Ibrahim — All Rights Reserved.
"""

from decimal import Decimal
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QTextEdit, QPushButton, QFrame, QTableWidget, 
    QTableWidgetItem, QHeaderView, QMessageBox, QSplitter,
    QProgressBar, QGroupBox, QGridLayout
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

from app.nlp.transaction_parser import TransactionParser
from app.accounting.rules_engine import RulesEngine
from app.database.db_manager import DatabaseManager
from app.utils.logger import get_logger

logger = get_logger(__name__)


class SmartJournalScreen(QWidget):
    """Smart Journal entry screen with NLP parsing"""
    
    def __init__(self):
        super().__init__()
        
        self.parser = TransactionParser()
        self.rules_engine = RulesEngine()
        self.db_manager = DatabaseManager()
        self.current_analysis = None
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # Title
        title_label = QLabel("🧠 القيد الذكي")
        title_label.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title_label.setStyleSheet("color: #4CAF50;")
        main_layout.addWidget(title_label)
        
        # Description
        desc_label = QLabel("اكتب العملية المحاسبية باللغة الطبيعية وسيقوم النظام بتحليلها تلقائيًا")
        desc_label.setFont(QFont("Segoe UI", 11))
        desc_label.setStyleSheet("color: #888;")
        main_layout.addWidget(desc_label)
        
        # Input section
        input_group = QGroupBox("إدخال العملية")
        input_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                color: #E0E0E0;
                border: 1px solid #3D3D3D;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        input_layout = QVBoxLayout()
        input_layout.setSpacing(15)
        
        # Text input
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText(
            "مثال:\n"
            "• شراء بضاعة نقدًا بمبلغ 10000 جنيه\n"
            "• دفعت إيجار المكتب 5000 جنيه من البنك\n"
            "• استلمت من العميل أحمد 15000 جنيه نقدًا\n"
            "• اشتريت بضاعة من شركة النور بمبلغ 11400 شامل ضريبة القيمة المضافة"
        )
        self.text_input.setFont(QFont("Segoe UI", 12))
        self.text_input.setMinimumHeight(120)
        self.text_input.setStyleSheet("""
            QTextEdit {
                background-color: #2D2D2D;
                color: #E0E0E0;
                border: 1px solid #3D3D3D;
                border-radius: 8px;
                padding: 10px;
            }
            QTextEdit:focus {
                border: 1px solid #4CAF50;
            }
        """)
        input_layout.addWidget(self.text_input)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)
        
        self.analyze_btn = QPushButton("🔍 تحليل العملية")
        self.analyze_btn.setFixedHeight(50)
        self.analyze_btn.setCursor(Qt.PointingHandCursor)
        self.analyze_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                padding: 10px 30px;
            }
            QPushButton:hover {
                background-color: #45A049;
            }
            QPushButton:disabled {
                background-color: #555;
            }
        """)
        self.analyze_btn.clicked.connect(self.analyze_transaction)
        btn_layout.addWidget(self.analyze_btn)
        
        btn_layout.addStretch()
        input_layout.addLayout(btn_layout)
        input_group.setLayout(input_layout)
        main_layout.addWidget(input_group)
        
        # Results section (hidden initially)
        self.results_frame = QFrame()
        self.results_frame.setVisible(False)
        self.results_frame.setStyleSheet("background-color: #2D2D2D; border-radius: 12px;")
        
        results_layout = QVBoxLayout()
        results_layout.setSpacing(20)
        results_layout.setContentsMargins(20, 20, 20, 20)
        
        # Analysis summary
        summary_title = QLabel("نتائج التحليل")
        summary_title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        summary_title.setStyleSheet("color: #4CAF50;")
        results_layout.addWidget(summary_title)
        
        # Summary grid
        summary_grid = QGridLayout()
        summary_grid.setSpacing(15)
        
        self.summary_labels = {}
        summary_fields = [
            ("نوع العملية", "transaction_type"),
            ("المبلغ", "amount"),
            ("طريقة الدفع", "payment_method"),
            ("درجة الثقة", "confidence"),
        ]
        
        for i, (label_text, key) in enumerate(summary_fields):
            label = QLabel(label_text + ":")
            label.setFont(QFont("Segoe UI", 11))
            label.setStyleSheet("color: #888;")
            summary_grid.addWidget(label, i, 0)
            
            value_label = QLabel("-")
            value_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
            value_label.setStyleSheet("color: #E0E0E0;")
            summary_grid.addWidget(value_label, i, 1)
            self.summary_labels[key] = value_label
        
        results_layout.addLayout(summary_grid)
        
        # Confidence progress bar
        confidence_label = QLabel("درجة الثقة:")
        confidence_label.setFont(QFont("Segoe UI", 11))
        confidence_label.setStyleSheet("color: #888;")
        results_layout.addWidget(confidence_label)
        
        self.confidence_bar = QProgressBar()
        self.confidence_bar.setRange(0, 100)
        self.confidence_bar.setValue(0)
        self.confidence_bar.setFormat("%p%")
        self.confidence_bar.setStyleSheet("""
            QProgressBar {
                background-color: #3D3D3D;
                border-radius: 8px;
                text-align: center;
                color: white;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                border-radius: 8px;
            }
        """)
        results_layout.addWidget(self.confidence_bar)
        
        # Journal entries table
        table_title = QLabel("القيد المقترح:")
        table_title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        table_title.setStyleSheet("color: #E0E0E0;")
        results_layout.addWidget(table_title)
        
        self.entries_table = QTableWidget()
        self.entries_table.setColumnCount(4)
        self.entries_table.setHorizontalHeaderLabels(["الحساب", "البيان", "مدين", "دائن"])
        self.entries_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.entries_table.setAlternatingRowColors(True)
        self.entries_table.setStyleSheet("""
            QTableWidget {
                background-color: #1E1E1E;
                color: #E0E0E0;
                border: 1px solid #3D3D3D;
                border-radius: 8px;
                gridline-color: #3D3D3D;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QHeaderView::section {
                background-color: #2D2D2D;
                color: #4CAF50;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """)
        self.entries_table.setFixedHeight(200)
        results_layout.addWidget(self.entries_table)
        
        # Balance info
        self.balance_label = QLabel("")
        self.balance_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.balance_label.setAlignment(Qt.AlignCenter)
        results_layout.addWidget(self.balance_label)
        
        # Action buttons
        action_btn_layout = QHBoxLayout()
        action_btn_layout.setSpacing(15)
        
        self.approve_btn = QPushButton("✓ اعتماد القيد")
        self.approve_btn.setFixedHeight(45)
        self.approve_btn.setCursor(Qt.PointingHandCursor)
        self.approve_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45A049;
            }
            QPushButton:disabled {
                background-color: #555;
            }
        """)
        self.approve_btn.clicked.connect(self.approve_entry)
        self.approve_btn.setEnabled(False)
        action_btn_layout.addWidget(self.approve_btn)
        
        self.edit_btn = QPushButton("✏️ تعديل")
        self.edit_btn.setFixedHeight(45)
        self.edit_btn.setCursor(Qt.PointingHandCursor)
        self.edit_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        self.edit_btn.clicked.connect(self.edit_entry)
        action_btn_layout.addWidget(self.edit_btn)
        
        self.retry_btn = QPushButton("🔄 إعادة التحليل")
        self.retry_btn.setFixedHeight(45)
        self.retry_btn.setCursor(Qt.PointingHandCursor)
        self.retry_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #F57C00;
            }
        """)
        self.retry_btn.clicked.connect(self.retry_analysis)
        action_btn_layout.addWidget(self.retry_btn)
        
        action_btn_layout.addStretch()
        results_layout.addLayout(action_btn_layout)
        
        self.results_frame.setLayout(results_layout)
        main_layout.addWidget(self.results_frame)
        
        main_layout.addStretch()
        self.setLayout(main_layout)
    
    def analyze_transaction(self):
        """Analyze the entered transaction text"""
        text = self.text_input.toPlainText().strip()
        
        if not text:
            QMessageBox.warning(self, "تحذير", "الرجاء إدخال نص العملية المحاسبية")
            return
        
        try:
            logger.info(f"Analyzing transaction: {text}")
            
            # Parse using NLP
            result = self.parser.parse(text)
            
            # Apply rules engine
            rule_result = self.rules_engine.apply_rules(result)
            
            self.current_analysis = rule_result
            
            # Display results
            self.display_results(rule_result)
            
        except Exception as e:
            logger.error(f"Error analyzing transaction: {e}")
            QMessageBox.critical(
                self, "خطأ",
                f"حدث خطأ أثناء تحليل العملية:\n{str(e)}"
            )
    
    def display_results(self, result: dict):
        """Display analysis results"""
        self.results_frame.setVisible(True)
        
        # Update summary labels
        self.summary_labels['transaction_type'].setText(
            result.get('transaction_type', 'غير محدد')
        )
        
        amount = result.get('amount', Decimal('0'))
        currency = result.get('currency', 'EGP')
        self.summary_labels['amount'].setText(
            f"{amount:,.2f} {currency}"
        )
        
        self.summary_labels['payment_method'].setText(
            result.get('payment_method', 'غير محدد')
        )
        
        confidence = result.get('confidence', 0)
        self.summary_labels['confidence'].setText(f"{confidence}%")
        
        # Update confidence bar
        self.confidence_bar.setValue(int(confidence))
        
        # Color code confidence
        if confidence >= 90:
            color = "#4CAF50"  # Green
        elif confidence >= 75:
            color = "#8BC34A"  # Light green
        elif confidence >= 50:
            color = "#FF9800"  # Orange
        else:
            color = "#F44336"  # Red
        
        self.confidence_bar.setStyleSheet(f"""
            QProgressBar {{
                background-color: #3D3D3D;
                border-radius: 8px;
                text-align: center;
                color: white;
                font-weight: bold;
            }}
            QProgressBar::chunk {{
                background-color: {color};
                border-radius: 8px;
            }}
        """)
        
        # Populate journal entries table
        entries = result.get('entries', [])
        self.entries_table.setRowCount(len(entries))
        
        total_debit = Decimal('0')
        total_credit = Decimal('0')
        
        for row, entry in enumerate(entries):
            account = entry.get('account', '')
            description = entry.get('description', '')
            debit = entry.get('debit', Decimal('0'))
            credit = entry.get('credit', Decimal('0'))
            
            self.entries_table.setItem(row, 0, QTableWidgetItem(account))
            self.entries_table.setItem(row, 1, QTableWidgetItem(description))
            self.entries_table.setItem(row, 2, QTableWidgetItem(f"{debit:,.2f}"))
            self.entries_table.setItem(row, 3, QTableWidgetItem(f"{credit:,.2f}"))
            
            total_debit += debit
            total_credit += credit
        
        # Update balance label
        if total_debit == total_credit:
            self.balance_label.setText(
                f"✓ القيد متوازن | إجمالي المدين: {total_debit:,.2f} | إجمالي الدائن: {total_credit:,.2f}"
            )
            self.balance_label.setStyleSheet("color: #4CAF50;")
            self.approve_btn.setEnabled(True)
        else:
            self.balance_label.setText(
                f"⚠️ القيد غير متوازن | مدين: {total_debit:,.2f} | دائن: {total_credit:,.2f}"
            )
            self.balance_label.setStyleSheet("color: #F44336;")
            self.approve_btn.setEnabled(False)
    
    def approve_entry(self):
        """Approve and save the journal entry"""
        if not self.current_analysis:
            return
        
        try:
            # TODO: Save to database
            QMessageBox.information(
                self, "نجاح",
                "تم اعتماد القيد بنجاح (سيتم الحفظ في قاعدة البيانات قريبًا)"
            )
            logger.info("Journal entry approved")
            
        except Exception as e:
            logger.error(f"Error approving entry: {e}")
            QMessageBox.critical(
                self, "خطأ",
                f"حدث خطأ أثناء اعتماد القيد:\n{str(e)}"
            )
    
    def edit_entry(self):
        """Edit the journal entry"""
        QMessageBox.information(
            self, "تعديل",
            "ستكون ميزة التعديل متاحة قريبًا"
        )
        logger.info("Edit entry clicked")
    
    def retry_analysis(self):
        """Retry the analysis"""
        self.text_input.clear()
        self.results_frame.setVisible(False)
        self.current_analysis = None
        logger.info("Analysis reset")
