"""
Finovate Journal AI - UI Module
"""
from app.ui.main_window import MainWindow
from app.ui.sidebar import SideBar
from app.ui.dashboard import DashboardWidget
from app.ui.smart_journal import SmartJournalWidget
from app.ui.widgets import (
    ManualJournalWidget,
    ChartOfAccountsWidget,
    JournalViewerWidget,
    LedgerWidget,
    TrialBalanceWidget,
    SettingsWidget,
    AboutDialog
)

__all__ = [
    'MainWindow',
    'SideBar',
    'DashboardWidget',
    'SmartJournalWidget',
    'ManualJournalWidget',
    'ChartOfAccountsWidget',
    'JournalViewerWidget',
    'LedgerWidget',
    'TrialBalanceWidget',
    'SettingsWidget',
    'AboutDialog'
]
