"""
Finovate Journal AI - Sidebar Navigation
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QScrollArea,
    QFrame, QSpacerItem, QSizePolicy
)
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QFont


class SideBar(QWidget):
    """Sidebar navigation component"""
    
    navigation_requested = Signal(int)  # page_index
    about_requested = Signal()
    
    def __init__(self):
        super().__init__()
        
        self.setMinimumWidth(250)
        self.setMaximumWidth(300)
        
        self._setup_ui()
        self._apply_styles()
        
    def _setup_ui(self):
        """Setup sidebar UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 20, 10, 10)
        layout.setSpacing(5)
        
        # Logo/Title section
        title_label = QLabel("Finovate\nJournal AI")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        title_label.setStyleSheet("color: #2c3e50; padding: 15px;")
        layout.addWidget(title_label)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("background-color: #bdc3c7;")
        layout.addWidget(separator)
        
        # Scrollable navigation buttons
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("border: none; background-color: transparent;")
        
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 10, 0, 10)
        scroll_layout.setSpacing(5)
        
        # Navigation buttons
        self.nav_buttons = []
        
        nav_items = [
            ("🏠 الرئيسية / Dashboard", 0),
            ("🧠 القيد الذكي / Smart Journal", 1),
            ("📝 قيد يدوي / Manual Journal", 2),
            ("📚 دليل الحسابات / Chart of Accounts", 3),
            ("📖 دفتر اليومية / Journal", 4),
            ("📕 دفتر الأستاذ / Ledger", 5),
            ("⚖️ ميزان المراجعة / Trial Balance", 6),
            ("⚙️ الإعدادات / Settings", 7),
        ]
        
        for text, index in nav_items:
            btn = QPushButton(text)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setFixedHeight(45)
            btn.clicked.connect(lambda checked, idx=index: self.navigation_requested.emit(idx))
            scroll_layout.addWidget(btn)
            self.nav_buttons.append(btn)
        
        # Spacer
        scroll_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # About button
        about_btn = QPushButton("ℹ️ حول البرنامج / About")
        about_btn.setCursor(Qt.PointingHandCursor)
        about_btn.setFixedHeight(45)
        about_btn.clicked.connect(lambda: self.about_requested.emit())
        scroll_layout.addWidget(about_btn)
        
        scroll_area.setWidget(scroll_content)
        layout.addWidget(scroll_area)
        
    def _apply_styles(self):
        """Apply styles to sidebar"""
        self.setStyleSheet("""
            SideBar {
                background-color: #ecf0f1;
                border-right: 2px solid #3498db;
            }
            
            QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 5px;
                text-align: left;
                padding-left: 15px;
                font-size: 13px;
                color: #2c3e50;
            }
            
            QPushButton:hover {
                background-color: #3498db;
                color: white;
            }
            
            QPushButton:pressed {
                background-color: #2980b9;
            }
        """)
        
    def set_active_page(self, index: int):
        """Set active navigation button"""
        for i, btn in enumerate(self.nav_buttons):
            if i == index:
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #3498db;
                        color: white;
                        font-weight: bold;
                    }
                """)
            else:
                btn.setStyleSheet("")
