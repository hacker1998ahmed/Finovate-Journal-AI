# Finovate Journal AI

## AI-Powered Desktop Accounting & Journal Entry Assistant

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.12+-green.svg)
![License](https://img.shields.io/badge/license-proprietary-red.svg)

---

## 📖 Overview

**Finovate Journal AI** is a professional desktop accounting application designed to transform natural language accounting transactions into accurate journal entries. Built with Egyptian accounting standards in mind, it combines rule-based accounting engines with optional AI assistance.

### 🎯 Main Features

- **Smart Journal**: Write transactions in natural language (Arabic/English)
- **Hybrid Accounting Engine**: Rule-based + Optional AI
- **Chart of Accounts**: Fully customizable COA
- **Journal & Ledger**: Complete double-entry bookkeeping
- **Trial Balance**: Automatic balance verification
- **Financial Reports**: Income Statement, Balance Sheet
- **Customers & Suppliers**: Full subsidiary ledgers
- **Tax Engine**: VAT support with configurable rates
- **Multi-company**: Support multiple companies
- **Excel Import/Export**: Seamless data exchange
- **PDF Reports**: Professional report generation
- **Backup & Restore**: Data protection
- **Dark/Light Mode**: Modern UI themes
- **Bilingual**: Arabic (RTL) and English (LTR)

---

## 🏗️ Architecture

```
Finovate Journal AI
│
├── app/
│   ├── main.py              # Application entry point
│   ├── config/              # Configuration management
│   ├── database/            # Database connection & migrations
│   ├── models/              # SQLAlchemy ORM models
│   ├── repositories/        # Data access layer
│   ├── services/            # Business logic layer
│   ├── accounting/          # Accounting engine & rules
│   ├── ai/                  # AI providers abstraction
│   ├── nlp/                 # Natural language processing
│   ├── reports/             # Report generation
│   ├── imports/             # Data import handlers
│   ├── exports/             # Data export handlers
│   ├── security/            # Authentication & authorization
│   ├── ui/                  # PySide6 user interface
│   └── utils/               # Utility functions
│
├── assets/                  # Icons, images, resources
├── templates/               # PDF & report templates
├── reports/                 # Generated reports
├── tests/                   # Unit & integration tests
├── migrations/              # Database migrations
├── data/                    # Application data
├── logs/                    # Application logs
├── i18n/                    # Internationalization files
├── requirements.txt         # Python dependencies
├── README.md               # This file
└── build/                   # Build artifacts
```

---

## 💻 Installation

### Prerequisites

- Python 3.12 or higher
- Windows 10/11 (recommended)
- 4GB RAM minimum
- 500MB free disk space

### Setup Steps

1. **Clone or download the project**

```bash
cd finovate_journal_ai
```

2. **Create virtual environment**

```bash
python -m venv venv
```

3. **Activate virtual environment**

```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. **Install dependencies**

```bash
pip install -r requirements.txt
```

5. **Run the application**

```bash
python -m app.main
```

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Database
DATABASE_URL=sqlite:///data/finovate.db

# AI Provider (optional)
AI_PROVIDER=disabled
# Options: disabled, openai, openrouter, ollama, lmstudio

# OpenAI Compatible (if using online AI)
OPENAI_API_KEY=your_api_key_here
OPENAI_BASE_URL=https://api.openai.com/v1

# Ollama (if using local AI)
OLLAMA_BASE_URL=http://localhost:11434

# LM Studio (if using local AI)
LMSTUDIO_BASE_URL=http://localhost:1234

# Application
APP_ENV=development
LOG_LEVEL=INFO
```

### Settings Panel

Access settings from the main menu:
- Company information
- Fiscal year configuration
- Tax rates and accounts
- AI provider settings
- Backup preferences
- Appearance (Dark/Light mode)
- Language selection

---

## 🤖 AI Providers

Finovate Journal AI supports multiple AI providers:

### Disabled (Offline Mode)
- Uses only rule-based engine
- No internet connection required
- Full accounting functionality

### OpenAI Compatible
- Supports OpenAI API
- Supports Azure OpenAI
- Supports other OpenAI-compatible APIs

### OpenRouter
- Access to multiple LLM models
- Pay-per-use pricing

### Ollama (Local)
- Run LLMs locally
- No data sent externally
- Requires Ollama installation

### LM Studio (Local)
- Run LLMs locally
- User-friendly interface
- Requires LM Studio installation

### AI Fallback Chain

```
Local AI (Ollama/LM Studio)
    ↓ (if unavailable)
Online AI (OpenAI/OpenRouter)
    ↓ (if unavailable)
Rule Engine (always available)
```

---

## 📊 Accounting Features

### Smart Journal

Write transactions in natural language:

**Arabic Examples:**
- "شراء بضاعة نقدًا بمبلغ 10000 جنيه"
- "دفعت إيجار المكتب 5000 من البنك"
- "استلمت من العميل أحمد 15000 نقدًا"

**English Examples:**
- "Purchased goods for cash 10000 EGP"
- "Paid office rent 5000 from bank"
- "Received from customer Ahmed 15000 cash"

### Confidence Score

The system calculates confidence based on:
- Amount clarity
- Transaction type identification
- Account matching accuracy
- Payment method detection
- Tax detection
- Validation success

**Confidence Levels:**
- 90–100% = Very High
- 75–89% = High
- 50–74% = Medium
- < 50% = Needs Review

### Chart of Accounts

Pre-configured Egyptian COA structure:
```
1 Assets
  11 Current Assets
    1101 Cash
    1102 Bank
    1103 Customers
    1104 Inventory
2 Liabilities
  21 Suppliers
3 Equity
4 Revenue
  41 Sales
5 Expenses
  51 Purchases
  52 Rent
  53 Salaries
```

### Tax Engine

- Configurable tax rates
- Input VAT tracking
- Output VAT tracking
- Tax-inclusive/exclusive pricing
- Tax reports

---

## 📁 Data Management

### Excel Import/Export

**Import:**
- Chart of Accounts
- Customers
- Suppliers
- Journal Entries
- Items

**Export:**
- Journal
- Ledger
- Trial Balance
- Financial Statements
- Customer/Supplier Lists

### PDF Reports

Professional PDF generation with:
- Company logo
- Report headers
- Formatted tables
- Totals and subtotals
- Date ranges
- Footer with developer info

### Backup & Restore

**Manual Backup:**
- One-click backup creation
- Includes database and attachments

**Automatic Backup:**
- Daily/Weekly/Monthly schedules
- Configurable retention

**Restore:**
- Select backup file
- Warning before restore
- Data integrity check

---

## 🔐 Security

- Password hashing (bcrypt)
- Role-based access control
- Audit logging
- Session management
- SQL injection prevention
- Input validation
- API key encryption

### User Roles

| Role | Permissions |
|------|-------------|
| Administrator | Full access |
| Accountant | Create/edit entries, reports |
| Reviewer | Review and approve entries |
| Viewer | Read-only access |

---

## 🧪 Testing

Run tests with pytest:

```bash
pytest tests/ -v --cov=app
```

### Test Coverage

- Accounting engine
- Rule engine
- NLP parser
- Validation pipeline
- Database operations
- Excel import/export
- PDF generation
- UI components

---

## 🌍 Internationalization

Currently supported languages:
- 🇸🇦 Arabic (العربية) - RTL
- 🇬🇧 English

Adding new languages:
1. Create `i18n/{lang_code}.json`
2. Add translations
3. Update language selector

---

## 📝 Developer Information

**Developer:** Ahmed Mostafa Ibrahim

**Brand:** Finovate – AHMED EG

**Office:** Finovate – AHMED EG

**Email:** [GOGOM8870@GMAIL.COM](mailto:GOGOM8870@GMAIL.COM)

**Phone:** 01225155329

**Copyright:** © 2025 Ahmed Mostafa Ibrahim — All Rights Reserved.

---

## ⚠️ Disclaimer

> This software is an assistive tool for analyzing and preparing accounting journal entries. It does not replace professional review, accounting consultation, legal advice, or tax consultation. Users must review and approve entries before final posting and ensure compliance with applicable laws and standards for their organization.

---

## 📄 License

Proprietary Software - All Rights Reserved

© 2025 Ahmed Mostafa Ibrahim

---

## 🔄 Version History

### Version 1.0.0 (Initial Release)

**Core Features:**
- Dashboard with KPIs
- Smart Journal (Arabic/English)
- Manual Journal Entry
- Chart of Accounts
- Journal & Ledger
- Trial Balance
- Customers & Suppliers
- Tax Engine
- Excel Import/Export
- PDF Reports
- Backup & Restore
- Settings & Configuration
- Dark/Light Mode
- Bilingual Support (Arabic/English)

---

## 🆘 Support

For support and inquiries:
- Email: GOGOM8870@GMAIL.COM
- Phone: 01225155329

---

## 🚀 Future Roadmap

- [ ] E-Invoicing (ETA Egypt)
- [ ] Cloud Sync
- [ ] Mobile App
- [ ] Web Dashboard
- [ ] Multi-user Server
- [ ] PostgreSQL Support
- [ ] REST API
- [ ] OCR for Receipts
- [ ] Bank Integration
- [ ] Advanced Inventory
- [ ] Payroll System
- [ ] Budget Management
- [ ] Fixed Assets Module
