# Finovate Journal AI

## AI-Powered Desktop Accounting & Journal Entry Assistant

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.12+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

---

## 📋 Overview

**Finovate Journal AI** is a professional desktop accounting application for Windows that transforms natural language accounting transactions into journal entries ready for review and posting. It features a local accounting engine, chart of accounts, general journal, general ledger, trial balance, financial reports, Excel import/export, PDF generation, and optional AI components.

### Developer Information

- **Developer:** Ahmed Mostafa Ibrahim
- **Brand:** Finovate – AHMED EG
- **Office:** Finovate – AHMED EG
- **Email:** [GOGOM8870@GMAIL.COM](mailto:GOGOM8870@GMAIL.COM)
- **Phone:** 01225155329
- **Copyright:** © 2025 Ahmed Mostafa Ibrahim — All Rights Reserved.

---

## ✨ Features

### Core Accounting
- ✅ Chart of Accounts (Multi-level, customizable)
- ✅ General Journal (Manual & Smart)
- ✅ General Ledger
- ✅ Trial Balance
- ✅ Debit/Credit Validation
- ✅ Multi-company support
- ✅ Fiscal Year Management
- ✅ Cost Centers & Projects

### Smart Journal
- ✅ Natural Language Processing (Arabic & English)
- ✅ Transaction Type Detection
- ✅ Amount & Currency Extraction
- ✅ Account Matching
- ✅ Payment Method Detection
- ✅ Tax Detection (VAT)
- ✅ Confidence Scoring
- ✅ Ambiguity Detection
- ✅ Accounting Explanation

### AI Assistant
- ✅ Multiple AI Providers (OpenAI, OpenRouter, Ollama, LM Studio)
- ✅ Local AI Support (Offline)
- ✅ Hybrid Engine (Rules + AI)
- ✅ Privacy Controls
- ✅ Structured JSON Output

### Reports
- ✅ Journal Report
- ✅ Ledger Report
- ✅ Trial Balance
- ✅ Income Statement
- ✅ Balance Sheet
- ✅ Customer/Supplier Statements
- ✅ Cash/Bank Movements
- ✅ Expense Analysis
- ✅ Revenue Analysis

### Data Management
- ✅ Excel Import/Export
- ✅ PDF Generation (RTL Support)
- ✅ Automatic Backup
- ✅ Restore Backup
- ✅ Audit Logs
- ✅ Attachment Support

### Security & Access
- ✅ Role-Based Access Control
- ✅ Password Hashing
- ✅ Session Management
- ✅ Audit Trail
- ✅ Data Integrity Checks

### UI/UX
- ✅ Modern Professional Design
- ✅ Dark/Light Mode
- ✅ Arabic (RTL) & English (LTR)
- ✅ Responsive Dashboard
- ✅ Global Search
- ✅ Notifications
- ✅ Keyboard Navigation

---

## 🏗️ Architecture

```
FinovateJournalAI/
├── app/
│   ├── main.py              # Application entry point
│   ├── config/              # Configuration management
│   ├── database/            # Database connection & migrations
│   ├── models/              # SQLAlchemy models
│   ├── repositories/        # Data access layer
│   ├── services/            # Business logic layer
│   ├── accounting/          # Accounting engine & rules
│   ├── ai/                  # AI providers & integration
│   ├── nlp/                 # NLP parsers
│   ├── reports/             # Report generators
│   ├── imports/             # Import handlers
│   ├── exports/             # Export handlers
│   ├── security/            # Authentication & authorization
│   ├── ui/                  # PySide6 UI components
│   └── utils/               # Utilities & helpers
├── assets/                  # Icons, images, resources
├── templates/               # Report templates
├── reports/                 # Generated reports
├── tests/                   # Unit & integration tests
├── migrations/              # Database migrations
├── data/                    # Application data
├── logs/                    # Log files
├── i18n/                    # Translation files
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── CHANGELOG.md            # Version history
├── LICENSE                 # License file
└── build/                  # Build artifacts
```

