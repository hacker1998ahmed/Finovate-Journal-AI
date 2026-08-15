"""
Dashboard Page - Main overview with key metrics and charts
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QFrame, QScrollArea, QPushButton
)
from PySide6.QtCore import Qt
from decimal import Decimal


class MetricCard(QFrame):
    """Card widget for displaying a metric."""
    
    def __init__(self, title: str, value: str, icon: str = "📊", color: str = "#1976d2"):
        super().__init__()
        
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border-radius: 8px;
                padding: 20px;
                border-left: 4px solid {color};
            }}
            QFrame:hover {{
                background-color: #f5f5f5;
            }}
        """)
        
        layout = QVBoxLayout(self)
        
        # Icon and title row
        header_layout = QHBoxLayout()
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 24px;")
        header_layout.addWidget(icon_label)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 12px; color: #666; font-weight: bold;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        # Value
        value_label = QLabel(value)
        value_label.setStyleSheet(f"font-size: 28px; font-weight: bold; color: {color};")
        layout.addWidget(value_label)
    
    def update_value(self, value: str):
        """Update the displayed value."""
        for i in range(self.layout().count()):
            widget = self.layout().itemAt(i).widget()
            if isinstance(widget, QLabel) and i == 1:
                widget.setText(value)
                break


class DashboardPage(QWidget):
    """Main dashboard with accounting metrics."""
    
    def __init__(self):
        super().__init__()
        
        self.setStyleSheet("background-color: #f8f9fa;")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Title
        title_label = QLabel("🏠 لوحة التحكم الرئيسية")
        title_label.setFont(title_label.font())
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")
        layout.addWidget(title_label)
        
        # Scrollable content area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("border: none; background-color: transparent;")
        
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(20)
        
        # Metrics grid
        metrics_frame = QFrame()
        metrics_layout = QGridLayout(metrics_frame)
        metrics_layout.setSpacing(15)
        
        # Create metric cards
        self.metrics = {
            "total_entries": MetricCard("إجمالي القيود", "0", "📝", "#1976d2"),
            "today_entries": MetricCard("قيود اليوم", "0", "📅", "#4caf50"),
            "total_debit": MetricCard("إجمالي المدين", "0 ج.م", "💰", "#ff9800"),
            "total_credit": MetricCard("إجمالي الدائن", "0 ج.م", "💵", "#2196f3"),
            "customers": MetricCard("عدد العملاء", "0", "👥", "#9c27b0"),
            "suppliers": MetricCard("عدد الموردين", "0", "🏢", "#00bcd4"),
            "cash_balance": MetricCard("رصيد الصندوق", "0 ج.م", "💳", "#4caf50"),
            "bank_balance": MetricCard("أرصدة البنوك", "0 ج.م", "🏦", "#3f51b5"),
        }
        
        # Add cards to grid (2 rows x 4 columns)
        positions = [
            (0, 0), (0, 1), (0, 2), (0, 3),
            (1, 0), (1, 1), (1, 2), (1, 3)
        ]
        
        for (row, col), (key, card) in zip(positions, self.metrics.items()):
            metrics_layout.addWidget(card, row, col)
        
        content_layout.addWidget(metrics_frame)
        
        # Recent entries section
        recent_frame = QFrame()
        recent_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                padding: 20px;
            }
        """)
        recent_layout = QVBoxLayout(recent_frame)
        
        recent_title = QLabel("📋 آخر القيود")
        recent_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")
        recent_layout.addWidget(recent_title)
        
        # Placeholder for recent entries table
        no_data_label = QLabel("لا توجد قيود حديثة")
        no_data_label.setStyleSheet("color: #999; font-size: 14px; padding: 20px;")
        no_data_label.setAlignment(Qt.AlignCenter)
        recent_layout.addWidget(no_data_label)
        
        content_layout.addWidget(recent_frame)
        
        # Alerts section
        alerts_frame = QFrame()
        alerts_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                padding: 20px;
            }
        """)
        alerts_layout = QVBoxLayout(alerts_frame)
        
        alerts_title = QLabel("⚠️ تنبيهات محاسبية")
        alerts_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")
        alerts_layout.addWidget(alerts_title)
        
        # Placeholder for alerts
        no_alerts_label = QLabel("لا توجد تنبيهات حالية")
        no_alerts_label.setStyleSheet("color: #999; font-size: 14px; padding: 20px;")
        no_alerts_label.setAlignment(Qt.AlignCenter)
        alerts_layout.addWidget(no_alerts_label)
        
        content_layout.addWidget(alerts_frame)
        
        content_layout.addStretch()
        
        scroll.setWidget(content_widget)
        layout.addWidget(scroll)
    
    def refresh_data(self):
        """Refresh dashboard data from database."""
        # TODO: Implement data loading from database
        pass
