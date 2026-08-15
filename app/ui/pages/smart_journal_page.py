"""
Smart Journal Page - Natural language to journal entry converter
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit,
    QPushButton, QFrame, QTableWidget, QTableWidgetItem,
    QHeaderView, QMessageBox, QProgressBar, QGridLayout
)
from PySide6.QtCore import Qt, Signal
from decimal import Decimal

import logging
from nlp.parser import parse_transaction
from accounting.engine import rules_engine

logger = logging.getLogger(__name__)


class SmartJournalPage(QWidget):
    """Smart Journal page for natural language transaction entry."""
    
    # Signals
    transaction_analyzed = Signal(object)
    
    def __init__(self):
        super().__init__()
        
        self.setStyleSheet("background-color: #f8f9fa;")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title
        title_label = QLabel("🧠 القيد الذكي")
        title_label.setFont(title_label.font())
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")
        layout.addWidget(title_label)
        
        # Description
        desc_label = QLabel(
            "اكتب العملية المحاسبية باللغة الطبيعية (عربي أو إنجليزي) وسيقوم النظام بتحليلها تلقائيًا"
        )
        desc_label.setStyleSheet("color: #666; font-size: 14px;")
        layout.addWidget(desc_label)
        
        # Input section
        input_frame = QFrame()
        input_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                padding: 20px;
            }
        """)
        input_layout = QVBoxLayout(input_frame)
        
        # Text input
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText(
            "اكتب العملية المحاسبية هنا...\n\nأمثلة:\n"
            "• شراء بضاعة نقدًا بمبلغ 10000 جنيه\n"
            "• دفعت إيجار المكتب 5000 من البنك\n"
            "• استلمت من العميل أحمد 15000 جنيه نقدًا\n"
            "• Paid office rent 5000 EGP from bank"
        )
        self.text_input.setMinimumHeight(100)
        self.text_input.setStyleSheet("""
            QTextEdit {
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                padding: 12px;
                font-size: 14px;
                font-family: 'Segoe UI', Arial;
            }
            QTextEdit:focus {
                border: 2px solid #1976d2;
            }
        """)
        input_layout.addWidget(self.text_input)
        
        # Analyze button
        analyze_btn = QPushButton("🔍 تحليل العملية")
        analyze_btn.setMinimumHeight(45)
        analyze_btn.setStyleSheet("""
            QPushButton {
                background-color: #1976d2;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
                padding: 12px 24px;
            }
            QPushButton:hover {
                background-color: #1565c0;
            }
            QPushButton:pressed {
                background-color: #0d47a1;
            }
        """)
        analyze_btn.clicked.connect(self.analyze_transaction)
        input_layout.addWidget(analyze_btn)
        
        layout.addWidget(input_frame)
        
        # Results section (initially hidden)
        self.results_frame = QFrame()
        self.results_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                padding: 20px;
            }
        """)
        results_layout = QVBoxLayout(self.results_frame)
        
        # Analysis summary
        summary_grid = QGridLayout()
        
        self.lbl_type = QLabel("نوع العملية: -")
        self.lbl_type.setStyleSheet("font-size: 13px; color: #333;")
        summary_grid.addWidget(self.lbl_type, 0, 0)
        
        self.lbl_amount = QLabel("المبلغ: -")
        self.lbl_amount.setStyleSheet("font-size: 13px; color: #333;")
        summary_grid.addWidget(self.lbl_amount, 0, 1)
        
        self.lbl_payment = QLabel("طريقة الدفع: -")
        self.lbl_payment.setStyleSheet("font-size: 13px; color: #333;")
        summary_grid.addWidget(self.lbl_payment, 1, 0)
        
        self.lbl_confidence = QLabel("درجة الثقة: -")
        self.lbl_confidence.setStyleSheet("font-size: 13px; font-weight: bold; color: #1976d2;")
        summary_grid.addWidget(self.lbl_confidence, 1, 1)
        
        results_layout.addLayout(summary_grid)
        
        # Confidence progress bar
        confidence_label = QLabel("درجة الثقة:")
        confidence_label.setStyleSheet("font-size: 12px; color: #666;")
        results_layout.addWidget(confidence_label)
        
        self.confidence_bar = QProgressBar()
        self.confidence_bar.setMinimum(0)
        self.confidence_bar.setMaximum(100)
        self.confidence_bar.setValue(0)
        self.confidence_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                text-align: center;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background-color: #4caf50;
            }
        """)
        results_layout.addWidget(self.confidence_bar)
        
        # Journal entries table
        table_label = QLabel("القيود المقترحة:")
        table_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #333; margin-top: 15px;")
        results_layout.addWidget(table_label)
        
        self.entries_table = QTableWidget()
        self.entries_table.setColumnCount(4)
        self.entries_table.setHorizontalHeaderLabels(["الحساب", "البيان", "مدين", "دائن"])
        self.entries_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.entries_table.setMinimumHeight(150)
        self.entries_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                gridline-color: #e0e0e0;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QHeaderView::section {
                background-color: #f5f5f5;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """)
        results_layout.addWidget(self.entries_table)
        
        # Balance status
        self.balance_label = QLabel("")
        self.balance_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        results_layout.addWidget(self.balance_label)
        
        # Action buttons
        btn_layout = QHBoxLayout()
        
        approve_btn = QPushButton("✓ اعتماد القيد")
        approve_btn.setStyleSheet("""
            QPushButton {
                background-color: #4caf50;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 13px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #43a047;
            }
        """)
        approve_btn.clicked.connect(self.approve_entry)
        btn_layout.addWidget(approve_btn)
        
        edit_btn = QPushButton("✏️ تعديل")
        edit_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff9800;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 13px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #fb8c00;
            }
        """)
        btn_layout.addWidget(edit_btn)
        
        reanalyze_btn = QPushButton("🔄 إعادة التحليل")
        reanalyze_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196f3;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 13px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #1e88e5;
            }
        """)
        reanalyze_btn.clicked.connect(self.reanalyze)
        btn_layout.addWidget(reanalyze_btn)
        
        btn_layout.addStretch()
        results_layout.addLayout(btn_layout)
        
        layout.addWidget(self.results_frame)
        layout.addStretch()
        
        # Hide results initially
        self.results_frame.setVisible(False)
        
        logger.info("Smart Journal page initialized")
    
    def analyze_transaction(self):
        """Analyze the entered transaction text."""
        text = self.text_input.toPlainText().strip()
        
        if not text:
            QMessageBox.warning(
                self,
                "تحذير",
                "الرجاء إدخال نص العملية المحاسبية"
            )
            return
        
        try:
            logger.info(f"Analyzing transaction: {text}")
            
            # Parse with NLP
            parsed = parse_transaction(text)
            
            # Match against rules engine
            rule_match = rules_engine.match_transaction(text, parsed.language)
            if rule_match:
                parsed.rule_matched = rule_match["rule_key"]
            
            # Display results
            self.display_analysis(parsed)
            
            self.transaction_analyzed.emit(parsed)
            
        except Exception as e:
            logger.exception(f"Error analyzing transaction: {e}")
            QMessageBox.critical(
                self,
                "خطأ",
                f"حدث خطأ أثناء التحليل: {str(e)}"
            )
    
    def display_analysis(self, parsed):
        """Display analysis results."""
        self.results_frame.setVisible(True)
        
        # Update summary labels
        type_text = parsed.transaction_type or "غير محدد"
        self.lbl_type.setText(f"نوع العملية: {type_text}")
        
        amount_text = f"{parsed.amount:,} {parsed.currency}" if parsed.amount else "غير محدد"
        self.lbl_amount.setText(f"المبلغ: {amount_text}")
        
        payment_text = parsed.payment_method or "غير محدد"
        self.lbl_payment.setText(f"طريقة الدفع: {payment_text}")
        
        # Update confidence
        confidence = int(parsed.confidence)
        self.lbl_confidence.setText(f"درجة الثقة: {confidence}%")
        self.confidence_bar.setValue(confidence)
        
        # Color code confidence
        if confidence >= 90:
            color = "#4caf50"  # Green
        elif confidence >= 75:
            color = "#8bc34a"  # Light green
        elif confidence >= 50:
            color = "#ff9800"  # Orange
        else:
            color = "#f44336"  # Red
        
        self.confidence_bar.setStyleSheet(f"""
            QProgressBar {{
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                text-align: center;
                font-weight: bold;
            }}
            QProgressBar::chunk {{
                background-color: {color};
            }}
        """)
        
        # Clear and populate table
        self.entries_table.setRowCount(0)
        
        # TODO: Add actual journal lines based on parsed data
        # For now, show placeholder
        self.entries_table.setRowCount(2)
        self.entries_table.setItem(0, 0, QTableWidgetItem("المشتريات"))
        self.entries_table.setItem(0, 2, QTableWidgetItem(str(parsed.amount or 0)))
        self.entries_table.setItem(1, 0, QTableWidgetItem("الصندوق"))
        self.entries_table.setItem(1, 3, QTableWidgetItem(str(parsed.amount or 0)))
        
        # Update balance status
        if parsed.amount:
            self.balance_label.setText("✓ القيد متوازن")
            self.balance_label.setStyleSheet(
                "font-size: 14px; font-weight: bold; color: #4caf50;"
            )
        else:
            self.balance_label.setText("⚠️ يحتاج مراجعة")
            self.balance_label.setStyleSheet(
                "font-size: 14px; font-weight: bold; color: #ff9800;"
            )
        
        # Show ambiguities if any
        if parsed.ambiguities:
            ambiguity_msg = "\n".join(f"• {amb}" for amb in parsed.ambiguities)
            QMessageBox.information(
                self,
                "غموض في البيانات",
                f"تم اكتشاف بعض الغموض:\n\n{ambiguity_msg}"
            )
    
    def approve_entry(self):
        """Approve and save the journal entry."""
        QMessageBox.information(
            self,
            "تم الاعتماد",
            "سيتم حفظ القيد بعد المراجعة النهائية (ميزة قيد التطوير)"
        )
    
    def reanalyze(self):
        """Re-analyze the transaction."""
        self.text_input.clear()
        self.results_frame.setVisible(False)
        self.text_input.setFocus()
