"""
Finovate Journal AI - Main Application Entry Point
"""
import sys
from pathlib import Path

# Add app directory to path
app_dir = Path(__file__).parent
sys.path.insert(0, str(app_dir))

from PySide6.QtWidgets import QApplication, QSplashScreen
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap, QFont
import logging

from config import get_app_settings, get_developer_info
from utils import setup_logging


def main():
    """Main application entry point."""
    
    # Initialize settings first to get paths
    settings = get_app_settings()
    
    # Setup logging
    setup_logging(settings.logs_dir, level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    logger.info("Starting Finovate Journal AI...")
    
    try:
        # Create Qt application
        app = QApplication(sys.argv)
        app.setApplicationName(settings.app_name)
        app.setOrganizationName(settings.organization)
        app.setApplicationVersion(settings.version)
        
        # Set application metadata
        app.setApplicationDisplayName("Finovate Journal AI")
        
        # Enable RTL for Arabic
        if settings.default_language == 'ar':
            app.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        
        # Set default font
        font = QFont("Segoe UI", settings.font_size)
        app.setFont(font)
        
        logger.info(f"Application initialized: {settings.app_name} v{settings.version}")
        logger.info(f"Data directory: {settings.data_dir}")
        logger.info(f"Language: {settings.default_language}")
        
        # Show splash screen (optional)
        # splash_path = settings.assets_dir / "splash.png"
        # if splash_path.exists():
        #     pixmap = QPixmap(str(splash_path))
        #     splash = QSplashScreen(pixmap, Qt.WindowStaysOnTopHint)
        #     splash.showMessage(
        #         f"{settings.app_name}\nVersion {settings.version}",
        #         Qt.AlignCenter | Qt.AlignBottom,
        #         Qt.white
        #     )
        #     splash.show()
        #     app.processEvents()
        
        # Import and show main window
        from ui.main_window import MainWindow
        
        window = MainWindow()
        window.show()
        
        # splash.finish(window)
        
        logger.info("Main window displayed")
        
        # Run application event loop
        exit_code = app.exec()
        
        logger.info(f"Application exiting with code: {exit_code}")
        
        return exit_code
        
    except Exception as e:
        logger.exception(f"Fatal error in main application: {e}")
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
