"""
Finovate Journal AI - Main Application Entry Point
"""
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from PySide6.QtWidgets import QApplication, QSplashScreen
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap, QFont

from app.config.settings import get_settings
from app.database.database import get_session_manager
from app.ui.main_window import MainWindow
from app.utils.logging_config import setup_logging, get_logger


def main():
    """Main application entry point"""
    
    # Setup logging
    log_file = setup_logging()
    
    logger = get_logger(__name__)
    logger.info("Starting Finovate Journal AI v1.0.0")
    
    # Get settings
    settings = get_settings()
    
    # Create Qt Application
    app = QApplication(sys.argv)
    app.setApplicationName("Finovate Journal AI")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Finovate - AHMED EG")
    
    # Set application style
    app.setStyle("Fusion")
    
    # Set font
    font = QFont("Segoe UI", 10)
    if settings.language == "ar":
        font = QFont("Arial", 10)
    app.setFont(font)
    
    # Show splash screen
    splash_pix = QPixmap(400, 300)
    splash_pix.fill(Qt.white)
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.showMessage(
        "Finovate Journal AI\nVersion 1.0.0\n\nAI-Powered Accounting Assistant\n\n© 2025 Ahmed Mostafa Ibrahim",
        Qt.AlignCenter,
        Qt.black
    )
    splash.show()
    app.processEvents()
    
    try:
        # Initialize database
        logger.info("Initializing database...")
        session_manager = get_session_manager()
        
        # Create main window
        logger.info("Creating main window...")
        window = MainWindow()
        
        # Close splash after delay
        QTimer.singleShot(2000, splash.close)
        
        # Show main window
        window.show()
        
        logger.info("Application started successfully")
        
        # Run application
        sys.exit(app.exec())
        
    except Exception as e:
        logger.exception("Fatal error during startup: %s", str(e))
        splash.close()
        raise


if __name__ == "__main__":
    main()
