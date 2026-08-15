"""
Finovate Journal AI - Dashboard Widget
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QFrame, QScrollArea, QPushButton
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class DashboardWidget(QWidget):
    """Dashboard widget showing key metrics and recent activity"""
    
    def __init__(self):
        super().__init__()
        
        self._setup_ui()
        
    def _setup_ui(self):
        """Setup dashboard UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("📊 لوحة التحكم / Dashboard")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setStyleSheet("color: #2c3e50; padding: 10px;")
        layout.addWidget(title)
        
        # Scrollable content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("border: none; background-color: transparent;")
        
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(20)
        
        # Metrics grid
        metrics_frame = self._create_metrics_grid()
        scroll_layout.addWidget(metrics_frame)
        
        # Recent entries section
        recent_frame = self._create_recent_entries_section()
        scroll_layout.addWidget(recent_frame)
        
        # Alerts section
        alerts_frame = self._create_alerts_section()
        scroll_layout.addWidget(alerts_frame)
        
        scroll_area.setWidget(scroll_content)
        layout.addWidget(scroll_area)
        
    def _create_metrics_grid(self) -> QFrame:
        """Create metrics cards grid"""
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        
        layout = QGridLayout(frame)
        layout.setSpacing(15)
        
        # Metric cards
        metrics = [
            ("📝 إجمالي القيود / Total Entries", "0", "#3498db"),
            ("📅 قيود اليوم / Today's Entries", "0", "#2ecc71"),
            ("💰 إجمالي المدين / Total Debit", "0.00 EGP", "#e74c3c"),
            ("💵 إجمالي الدائن / Total Credit", "0.00 EGP", "#f39c12"),
            ("👥 العملاء / Customers", "0", "#9b59b6"),
            ("🏢 الموردون / Suppliers", "0", "#1abc9c"),
            ("📦 رصيد الصندوق / Cash Balance", "0.00 EGP", "#34495e"),
            ("🏦 أرصدة البنوك / Bank Balances", "0.00 EGP", "#7f8c8d"),
        ]
        
        row = 0
        col = 0
        for i, (title, value, color) in enumerate(metrics):
            card = self._create_metric_card(title, value, color)
            layout.addWidget(card, row, col)
            
            col += 1
            if col > 3:
                col = 0
                row += 1
        
        return frame
    
    def _create_metric_card(self, title: str, value: str, color: str) -> QFrame:
        """Create a single metric card"""
        card = QFrame()
        card.setMinimumHeight(100)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {color}15;
                border-left: 4px solid {color};
                border-radius: 8px;
                padding: 10px;
            }}
        """)
        
        layout = QVBoxLayout(card)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 11))
        title_label.setStyleSheet("color: #7f8c8d;")
        title_label.setWordWrap(True)
        layout.addWidget(title_label)
        
        value_label = QLabel(value)
        value_label.setFont(QFont("Arial", 16, QFont.Bold))
        value_label.setStyleSheet(f"color: {color};")
        layout.addWidget(value_label)
        
        layout.addStretch()
        
        return card
    
    def _create_recent_entries_section(self) -> QFrame:
        """Create recent journal entries section"""
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        
        layout = QVBoxLayout(frame)
        
        title = QLabel("📋 آخر القيود / Recent Entries")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setStyleSheet("color: #2c3e50;")
        layout.addWidget(title)
        
        # Placeholder for recent entries table
        placeholder = QLabel("لا توجد قيود حديثة / No recent entries")
        placeholder.setAlignment(Qt.AlignCenter)
        placeholder.setStyleSheet("color: #95a5a6; padding: 30px;")
        layout.addWidget(placeholder)
        
        return frame
    
    def _create_alerts_section(self) -> QFrame:
        """Create alerts section"""
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        
        layout = QVBoxLayout(frame)
        
        title = QLabel("⚠️ تنبيهات / Alerts")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setStyleSheet("color: #2c3e50;")
        layout.addWidget(title)
        
        # Placeholder for alerts
        placeholder = QLabel("لا توجد تنبيهات / No alerts")
        placeholder.setAlignment(Qt.AlignCenter)
        placeholder.setStyleSheet("color: #95a5a6; padding: 20px;")
        layout.addWidget(placeholder)
        
        return frame
    
    def refresh_data(self):
        """Refresh dashboard data from database"""
        # TODO: Implement data loading from database
        pass
