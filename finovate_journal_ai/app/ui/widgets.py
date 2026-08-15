"""
Finovate Journal AI - Placeholder UI Widgets
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QFrame
)
from PySide6.QtGui import QFont


class ManualJournalWidget(QWidget):
    """Manual Journal Entry Widget - Placeholder"""
    
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        title = QLabel("📝 قيد يدوي / Manual Journal")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        layout.addWidget(title)
        
        placeholder = QLabel("سيتم تطوير شاشة القيد اليدوي قريباً\nManual Journal entry coming soon")
        placeholder.setAlignment(Qt.AlignCenter)
        placeholder.setStyleSheet("padding: 50px; color: #7f8c8d;")
        layout.addWidget(placeholder)


class ChartOfAccountsWidget(QWidget):
    """Chart of Accounts Widget - Placeholder"""
    
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        title = QLabel("📚 دليل الحسابات / Chart of Accounts")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        layout.addWidget(title)
        
        placeholder = QLabel("سيتم تطوير دليل الحسابات قريباً\nChart of Accounts coming soon")
        placeholder.setAlignment(Qt.AlignCenter)
        placeholder.setStyleSheet("padding: 50px; color: #7f8c8d;")
        layout.addWidget(placeholder)
    
    def refresh_data(self):
        pass


class JournalViewerWidget(QWidget):
    """Journal Viewer Widget - Placeholder"""
    
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        title = QLabel("📖 دفتر اليومية / Journal Viewer")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        layout.addWidget(title)
        
        placeholder = QLabel("سيتم تطوير دفتر اليومية قريباً\nJournal Viewer coming soon")
        placeholder.setAlignment(Qt.AlignCenter)
        placeholder.setStyleSheet("padding: 50px; color: #7f8c8d;")
        layout.addWidget(placeholder)
    
    def refresh_data(self):
        pass


class LedgerWidget(QWidget):
    """Ledger Widget - Placeholder"""
    
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        title = QLabel("📕 دفتر الأستاذ / Ledger")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        layout.addWidget(title)
        
        placeholder = QLabel("سيتم تطوير دفتر الأستاذ قريباً\nLedger coming soon")
        placeholder.setAlignment(Qt.AlignCenter)
        placeholder.setStyleSheet("padding: 50px; color: #7f8c8d;")
        layout.addWidget(placeholder)


class TrialBalanceWidget(QWidget):
    """Trial Balance Widget - Placeholder"""
    
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        title = QLabel("⚖️ ميزان المراجعة / Trial Balance")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        layout.addWidget(title)
        
        placeholder = QLabel("سيتم تطوير ميزان المراجعة قريباً\nTrial Balance coming soon")
        placeholder.setAlignment(Qt.AlignCenter)
        placeholder.setStyleSheet("padding: 50px; color: #7f8c8d;")
        layout.addWidget(placeholder)


class SettingsWidget(QWidget):
    """Settings Widget - Placeholder"""
    
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        title = QLabel("⚙️ الإعدادات / Settings")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        layout.addWidget(title)
        
        placeholder = QLabel("سيتم تطوير الإعدادات قريباً\nSettings coming soon")
        placeholder.setAlignment(Qt.AlignCenter)
        placeholder.setStyleSheet("padding: 50px; color: #7f8c8d;")
        layout.addWidget(placeholder)


class AboutDialog:
    """About Dialog - Simple implementation"""
    
    def __init__(self, parent=None):
        self.parent = parent
        from PySide6.QtWidgets import QMessageBox
        from PySide6.QtCore import Qt
        
        self.msg = QMessageBox(parent)
        self.msg.setWindowTitle("حول البرنامج / About")
        self.msg.setIcon(QMessageBox.Information)
        
        about_text = """
        <h2>Finovate Journal AI</h2>
        <p>AI-Powered Accounting Journal Assistant</p>
        <p><b>Version:</b> 1.0.0</p>
        <hr>
        <p><b>Developed by:</b><br>
        Ahmed Mostafa Ibrahim<br>
        Finovate – AHMED EG</p>
        <p><b>Email:</b> GOGOM8870@GMAIL.COM<br>
        <b>Phone:</b> 01225155329</p>
        <hr>
        <p>© 2025 Ahmed Mostafa Ibrahim — All Rights Reserved.</p>
        """
        
        self.msg.setText(about_text)
        self.msg.setStandardButtons(QMessageBox.Ok)
        
    def exec(self):
        self.msg.exec()
