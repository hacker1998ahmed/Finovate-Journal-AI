"""
Placeholder Page for unimplemented features
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PySide6.QtCore import Qt


class PlaceholderPage(QWidget):
    """Placeholder page for features not yet implemented."""
    
    def __init__(self, page_key: str):
        super().__init__()
        
        self.page_key = page_key
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        
        # Create placeholder frame
        frame = QFrame()
        frame.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 40px;
                border: 2px dashed #ccc;
            }
        """)
        
        frame_layout = QVBoxLayout(frame)
        frame_layout.setAlignment(Qt.AlignCenter)
        
        # Icon/emoji
        icon_label = QLabel("🚧")
        icon_label.setFont(icon_label.font())
        icon_label.setStyleSheet("font-size: 64px;")
        icon_label.setAlignment(Qt.AlignCenter)
        frame_layout.addWidget(icon_label)
        
        # Title
        title_label = QLabel(f"{page_key.replace('_', ' ').title()}")
        title_label.setFont(title_label.font())
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")
        title_label.setAlignment(Qt.AlignCenter)
        frame_layout.addWidget(title_label)
        
        # Description
        desc_label = QLabel(
            "This feature is under development.\n"
            "Coming soon in a future update!"
        )
        desc_label.setStyleSheet("font-size: 14px; color: #666;")
        desc_label.setAlignment(Qt.AlignCenter)
        frame_layout.addWidget(desc_label)
        
        layout.addWidget(frame)
