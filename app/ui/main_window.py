"""
Main Window for Finovate Journal AI
Professional desktop interface with sidebar navigation
"""
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QStackedWidget, QPushButton, QLabel, QFrame,
    QScrollArea, QSizePolicy, QMessageBox, QToolBar
)
from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtGui import QIcon, QFont, QAction

import logging
from config import get_app_settings, get_developer_info

logger = logging.getLogger(__name__)


class SidebarButton(QPushButton):
    """Styled button for sidebar navigation."""
    
    def __init__(self, text: str, icon_path: str = None):
        super().__init__(text)
        self.setCheckable(True)
        self.setCursor(Qt.PointingHandCursor)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setMinimumHeight(45)
        self.setStyleSheet(self._get_stylesheet())
        
    def _get_stylesheet(self) -> str:
        return """
            QPushButton {
                background-color: transparent;
                border: none;
                border-left: 3px solid transparent;
                padding: 12px 15px;
                text-align: left;
                font-size: 13px;
                color: #333333;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
            QPushButton:checked {
                background-color: #e3f2fd;
                border-left: 3px solid #1976d2;
                color: #1976d2;
                font-weight: bold;
            }
        """


class MainWindow(QMainWindow):
    """Main application window with sidebar and content area."""
    
    # Signals for navigation
    page_changed = Signal(str)
    
    def __init__(self):
        super().__init__()
        
        self.settings = get_app_settings()
        self.developer = get_developer_info()
        
        logger.info("Initializing main window...")
        
        self._setup_window()
        self._create_sidebar()
        self._create_content_area()
        self._create_pages()
        self._connect_signals()
        
        logger.info("Main window initialized successfully")
    
    def _setup_window(self):
        """Configure main window properties."""
        self.setWindowTitle(f"{self.settings.app_name} v{self.settings.version}")
        self.setMinimumSize(1280, 720)
        self.resize(1400, 800)
        
        # Set window icon if available
        # icon_path = self.settings.assets_dir / "icon.ico"
        # if icon_path.exists():
        #     self.setWindowIcon(QIcon(str(icon_path)))
    
    def _create_sidebar(self):
        """Create the sidebar navigation panel."""
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(250)
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setStyleSheet("""
            QFrame#sidebar {
                background-color: #ffffff;
                border-right: 1px solid #e0e0e0;
            }
        """)
        
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)
        
        # App logo/title section
        header_frame = QFrame()
        header_frame.setFixedHeight(80)
        header_frame.setStyleSheet("""
            QFrame {
                background-color: #1976d2;
                border-bottom: 2px solid #1565c0;
            }
        """)
        header_layout = QVBoxLayout(header_frame)
        header_layout.setAlignment(Qt.AlignCenter)
        
        app_label = QLabel(self.settings.app_name)
        app_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        app_label.setStyleSheet("color: white; padding: 10px;")
        app_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(app_label)
        
        version_label = QLabel(f"v{self.settings.version}")
        version_label.setStyleSheet("color: rgba(255,255,255,0.8); font-size: 11px;")
        version_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(version_label)
        
        sidebar_layout.addWidget(header_frame)
        
        # Scrollable buttons area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("border: none; background-color: transparent;")
        
        buttons_widget = QWidget()
        buttons_layout = QVBoxLayout(buttons_widget)
        buttons_layout.setContentsMargins(0, 10, 0, 10)
        buttons_layout.setSpacing(2)
        buttons_layout.addStretch()
        
        # Navigation buttons
        menu_items = [
            ("home", "🏠 الرئيسية", "Dashboard"),
            ("smart_journal", "🧠 القيد الذكي", "Smart Journal"),
            ("manual_journal", "📝 قيد يدوي", "Manual Journal"),
            ("chart_of_accounts", "📚 دليل الحسابات", "Chart of Accounts"),
            ("journal", "📖 دفتر اليومية", "Journal"),
            ("ledger", "📕 دفتر الأستاذ", "Ledger"),
            ("trial_balance", "⚖️ ميزان المراجعة", "Trial Balance"),
            ("customers", "👥 العملاء", "Customers"),
            ("suppliers", "🏢 الموردون", "Suppliers"),
            ("reports", "📊 التقارير", "Reports"),
            ("settings", "⚙️ الإعدادات", "Settings"),
            ("about", "ℹ️ حول البرنامج", "About"),
        ]
        
        self.sidebar_buttons = {}
        for key, ar_text, en_text in menu_items:
            display_text = ar_text if self.settings.default_language == 'ar' else en_text
            btn = SidebarButton(f"  {display_text}")
            btn.setProperty("page_key", key)
            btn.clicked.connect(lambda checked, k=key: self._navigate_to(k))
            buttons_layout.addWidget(btn)
            self.sidebar_buttons[key] = btn
        
        buttons_layout.addStretch()
        scroll.setWidget(buttons_widget)
        sidebar_layout.addWidget(scroll)
        
        # Developer info footer
        footer_frame = QFrame()
        footer_frame.setFixedHeight(50)
        footer_frame.setStyleSheet("""
            QFrame {
                background-color: #f5f5f5;
                border-top: 1px solid #e0e0e0;
            }
        """)
        footer_layout = QVBoxLayout(footer_frame)
        footer_layout.setContentsMargins(10, 5, 10, 5)
        
        dev_label = QLabel(f"{self.developer.brand}")
        dev_label.setFont(QFont("Segoe UI", 9))
        dev_label.setStyleSheet("color: #666;")
        dev_label.setAlignment(Qt.AlignCenter)
        footer_layout.addWidget(dev_label)
        
        sidebar_layout.addWidget(footer_frame)
    
    def _create_content_area(self):
        """Create the main content area."""
        self.content_stack = QStackedWidget()
        self.content_stack.setStyleSheet("background-color: #f8f9fa;")
    
    def _create_pages(self):
        """Create all application pages."""
        # Placeholder pages - will be implemented progressively
        from ui.pages.dashboard_page import DashboardPage
        from ui.pages.smart_journal_page import SmartJournalPage
        from ui.pages.placeholder_page import PlaceholderPage
        
        # Dashboard
        self.dashboard_page = DashboardPage()
        self.content_stack.addWidget(self.dashboard_page)
        self.page_widgets = {"home": self.dashboard_page}
        
        # Smart Journal
        self.smart_journal_page = SmartJournalPage()
        self.content_stack.addWidget(self.smart_journal_page)
        self.page_widgets["smart_journal"] = self.smart_journal_page
        
        # Other pages (placeholders)
        placeholder_pages = [
            "manual_journal", "chart_of_accounts", "journal", 
            "ledger", "trial_balance", "customers", "suppliers",
            "reports", "settings", "about"
        ]
        
        for page_key in placeholder_pages:
            if page_key not in self.page_widgets:
                page = PlaceholderPage(page_key)
                self.content_stack.addWidget(page)
                self.page_widgets[page_key] = page
    
    def _connect_signals(self):
        """Connect signals and slots."""
        pass
    
    def _navigate_to(self, page_key: str):
        """Navigate to a specific page."""
        if page_key in self.page_widgets:
            # Update button states
            for key, btn in self.sidebar_buttons.items():
                btn.setChecked(key == page_key)
            
            # Switch to page
            index = self.content_stack.indexOf(self.page_widgets[page_key])
            self.content_stack.setCurrentIndex(index)
            
            # Emit signal
            self.page_changed.emit(page_key)
            
            logger.debug(f"Navigated to page: {page_key}")
    
    def closeEvent(self, event):
        """Handle application close event."""
        reply = QMessageBox.question(
            self,
            'Exit Application',
            'Are you sure you want to exit?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            logger.info("Application closing...")
            event.accept()
        else:
            event.ignore()
