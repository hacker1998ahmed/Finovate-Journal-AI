"""UI module for Finovate Journal AI."""

from .main_window import MainWindow
from .dashboard import DashboardPage
from .smart_journal import SmartJournalPage
from .manual_journal import ManualJournalPage
from .chart_of_accounts import ChartOfAccountsPage
from .journal_viewer import JournalViewerPage
from .settings_page import SettingsPage
from .about_dialog import AboutDialog

__all__ = [
    "MainWindow",
    "DashboardPage",
    "SmartJournalPage",
    "ManualJournalPage",
    "ChartOfAccountsPage",
    "JournalViewerPage",
    "SettingsPage",
    "AboutDialog",
]
