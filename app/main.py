# Finovate Journal AI - Main Application Entry Point

"""
Main entry point for Finovate Journal AI application.
Initializes the database and starts the PySide6 UI.
"""

import sys
import os
from pathlib import Path

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PySide6.QtCore import Qt, QTranslator, QLocale
from PySide6.QtGui import QFont

from app.config.constants import APP_INFO, DEVELOPER_INFO
from app.config.app_settings import settings
from app.database.base import init_db


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_INFO.name)
        self.setMinimumSize(1200, 800)
        
        # Initialize UI (placeholder for now)
        self._init_ui()
    
    def _init_ui(self):
        """Initialize the user interface."""
        from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # Welcome label
        welcome_label = QLabel(f"مرحبًا بك في {APP_INFO.name}")
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("font-size: 24px; font-weight: bold; padding: 20px;")
        layout.addWidget(welcome_label)
        
        # Version info
        version_label = QLabel(f"الإصدار {APP_INFO.version}")
        version_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(version_label)
        
        # Developer info
        dev_label = QLabel(f"المطور: {DEVELOPER_INFO.name}")
        dev_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(dev_label)
        
        # TODO button
        todo_btn = QPushButton("القيد الذكي (قريبًا)")
        todo_btn.clicked.connect(lambda: QMessageBox.information(
            self, "تحت الإنشاء", "هذه الميزة سيتم تنفيذها في التحديث القادم."
        ))
        layout.addWidget(todo_btn)
        
        # Database status
        db_label = QLabel("✓ قاعدة البيانات جاهزة")
        db_label.setAlignment(Qt.AlignCenter)
        db_label.setStyleSheet("color: green;")
        layout.addWidget(db_label)


def main():
    """Main function to start the application."""
    # Initialize database
    init_db()
    print("Database initialized successfully.")
    
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName(APP_INFO.name)
    app.setApplicationVersion(APP_INFO.version)
    app.setOrganizationName(DEVELOPER_INFO.brand)
    
    # Set RTL for Arabic
    if settings.language == "ar":
        app.setLayoutDirection(Qt.RightToLeft)
    
    # Set font
    font = QFont("Segoe UI" if os.name == 'nt' else "Ubuntu", settings.font_size)
    app.setFont(font)
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Run application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
