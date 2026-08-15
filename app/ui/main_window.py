"""
Finovate Journal AI - Main Window
Copyright © 2025 Ahmed Mostafa Ibrahim — All Rights Reserved.
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QStackedWidget, QPushButton, QLabel, QFrame,
    QScrollArea, QSizePolicy, QSpacerItem
)
from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtGui import QIcon, QFont

from app.config.settings import AppSettings
from app.ui.screens.dashboard_screen import DashboardScreen
from app.ui.screens.smart_journal_screen import SmartJournalScreen
from app.ui.screens.manual_journal_screen import ManualJournalScreen
from app.ui.screens.chart_of_accounts_screen import ChartOfAccountsScreen
from app.ui.screens.journal_screen import JournalScreen
from app.ui.screens.settings_screen import SettingsScreen
from app.ui.screens.about_screen import AboutScreen
from app.utils.logger import get_logger

logger = get_logger(__name__)


class SidebarButton(QPushButton):
    """Custom sidebar button with icon and text"""
    
    def __init__(self, icon_text: str, label: str, parent=None):
        super().__init__(parent)
        self.setFixedHeight(50)
        self.setCursor(Qt.PointingHandCursor)
        
        # Layout
        layout = QHBoxLayout()
        layout.setContentsMargins(15, 5, 15, 5)
        
        # Icon label
        icon_label = QLabel(icon_text)
        icon_label.setFont(QFont("Segoe UI Emoji", 14))
        icon_label.setFixedWidth(30)
        layout.addWidget(icon_label)
        
        # Text label
        text_label = QLabel(label)
        text_label.setFont(QFont("Segoe UI", 10))
        text_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        layout.addWidget(text_label)
        
        layout.addStretch()
        self.setLayout(layout)
        
        # Style
        self.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 8px;
                color: #E0E0E0;
                text-align: left;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
            QPushButton:checked {
                background-color: rgba(255, 255, 255, 0.15);
                border-left: 4px solid #4CAF50;
            }
        """)


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Finovate Journal AI")
        self.setMinimumSize(1200, 800)
        self.resize(1400, 900)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create sidebar
        sidebar = self.create_sidebar()
        main_layout.addWidget(sidebar)
        
        # Create content area
        content_area = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setSpacing(0)
        content_layout.setContentsMargins(0, 0, 0, 0)
        
        # Top bar
        top_bar = self.create_top_bar()
        content_layout.addWidget(top_bar)
        
        # Stacked widget for screens
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Add screens
        self.screens = {}
        self.add_screen("dashboard", DashboardScreen(), "🏠")
        self.add_screen("smart_journal", SmartJournalScreen(), "🧠")
        self.add_screen("manual_journal", ManualJournalScreen(), "📝")
        self.add_screen("chart_of_accounts", ChartOfAccountsScreen(), "📚")
        self.add_screen("journal", JournalScreen(), "📖")
        self.add_screen("settings", SettingsScreen(), "⚙️")
        self.add_screen("about", AboutScreen(), "ℹ️")
        
        content_layout.addWidget(self.stacked_widget)
        content_area.setLayout(content_layout)
        
        main_layout.addWidget(content_area, 1)
        
        central_widget.setLayout(main_layout)
        
        # Apply stylesheet
        self.apply_styles()
        
        logger.info("Main window initialized")
    
    def create_sidebar(self) -> QWidget:
        """Create the sidebar navigation"""
        sidebar = QFrame()
        sidebar.setFixedWidth(250)
        sidebar.setObjectName("sidebar")
        
        layout = QVBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(10, 20, 10, 20)
        
        # Logo/Title
        title_label = QLabel("Finovate\nJournal AI")
        title_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #4CAF50; padding: 15px;")
        layout.addWidget(title_label)
        
        layout.addSpacing(20)
        
        # Navigation buttons
        self.nav_buttons = {}
        
        nav_items = [
            ("dashboard", "🏠", "الرئيسية"),
            ("smart_journal", "🧠", "القيد الذكي"),
            ("manual_journal", "📝", "قيد يدوي"),
            ("chart_of_accounts", "📚", "دليل الحسابات"),
            ("journal", "📖", "دفتر اليومية"),
            ("settings", "⚙️", "الإعدادات"),
            ("about", "ℹ️", "حول البرنامج"),
        ]
        
        for screen_id, icon, label in nav_items:
            btn = SidebarButton(icon, label)
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, sid=screen_id: self.navigate_to(sid))
            layout.addWidget(btn)
            self.nav_buttons[screen_id] = btn
        
        # Set first button as checked
        if self.nav_buttons:
            first_key = list(self.nav_buttons.keys())[0]
            self.nav_buttons[first_key].setChecked(True)
        
        layout.addStretch()
        
        # Footer
        footer_label = QLabel(f"v{AppSettings.VERSION}\n© 2025 Finovate")
        footer_label.setFont(QFont("Segoe UI", 8))
        footer_label.setAlignment(Qt.AlignCenter)
        footer_label.setStyleSheet("color: #888; padding: 10px;")
        layout.addWidget(footer_label)
        
        sidebar.setLayout(layout)
        return sidebar
    
    def create_top_bar(self) -> QWidget:
        """Create the top bar with user info and actions"""
        top_bar = QFrame()
        top_bar.setFixedHeight(60)
        top_bar.setObjectName("topBar")
        
        layout = QHBoxLayout()
        layout.setContentsMargins(20, 10, 20, 10)
        
        # Current screen title
        self.title_label = QLabel("الرئيسية")
        self.title_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        layout.addWidget(self.title_label)
        
        layout.addStretch()
        
        # User info
        user_label = QLabel("👤 Admin")
        user_label.setFont(QFont("Segoe UI", 10))
        layout.addWidget(user_label)
        
        top_bar.setLayout(layout)
        return top_bar
    
    def add_screen(self, screen_id: str, screen_widget: QWidget, icon: str):
        """Add a screen to the stacked widget"""
        self.stacked_widget.addWidget(screen_widget)
        self.screens[screen_id] = {
            'widget': screen_widget,
            'icon': icon,
            'index': self.stacked_widget.count() - 1
        }
    
    def navigate_to(self, screen_id: str):
        """Navigate to a specific screen"""
        if screen_id in self.screens:
            # Update stacked widget
            self.stacked_widget.setCurrentIndex(self.screens[screen_id]['index'])
            
            # Update title
            titles = {
                "dashboard": "الرئيسية",
                "smart_journal": "القيد الذكي",
                "manual_journal": "قيد يدوي",
                "chart_of_accounts": "دليل الحسابات",
                "journal": "دفتر اليومية",
                "settings": "الإعدادات",
                "about": "حول البرنامج"
            }
            self.title_label.setText(titles.get(screen_id, ""))
            
            # Update button states
            for btn_id, btn in self.nav_buttons.items():
                btn.setChecked(btn_id == screen_id)
            
            logger.info(f"Navigated to {screen_id}")
    
    def apply_styles(self):
        """Apply application styles"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1E1E1E;
            }
            QFrame#sidebar {
                background-color: #2D2D2D;
                border-right: 1px solid #3D3D3D;
            }
            QFrame#topBar {
                background-color: #2D2D2D;
                border-bottom: 1px solid #3D3D3D;
            }
            QLabel {
                color: #E0E0E0;
            }
            QStackedWidget {
                background-color: #1E1E1E;
            }
            QScrollArea {
                border: none;
                background-color: #1E1E1E;
            }
        """)
