"""Main entry point for Finovate Journal AI."""

import sys
from pathlib import Path

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent))

from PySide6.QtWidgets import QApplication, QSplashScreen
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap, QFont

from app.config.constants import (
    APP_NAME, 
    VERSION, 
    DEFAULT_WINDOW_WIDTH, 
    DEFAULT_WINDOW_HEIGHT,
    DEFAULT_LANGUAGE,
)
from app.utils.logging_config import get_logger
from app.database.database import init_db

logger = get_logger(__name__)


def main():
    """Main application entry point."""
    try:
        # Initialize database
        logger.info(f"Starting {APP_NAME} v{VERSION}")
        if not init_db():
            logger.error("Failed to initialize database")
            return 1
        
        # Create application
        app = QApplication(sys.argv)
        app.setApplicationName(APP_NAME)
        app.setOrganizationName("Finovate – AHMED EG")
        app.setApplicationVersion(VERSION)
        
        # Set application font
        font = QFont("Segoe UI", 10)
        if DEFAULT_LANGUAGE == "ar":
            font.setFamily("Arial")
        app.setFont(font)
        
        # Show splash screen
        splash_pixmap = QPixmap(400, 300)
        splash_pixmap.fill(Qt.white)
        splash = QSplashScreen(splash_pixmap, Qt.WindowStaysOnTopHint)
        
        splash_message = f"""
        <div style='text-align: center; padding: 20px;'>
            <h2 style='color: #2E86AB;'>{APP_NAME}</h2>
            <p style='font-size: 14px;'>Version {VERSION}</p>
            <p style='font-size: 12px; color: #666;'>Professional Desktop Accounting</p>
            <p style='font-size: 11px; color: #999; margin-top: 30px;'>
                Developed by<br/>
                <b>Ahmed Mostafa Ibrahim</b><br/>
                Finovate – AHMED EG
            </p>
        </div>
        """
        splash.showMessage(
            splash_message,
            Qt.AlignCenter,
            Qt.black
        )
        splash.show()
        app.processEvents()
        
        # Import and create main window (will be implemented)
        from app.ui.main_window import MainWindow
        
        window = MainWindow()
        window.resize(DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT)
        
        # Close splash after delay
        QTimer.singleShot(2000, splash.finish)
        QTimer.singleShot(2000, window.show)
        
        logger.info("Application started successfully")
        
        # Run application
        sys.exit(app.exec())
        
    except Exception as e:
        logger.exception(f"Fatal error: {e}")
        from PySide6.QtWidgets import QMessageBox
        app = QApplication.instance() or QApplication(sys.argv)
        QMessageBox.critical(
            None,
            "Fatal Error",
            f"An unexpected error occurred:\n\n{str(e)}\n\nPlease check the logs for details."
        )
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
