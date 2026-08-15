"""Main window for Finovate Journal AI."""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QStackedWidget, QLabel, QPushButton, QFrame
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon

from ..config.constants import APP_NAME, VERSION, DEVELOPER_INFO
from .dashboard import DashboardPage
from .smart_journal import SmartJournalPage
from .manual_journal import ManualJournalPage
from .chart_of_accounts import ChartOfAccountsPage
from .journal_viewer import JournalViewerPage
from .settings_page import SettingsPage
from .about_dialog import AboutDialog


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self):
        super().__init__()
        
        self.setWindowTitle(APP_NAME)
        self.setMinimumSize(1200, 800)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Sidebar
        self.sidebar = self._create_sidebar()
        main_layout.addWidget(self.sidebar)
        
        # Content area
        content_frame = QFrame()
        content_frame.setObjectName("contentFrame")
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Stacked widget for pages
        self.stack = QStackedWidget()
        
        # Add pages
        self.dashboard_page = DashboardPage()
        self.smart_journal_page = SmartJournalPage()
        self.manual_journal_page = ManualJournalPage()
        self.chart_of_accounts_page = ChartOfAccountsPage()
        self.journal_viewer_page = JournalViewerPage()
        self.settings_page = SettingsPage()
        
        self.stack.addWidget(self.dashboard_page)
        self.stack.addWidget(self.smart_journal_page)
        self.stack.addWidget(self.manual_journal_page)
        self.stack.addWidget(self.chart_of_accounts_page)
        self.stack.addWidget(self.journal_viewer_page)
        self.stack.addWidget(self.settings_page)
        
        content_layout.addWidget(self.stack)
        main_layout.addWidget(content_frame, 1)
        
        # Apply styles
        self._apply_styles()
        
    def _create_sidebar(self) -> QFrame:
        """Create sidebar navigation."""
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(250)
        
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(10, 20, 10, 10)
        layout.setSpacing(5)
        
        # App title
        title_label = QLabel(f"{APP_NAME}\nv{VERSION}")
        title_label.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #2E86AB;
            padding: 15px;
        """)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Navigation buttons
        nav_buttons = [
            ("🏠 الرئيسية", 0),
            ("🧠 القيد الذكي", 1),
            ("📝 قيد يدوي", 2),
            ("📚 دليل الحسابات", 3),
            ("📖 دفتر اليومية", 4),
            ("⚙️ الإعدادات", 5),
        ]
        
        for text, index in nav_buttons:
            btn = QPushButton(text)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                    padding: 12px;
                    text-align: right;
                    font-size: 14px;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #E8F4F8;
                }
                QPushButton:checked {
                    background-color: #2E86AB;
                    color: white;
                }
            """)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setCheckable(True)
            if index == 0:
                btn.setChecked(True)
            btn.clicked.connect(lambda checked, i=index: self.stack.setCurrentIndex(i))
            layout.addWidget(btn)
        
        layout.addStretch()
        
        # About button
        about_btn = QPushButton("ℹ️ حول البرنامج")
        about_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                padding: 12px;
                text-align: right;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #E8F4F8;
            }
        """)
        about_btn.setCursor(Qt.PointingHandCursor)
        about_btn.clicked.connect(self._show_about)
        layout.addWidget(about_btn)
        
        return sidebar
    
    def _apply_styles(self):
        """Apply application styles."""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F5F5F5;
            }
            #sidebar {
                background-color: #FFFFFF;
                border-right: 1px solid #E0E0E0;
            }
            #contentFrame {
                background-color: #F5F5F5;
            }
            QStackedWidget {
                background-color: #F5F5F5;
            }
        """)
    
    def _show_about(self):
        """Show about dialog."""
        dialog = AboutDialog(self)
        dialog.exec()
