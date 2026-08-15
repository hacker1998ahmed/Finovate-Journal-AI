"""
Finovate Journal AI - Main Application Entry Point
Copyright © 2025 Ahmed Mostafa Ibrahim — All Rights Reserved.
"""

import sys
import os
from pathlib import Path

# Add app directory to path
app_dir = Path(__file__).parent
sys.path.insert(0, str(app_dir))

from PySide6.QtWidgets import QApplication, QSplashScreen
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap, QFont

from app.config.settings import AppSettings
from app.database.db_manager import DatabaseManager
from app.ui.main_window import MainWindow
from app.utils.logger import get_logger

logger = get_logger(__name__)


def main():
    """Main application entry point"""
    
    # Set high DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("Finovate Journal AI")
    app.setApplicationVersion(AppSettings.VERSION)
    app.setOrganizationName("Finovate – AHMED EG")
    
    # Set application style
    app.setStyle("Fusion")
    
    # Set default font
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    # Initialize database
    try:
        db_manager = DatabaseManager()
        db_manager.initialize()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.critical(
            None,
            "Database Error",
            f"Failed to initialize database:\n{str(e)}\n\nThe application will now close."
        )
        return 1
    
    # Show splash screen
    splash_pix = QPixmap(400, 300)
    splash_pix.fill(Qt.white)
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.showMessage(
        "Finovate Journal AI\nVersion " + AppSettings.VERSION + 
        "\n\nAI-Powered Accounting Assistant\n\n" +
        "© 2025 Ahmed Mostafa Ibrahim\nFinovate – AHMED EG",
        Qt.AlignCenter,
        Qt.black
    )
    splash.show()
    app.processEvents()
    
    # Create main window after a short delay
    def show_main_window():
        try:
            window = MainWindow()
            window.show()
            splash.finish(window)
            logger.info("Main window displayed")
        except Exception as e:
            logger.error(f"Failed to create main window: {e}")
            splash.close()
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.critical(
                None,
                "Application Error",
                f"Failed to start application:\n{str(e)}"
            )
    
    QTimer.singleShot(2000, show_main_window)
    
    # Run application
    sys.exit(app.exec())


if __name__ == "__main__":
    sys.exit(main())
