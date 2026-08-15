# Finovate Journal AI

## Professional Desktop Accounting & AI Journal Entry Assistant

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.12+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

**Finovate Journal AI** is a professional desktop accounting application for Windows that transforms natural language accounting entries into accurate journal entries. Built with Python, PySide6, and SQLite.

---

## 🌟 Features

### Core Accounting
- ✅ **Smart Journal**: Write entries in natural language (Arabic/English)
- ✅ **Manual Journal**: Traditional double-entry bookkeeping
- ✅ **Chart of Accounts**: Hierarchical account structure
- ✅ **Journal Ledger**: Complete transaction history
- ✅ **General Ledger**: Account-wise transaction details
- ✅ **Trial Balance**: Automated balance verification
- ✅ **Tax Engine**: VAT support with configurable rates
- ✅ **Multi-Company**: Manage multiple companies separately
- ✅ **Fiscal Years**: Open/close accounting periods

### AI-Powered
- ✅ **NLP Parser**: Arabic & English natural language processing
- ✅ **Confidence Score**: Reliability indicator for AI suggestions
- ✅ **Hybrid Engine**: Rules + AI with validation layer
- ✅ **Multiple Providers**: OpenAI, Ollama, LM Studio, Local
- ✅ **Offline Mode**: Works without internet connectivity

### Reports & Export
- ✅ **Financial Reports**: Income Statement, Balance Sheet
- ✅ **PDF Export**: Professional report generation
- ✅ **Excel Import/Export**: Bulk data operations
- ✅ **Charts & Analytics**: Visual financial insights

### Security & Compliance
- ✅ **Role-Based Access**: Admin, Accountant, Reviewer, Viewer
- ✅ **Audit Trail**: Complete change tracking
- ✅ **Data Encryption**: Secure credential storage
- ✅ **Backup & Restore**: Automated data protection

---

## 🚀 Installation

### Prerequisites
- Python 3.12 or higher
- Windows 10/11 (Linux/Mac supported with minor adjustments)

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

### Build Executable

```bash
# Build standalone executable
pyinstaller --name "Finovate Journal AI" --windowed --icon=assets/icon.ico app/main.py
```

---

## 📖 Usage

### Smart Journal Example

Write naturally:
```
شراء بضاعة نقدًا بمبلغ 10000 جنيه
```

Or in English:
```
Purchased goods for cash 10000 EGP
```

The system will:
1. Parse the transaction
2. Identify accounts (Dr Purchases, Cr Cash)
3. Calculate tax if applicable
4. Show confidence score
5. Require user approval before posting

### Manual Journal

Traditional double-entry with:
- Debit/Credit validation
- Account selection from Chart of Accounts
- Cost centers & projects
- Attachments support

---

## 🏗️ Architecture

```
FinovateJournalAI/
├── app/
│   ├── accounting/      # Rules engine, validation
│   ├── ai/              # AI providers, prompts
│   ├── config/          # Settings, constants
│   ├── database/        # SQLAlchemy models, sessions
│   ├── models/          # Pydantic schemas
│   ├── nlp/             # Natural language parser
│   ├── reports/         # PDF, Excel generators
│   ├── ui/              # PySide6 interfaces
│   └── utils/           # Helpers, logging
├── assets/              # Icons, images
├── backups/             # Database backups
├── data/                # SQLite databases
├── i18n/                # Translations (ar/en)
├── logs/                # Application logs
├── reports/             # Generated reports
├── templates/           # PDF templates
├── tests/               # Unit & integration tests
├── requirements.txt
├── README.md
└── main.py
```

---

## ⚙️ Configuration

### Developer Information

**Developer:** Ahmed Mostafa Ibrahim  
**Brand:** Finovate – AHMED EG  
**Email:** GOGOM8870@GMAIL.COM  
**Phone:** 01225155329  
**Copyright:** © 2025 Ahmed Mostafa Ibrahim — All Rights Reserved.

### Settings File

Edit `app/config/settings.py` to customize:
- Company defaults
- Tax rates
- AI providers
- Backup schedules
- UI preferences

---

## 🤖 AI Integration

### Supported Providers

1. **Offline Rules Engine** (Default)
2. **Local LLM** (Ollama, LM Studio)
3. **OpenAI Compatible**
4. **OpenRouter**

### Setup AI (Optional)

```python
# In Settings > AI Configuration
Provider: OpenAI
API Key: sk-...
Model: gpt-4o-mini
```

⚠️ **Privacy Note**: No data is sent to external AI services without explicit user consent.

---

## 📊 Sample Transactions

| Natural Language | Result |
|-----------------|--------|
| شراء بضاعة نقدًا 10000 | Dr Purchases, Cr Cash |
| بيع آجل للعميل أحمد 15000 | Dr Customer, Cr Sales |
| دفعت إيجار 5000 من البنك | Dr Rent Expense, Cr Bank |
| استلمت من عميل 8000 | Dr Cash, Cr Customer |
| شراء كمبيوتر 30000 شامل ضريبة | Dr Fixed Asset, Dr Input VAT, Cr Cash |

---

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=app --cov-report=html
```

---

## 🔒 Security

- Passwords hashed with bcrypt
- SQL injection prevention via SQLAlchemy ORM
- API keys stored in encrypted config
- Audit logs for all critical actions
- Role-based access control

---

## 📝 License

MIT License - See [LICENSE](LICENSE) file

---

## 📞 Support

For issues, questions, or contributions:
- Email: GOGOM8870@GMAIL.COM
- Phone: 01225155329

---

## ⚠️ Disclaimer

This software is an辅助 tool for accounting analysis and journal entry preparation. It does not replace professional accounting review, legal advice, or tax consultation. Users must review and approve all entries before final posting and ensure compliance with applicable laws and standards for their organization.

---

**Built with ❤️ by Finovate – AHMED EG**
