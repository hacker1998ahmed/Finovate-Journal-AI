# CHANGELOG

All notable changes to **Finovate Journal AI** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-01-01

### Added

#### Core Features
- Initial release of Finovate Journal AI v1.0.0
- Hybrid Accounting Engine (Rule Engine + NLP Parser + AI Assistant)
- Smart Journal for natural language transaction entry (Arabic & English)
- Manual Journal Entry with full validation
- Chart of Accounts with hierarchical structure
- Journal Book (دفتر اليومية)
- Ledger Book (دفتر الأستاذ)
- Trial Balance (ميزان المراجعة)
- Customer and Supplier Management
- Cash and Bank Accounts Management
- Tax Engine with configurable VAT rates
- Cost Centers and Projects (basic support)

#### User Interface
- Modern PySide6 Desktop Interface
- Dashboard with key metrics and charts
- Sidebar navigation with RTL/LTR support
- Dark Mode and Light Mode
- Bilingual support (Arabic/English)
- Global Search functionality
- Notification system

#### AI & NLP
- Arabic and English NLP Parser
- Confidence Score calculation
- Ambiguity detection and user guidance
- AI Provider abstraction layer (OpenAI, Ollama, LM Studio, OpenRouter)
- Local AI support (offline capability)
- Rule-based fallback when AI is unavailable

#### Reports & Export
- Excel Import/Export (openpyxl, pandas)
- PDF Report generation (reportlab)
- Journal, Ledger, and Trial Balance reports
- Basic Financial Statements (Income Statement, Balance Sheet)

#### Security & Data Integrity
- Role-Based Access Control (Admin, Accountant, Reviewer, Viewer)
- Password hashing (bcrypt)
- Audit Log for all critical operations
- Database transactions for data integrity
- Backup and Restore functionality
- Session management

#### Developer Information
- Developer: Ahmed Mostafa Ibrahim
- Brand: Finovate – AHMED EG
- Email: GOGOM8870@GMAIL.COM
- Phone: 01225155329

### Technical Stack
- Python 3.12+
- PySide6 (Qt for Python)
- SQLAlchemy (ORM)
- SQLite (Database)
- Pydantic (Data Validation)
- openpyxl, pandas (Excel)
- reportlab (PDF)
- matplotlib (Charts)
- pytest (Testing)

### Known Issues
- Advanced inventory management is in preliminary stage
- E-Invoice integration planned for future versions
- Cloud sync not yet implemented

---

## [Unreleased]

### Planned Features
- Advanced Inventory Management
- E-Invoice Integration (Egyptian Tax Authority)
- Cloud Sync capabilities
- Mobile App companion
- Web Dashboard
- Multi-user server mode
- PostgreSQL support
- REST API
- OCR for receipt scanning
- Bank Integration
- POS Module
- Payroll System
- CPA Practice Mode
- Accounting Training Mode with gamification

---

© 2025 Ahmed Mostafa Ibrahim — All Rights Reserved.
