"""Dashboard page for Finovate Journal AI."""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, 
    QGridLayout, QPushButton, QScrollArea
)
from PySide6.QtCore import Qt


class DashboardPage(QWidget):
    """Dashboard page with KPIs and charts."""

    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Page title
        title = QLabel("🏠 لوحة التحكم")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2E86AB; padding: 10px;")
        layout.addWidget(title)
        
        # Scrollable content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(15)
        
        # KPI Cards
        kpi_grid = QGridLayout()
        kpi_grid.setSpacing(15)
        
        kpis = [
            ("📊 إجمالي القيود", "0", "#4A90A4"),
            ("📅 قيود اليوم", "0", "#50C878"),
            ("💰 إجمالي المدين", "0 ج.م", "#E74C3C"),
            ("💳 إجمالي الدائن", "0 ج.م", "#3498DB"),
            ("👥 عدد العملاء", "0", "#9B59B6"),
            ("🏢 عدد الموردين", "0", "#F39C12"),
            ("📦 رصيد الصندوق", "0 ج.م", "#1ABC9C"),
            ("🏦 أرصدة البنوك", "0 ج.م", "#34495E"),
        ]
        
        for i, (title_text, value, color) in enumerate(kpis):
            card = self._create_kpi_card(title_text, value, color)
            row = i // 4
            col = i % 4
            kpi_grid.addWidget(card, row, col)
        
        content_layout.addLayout(kpi_grid)
        
        # Recent entries section
        recent_frame = QFrame()
        recent_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        recent_layout = QVBoxLayout(recent_frame)
        
        recent_title = QLabel("📝 آخر القيود")
        recent_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")
        recent_layout.addWidget(recent_title)
        
        no_entries_label = QLabel("لا توجد قيود حديثة")
        no_entries_label.setStyleSheet("color: #999; padding: 20px;")
        no_entries_label.setAlignment(Qt.AlignCenter)
        recent_layout.addWidget(no_entries_label)
        
        content_layout.addWidget(recent_frame)
        
        # Alerts section
        alerts_frame = QFrame()
        alerts_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        alerts_layout = QVBoxLayout(alerts_frame)
        
        alerts_title = QLabel("⚠️ تنبيهات محاسبية")
        alerts_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")
        alerts_layout.addWidget(alerts_title)
        
        no_alerts_label = QLabel("لا توجد تنبيهات حالية")
        no_alerts_label.setStyleSheet("color: #999; padding: 20px;")
        no_alerts_label.setAlignment(Qt.AlignCenter)
        alerts_layout.addWidget(no_alerts_label)
        
        content_layout.addWidget(alerts_frame)
        content_layout.addStretch()
        
        scroll.setWidget(content_widget)
        layout.addWidget(scroll)
    
    def _create_kpi_card(self, title: str, value: str, color: str) -> QFrame:
        """Create a KPI card widget."""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border-radius: 10px;
                padding: 15px;
                border-left: 4px solid {color};
            }}
        """)
        
        layout = QVBoxLayout(card)
        layout.setSpacing(5)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("color: #666; font-size: 13px;")
        layout.addWidget(title_label)
        
        value_label = QLabel(value)
        value_label.setStyleSheet(f"color: {color}; font-size: 24px; font-weight: bold;")
        layout.addWidget(value_label)
        
        return card
