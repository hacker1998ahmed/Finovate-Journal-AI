"""
Finovate Journal AI - Smart Journal Widget
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton,
    QLabel, QFrame, QTableWidget, QTableWidgetItem, QHeaderView,
    QMessageBox, QProgressBar, QGroupBox, QGridLayout, QApplication
)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont

from decimal import Decimal
from app.nlp.parser import get_parser, ParsedTransaction
from app.accounting.rules import get_rule_engine


class SmartJournalWidget(QWidget):
    """Smart Journal widget for natural language transaction entry"""
    
    def __init__(self):
        super().__init__()
        
        self.parser = get_parser()
        self.rule_engine = get_rule_engine()
        self.current_analysis = None
        
        self._setup_ui()
        self._connect_signals()
        
    def _setup_ui(self):
        """Setup Smart Journal UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("🧠 القيد الذكي / Smart Journal")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setStyleSheet("color: #2c3e50; padding: 10px;")
        layout.addWidget(title)
        
        # Input section
        input_group = QGroupBox("أدخل العملية المحاسبية / Enter Transaction")
        input_group.setFont(QFont("Arial", 12, QFont.Bold))
        input_layout = QVBoxLayout(input_group)
        
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText(
            "اكتب العملية المحاسبية هنا...\n"
            "مثال: شراء بضاعة نقدًا بمبلغ 10000 جنيه\n"
            "Example: Purchased goods for cash 10000 EGP"
        )
        self.input_text.setMinimumHeight(100)
        self.input_text.setFont(QFont("Arial", 12))
        input_layout.addWidget(self.input_text)
        
        # Action buttons
        btn_layout = QHBoxLayout()
        
        self.analyze_btn = QPushButton("🔍 تحليل العملية / Analyze Transaction")
        self.analyze_btn.setMinimumHeight(40)
        self.analyze_btn.setFont(QFont("Arial", 11, QFont.Bold))
        self.analyze_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        btn_layout.addWidget(self.analyze_btn)
        
        self.clear_btn = QPushButton("🗑️ مسح / Clear")
        self.clear_btn.setMinimumHeight(40)
        self.clear_btn.setFont(QFont("Arial", 11))
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        btn_layout.addWidget(self.clear_btn)
        
        input_layout.addLayout(btn_layout)
        layout.addWidget(input_group)
        
        # Analysis results section
        self.results_group = QGroupBox("نتائج التحليل / Analysis Results")
        self.results_group.setFont(QFont("Arial", 12, QFont.Bold))
        self.results_group.setVisible(False)
        
        results_layout = QVBoxLayout(self.results_group)
        
        # Confidence score
        confidence_layout = QHBoxLayout()
        confidence_layout.addWidget(QLabel("درجة الثقة / Confidence:"))
        
        self.confidence_progress = QProgressBar()
        self.confidence_progress.setMaximumHeight(25)
        self.confidence_progress.setStyleSheet("""
            QProgressBar {
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #2ecc71;
            }
        """)
        confidence_layout.addWidget(self.confidence_progress)
        
        self.confidence_label = QLabel("0%")
        self.confidence_label.setFont(QFont("Arial", 11, QFont.Bold))
        self.confidence_label.setMinimumWidth(60)
        confidence_layout.addWidget(self.confidence_label)
        
        results_layout.addLayout(confidence_layout)
        
        # Transaction details
        details_grid = QGridLayout()
        
        self.detail_labels = {}
        details = [
            ("نوع العملية / Type:", "type"),
            ("المبلغ / Amount:", "amount"),
            ("طريقة الدفع / Payment:", "payment"),
            ("الطرف / Party:", "party"),
            ("الضريبة / Tax:", "tax"),
        ]
        
        for i, (label_text, key) in enumerate(details):
            label = QLabel(label_text)
            label.setFont(QFont("Arial", 10, QFont.Bold))
            value = QLabel("-")
            value.setObjectName(f"value_{key}")
            self.detail_labels[key] = value
            
            details_grid.addWidget(label, i, 0)
            details_grid.addWidget(value, i, 1)
        
        results_layout.addLayout(details_grid)
        
        # Journal entries table
        entries_label = QLabel("القيود المقترحة / Suggested Entries:")
        entries_label.setFont(QFont("Arial", 11, QFont.Bold))
        results_layout.addWidget(entries_label)
        
        self.entries_table = QTableWidget()
        self.entries_table.setColumnCount(4)
        self.entries_table.setHorizontalHeaderLabels([
            "الحساب / Account",
            "البيان / Description",
            "مدين / Debit",
            "دائن / Credit"
        ])
        self.entries_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.entries_table.setMinimumHeight(150)
        results_layout.addWidget(self.entries_table)
        
        # Ambiguities warning
        self.ambiguities_label = QLabel()
        self.ambiguities_label.setWordWrap(True)
        self.ambiguities_label.setStyleSheet("""
            QLabel {
                background-color: #f39c1220;
                border-left: 4px solid #f39c12;
                padding: 10px;
                border-radius: 5px;
            }
        """)
        self.ambiguities_label.setVisible(False)
        results_layout.addWidget(self.ambiguities_label)
        
        # Action buttons for entries
        action_layout = QHBoxLayout()
        
        self.approve_btn = QPushButton("✓ اعتماد القيد / Approve Entry")
        self.approve_btn.setMinimumHeight(40)
        self.approve_btn.setFont(QFont("Arial", 11, QFont.Bold))
        self.approve_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        action_layout.addWidget(self.approve_btn)
        
        self.edit_btn = QPushButton("✏️ تعديل / Edit")
        self.edit_btn.setMinimumHeight(40)
        self.edit_btn.setFont(QFont("Arial", 11))
        edit_btn_style = """
            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 5px;
                padding: 10px;
            }
        """
        self.edit_btn.setStyleSheet(edit_btn_style)
        action_layout.addWidget(self.edit_btn)
        
        self.reanalyze_btn = QPushButton("🔄 إعادة التحليل / Re-analyze")
        self.reanalyze_btn.setMinimumHeight(40)
        self.reanalyze_btn.setStyleSheet(edit_btn_style)
        action_layout.addWidget(self.reanalyze_btn)
        
        results_layout.addLayout(action_layout)
        layout.addWidget(self.results_group)
        
        # Example transactions
        examples_group = QGroupBox("أمثلة / Examples")
        examples_layout = QVBoxLayout(examples_group)
        
        examples = [
            "شراء بضاعة نقدًا بمبلغ 10000 جنيه",
            "دفع إيجار المكتب 5000 من البنك",
            "استلمت من العميل أحمد 15000 جنيه نقدًا",
            "بيع بضاعة للعميل محمد آجلًا بمبلغ 8000 جنيه",
            "سداد مورد لشركة النور 12000 من البنك",
        ]
        
        for example in examples:
            btn = QPushButton(f"➤ {example}")
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    text-align: left;
                    padding: 8px;
                    background-color: transparent;
                    border: 1px solid #ecf0f1;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #ecf0f1;
                }
            """)
            btn.clicked.connect(lambda checked, ex=example: self._load_example(ex))
            examples_layout.addWidget(btn)
        
        layout.addWidget(examples_group)
        
        layout.addStretch()
        
    def _connect_signals(self):
        """Connect signals"""
        self.analyze_btn.clicked.connect(self._analyze_transaction)
        self.clear_btn.clicked.connect(self._clear_all)
        self.reanalyze_btn.clicked.connect(self._analyze_transaction)
        self.approve_btn.clicked.connect(self._approve_entry)
        self.edit_btn.clicked.connect(self._edit_entry)
        
    def _load_example(self, example: str):
        """Load example into input"""
        self.input_text.setText(example)
        
    def _analyze_transaction(self):
        """Analyze the transaction text"""
        text = self.input_text.toPlainText().strip()
        
        if not text:
            QMessageBox.warning(self, "تحذير", "الرجاء إدخال نص العملية المحاسبية")
            return
        
        # Parse with NLP
        parsed = self.parser.parse(text)
        
        # Match with rules
        rule, lines = self.rule_engine.suggest_accounts(text, parsed.amount or Decimal("0"))
        
        self.current_analysis = {
            'parsed': parsed,
            'rule': rule,
            'lines': lines
        }
        
        # Display results
        self._display_results(parsed, lines)
        
    def _display_results(self, parsed: ParsedTransaction, lines):
        """Display analysis results"""
        self.results_group.setVisible(True)
        
        # Update confidence
        confidence = int(parsed.confidence)
        self.confidence_progress.setValue(confidence)
        self.confidence_label.setText(f"{confidence}%")
        
        # Color code confidence
        if confidence >= 90:
            color = "#2ecc71"  # Green
        elif confidence >= 75:
            color = "#f39c12"  # Orange
        else:
            color = "#e74c3c"  # Red
        
        self.confidence_progress.setStyleSheet(f"""
            QProgressBar {{
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                text-align: center;
            }}
            QProgressBar::chunk {{
                background-color: {color};
            }}
        """)
        
        # Update details
        self.detail_labels['type'].setText(parsed.transaction_type or "-")
        self.detail_labels['amount'].setText(f"{parsed.amount:.2f} {parsed.currency}" if parsed.amount else "-")
        payment_text = {'cash': 'نقدي', 'bank': 'بنكي', 'credit': 'آجل'}.get(parsed.payment_method, parsed.payment_method)
        self.detail_labels['payment'].setText(payment_text)
        self.detail_labels['party'].setText(parsed.party or "-")
        tax_text = f"نعم ({parsed.tax_amount})" if parsed.tax_detected else "لا"
        self.detail_labels['tax'].setText(tax_text)
        
        # Update entries table
        self.entries_table.setRowCount(len(lines))
        for i, line in enumerate(lines):
            self.entries_table.setItem(i, 0, QTableWidgetItem(line.account_name))
            self.entries_table.setItem(i, 1, QTableWidgetItem(line.description))
            self.entries_table.setItem(i, 2, QTableWidgetItem(str(line.debit)))
            self.entries_table.setItem(i, 3, QTableWidgetItem(str(line.credit)))
        
        # Show ambiguities
        if parsed.ambiguities:
            self.ambiguities_label.setText("⚠️ " + "\n".join(parsed.ambiguities))
            self.ambiguities_label.setVisible(True)
        else:
            self.ambiguities_label.setVisible(False)
        
    def _clear_all(self):
        """Clear all fields"""
        self.input_text.clear()
        self.results_group.setVisible(False)
        self.current_analysis = None
        self.entries_table.setRowCount(0)
        
    def _approve_entry(self):
        """Approve and save the journal entry"""
        if not self.current_analysis:
            return
        
        # TODO: Implement saving to database
        QMessageBox.information(self, "تم", "سيتم حفظ القيد قريباً (قيد التطوير)")
        
    def _edit_entry(self):
        """Edit the journal entry manually"""
        # TODO: Open manual journal with pre-filled data
        QMessageBox.information(self, "قيد التطوير", "سيتم فتح شاشة التعديل قريباً")