---

## 🚀 Installation

### Prerequisites

- Python 3.12 or higher
- Windows 10/11 (recommended)
- pip package manager

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/finovate-journal-ai.git
cd finovate-journal-ai
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Download NLP Models (Optional for Arabic NLP)

```bash
python -m spacy download en_core_web_sm
```

### Step 5: Run the Application

```bash
python -m app.main
```

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Database
DATABASE_URL=sqlite:///data/finovate.db

# AI Provider (disabled, openai, openrouter, ollama, lmstudio)
AI_PROVIDER=disabled
AI_API_KEY=your_api_key_here
AI_API_URL=https://api.openai.com/v1
AI_MODEL=gpt-3.5-turbo
AI_TEMPERATURE=0.3

# Local AI (Ollama/LM Studio)
LOCAL_AI_URL=http://localhost:11434
LOCAL_AI_MODEL=llama2

# Application
APP_LANGUAGE=ar
APP_THEME=dark
BACKUP_ENABLED=true
BACKUP_PATH=backups/
```

### Settings UI

Access settings from the main menu to configure:
- Company Information
- Fiscal Year
- Tax Rates
- AI Provider
- Backup Schedule
- Appearance (Theme, Language, Font Size)

---

## 📖 Usage Guide

### First Run

On first launch, you will be prompted to:
1. Create a new company
2. Try the Demo company
3. Restore from backup

### Smart Journal

1. Navigate to **Smart Journal** from the sidebar
2. Enter a transaction in natural language:
   - Arabic: "شراء بضاعة نقدًا بمبلغ 10000 جنيه"
   - English: "Purchased goods for cash 10000 EGP"
3. Click **Analyze**
4. Review the suggested entry
5. Edit if needed
6. Click **Post Entry**

### Manual Journal

1. Navigate to **Manual Journal**
2. Enter debit and credit lines
3. Ensure debits equal credits
4. Add description and reference
5. Post the entry

### Chart of Accounts

1. Navigate to **Chart of Accounts**
2. View default accounts (Assets, Liabilities, Equity, Revenue, Expenses)
3. Add, edit, or deactivate accounts
4. Create parent-child relationships

### Reports

1. Navigate to **Reports**
2. Select report type
3. Set date range and filters
4. Preview, export to Excel or PDF

---

## 🤖 AI Integration

### Supported Providers

| Provider | Type | Offline | Setup |
|----------|------|---------|-------|
| Disabled | None | ✅ | Default |
| OpenAI | Cloud | ❌ | API Key required |
| OpenRouter | Cloud | ❌ | API Key required |
| Ollama | Local | ✅ | Install Ollama |
| LM Studio | Local | ✅ | Install LM Studio |

### Privacy

- AI is **disabled by default**
- No data is sent externally without explicit consent
- Local AI providers run entirely offline
- API keys are encrypted and never logged
- Database is never sent to AI providers

### Configuring AI

1. Go to **Settings → AI**
2. Select provider
3. Enter API key (if cloud provider)
4. Set endpoint URL (if local provider)
5. Test connection
6. Save settings

---

## 📊 Accounting Engine

### Rule Engine

The hybrid accounting engine uses predefined rules:

| Transaction Type | Debit | Credit |
|-----------------|-------|--------|
| Cash Purchase | Purchases | Cash |
| Credit Purchase | Purchases | Suppliers |
| Cash Sale | Cash | Sales |
| Credit Sale | Customers | Sales |
| Receive from Customer | Cash/Bank | Customer |
| Pay Supplier | Supplier | Cash/Bank |
| Pay Rent | Rent Expense | Cash/Bank |
| Pay Salaries | Salaries Expense | Cash/Bank |
| Buy Fixed Asset | Fixed Asset | Cash/Bank/Supplier |

### Validation Pipeline

Every journal entry passes through:

1. Input Validation
2. Account Validation
3. Amount Validation
4. Tax Validation
5. Debit/Credit Balance Check
6. Business Rules
7. User Review
8. Posting

### Decimal Precision

All financial calculations use Python's `Decimal` type to avoid floating-point errors.

---

## 🗄️ Database

### Technology

- SQLite (local)
- SQLAlchemy ORM
- Alembic Migrations

### Main Tables

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
- invoices
- invoice_lines
- taxes
- cost_centers
- projects
- attachments
- ai_requests
- audit_logs
- settings

### Multi-Company

Each company has isolated:
- Chart of Accounts
- Journal Entries
- Customers & Suppliers
- Reports
- Tax Settings

---

## 🔐 Security

### Access Control

| Role | Permissions |
|------|-------------|
| Administrator | Full access |
| Accountant | Create/Edit entries, Reports |
| Reviewer | Review & Post entries |
| Viewer | Read-only |

### Data Protection

- Password hashing with bcrypt
- Encrypted API keys
- SQL injection prevention (parameterized queries)
- Input validation on all forms
- Audit logging of sensitive operations
- No sensitive data in logs

---

## 📝 Testing

### Run Tests

```bash
pytest tests/ -v --cov=app
```

### Test Coverage

Tests cover:
- Account creation
- Journal entry validation
- Debit/Credit balance
- Tax calculations
- Decimal precision
- Ledger accuracy
- Trial balance
- Excel import/export
- PDF generation
- AI parsing
- Rule engine
- Backup/Restore
- Permissions

---

## 📦 Building Executable

### Using PyInstaller

```bash
pyinstaller --name="Finovate Journal AI" --windowed --icon=assets/icons/app.ico app/main.py
```

### Portable Mode

Build a portable version that runs without installation:

```bash
pyinstaller --name="Finovate Journal AI Portable" --windowed --onefile app/main.py
```

---

## 🌍 Localization

### Supported Languages

- Arabic (العربية) - RTL
- English

### Adding Languages

Translation files are in `i18n/`:
- `ar.json` - Arabic
- `en.json` - English

To add a new language:
1. Create `i18n/xx.json`
2. Translate all keys
3. Add language to settings

---

## 📄 Disclaimer

> This software is an assistive tool for analyzing and preparing accounting journal entries. It is not a substitute for professional review, accounting consultation, legal advice, or tax consultation. Users must review and approve entries before final posting and ensure compliance with applicable laws, regulations, and standards for their organization.

---

## 🔄 Version History

### v1.0.0 (2025)

Initial Release:
- Dashboard with KPIs
- Smart Journal (NLP)
- Manual Journal
- Chart of Accounts
- General Journal
- General Ledger
- Trial Balance
- Customers & Suppliers
- Tax Engine (VAT)
- AI Provider Abstraction
- Excel Import/Export
- PDF Reports
- Backup & Restore
- Multi-language (AR/EN)
- Dark/Light Theme
- Role-Based Access
- Audit Logs

---

## 📞 Support

For issues, questions, or contributions:

- **Email:** [GOGOM8870@GMAIL.COM](mailto:GOGOM8870@GMAIL.COM)
- **Phone:** 01225155329
- **GitHub Issues:** [Create an issue](https://github.com/yourusername/finovate-journal-ai/issues)

---

## 📜 License

MIT License - See [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Developed by **Ahmed Mostafa Ibrahim**
- Brand: **Finovate – AHMED EG**
- © 2025 All Rights Reserved

---

## 🎯 Roadmap

### Phase 2 (Future Updates)
- [ ] Advanced Inventory Management
- [ ] E-Invoicing (Egyptian Tax Authority)
- [ ] Cloud Sync
- [ ] Mobile App
- [ ] Web Dashboard
- [ ] PostgreSQL Support
- [ ] REST API
- [ ] OCR for Receipts
- [ ] Bank Integration
- [ ] POS Module
- [ ] Payroll System
- [ ] Budget Management
- [ ] Advanced Analytics

---

**Built with ❤️ for the Accounting Community**
