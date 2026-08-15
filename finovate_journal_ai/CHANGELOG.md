# CHANGELOG

All notable changes to **Finovate Journal AI** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-01-01

### Added

#### Core
- Initial release of Finovate Journal AI
- Python 3.12+ support
- PySide6 desktop application
- SQLite database with SQLAlchemy ORM
- Modular architecture with separation of concerns

#### Accounting Engine
- Hybrid accounting engine (Rule-based + Optional AI)
- Double-entry bookkeeping system
- Chart of Accounts with hierarchical structure
- Journal Entry creation and management
- Journal Lines with debit/credit validation
- Automatic journal numbering (JE-YYYY-NNNNNN)
- Entry status workflow (Draft → Reviewed → Posted)
- Decimal-based financial calculations (no float)

#### Smart Journal
- Natural language processing for Arabic and English
- Transaction type detection
- Amount extraction with currency detection
- Account matching from Chart of Accounts
- Payment method identification
- Confidence score calculation
- Ambiguity detection and user prompts
- Rule-based transaction classification

#### Rule Engine
- Pre-configured accounting rules:
  - Cash purchases
  - Credit purchases
  - Cash sales
  - Credit sales
  - Customer collections
  - Supplier payments
  - Rent payments
  - Salary payments
  - Fixed asset purchases
- Extensible rule system
- Priority-based rule matching

#### Tax Engine
- Configurable tax rates
- VAT support (default 14%)
- Input VAT tracking
- Output VAT tracking
- Tax-inclusive pricing support
- Tax-exclusive pricing support
- Separate tax accounts configuration

#### Reports
- Journal report
- Ledger report per account
- Trial Balance with balance verification
- Income Statement (Profit & Loss)
- Balance Sheet
- Customer statement
- Supplier statement
- PDF export for all reports
- Excel export for all reports

#### Customers & Suppliers
- Customer management with opening balances
- Supplier management with opening balances
- Credit limit tracking
- Tax number support
- Contact information
- Account statements

#### Cash & Banks
- Multiple cash accounts
- Multiple bank accounts
- Opening balances
- Deposits and withdrawals
- Transfer between accounts

#### Data Management
- Excel import for:
  - Chart of Accounts
  - Customers
  - Suppliers
  - Journal entries
- Excel export for all major reports
- Manual backup creation
- Automatic backup scheduling (Daily/Weekly/Monthly)
- Restore from backup files

#### AI Integration
- AI Provider abstraction layer
- Support for multiple providers:
  - Disabled (Offline mode)
  - OpenAI Compatible
  - OpenRouter
  - Ollama (Local)
  - LM Studio (Local)
- AI fallback chain
- Structured JSON output from AI
- AI suggestion review interface
- Privacy controls for AI data sharing

#### User Interface
- Modern PySide6 interface
- Dashboard with KPIs:
  - Total journal entries
  - Today's entries
  - Total debit/credit
  - Customer/supplier counts
  - Cash and bank balances
  - Approximate net profit
  - Recent entries
  - Alerts and notifications
- Professional sidebar navigation
- Smart Journal screen with large input area
- Manual journal entry form
- Chart of Accounts tree view
- Journal listing with filters
- Ledger view per account
- Trial Balance table
- Settings panel
- About dialog with developer info
- Dark mode support
- Light mode support
- RTL support for Arabic
- LTR support for English
- Responsive layouts
- Loading indicators
- Error dialogs
- Success notifications

#### Security
- User authentication with bcrypt password hashing
- Role-based access control:
  - Administrator
  - Accountant
  - Reviewer
  - Viewer
- Audit logging for all critical operations
- Session management
- SQL injection prevention
- Input validation with Pydantic
- API key encryption

#### Internationalization
- Arabic language support (RTL)
- English language support (LTR)
- Translation system with JSON files
- Currency formatting (EGP default)
- Date format configuration

#### Multi-Company Support
- Company creation and management
- Separate data per company
- Company-specific settings
- Fiscal year management per company

#### Logging
- Application logging
- Error logging
- AI request logging
- Audit logging
- Log rotation
- Sensitive data filtering from logs

#### Testing
- Unit tests for accounting engine
- Tests for rule engine
- NLP parser tests
- Validation pipeline tests
- Database operation tests
- Excel import/export tests
- PDF generation tests

#### Documentation
- Comprehensive README
- Developer documentation
- User guide structure
- API documentation
- Installation instructions

### Technical Details

#### Dependencies
- PySide6 >= 6.6.0
- SQLAlchemy >= 2.0.23
- Pydantic >= 2.5.0
- openpyxl >= 3.1.2
- pandas >= 2.1.3
- reportlab >= 4.0.7
- matplotlib >= 3.8.2
- pytest >= 7.4.3
- bcrypt >= 4.1.2
- httpx >= 0.25.2

#### Database Schema
- users
- companies
- fiscal_years
- accounts
- account_groups
- journal_entries
- journal_lines
- customers
- suppliers
- cash_accounts
- bank_accounts
- invoices (foundation)
- invoice_lines (foundation)
- items (foundation)
- taxes
- cost_centers (foundation)
- projects (foundation)
- attachments (foundation)
- ai_requests
- audit_logs
- settings

### Known Limitations

- Inventory module is foundation only (basic item support)
- Invoicing module is foundation only
- Projects and Cost Centers are foundation only
- Advanced analytics planned for future versions
- E-Invoicing (ETA Egypt) not yet implemented
- Cloud sync not yet implemented
- Mobile app not yet implemented
- Web dashboard not yet implemented
- PostgreSQL support planned for future
- REST API planned for future
- OCR for receipts planned for future
- Bank integration planned for future
- Payroll system planned for future

### Developer Information

**Developer:** Ahmed Mostafa Ibrahim  
**Brand:** Finovate – AHMED EG  
**Email:** GOGOM8870@GMAIL.COM  
**Phone:** 01225155329  
**Copyright:** © 2025 Ahmed Mostafa Ibrahim — All Rights Reserved.

---

## [Unreleased]

### Planned Features
- E-Invoicing integration (Egyptian Tax Authority)
- Advanced inventory management
- Complete invoicing system
- Project accounting
- Cost center accounting
- Budget management
- Fixed assets module
- Payroll system
- Bank reconciliation
- OCR for receipts and invoices
- Cloud synchronization
- Mobile application
- Web dashboard
- REST API
- PostgreSQL support
- Multi-user server mode
- Advanced analytics and dashboards
- Cash flow statements
- Financial ratios analysis
- Comparative reports
- Custom report builder
