# Changelog

All notable changes to **Finovate Journal AI** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-01-01

### Added

#### Core Features
- Initial release of Finovate Journal AI
- Desktop application with PySide6
- SQLite database with SQLAlchemy ORM
- Multi-company support
- Fiscal year management

#### Accounting Engine
- Chart of Accounts (multi-level hierarchy)
- General Journal (manual entry)
- Smart Journal (NLP-powered)
- General Ledger
- Trial Balance
- Debit/Credit validation
- Decimal precision for all financial calculations
- Tax engine (VAT support)
- Journal entry workflow (Draft → Reviewed → Posted)

#### Smart Journal
- Arabic and English NLP parsing
- Transaction type detection
- Amount and currency extraction
- Account matching
- Payment method detection
- Tax detection
- Confidence scoring (0-100%)
- Ambiguity detection
- Accounting explanation generation

#### AI Integration
- AI Provider abstraction layer
- OpenAI-compatible provider
- OpenRouter provider
- Ollama local provider
- LM Studio local provider
- Hybrid engine (Rules + AI)
- Privacy controls
- Offline mode support

#### Reports
- Journal report
- Ledger report
- Trial balance report
- Income statement
- Balance sheet
- Customer statements
- Supplier statements
- Cash movement report
- Bank movement report
- PDF export with RTL support
- Excel export

#### Data Management
- Excel import (accounts, customers, suppliers, entries)
- Excel export (all reports)
- Manual backup creation
- Automatic backup scheduling
- Restore from backup
- Attachment support for entries

#### Security
- User authentication with bcrypt password hashing
- Role-based access control (Admin, Accountant, Reviewer, Viewer)
- Audit logging
- Session management
- SQL injection prevention
- Input validation

#### UI/UX
- Modern professional design
- Dashboard with KPIs
- Sidebar navigation
- Dark/Light theme
- Arabic (RTL) and English (LTR) language support
- Global search
- Notifications system
- Keyboard navigation
- Responsive layouts

#### Localization
- Arabic translation
- English translation
- i18n JSON-based translation system

#### Developer Information
- Developer: Ahmed Mostafa Ibrahim
- Brand: Finovate – AHMED EG
- Email: GOGOM8870@GMAIL.COM
- Phone: 01225155329

### Technical
- Python 3.12+
- PySide6 for GUI
- SQLAlchemy 2.0+ for ORM
- Pydantic for data validation
- openpyxl for Excel
- ReportLab for PDF
- matplotlib for charts
- pytest for testing
- Alembic for migrations

### Changed
- N/A (Initial release)

### Deprecated
- N/A

### Removed
- N/A

### Fixed
- N/A (Initial release)

### Security
- Encrypted API key storage
- No sensitive data in logs
- Parameterized queries
- Password hashing
- Role-based permissions

---

## [Unreleased]

### Planned for Future Versions
- Advanced inventory management
- E-invoicing (Egyptian Tax Authority)
- Cloud synchronization
- Mobile application
- Web dashboard
- PostgreSQL support
- REST API
- OCR for receipts
- Bank integration
- POS module
- Payroll system
- Budget management
- Advanced analytics
- CPA practice mode
- Accounting training mode
