"""
Finovate Journal AI - About Screen
Copyright © 2025 Ahmed Mostafa Ibrahim — All Rights Reserved.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFrame, QMessageBox, QScrollArea
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from app.config.settings import AppSettings


class AboutScreen(QWidget):
    """About application screen"""
    
    def __init__(self):
        super().__init__()
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        main_layout = QVBoxLayout()
        main_layout.setSpacing(30)
        main_layout.setContentsMargins(50, 50, 50, 50)
        
        # Scroll area for content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        content_widget = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setSpacing(25)
        content_layout.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        
        # Application logo/icon placeholder
        logo_label = QLabel("🧾")
        logo_label.setFont(QFont("Segoe UI Emoji", 72))
        logo_label.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(logo_label)
        
        # Application name
        app_name = QLabel("Finovate Journal AI")
        app_name.setFont(QFont("Segoe UI", 28, QFont.Bold))
        app_name.setStyleSheet("color: #4CAF50;")
        app_name.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(app_name)
        
        # Version
        version_label = QLabel(f"Version {AppSettings.VERSION}")
        version_label.setFont(QFont("Segoe UI", 14))
        version_label.setStyleSheet("color: #888;")
        version_label.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(version_label)
        
        # Tagline
        tagline = QLabel("AI-Powered Accounting Journal Assistant\nمساعد القيود المحاسبية المدعوم بالذكاء الاصطناعي")
        tagline.setFont(QFont("Segoe UI", 12))
        tagline.setStyleSheet("color: #E0E0E0;")
        tagline.setAlignment(Qt.AlignCenter)
        tagline.setWordWrap(True)
        content_layout.addWidget(tagline)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("background-color: #3D3D3D; min-height: 1px; max-height: 1px;")
        separator.setFixedWidth(400)
        content_layout.addWidget(separator)
        
        # Developer information
        dev_title = QLabel("Developer / المطور")
        dev_title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        dev_title.setStyleSheet("color: #4CAF50;")
        dev_title.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(dev_title)
        
        dev_name = QLabel("Ahmed Mostafa Ibrahim")
        dev_name.setFont(QFont("Segoe UI", 16, QFont.Bold))
        dev_name.setStyleSheet("color: #E0E0E0;")
        dev_name.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(dev_name)
        
        dev_brand = QLabel("Finovate – AHMED EG")
        dev_brand.setFont(QFont("Segoe UI", 12))
        dev_brand.setStyleSheet("color: #888;")
        dev_brand.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(dev_brand)
        
        # Contact info
        contact_frame = QFrame()
        contact_frame.setStyleSheet("background-color: #2D2D2D; border-radius: 8px; padding: 15px;")
        contact_layout = QVBoxLayout()
        contact_layout.setSpacing(10)
        
        email_label = QLabel("📧 Email: GOGOM8870@GMAIL.COM")
        email_label.setFont(QFont("Segoe UI", 11))
        email_label.setStyleSheet("color: #E0E0E0;")
        email_label.setAlignment(Qt.AlignCenter)
        email_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        contact_layout.addWidget(email_label)
        
        phone_label = QLabel("📱 Phone: 01225155329")
        phone_label.setFont(QFont("Segoe UI", 11))
        phone_label.setStyleSheet("color: #E0E0E0;")
        phone_label.setAlignment(Qt.AlignCenter)
        phone_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        contact_layout.addWidget(phone_label)
        
        contact_frame.setLayout(contact_layout)
        content_layout.addWidget(contact_frame)
        
        # Copyright
        copyright_label = QLabel("© 2025 Ahmed Mostafa Ibrahim — All Rights Reserved.")
        copyright_label.setFont(QFont("Segoe UI", 10))
        copyright_label.setStyleSheet("color: #666;")
        copyright_label.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(copyright_label)
        
        # Disclaimer
        disclaimer_frame = QFrame()
        disclaimer_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 152, 0, 0.1);
                border: 1px solid #FF9800;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        disclaimer_layout = QVBoxLayout()
        disclaimer_layout.setSpacing(10)
        
        disclaimer_title = QLabel("⚠️ إخلاء مسؤولية / Disclaimer")
        disclaimer_title.setFont(QFont("Segoe UI", 12, QFont.Bold))
        disclaimer_title.setStyleSheet("color: #FF9800;")
        disclaimer_title.setAlignment(Qt.AlignCenter)
        disclaimer_layout.addWidget(disclaimer_title)
        
        disclaimer_text = QLabel(
            "البرنامج أداة مساعدة في التحليل وإعداد القيود المحاسبية، ولا يُعد بديلًا عن المراجعة المهنية "
            "أو الاستشارة المحاسبية أو القانونية أو الضريبية. يجب على المستخدم مراجعة واعتماد القيود قبل "
            "تسجيلها نهائيًا، والتأكد من توافق المعالجة مع القوانين والمعايير المطبقة على منشأته.\n\n"
            "The program is an auxiliary tool for analysis and preparation of accounting entries, and does not "
            "replace professional review or accounting, legal, or tax consultation. Users must review and approve "
            "entries before final posting and ensure compliance with applicable laws and standards."
        )
        disclaimer_text.setFont(QFont("Segoe UI", 10))
        disclaimer_text.setStyleSheet("color: #BDBDBD;")
        disclaimer_text.setAlignment(Qt.AlignCenter)
        disclaimer_text.setWordWrap(True)
        disclaimer_layout.addWidget(disclaimer_text)
        
        disclaimer_frame.setLayout(disclaimer_layout)
        content_layout.addWidget(disclaimer_frame)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)
        btn_layout.setAlignment(Qt.AlignCenter)
        
        check_updates_btn = QPushButton("🔄 التحقق من التحديثات")
        check_updates_btn.setFixedHeight(45)
        check_updates_btn.setCursor(Qt.PointingHandCursor)
        check_updates_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 13px;
                font-weight: bold;
                padding: 0 25px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        check_updates_btn.clicked.connect(self.check_updates)
        btn_layout.addWidget(check_updates_btn)
        
        licenses_btn = QPushButton("📄 التراخيص")
        licenses_btn.setFixedHeight(45)
        licenses_btn.setCursor(Qt.PointingHandCursor)
        licenses_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 13px;
                font-weight: bold;
                padding: 0 25px;
            }
            QPushButton:hover {
                background-color: #45A049;
            }
        """)
        licenses_btn.clicked.connect(self.show_licenses)
        btn_layout.addWidget(licenses_btn)
        
        content_layout.addLayout(btn_layout)
        content_layout.addStretch()
        
        content_widget.setLayout(content_layout)
        scroll.setWidget(content_widget)
        
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)
    
    def check_updates(self):
        """Check for updates"""
        QMessageBox.information(
            self, "التحديثات",
            "أنت تستخدم أحدث إصدار\nVersion 1.0.0"
        )
    
    def show_licenses(self):
        """Show licenses"""
        QMessageBox.information(
            self, "التراخيص",
            "Finovate Journal AI\n"
            "© 2025 Ahmed Mostafa Ibrahim\n\n"
            "جميع الحقوق محفوظة.\nAll Rights Reserved."
        )
