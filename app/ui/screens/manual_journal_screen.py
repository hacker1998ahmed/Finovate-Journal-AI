"""
Finovate Journal AI - Manual Journal Screen
Copyright © 2025 Ahmed Mostafa Ibrahim — All Rights Reserved.
"""

from decimal import Decimal
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFrame, QTableWidget,
    QHeaderView, QDateEdit, QLineEdit, QComboBox,
    QMessageBox, QGroupBox, QGridLayout, QSpinBox
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont

from app.database.db_manager import DatabaseManager
from app.utils.logger import get_logger

logger = get_logger(__name__)


class ManualJournalScreen(QWidget):
    """Manual journal entry screen"""
    
    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager()
        self.init_ui()
    
    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        title_label = QLabel("📝 قيد يدوي")
        title_label.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title_label.setStyleSheet("color: #4CAF50;")
        main_layout.addWidget(title_label)
        
        desc_label = QLabel("إدخال القيد المحاسبي يدويًا مع التحقق من التوازن")
        desc_label.setFont(QFont("Segoe UI", 11))
        desc_label.setStyleSheet("color: #888;")
        main_layout.addWidget(desc_label)
        
        details_group = QGroupBox("بيانات القيد")
        details_group.setStyleSheet("""
            QGroupBox { font-weight: bold; color: #E0E0E0; border: 1px solid #3D3D3D; border-radius: 8px; margin-top: 10px; padding-top: 10px; }
            QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px; }
        """)
        details_layout = QGridLayout()
        details_layout.setSpacing(15)
        
        details_layout.addWidget(QLabel("التاريخ:"), 0, 0)
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setStyleSheet("QDateEdit { background-color: #2D2D2D; color: #E0E0E0; border: 1px solid #3D3D3D; border-radius: 6px; padding: 8px; }")
        details_layout.addWidget(self.date_edit, 0, 1)
        
        details_layout.addWidget(QLabel("المرجع:"), 0, 2)
        self.ref_edit = QLineEdit()
        self.ref_edit.setPlaceholderText("رقم المرجع")
        self.ref_edit.setStyleSheet("QLineEdit { background-color: #2D2D2D; color: #E0E0E0; border: 1px solid #3D3D3D; border-radius: 6px; padding: 8px; }")
        details_layout.addWidget(self.ref_edit, 0, 3)
        
        details_layout.addWidget(QLabel("البيان:"), 1, 0)
        self.desc_edit = QLineEdit()
        self.desc_edit.setPlaceholderText("وصف العملية")
        self.desc_edit.setStyleSheet("QLineEdit { background-color: #2D2D2D; color: #E0E0E0; border: 1px solid #3D3D3D; border-radius: 6px; padding: 8px; }")
        details_layout.addWidget(self.desc_edit, 1, 1, 1, 3)
        
        details_group.setLayout(details_layout)
        main_layout.addWidget(details_group)
        
        lines_group = QGroupBox("سطور القيد")
        lines_group.setStyleSheet("""
            QGroupBox { font-weight: bold; color: #E0E0E0; border: 1px solid #3D3D3D; border-radius: 8px; margin-top: 10px; padding-top: 10px; }
            QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px; }
        """)
        lines_layout = QVBoxLayout()
        
        self.lines_table = QTableWidget()
        self.lines_table.setColumnCount(5)
        self.lines_table.setHorizontalHeaderLabels(["الحساب", "البيان", "مدين", "دائن", "حذف"])
        self.lines_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.lines_table.setAlternatingRowColors(True)
        self.lines_table.setStyleSheet("""
            QTableWidget { background-color: #1E1E1E; color: #E0E0E0; border: 1px solid #3D3D3D; border-radius: 8px; gridline-color: #3D3D3D; }
            QTableWidget::item { padding: 8px; }
            QHeaderView::section { background-color: #2D2D2D; color: #4CAF50; padding: 8px; border: none; font-weight: bold; }
        """)
        self.lines_table.setFixedHeight(300)
        lines_layout.addWidget(self.lines_table)
        
        add_btn = QPushButton("+ إضافة سطر")
        add_btn.setFixedHeight(40)
        add_btn.setCursor(Qt.PointingHandCursor)
        add_btn.setStyleSheet("QPushButton { background-color: #2196F3; color: white; border: none; border-radius: 6px; font-size: 13px; font-weight: bold; } QPushButton:hover { background-color: #1976D2; }")
        add_btn.clicked.connect(self.add_line)
        lines_layout.addWidget(add_btn)
        
        lines_group.setLayout(lines_layout)
        main_layout.addWidget(lines_group)
        
        balance_frame = QFrame()
        balance_frame.setStyleSheet("background-color: #2D2D2D; border-radius: 8px;")
        balance_layout = QHBoxLayout()
        balance_layout.setContentsMargins(20, 15, 20, 15)
        
        self.balance_label = QLabel("إجمالي المدين: 0.00 | إجمالي الدائن: 0.00")
        self.balance_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.balance_label.setStyleSheet("color: #E0E0E0;")
        balance_layout.addWidget(self.balance_label)
        balance_layout.addStretch()
        
        self.status_label = QLabel("● متوازن")
        self.status_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.status_label.setStyleSheet("color: #4CAF50;")
        balance_layout.addWidget(self.status_label)
        
        balance_frame.setLayout(balance_layout)
        main_layout.addWidget(balance_frame)
        
        action_layout = QHBoxLayout()
        action_layout.setSpacing(15)
        
        save_btn = QPushButton("💾 حفظ القيد")
        save_btn.setFixedHeight(50)
        save_btn.setCursor(Qt.PointingHandCursor)
        save_btn.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; border: none; border-radius: 8px; font-size: 14px; font-weight: bold; padding: 10px 30px; } QPushButton:hover { background-color: #45A049; } QPushButton:disabled { background-color: #555; }")
        save_btn.clicked.connect(self.save_entry)
        action_layout.addWidget(save_btn)
        
        clear_btn = QPushButton("🗑️ مسح")
        clear_btn.setFixedHeight(50)
        clear_btn.setCursor(Qt.PointingHandCursor)
        clear_btn.setStyleSheet("QPushButton { background-color: #F44336; color: white; border: none; border-radius: 8px; font-size: 14px; font-weight: bold; padding: 10px 30px; } QPushButton:hover { background-color: #D32F2F; }")
        clear_btn.clicked.connect(self.clear_form)
        action_layout.addWidget(clear_btn)
        
        action_layout.addStretch()
        main_layout.addLayout(action_layout)
        main_layout.addStretch()
        self.setLayout(main_layout)
        self.add_line()
        self.add_line()
    
    def add_line(self):
        row_position = self.lines_table.rowCount()
        self.lines_table.insertRow(row_position)
        
        account_combo = QComboBox()
        account_combo.addItem("اختر حساب...")
        account_combo.addItems(["1101 - الصندوق", "1102 - البنك", "1103 - العملاء", "5101 - المشتريات", "4101 - المبيعات", "5201 - إيجار", "5301 - رواتب"])
        account_combo.setStyleSheet("QComboBox { background-color: #2D2D2D; color: #E0E0E0; border: 1px solid #3D3D3D; border-radius: 4px; padding: 5px; }")
        self.lines_table.setCellWidget(row_position, 0, account_combo)
        
        desc_edit = QLineEdit()
        desc_edit.setPlaceholderText("البيان")
        desc_edit.setStyleSheet("QLineEdit { background-color: #2D2D2D; color: #E0E0E0; border: 1px solid #3D3D3D; border-radius: 4px; padding: 5px; }")
        self.lines_table.setCellWidget(row_position, 1, desc_edit)
        
        debit_spin = QSpinBox()
        debit_spin.setRange(0, 999999999)
        debit_spin.setValue(0)
        debit_spin.setStyleSheet("QSpinBox { background-color: #2D2D2D; color: #E0E0E0; border: 1px solid #3D3D3D; border-radius: 4px; padding: 5px; }")
        debit_spin.valueChanged.connect(self.update_balance)
        self.lines_table.setCellWidget(row_position, 2, debit_spin)
        
        credit_spin = QSpinBox()
        credit_spin.setRange(0, 999999999)
        credit_spin.setValue(0)
        credit_spin.setStyleSheet("QSpinBox { background-color: #2D2D2D; color: #E0E0E0; border: 1px solid #3D3D3D; border-radius: 4px; padding: 5px; }")
        credit_spin.valueChanged.connect(self.update_balance)
        self.lines_table.setCellWidget(row_position, 3, credit_spin)
        
        delete_btn = QPushButton("🗑️")
        delete_btn.setFixedWidth(50)
        delete_btn.setCursor(Qt.PointingHandCursor)
        delete_btn.setStyleSheet("QPushButton { background-color: #F44336; color: white; border: none; border-radius: 4px; font-weight: bold; } QPushButton:hover { background-color: #D32F2F; }")
        delete_btn.clicked.connect(lambda: self.remove_line(row_position))
        self.lines_table.setCellWidget(row_position, 4, delete_btn)
        
        self.update_balance()
    
    def remove_line(self, row: int):
        if self.lines_table.rowCount() > 2:
            self.lines_table.removeRow(row)
            self.update_balance()
        else:
            QMessageBox.warning(self, "تحذير", "يجب أن يحتوي القيد على سطرين على الأقل")
    
    def update_balance(self):
        total_debit = Decimal('0')
        total_credit = Decimal('0')
        
        for row in range(self.lines_table.rowCount()):
            debit_widget = self.lines_table.cellWidget(row, 2)
            credit_widget = self.lines_table.cellWidget(row, 3)
            if debit_widget and isinstance(debit_widget, QSpinBox):
                total_debit += Decimal(str(debit_widget.value()))
            if credit_widget and isinstance(credit_widget, QSpinBox):
                total_credit += Decimal(str(credit_widget.value()))
        
        self.balance_label.setText(f"إجمالي المدين: {total_debit:,.2f} | إجمالي الدائن: {total_credit:,.2f}")
        
        if total_debit == total_credit and total_debit > 0:
            self.status_label.setText("✓ متوازن")
            self.status_label.setStyleSheet("color: #4CAF50;")
        elif total_debit == total_credit:
            self.status_label.setText("○ متوازن (بدون مبالغ)")
            self.status_label.setStyleSheet("color: #FF9800;")
        else:
            self.status_label.setText("✗ غير متوازن")
            self.status_label.setStyleSheet("color: #F44336;")
    
    def save_entry(self):
        total_debit = Decimal('0')
        total_credit = Decimal('0')
        
        for row in range(self.lines_table.rowCount()):
            debit_widget = self.lines_table.cellWidget(row, 2)
            credit_widget = self.lines_table.cellWidget(row, 3)
            if debit_widget and isinstance(debit_widget, QSpinBox):
                total_debit += Decimal(str(debit_widget.value()))
            if credit_widget and isinstance(credit_widget, QSpinBox):
                total_credit += Decimal(str(credit_widget.value()))
        
        if total_debit != total_credit:
            QMessageBox.warning(self, "تحذير", "القيد غير متوازن! يجب أن يتساوى المدين والدائن.")
            return
        if total_debit == 0:
            QMessageBox.warning(self, "تحذير", "لا يمكن حفظ قيد بدون مبالغ.")
            return
        
        QMessageBox.information(self, "نجاح", "تم حفظ القيد بنجاح (سيتم التطبيق الكامل قريبًا)")
        logger.info("Manual journal entry saved")
    
    def clear_form(self):
        self.desc_edit.clear()
        self.ref_edit.clear()
        while self.lines_table.rowCount() > 2:
            self.lines_table.removeRow(0)
        for row in range(self.lines_table.rowCount()):
            account_combo = self.lines_table.cellWidget(row, 0)
            if account_combo: account_combo.setCurrentIndex(0)
            desc_edit = self.lines_table.cellWidget(row, 1)
            if desc_edit: desc_edit.clear()
            debit_spin = self.lines_table.cellWidget(row, 2)
            if debit_spin: debit_spin.setValue(0)
            credit_spin = self.lines_table.cellWidget(row, 3)
            if credit_spin: credit_spin.setValue(0)
        self.update_balance()
        logger.info("Manual journal form cleared")
