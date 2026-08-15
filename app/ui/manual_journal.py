"""Manual Journal Entry page."""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

class ManualJournalPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        title = QLabel("📝 قيد يدوي")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2E86AB; padding: 20px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        info = QLabel("سيتم تطبيق صفحة القيد اليدوي في التحديث القادم")
        info.setStyleSheet("font-size: 16px; color: #666; padding: 20px;")
        info.setAlignment(Qt.AlignCenter)
        layout.addWidget(info)
        layout.addStretch()
