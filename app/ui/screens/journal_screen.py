"""
Finovate Journal AI - Journal Screen
Copyright © 2025 Ahmed Mostafa Ibrahim — All Rights Reserved.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QGroupBox, QLineEdit, QDateEdit,
    QComboBox, QMessageBox
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont

from app.database.db_manager import DatabaseManager
from app.utils.logger import get_logger

logger = get_logger(__name__)


class JournalScreen(QWidget):
    """Journal entries view screen"""
    
    def __init__(self):
        super().__init__()
        
        self.db_manager = DatabaseManager()
        
        self.init_ui()
        self.load_entries()
    
    def init_ui(self):
        """Initialize the user interface"""
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # Title
        title_label = QLabel("📖 دفتر اليومية")
        title_label.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title_label.setStyleSheet("color: #4CAF50;")
        main_layout.addWidget(title_label)
        
        # Description
        desc_label = QLabel("عرض جميع القيود المحاسبية المسجلة")
        desc_label.setFont(QFont("Segoe UI", 11))
        desc_label.setStyleSheet("color: #888;")
        main_layout.addWidget(desc_label)
        
        # Filters
        filters_group = QGroupBox("تصفية البيانات")
        filters_group.setStyleSheet("""
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
        
        filters_layout = QHBoxLayout()
        filters_layout.setSpacing(15)
        
        # Date from
        filters_layout.addWidget(QLabel("من:"))
        self.date_from = QDateEdit()
        self.date_from.setDate(QDate.currentDate().addMonths(-1))
        self.date_from.setCalendarPopup(True)
        self.date_from.setStyleSheet("""
            QDateEdit {
                background-color: #2D2D2D;
                color: #E0E0E0;
                border: 1px solid #3D3D3D;
                border-radius: 6px;
                padding: 8px;
            }
        """)
        filters_layout.addWidget(self.date_from)
        
        # Date to
        filters_layout.addWidget(QLabel("إلى:"))
        self.date_to = QDateEdit()
        self.date_to.setDate(QDate.currentDate())
        self.date_to.setCalendarPopup(True)
        self.date_to.setStyleSheet("""
            QDateEdit {
                background-color: #2D2D2D;
                color: #E0E0E0;
                border: 1px solid #3D3D3D;
                border-radius: 6px;
                padding: 8px;
            }
        """)
        filters_layout.addWidget(self.date_to)
        
        # Status filter
        filters_layout.addWidget(QLabel("الحالة:"))
        self.status_filter = QComboBox()
        self.status_filter.addItems(["الكل", "مسودة", "مراجع", "معتمد", "ملغى"])
        self.status_filter.setStyleSheet("""
            QComboBox {
                background-color: #2D2D2D;
                color: #E0E0E0;
                border: 1px solid #3D3D3D;
                border-radius: 6px;
                padding: 8px;
            }
        """)
        filters_layout.addWidget(self.status_filter)
        
        filters_layout.addStretch()
        
        # Search
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("🔍 بحث...")
        self.search_edit.setFixedWidth(250)
        self.search_edit.setStyleSheet("""
            QLineEdit {
                background-color: #2D2D2D;
                color: #E0E0E0;
                border: 1px solid #3D3D3D;
                border-radius: 6px;
                padding: 8px;
            }
        """)
        filters_layout.addWidget(self.search_edit)
        
        filters_group.setLayout(filters_layout)
        main_layout.addWidget(filters_group)
        
        # Entries table
        entries_group = QGroupBox("القيود المسجلة")
        entries_group.setStyleSheet("""
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
        
        table_layout = QVBoxLayout()
        
        self.entries_table = QTableWidget()
        self.entries_table.setColumnCount(8)
        self.entries_table.setHorizontalHeaderLabels([
            "رقم القيد", "التاريخ", "البيان", "الحساب", "مدين", "دائن", "المستخدم", "الحالة"
        ])
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
        self.entries_table.setFixedHeight(400)
        table_layout.addWidget(self.entries_table)
        
        entries_group.setLayout(table_layout)
        main_layout.addWidget(entries_group)
        
        # Action buttons
        action_layout = QHBoxLayout()
        action_layout.setSpacing(15)
        
        refresh_btn = QPushButton("🔄 تحديث")
        refresh_btn.setFixedHeight(45)
        refresh_btn.setCursor(Qt.PointingHandCursor)
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 13px;
                font-weight: bold;
                padding: 0 25px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        refresh_btn.clicked.connect(self.load_entries)
        action_layout.addWidget(refresh_btn)
        
        export_btn = QPushButton("📤 تصدير Excel")
        export_btn.setFixedHeight(45)
        export_btn.setCursor(Qt.PointingHandCursor)
        export_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 13px;
                font-weight: bold;
                padding: 0 25px;
            }
            QPushButton:hover {
                background-color: #45A049;
            }
        """)
        export_btn.clicked.connect(self.export_excel)
        action_layout.addWidget(export_btn)
        
        pdf_btn = QPushButton("📄 تصدير PDF")
        pdf_btn.setFixedHeight(45)
        pdf_btn.setCursor(Qt.PointingHandCursor)
        pdf_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 13px;
                font-weight: bold;
                padding: 0 25px;
            }
            QPushButton:hover {
                background-color: #F57C00;
            }
        """)
        pdf_btn.clicked.connect(self.export_pdf)
        action_layout.addWidget(pdf_btn)
        
        action_layout.addStretch()
        main_layout.addLayout(action_layout)
        
        main_layout.addStretch()
        self.setLayout(main_layout)
    
    def load_entries(self):
        """Load journal entries from database"""
        self.entries_table.setRowCount(0)
        
        # Sample data - will be replaced with database query
        sample_entries = [
            ("JE-2025-000001", "2025-01-15", "شراء بضاعة نقدًا", "المشتريات", "10,000.00", "0.00", "Admin", "معتمد"),
            ("JE-2025-000001", "2025-01-15", "شراء بضاعة نقدًا", "الصندوق", "0.00", "10,000.00", "Admin", "معتمد"),
            ("JE-2025-000002", "2025-01-16", "دفع إيجار المكتب", "إيجار", "5,000.00", "0.00", "Admin", "معتمد"),
            ("JE-2025-000002", "2025-01-16", "دفع إيجار المكتب", "البنك", "0.00", "5,000.00", "Admin", "معتمد"),
            ("JE-2025-000003", "2025-01-17", "بيع بضاعة للعميل أحمد", "العملاء", "30,000.00", "0.00", "Admin", "مراجع"),
            ("JE-2025-000003", "2025-01-17", "بيع بضاعة للعميل أحمد", "المبيعات", "0.00", "30,000.00", "Admin", "مراجع"),
        ]
        
        for entry in sample_entries:
            row_position = self.entries_table.rowCount()
            self.entries_table.insertRow(row_position)
            
            for col, value in enumerate(entry):
                item = QTableWidgetItem(value)
                item.setTextAlignment(Qt.AlignCenter if col >= 4 else Qt.AlignLeft | Qt.AlignVCenter)
                self.entries_table.setItem(row_position, col, item)
                
                # Color code status
                if col == 7:
                    if value == "معتمد":
                        item.setBackground(Qt.darkGreen)
                        item.setForeground(Qt.white)
                    elif value == "مراجع":
                        item.setBackground(Qt.darkBlue)
                        item.setForeground(Qt.white)
                    elif value == "مسودة":
                        item.setBackground(Qt.darkGray)
                        item.setForeground(Qt.white)
                    elif value == "ملغى":
                        item.setBackground(Qt.darkRed)
                        item.setForeground(Qt.white)
        
        logger.info(f"Loaded {len(sample_entries)} journal entry lines")
    
    def export_excel(self):
        """Export journal to Excel"""
        QMessageBox.information(
            self, "تصدير Excel",
            "ستكون ميزة تصدير Excel متاحة قريبًا"
        )
        logger.info("Export to Excel clicked")
    
    def export_pdf(self):
        """Export journal to PDF"""
        QMessageBox.information(
            self, "تصدير PDF",
            "ستكون ميزة تصدير PDF متاحة قريبًا"
        )
        logger.info("Export to PDF clicked")
