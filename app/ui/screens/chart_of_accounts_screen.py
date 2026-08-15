"""
Finovate Journal AI - Chart of Accounts Screen
Copyright © 2025 Ahmed Mostafa Ibrahim — All Rights Reserved.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QTreeWidget, QTreeWidgetItem,
    QMessageBox, QGroupBox, QLineEdit, QComboBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from app.database.db_manager import DatabaseManager
from app.utils.logger import get_logger

logger = get_logger(__name__)


class ChartOfAccountsScreen(QWidget):
    """Chart of Accounts management screen"""
    
    def __init__(self):
        super().__init__()
        
        self.db_manager = DatabaseManager()
        
        self.init_ui()
        self.load_accounts()
    
    def init_ui(self):
        """Initialize the user interface"""
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # Title
        title_label = QLabel("📚 دليل الحسابات")
        title_label.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title_label.setStyleSheet("color: #4CAF50;")
        main_layout.addWidget(title_label)
        
        # Description
        desc_label = QLabel("إدارة هيكل الحسابات المحاسبية للشركة")
        desc_label.setFont(QFont("Segoe UI", 11))
        desc_label.setStyleSheet("color: #888;")
        main_layout.addWidget(desc_label)
        
        # Toolbar
        toolbar_layout = QHBoxLayout()
        toolbar_layout.setSpacing(15)
        
        # Search
        search_label = QLabel("🔍 بحث:")
        search_label.setStyleSheet("color: #E0E0E0;")
        toolbar_layout.addWidget(search_label)
        
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("ابحث عن حساب...")
        self.search_edit.setFixedWidth(300)
        self.search_edit.setStyleSheet("""
            QLineEdit {
                background-color: #2D2D2D;
                color: #E0E0E0;
                border: 1px solid #3D3D3D;
                border-radius: 6px;
                padding: 8px;
            }
        """)
        self.search_edit.textChanged.connect(self.filter_accounts)
        toolbar_layout.addWidget(self.search_edit)
        
        toolbar_layout.addStretch()
        
        # Action buttons
        add_btn = QPushButton("+ إضافة حساب")
        add_btn.setFixedHeight(40)
        add_btn.setCursor(Qt.PointingHandCursor)
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 13px;
                font-weight: bold;
                padding: 0 20px;
            }
            QPushButton:hover {
                background-color: #45A049;
            }
        """)
        add_btn.clicked.connect(self.add_account)
        toolbar_layout.addWidget(add_btn)
        
        edit_btn = QPushButton("✏️ تعديل")
        edit_btn.setFixedHeight(40)
        edit_btn.setCursor(Qt.PointingHandCursor)
        edit_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 13px;
                font-weight: bold;
                padding: 0 20px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        edit_btn.clicked.connect(self.edit_account)
        toolbar_layout.addWidget(edit_btn)
        
        delete_btn = QPushButton("🗑️ حذف")
        delete_btn.setFixedHeight(40)
        delete_btn.setCursor(Qt.PointingHandCursor)
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #F44336;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 13px;
                font-weight: bold;
                padding: 0 20px;
            }
            QPushButton:hover {
                background-color: #D32F2F;
            }
        """)
        delete_btn.clicked.connect(self.delete_account)
        toolbar_layout.addWidget(delete_btn)
        
        main_layout.addLayout(toolbar_layout)
        
        # Accounts tree
        accounts_group = QGroupBox("هيكل الحسابات")
        accounts_group.setStyleSheet("""
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
        
        tree_layout = QVBoxLayout()
        
        self.accounts_tree = QTreeWidget()
        self.accounts_tree.setHeaderLabels(["الكود", "اسم الحساب (عربي)", "Account Name (English)", "النوع", "الرصيد الطبيعي"])
        self.accounts_tree.header().setSectionResizeMode(0, QTreeWidget.ResizeToContents)
        self.accounts_tree.header().setSectionResizeMode(1, QTreeWidget.Stretch)
        self.accounts_tree.setAlternatingRowColors(True)
        self.accounts_tree.setStyleSheet("""
            QTreeWidget {
                background-color: #1E1E1E;
                color: #E0E0E0;
                border: 1px solid #3D3D3D;
                border-radius: 8px;
                gridline-color: #3D3D3D;
            }
            QTreeWidget::item {
                padding: 8px;
            }
            QTreeWidget::item:selected {
                background-color: #4CAF50;
            }
            QHeaderView::section {
                background-color: #2D2D2D;
                color: #4CAF50;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """)
        tree_layout.addWidget(self.accounts_tree)
        
        accounts_group.setLayout(tree_layout)
        main_layout.addWidget(accounts_group)
        
        # Info panel
        info_frame = QGroupBox("تفاصيل الحساب المحدد")
        info_frame.setStyleSheet("""
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
        
        info_layout = QVBoxLayout()
        
        self.info_label = QLabel("اختر حسابًا لعرض التفاصيل")
        self.info_label.setFont(QFont("Segoe UI", 11))
        self.info_label.setStyleSheet("color: #888;")
        self.info_label.setWordWrap(True)
        info_layout.addWidget(self.info_label)
        
        info_frame.setLayout(info_layout)
        main_layout.addWidget(info_frame)
        
        main_layout.addStretch()
        self.setLayout(main_layout)
    
    def load_accounts(self):
        """Load chart of accounts from database"""
        self.accounts_tree.clear()
        
        # Sample data - will be replaced with database query
        sample_accounts = [
            {
                'code': '1',
                'name_ar': 'الأصول',
                'name_en': 'Assets',
                'type': 'Asset',
                'balance': 'Debit',
                'children': [
                    {
                        'code': '11',
                        'name_ar': 'الأصول المتداولة',
                        'name_en': 'Current Assets',
                        'type': 'Asset',
                        'balance': 'Debit',
                        'children': [
                            {'code': '1101', 'name_ar': 'الصندوق', 'name_en': 'Cash', 'type': 'Asset', 'balance': 'Debit'},
                            {'code': '1102', 'name_ar': 'البنك', 'name_en': 'Bank', 'type': 'Asset', 'balance': 'Debit'},
                            {'code': '1103', 'name_ar': 'العملاء', 'name_en': 'Customers', 'type': 'Asset', 'balance': 'Debit'},
                            {'code': '1104', 'name_ar': 'المخزون', 'name_en': 'Inventory', 'type': 'Asset', 'balance': 'Debit'},
                        ]
                    },
                    {
                        'code': '12',
                        'name_ar': 'الأصول غير المتداولة',
                        'name_en': 'Non-Current Assets',
                        'type': 'Asset',
                        'balance': 'Debit',
                        'children': [
                            {'code': '1201', 'name_ar': 'الأصول الثابتة', 'name_en': 'Fixed Assets', 'type': 'Asset', 'balance': 'Debit'},
                            {'code': '1202', 'name_ar': 'الإهلاك المتراكم', 'name_en': 'Accumulated Depreciation', 'type': 'Asset', 'balance': 'Credit'},
                        ]
                    }
                ]
            },
            {
                'code': '2',
                'name_ar': 'الالتزامات',
                'name_en': 'Liabilities',
                'type': 'Liability',
                'balance': 'Credit',
                'children': [
                    {
                        'code': '21',
                        'name_ar': 'الالتزامات المتداولة',
                        'name_en': 'Current Liabilities',
                        'type': 'Liability',
                        'balance': 'Credit',
                        'children': [
                            {'code': '2101', 'name_ar': 'الموردون', 'name_en': 'Suppliers', 'type': 'Liability', 'balance': 'Credit'},
                            {'code': '2102', 'name_ar': 'ضريبة القيمة المضافة', 'name_en': 'VAT Payable', 'type': 'Liability', 'balance': 'Credit'},
                        ]
                    }
                ]
            },
            {
                'code': '3',
                'name_ar': 'حقوق الملكية',
                'name_en': 'Equity',
                'type': 'Equity',
                'balance': 'Credit',
                'children': [
                    {'code': '3101', 'name_ar': 'رأس المال', 'name_en': 'Capital', 'type': 'Equity', 'balance': 'Credit'},
                    {'code': '3102', 'name_ar': 'الأرباح المحتجزة', 'name_en': 'Retained Earnings', 'type': 'Equity', 'balance': 'Credit'},
                ]
            },
            {
                'code': '4',
                'name_ar': 'الإيرادات',
                'name_en': 'Revenue',
                'type': 'Revenue',
                'balance': 'Credit',
                'children': [
                    {'code': '4101', 'name_ar': 'المبيعات', 'name_en': 'Sales', 'type': 'Revenue', 'balance': 'Credit'},
                    {'code': '4102', 'name_ar': 'إيرادات أخرى', 'name_en': 'Other Income', 'type': 'Revenue', 'balance': 'Credit'},
                ]
            },
            {
                'code': '5',
                'name_ar': 'المصروفات',
                'name_en': 'Expenses',
                'type': 'Expense',
                'balance': 'Debit',
                'children': [
                    {'code': '5101', 'name_ar': 'المشتريات', 'name_en': 'Purchases', 'type': 'Expense', 'balance': 'Debit'},
                    {'code': '5201', 'name_ar': 'إيجار', 'name_en': 'Rent Expense', 'type': 'Expense', 'balance': 'Debit'},
                    {'code': '5301', 'name_ar': 'رواتب', 'name_en': 'Salaries Expense', 'type': 'Expense', 'balance': 'Debit'},
                    {'code': '5401', 'name_ar': 'كهرباء ومياه', 'name_en': 'Utilities', 'type': 'Expense', 'balance': 'Debit'},
                ]
            },
        ]
        
        def add_items(parent, items):
            for item_data in items:
                item = QTreeWidgetItem([
                    item_data['code'],
                    item_data['name_ar'],
                    item_data['name_en'],
                    item_data['type'],
                    item_data['balance']
                ])
                
                if parent is None:
                    self.accounts_tree.addTopLevelItem(item)
                else:
                    parent.addChild(item)
                
                if 'children' in item_data:
                    add_items(item, item_data['children'])
        
        add_items(None, sample_accounts)
        
        logger.info("Chart of accounts loaded")
    
    def filter_accounts(self, text: str):
        """Filter accounts based on search text"""
        # TODO: Implement filtering
        logger.info(f"Filtering accounts: {text}")
    
    def add_account(self):
        """Add new account"""
        QMessageBox.information(
            self, "إضافة حساب",
            "ستكون ميزة إضافة حساب متاحة قريبًا"
        )
        logger.info("Add account clicked")
    
    def edit_account(self):
        """Edit selected account"""
        selected = self.accounts_tree.selectedItems()
        if not selected:
            QMessageBox.warning(self, "تحذير", "الرجاء اختيار حساب أولاً")
            return
        
        QMessageBox.information(
            self, "تعديل حساب",
            "ستكون ميزة تعديل حساب متاحة قريبًا"
        )
        logger.info("Edit account clicked")
    
    def delete_account(self):
        """Delete selected account"""
        selected = self.accounts_tree.selectedItems()
        if not selected:
            QMessageBox.warning(self, "تحذير", "الرجاء اختيار حساب أولاً")
            return
        
        QMessageBox.warning(
            self, "تحذير",
            "لا يمكن حذف حساب له حركات أو حسابات فرعية.\n\nستكون ميزة الحذف متاحة قريبًا"
        )
        logger.info("Delete account clicked")
