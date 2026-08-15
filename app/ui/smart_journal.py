"""Smart Journal page for natural language entry."""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, 
    QPushButton, QFrame, QTableWidget, QTableWidgetItem,
    QHeaderView, QMessageBox, QProgressBar
)
from PySide6.QtCore import Qt
from decimal import Decimal

from ..nlp.parser import NLPParser
from ..config.constants import ENTRY_STATUS


class SmartJournalPage(QWidget):
    """Smart Journal page for natural language accounting entries."""

    def __init__(self):
        super().__init__()
        
        self.parser = NLPParser()
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Page title
        title = QLabel("🧠 القيد الذكي")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2E86AB; padding: 10px;")
        layout.addWidget(title)
        
        # Input section
        input_frame = QFrame()
        input_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        input_layout = QVBoxLayout(input_frame)
        
        input_label = QLabel("اكتب العملية المحاسبية هنا باللغة الطبيعية:")
        input_label.setStyleSheet("font-size: 14px; color: #333; padding: 5px;")
        input_layout.addWidget(input_label)
        
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText(
            "مثال: شراء بضاعة نقدًا بمبلغ 10000 جنيه\n"
            "Example: Purchase goods for cash 10000 EGP"
        )
        self.text_input.setMinimumHeight(100)
        self.text_input.setStyleSheet("""
            QTextEdit {
                border: 2px solid #E0E0E0;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
            }
            QTextEdit:focus {
                border: 2px solid #2E86AB;
            }
        """)
        input_layout.addWidget(self.text_input)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        self.analyze_btn = QPushButton("🔍 تحليل العملية")
        self.analyze_btn.setStyleSheet("""
            QPushButton {
                background-color: #2E86AB;
                color: white;
                border: none;
                padding: 12px 25px;
                font-size: 14px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1E6B8A;
            }
            QPushButton:pressed {
                background-color: #155570;
            }
        """)
        self.analyze_btn.setCursor(Qt.PointingHandCursor)
        self.analyze_btn.clicked.connect(self._analyze_transaction)
        btn_layout.addWidget(self.analyze_btn)
        
        btn_layout.addStretch()
        input_layout.addLayout(btn_layout)
        
        layout.addWidget(input_frame)
        
        # Analysis results section
        self.results_frame = QFrame()
        self.results_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        results_layout = QVBoxLayout(self.results_frame)
        
        # Results header
        results_title = QLabel("📊 نتيجة التحليل")
        results_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")
        results_layout.addWidget(results_title)
        
        # Confidence indicator
        confidence_layout = QHBoxLayout()
        confidence_layout.addWidget(QLabel("درجة الثقة:"))
        self.confidence_bar = QProgressBar()
        self.confidence_bar.setRange(0, 100)
        self.confidence_bar.setValue(0)
        self.confidence_bar.setTextVisible(True)
        self.confidence_bar.setFormat("%p%")
        self.confidence_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #E0E0E0;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #E74C3C;
                border-radius: 5px;
            }
        """)
        confidence_layout.addWidget(self.confidence_bar)
        results_layout.addLayout(confidence_layout)
        
        # Explanation
        self.explanation_label = QLabel("")
        self.explanation_label.setStyleSheet("color: #666; padding: 10px;")
        self.explanation_label.setWordWrap(True)
        results_layout.addWidget(self.explanation_label)
        
        # Journal entries table
        self.entries_table = QTableWidget()
        self.entries_table.setColumnCount(4)
        self.entries_table.setHorizontalHeaderLabels(["الحساب", "البيان", "مدين", "دائن"])
        self.entries_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.entries_table.setMinimumHeight(150)
        self.entries_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #E0E0E0;
                border-radius: 5px;
                gridline-color: #E0E0E0;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QHeaderView::section {
                background-color: #F5F5F5;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """)
        results_layout.addWidget(self.entries_table)
        
        # Balance status
        self.balance_label = QLabel("")
        self.balance_label.setStyleSheet("font-size: 14px; padding: 10px;")
        self.balance_label.setAlignment(Qt.AlignCenter)
        results_layout.addWidget(self.balance_label)
        
        # Action buttons
        action_layout = QHBoxLayout()
        
        self.approve_btn = QPushButton("✓ اعتماد القيد")
        self.approve_btn.setStyleSheet("""
            QPushButton {
                background-color: #27AE60;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #1E8449;
            }
            QPushButton:disabled {
                background-color: #95A5A6;
            }
        """)
        self.approve_btn.setCursor(Qt.PointingHandCursor)
        self.approve_btn.setEnabled(False)
        self.approve_btn.clicked.connect(self._approve_entry)
        action_layout.addWidget(self.approve_btn)
        
        self.edit_btn = QPushButton("✏️ تعديل")
        self.edit_btn.setStyleSheet("""
            QPushButton {
                background-color: #F39C12;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #D68910;
            }
        """)
        self.edit_btn.setCursor(Qt.PointingHandCursor)
        self.edit_btn.setEnabled(False)
        action_layout.addWidget(self.edit_btn)
        
        self.retry_btn = QPushButton("🔄 إعادة التحليل")
        self.retry_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498DB;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
        """)
        self.retry_btn.setCursor(Qt.PointingHandCursor)
        self.retry_btn.clicked.connect(self._retry_analysis)
        action_layout.addWidget(self.retry_btn)
        
        action_layout.addStretch()
        results_layout.addLayout(action_layout)
        
        layout.addWidget(self.results_frame)
        self.results_frame.setVisible(False)
        
        layout.addStretch()
    
    def _analyze_transaction(self):
        """Analyze the entered transaction."""
        text = self.text_input.toPlainText().strip()
        
        if not text:
            QMessageBox.warning(self, "تنبيه", "يرجى كتابة العملية المحاسبية أولاً")
            return
        
        # Parse the transaction
        result = self.parser.parse(text)
        
        # Update UI with results
        self._display_results(result)
    
    def _display_results(self, result: dict):
        """Display analysis results."""
        self.results_frame.setVisible(True)
        
        # Update confidence
        confidence = result.get("confidence", 0)
        self.confidence_bar.setValue(int(confidence))
        
        # Set confidence color
        if confidence >= 90:
            color = "#27AE60"  # Green
        elif confidence >= 75:
            color = "#F39C12"  # Orange
        else:
            color = "#E74C3C"  # Red
        
        self.confidence_bar.setStyleSheet(f"""
            QProgressBar {{
                border: 1px solid #E0E0E0;
                border-radius: 5px;
                text-align: center;
            }}
            QProgressBar::chunk {{
                background-color: {color};
                border-radius: 5px;
            }}
        """)
        
        # Update explanation
        if result.get("language") == "ar":
            self.explanation_label.setText(result.get("explanation_ar", ""))
        else:
            self.explanation_label.setText(result.get("explanation", ""))
        
        # Populate table
        self.entries_table.setRowCount(0)
        
        if result.get("debit_account") and result.get("credit_account") and result.get("amount"):
            amount = result["amount"]
            
            # Debit row
            debit_row = self.entries_table.rowCount()
            self.entries_table.insertRow(debit_row)
            self.entries_table.setItem(debit_row, 0, QTableWidgetItem(result["debit_account"]))
            self.entries_table.setItem(debit_row, 1, QTableWidgetItem(result.get("explanation", "")))
            self.entries_table.setItem(debit_row, 2, QTableWidgetItem(str(amount)))
            self.entries_table.setItem(debit_row, 3, QTableWidgetItem("0.000"))
            
            # Credit row
            credit_row = self.entries_table.rowCount()
            self.entries_table.insertRow(credit_row)
            self.entries_table.setItem(credit_row, 0, QTableWidgetItem(result["credit_account"]))
            self.entries_table.setItem(credit_row, 1, QTableWidgetItem("دفع"))
            self.entries_table.setItem(credit_row, 2, QTableWidgetItem("0.000"))
            self.entries_table.setItem(credit_row, 3, QTableWidgetItem(str(amount)))
            
            # Update balance label
            self.balance_label.setText(
                f"✓ القيد متوازن | إجمالي المدين: {amount} | إجمالي الدائن: {amount}"
            )
            self.balance_label.setStyleSheet("color: #27AE60; font-size: 14px; padding: 10px;")
            
            # Enable action buttons
            self.approve_btn.setEnabled(True)
            self.edit_btn.setEnabled(True)
        else:
            self.balance_label.setText("⚠️ لم يتم تحديد الحسابات أو المبلغ بشكل كامل")
            self.balance_label.setStyleSheet("color: #E74C3C; font-size: 14px; padding: 10px;")
            self.approve_btn.setEnabled(False)
            self.edit_btn.setEnabled(False)
    
    def _approve_entry(self):
        """Approve and save the journal entry."""
        QMessageBox.information(self, "تم", "سيتم حفظ القيد بعد تطبيق ميزة الاعتماد في النسخة الكاملة")
    
    def _retry_analysis(self):
        """Retry analysis."""
        self.text_input.clear()
        self.results_frame.setVisible(False)
        self.text_input.setFocus()
