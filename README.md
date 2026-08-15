# Finovate Journal AI

## AI-Powered Desktop Accounting & Journal Entry Assistant

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.12+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

**Finovate Journal AI** is a professional desktop accounting application that transforms natural language descriptions into accurate journal entries. Built for Egyptian accounting standards with full Arabic/English support.

---

## 🌟 Features

### Core Accounting
- ✅ **Smart Journal** - Convert natural language to journal entries (Arabic & English)
- ✅ **Manual Journal Entry** - Traditional double-entry bookkeeping
- ✅ **Chart of Accounts** - Fully customizable account structure
- ✅ **General Ledger** - Complete transaction history per account
- ✅ **Trial Balance** - Automated balance verification
- ✅ **Multi-company Support** - Manage multiple entities
- ✅ **Fiscal Years** - Open, close, and carry forward balances

### Intelligent Processing
- 🧠 **Hybrid Accounting Engine**
  - Rule-based validation (offline)
  - NLP parser for Arabic/English
  - Optional AI assistant (OpenAI, Ollama, LM Studio)
  - Confidence scoring & ambiguity detection

### Financial Management
- 💰 **Cash & Bank Management**
- 👥 **Customers & Suppliers**
- 📊 **Financial Reports** (Income Statement, Balance Sheet)
- 🧾 **Invoice System** (Basic)
- 🏷️ **Tax Engine** - VAT support with configurable rates
- 📍 **Cost Centers & Projects**

### Data & Security
- 🔒 **Role-Based Access Control** (Admin, Accountant, Reviewer, Viewer)
- 📝 **Complete Audit Trail**
- 💾 **Automatic Backup & Restore**
- 🔐 **Password Hashing & Session Management**
- 🛡️ **Data Integrity Checks**

### Internationalization
- 🌍 **Bilingual Interface** - Arabic (RTL) & English (LTR)
- 💱 **Multi-Currency Ready** (EGP base, extensible)
- 📅 **Flexible Date Formats**

### Export & Import
- 📤 **Excel Export** - All reports and data
- 📥 **Excel Import** - Charts of accounts, customers, suppliers
- 📄 **PDF Reports** - Professional formatted documents

---

## 🚀 Installation

### Prerequisites
- Python 3.12 or higher
- Windows 10/11 (tested), Linux, macOS

### Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/finovate-journal-ai.git
cd finovate-journal-ai

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run the application
python -m app.main
```

---

## 📖 Usage

### First Launch
On first run, you'll be prompted to:
1. Create a new company
2. Try the demo company
3. Restore from backup

### Smart Journal Example

Type in natural language:
```
شراء بضاعة نقدًا بمبلغ 10000 جنيه
```
or
```
Paid office rent 5000 EGP from bank
```

The system will:
1. Parse the transaction
2. Identify accounts (Debit/Credit)
3. Extract amount and currency
4. Detect tax if applicable
5. Show confidence score
6. Allow review before posting

### Manual Journal Entry
Traditional double-entry interface with:
- Automatic journal numbering (JE-2026-000001)
- Debit/Credit validation
- Cost center assignment
- Project tracking

---

## ⚙️ Configuration

### AI Providers
Configure in Settings → AI:

| Provider | Use Case | Offline |
|----------|----------|---------|
| Disabled | No AI, rules only | ✅ |
| Ollama | Local LLM | ✅ |
| LM Studio | Local LLM | ✅ |
| OpenAI Compatible | Cloud AI | ❌ |

**Privacy Note:** No accounting data is sent to external AI providers without explicit user consent.

### Tax Configuration
Navigate to Settings → Tax to configure:
- Tax name and rate
- Input/Output tax accounts
- Effective dates
- Tax codes

### Backup Settings
- Manual backup: Tools → Create Backup
- Auto backup: Daily, Weekly, Monthly
- Backup includes: Database + attachments

---

## 🏗️ Architecture

```
FinovateJournalAI/
├── app/
│   ├── main.py              # Application entry point
│   ├── config/              # Settings & configuration
│   ├── database/            # SQLAlchemy models & DB init
│   ├── models/              # Pydantic models
│   ├── repositories/        # Data access layer
│   ├── services/            # Business logic
│   ├── accounting/          # Accounting engine & rules
│   ├── ai/                  # AI provider abstraction
│   ├── nlp/                 # Natural language parser
│   ├── reports/             # Report generators
│   ├── imports/             # Excel import handlers
│   ├── exports/             # Excel/PDF export
│   ├── security/            # Auth & permissions
│   ├── ui/                  # PySide6 interfaces
│   └── utils/               # Helpers & utilities
├── assets/                  # Images, icons
├── templates/               # PDF templates
├── i18n/                    # Translations (ar.json, en.json)
├── data/                    # SQLite database (gitignored)
├── logs/                    # Application logs (gitignored)
├── backups/                 # Backup files (gitignored)
├── reports/                 # Generated reports (gitignored)
├── tests/                   # Unit & integration tests
└── requirements.txt
```

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test module
pytest tests/test_accounting_engine.py
```

---

## 📄 Developer Information

**Developer:** Ahmed Mostafa Ibrahim  
**Brand:** Finovate – AHMED EG  
**Email:** [GOGOM8870@GMAIL.COM](mailto:GOGOM8870@GMAIL.COM)  
**Phone:** 01225155329  

**Copyright:** © 2025 Ahmed Mostafa Ibrahim — All Rights Reserved.

---

## ⚠️ Disclaimer

This software is an辅助 tool for accounting analysis and journal entry preparation. It does not replace professional accounting review, legal advice, or tax consultation. Users must review and approve all entries before final posting and ensure compliance with applicable laws and standards for their organization.

---

## 📝 License

MIT License - See LICENSE file for details.

---

## 🔄 Version History

See [CHANGELOG.md](CHANGELOG.md) for version history and updates.

---

## 🛠️ Building Executable

```bash
# Install PyInstaller
pip install pyinstaller

# Build Windows executable
pyinstaller --onefile --windowed --name "Finovate Journal AI" --icon=assets/icon.ico app/main.py

# Output: dist/Finovate Journal AI.exe
```

For portable mode, use `--onedir` instead of `--onefile`.

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:
1. Fork the repository
2. Create a feature branch
3. Write tests for new features
4. Ensure all tests pass
5. Submit a pull request

---

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Email: GOGOM8870@GMAIL.COM
- Phone: 01225155329

---

**Built with ❤️ for the accounting community**
