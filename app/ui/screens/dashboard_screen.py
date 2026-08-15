"""
Finovate Journal AI - Dashboard Screen
Copyright © 2025 Ahmed Mostafa Ibrahim — All Rights Reserved.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
    QLabel, QFrame, QScrollArea, QPushButton
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from app.database.db_manager import DatabaseManager
from app.utils.logger import get_logger

logger = get_logger(__name__)


class DashboardCard(QFrame):
    """Dashboard statistics card"""
    
    def __init__(self, title: str, value: str, icon: str = "📊", color: str = "#4CAF50"):
        super().__init__()
        self.setFixedHeight(120)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: #2D2D2D;
                border-radius: 12px;
                border: 1px solid #3D3D3D;
            }}
            QFrame:hover {{
                border: 1px solid {color};
            }}
        """)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(20, 15, 20, 15)
        
        # Icon
        icon_label = QLabel(icon)
        icon_label.setFont(QFont("Segoe UI Emoji", 32))
        icon_label.setFixedWidth(60)
        icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon_label)
        
        # Content
        content_layout = QVBoxLayout()
        content_layout.setSpacing(5)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 11))
        title_label.setStyleSheet("color: #888;")
        content_layout.addWidget(title_label)
        
        value_label = QLabel(value)
        value_label.setFont(QFont("Segoe UI", 20, QFont.Bold))
        value_label.setStyleSheet(f"color: {color};")
        content_layout.addWidget(value_label)
        
        content_layout.addStretch()
        layout.addLayout(content_layout, 1)
        
        self.setLayout(layout)


class DashboardScreen(QWidget):
    """Dashboard screen with statistics and quick actions"""
    
    def __init__(self):
        super().__init__()
        
        self.db_manager = DatabaseManager()
        
        self.init_ui()
        self.load_data()
    
    def init_ui(self):
        """Initialize the user interface"""
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # Welcome section
        welcome_frame = QFrame()
        welcome_frame.setStyleSheet("background-color: #2D2D2D; border-radius: 12px;")
        welcome_layout = QVBoxLayout()
        welcome_layout.setContentsMargins(30, 20, 30, 20)
        
        welcome_title = QLabel("مرحبًا بك في Finovate Journal AI")
        welcome_title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        welcome_title.setStyleSheet("color: #4CAF50;")
        welcome_layout.addWidget(welcome_title)
        
        welcome_desc = QLabel("نظام القيود المحاسبية الذكي المدعوم بالذكاء الاصطناعي")
        welcome_desc.setFont(QFont("Segoe UI", 12))
        welcome_desc.setStyleSheet("color: #888;")
        welcome_layout.addWidget(welcome_desc)
        
        welcome_frame.setLayout(welcome_layout)
        main_layout.addWidget(welcome_frame)
        
        # Statistics grid
        stats_grid = QGridLayout()
        stats_grid.setSpacing(15)
        
        self.cards = {}
        
        # Create cards
        self.cards['total_entries'] = DashboardCard("إجمالي القيود", "0", "📝", "#2196F3")
        self.cards['today_entries'] = DashboardCard("قيود اليوم", "0", "📅", "#4CAF50")
        self.cards['total_debit'] = DashboardCard("إجمالي المدين", "0 ج.م", "💰", "#FF9800")
        self.cards['total_credit'] = DashboardCard("إجمالي الدائن", "0 ج.م", "💵", "#FF9800")
        self.cards['customers'] = DashboardCard("عدد العملاء", "0", "👥", "#9C27B0")
        self.cards['suppliers'] = DashboardCard("عدد الموردين", "0", "🏢", "#E91E63")
        self.cards['cash_balance'] = DashboardCard("رصيد الصندوق", "0 ج.م", "💳", "#00BCD4")
        self.cards['bank_balance'] = DashboardCard("أرصدة البنوك", "0 ج.م", "🏦", "#00BCD4")
        
        # Add cards to grid
        positions = [
            (0, 0, 'total_entries'),
            (0, 1, 'today_entries'),
            (0, 2, 'total_debit'),
            (0, 3, 'total_credit'),
            (1, 0, 'customers'),
            (1, 1, 'suppliers'),
            (1, 2, 'cash_balance'),
            (1, 3, 'bank_balance'),
        ]
        
        for row, col, key in positions:
            stats_grid.addWidget(self.cards[key], row, col)
        
        main_layout.addLayout(stats_grid)
        
        # Quick actions
        actions_title = QLabel("إجراءات سريعة")
        actions_title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        actions_title.setStyleSheet("color: #E0E0E0; margin-top: 10px;")
        main_layout.addWidget(actions_title)
        
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(15)
        
        quick_actions = [
            ("🧠 قيد ذكي", self.on_smart_journal),
            ("📝 قيد يدوي", self.on_manual_journal),
            ("📊 التقارير", self.on_reports),
            ("📚 دليل الحسابات", self.on_chart_of_accounts),
        ]
        
        for action_text, handler in quick_actions:
            btn = QPushButton(action_text)
            btn.setFixedHeight(50)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    font-size: 14px;
                    font-weight: bold;
                    padding: 10px 20px;
                }
                QPushButton:hover {
                    background-color: #45A049;
                }
            """)
            btn.clicked.connect(handler)
            actions_layout.addWidget(btn)
        
        actions_layout.addStretch()
        main_layout.addLayout(actions_layout)
        
        main_layout.addStretch()
        
        # Scroll area wrapper
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        content_widget = QWidget()
        content_widget.setLayout(main_layout)
        scroll.setWidget(content_widget)
        
        # Main layout for this widget
        outer_layout = QVBoxLayout()
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.addWidget(scroll)
        self.setLayout(outer_layout)
    
    def load_data(self):
        """Load dashboard data from database"""
        try:
            session = self.db_manager.get_session()
            
            # TODO: Load actual data from database
            # For now, show placeholder values
            
            session.close()
            
        except Exception as e:
            logger.error(f"Error loading dashboard data: {e}")
    
    def on_smart_journal(self):
        """Handle smart journal button click"""
        logger.info("Smart journal clicked")
        # Navigation will be handled by main window
    
    def on_manual_journal(self):
        """Handle manual journal button click"""
        logger.info("Manual journal clicked")
    
    def on_reports(self):
        """Handle reports button click"""
        logger.info("Reports clicked")
    
    def on_chart_of_accounts(self):
        """Handle chart of accounts button click"""
        logger.info("Chart of accounts clicked")
