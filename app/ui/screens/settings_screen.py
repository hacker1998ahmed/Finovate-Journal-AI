"""
Finovate Journal AI - Settings Screen
Copyright © 2025 Ahmed Mostafa Ibrahim — All Rights Reserved.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QGroupBox, QFormLayout, QLineEdit,
    QComboBox, QCheckBox, QSpinBox, QMessageBox, QTabWidget
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from app.config.settings import AppSettings
from app.utils.logger import get_logger

logger = get_logger(__name__)


class SettingsScreen(QWidget):
    """Application settings screen"""
    
    def __init__(self):
        super().__init__()
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # Title
        title_label = QLabel("⚙️ الإعدادات")
        title_label.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title_label.setStyleSheet("color: #4CAF50;")
        main_layout.addWidget(title_label)
        
        # Description
        desc_label = QLabel("تكوين إعدادات البرنامج")
        desc_label.setFont(QFont("Segoe UI", 11))
        desc_label.setStyleSheet("color: #888;")
        main_layout.addWidget(desc_label)
        
        # Tab widget
        tabs = QTabWidget()
        tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #3D3D3D;
                border-radius: 8px;
                background-color: #2D2D2D;
            }
            QTabBar::tab {
                background-color: #1E1E1E;
                color: #E0E0E0;
                padding: 10px 20px;
                border: none;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #4CAF50;
            }
            QTabBar::tab:hover {
                background-color: #3D3D3D;
            }
        """)
        
        # General settings tab
        general_tab = self.create_general_settings()
        tabs.addTab(general_tab, "📋 عام")
        
        # Accounting settings tab
        accounting_tab = self.create_accounting_settings()
        tabs.addTab(accounting_tab, "📒 محاسبة")
        
        # Tax settings tab
        tax_tab = self.create_tax_settings()
        tabs.addTab(tax_tab, "💰 ضريبة")
        
        # AI settings tab
        ai_tab = self.create_ai_settings()
        tabs.addTab(ai_tab, "🤖 ذكاء اصطناعي")
        
        # Appearance settings tab
        appearance_tab = self.create_appearance_settings()
        tabs.addTab(appearance_tab, "🎨 مظهر")
        
        main_layout.addWidget(tabs)
        
        # Save button
        save_btn = QPushButton("💾 حفظ الإعدادات")
        save_btn.setFixedHeight(50)
        save_btn.setCursor(Qt.PointingHandCursor)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                padding: 10px 30px;
            }
            QPushButton:hover {
                background-color: #45A049;
            }
        """)
        save_btn.clicked.connect(self.save_settings)
        main_layout.addWidget(save_btn)
        
        main_layout.addStretch()
        self.setLayout(main_layout)
    
    def create_general_settings(self) -> QWidget:
        """Create general settings tab"""
        widget = QWidget()
        layout = QFormLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Company name
        self.company_name = QLineEdit()
        self.company_name.setText("شركة example")
        self.company_name.setStyleSheet(self.get_input_style())
        layout.addRow("اسم الشركة:", self.company_name)
        
        # Language
        self.language = QComboBox()
        self.language.addItems(["العربية", "English"])
        self.language.setStyleSheet(self.get_input_style())
        layout.addRow("اللغة:", self.language)
        
        # Currency
        self.currency = QComboBox()
        self.currency.addItems(["EGP - جنيه مصري", "USD - دولار أمريكي", "EUR - يورو", "SAR - ريال سعودي"])
        self.currency.setStyleSheet(self.get_input_style())
        layout.addRow("العملة:", self.currency)
        
        # Date format
        self.date_format = QComboBox()
        self.date_format.addItems(["DD/MM/YYYY", "MM/DD/YYYY", "YYYY-MM-DD"])
        self.date_format.setStyleSheet(self.get_input_style())
        layout.addRow("تنسيق التاريخ:", self.date_format)
        
        widget.setLayout(layout)
        return widget
    
    def create_accounting_settings(self) -> QWidget:
        """Create accounting settings tab"""
        widget = QWidget()
        layout = QFormLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Fiscal year start
        self.fiscal_year_start = QComboBox()
        self.fiscal_year_start.addItems(["يناير", "يوليو", "أبريل"])
        self.fiscal_year_start.setStyleSheet(self.get_input_style())
        layout.addRow("بداية السنة المالية:", self.fiscal_year_start)
        
        # Journal numbering
        self.journal_numbering = QComboBox()
        self.journal_numbering.addItems(["JE-YYYY-NNNNNN", "J-YYYY-NNNN", "SEQ-NNNNNN"])
        self.journal_numbering.setStyleSheet(self.get_input_style())
        layout.addRow("ترقيم القيود:", self.journal_numbering)
        
        # Allow negative balances
        self.allow_negative = QCheckBox("السماح بالأرصدة المدينة")
        self.allow_negative.setChecked(False)
        layout.addRow("", self.allow_negative)
        
        widget.setLayout(layout)
        return widget
    
    def create_tax_settings(self) -> QWidget:
        """Create tax settings tab"""
        widget = QWidget()
        layout = QFormLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # VAT enabled
        self.vat_enabled = QCheckBox("تفعيل ضريبة القيمة المضافة")
        self.vat_enabled.setChecked(True)
        layout.addRow("", self.vat_enabled)
        
        # VAT rate
        self.vat_rate = QSpinBox()
        self.vat_rate.setRange(0, 100)
        self.vat_rate.setValue(14)
        self.vat_rate.setSuffix("%")
        self.vat_rate.setStyleSheet(self.get_input_style())
        layout.addRow("نسبة الضريبة:", self.vat_rate)
        
        # Tax number
        self.tax_number = QLineEdit()
        self.tax_number.setPlaceholderText("أدخل الرقم الضريبي")
        self.tax_number.setStyleSheet(self.get_input_style())
        layout.addRow("الرقم الضريبي:", self.tax_number)
        
        widget.setLayout(layout)
        return widget
    
    def create_ai_settings(self) -> QWidget:
        """Create AI settings tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # AI mode
        mode_group = QGroupBox("وضع الذكاء الاصطناعي")
        mode_layout = QVBoxLayout()
        
        self.ai_mode = QComboBox()
        self.ai_mode.addItems(["معطل", "محلي (Local)", "عبر الإنترنت (Online)", "تلقائي (Auto)"])
        self.ai_mode.setStyleSheet(self.get_input_style())
        mode_layout.addWidget(self.ai_mode)
        
        mode_group.setLayout(mode_layout)
        layout.addWidget(mode_group)
        
        # API settings
        api_group = QGroupBox("إعدادات API (لـ Online Mode)")
        api_layout = QFormLayout()
        
        self.api_url = QLineEdit()
        self.api_url.setPlaceholderText("https://api.openai.com/v1")
        self.api_url.setStyleSheet(self.get_input_style())
        api_layout.addRow("رابط API:", self.api_url)
        
        self.api_key = QLineEdit()
        self.api_key.setPlaceholderText("sk-...")
        self.api_key.setEchoMode(QLineEdit.Password)
        self.api_key.setStyleSheet(self.get_input_style())
        api_layout.addRow("مفتاح API:", self.api_key)
        
        self.ai_model = QComboBox()
        self.ai_model.addItems(["gpt-4", "gpt-3.5-turbo", "claude-3", "llama-2"])
        self.ai_model.setStyleSheet(self.get_input_style())
        api_layout.addRow("النموذج:", self.ai_model)
        
        api_group.setLayout(api_layout)
        layout.addWidget(api_group)
        
        # Privacy notice
        privacy_label = QLabel(
            "⚠️ الخصوصية:\n"
            "عند استخدام الذكاء الاصطناعي عبر الإنترنت، قد يتم إرسال بيانات العمليات إلى مزود الخدمة.\n"
            "الوضع المحلي (Local) لا يرسل أي بيانات خارج الجهاز."
        )
        privacy_label.setWordWrap(True)
        privacy_label.setStyleSheet("color: #FF9800; padding: 10px; background-color: rgba(255, 152, 0, 0.1); border-radius: 6px;")
        layout.addWidget(privacy_label)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def create_appearance_settings(self) -> QWidget:
        """Create appearance settings tab"""
        widget = QWidget()
        layout = QFormLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Theme
        self.theme = QComboBox()
        self.theme.addItems(["Dark (داكن)", "Light (فاتح)"])
        self.theme.setStyleSheet(self.get_input_style())
        layout.addRow("السمة:", self.theme)
        
        # Font size
        self.font_size = QSpinBox()
        self.font_size.setRange(8, 24)
        self.font_size.setValue(10)
        self.font_size.setStyleSheet(self.get_input_style())
        layout.addRow("حجم الخط:", self.font_size)
        
        widget.setLayout(layout)
        return widget
    
    def get_input_style(self) -> str:
        """Get standard input style"""
        return """
            QLineEdit, QComboBox, QSpinBox {
                background-color: #1E1E1E;
                color: #E0E0E0;
                border: 1px solid #3D3D3D;
                border-radius: 6px;
                padding: 8px;
            }
            QLineEdit:focus, QComboBox:focus, QSpinBox:focus {
                border: 1px solid #4CAF50;
            }
        """
    
    def save_settings(self):
        """Save settings"""
        try:
            # TODO: Save to database/settings file
            QMessageBox.information(
                self, "نجاح",
                "تم حفظ الإعدادات بنجاح\n(سيتم التطبيق الكامل في التحديث القادم)"
            )
            logger.info("Settings saved")
        except Exception as e:
            logger.error(f"Error saving settings: {e}")
            QMessageBox.critical(
                self, "خطأ",
                f"حدث خطأ أثناء حفظ الإعدادات:\n{str(e)}"
            )
