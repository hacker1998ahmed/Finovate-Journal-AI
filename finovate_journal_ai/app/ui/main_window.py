"""
Finovate Journal AI - Main Window
"""
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QStackedWidget, QLabel, QPushButton, QFrame
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QFont

from app.config.settings import get_settings
from app.ui.sidebar import SideBar
from app.ui.dashboard import DashboardWidget
from app.ui.smart_journal import SmartJournalWidget
from app.ui.manual_journal import ManualJournalWidget
from app.ui.chart_of_accounts import ChartOfAccountsWidget
from app.ui.journal_viewer import JournalViewerWidget
from app.ui.ledger import LedgerWidget
from app.ui.trial_balance import TrialBalanceWidget
from app.ui.settings_widget import SettingsWidget
from app.ui.about_dialog import AboutDialog


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        
        self.settings = get_settings()
        self.current_company_id = None
        
        self._setup_window()
        self._setup_ui()
        self._connect_signals()
        
    def _setup_window(self):
        """Setup main window properties"""
        self.setWindowTitle("Finovate Journal AI - v1.0.0")
        self.setMinimumSize(1280, 720)
        self.resize(1400, 900)
        
        # Set window style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
        """)
        
    def _setup_ui(self):
        """Setup user interface"""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Sidebar
        self.sidebar = SideBar()
        main_layout.addWidget(self.sidebar)
        
        # Content area
        content_frame = QFrame()
        content_frame.setObjectName("contentFrame")
        content_frame.setStyleSheet("""
            #contentFrame {
                background-color: white;
                border-left: 1px solid #e0e0e0;
            }
        """)
        
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(0, 0, 0, 0)
        
        # Stacked widget for pages
        self.stack = QStackedWidget()
        
        # Add pages
        self.dashboard = DashboardWidget()
        self.smart_journal = SmartJournalWidget()
        self.manual_journal = ManualJournalWidget()
        self.chart_of_accounts = ChartOfAccountsWidget()
        self.journal_viewer = JournalViewerWidget()
        self.ledger = LedgerWidget()
        self.trial_balance = TrialBalanceWidget()
        self.settings_widget = SettingsWidget()
        
        self.stack.addWidget(self.dashboard)          # 0 - Dashboard
        self.stack.addWidget(self.smart_journal)      # 1 - Smart Journal
        self.stack.addWidget(self.manual_journal)     # 2 - Manual Journal
        self.stack.addWidget(self.chart_of_accounts)  # 3 - Chart of Accounts
        self.stack.addWidget(self.journal_viewer)     # 4 - Journal Viewer
        self.stack.addWidget(self.ledger)             # 5 - Ledger
        self.stack.addWidget(self.trial_balance)      # 6 - Trial Balance
        self.stack.addWidget(self.settings_widget)    # 7 - Settings
        
        content_layout.addWidget(self.stack)
        main_layout.addWidget(content_frame)
        
        # Setup RTL for Arabic
        if self.settings.language == "ar":
            self.setLayoutDirection(Qt.RightToLeft)
    
    def _connect_signals(self):
        """Connect sidebar signals to slots"""
        self.sidebar.navigation_requested.connect(self._on_navigation)
        self.sidebar.about_requested.connect(self._show_about)
        
    def _on_navigation(self, page_index: int):
        """Handle navigation request"""
        if 0 <= page_index < self.stack.count():
            self.stack.setCurrentIndex(page_index)
            
            # Refresh data when navigating to specific pages
            if page_index == 0:  # Dashboard
                self.dashboard.refresh_data()
            elif page_index == 4:  # Journal Viewer
                self.journal_viewer.refresh_data()
            elif page_index == 3:  # Chart of Accounts
                self.chart_of_accounts.refresh_data()
    
    def _show_about(self):
        """Show about dialog"""
        dialog = AboutDialog(self)
        dialog.exec()
    
    def closeEvent(self, event):
        """Handle application close"""
        # TODO: Save settings, close database connections, etc.
        event.accept()
