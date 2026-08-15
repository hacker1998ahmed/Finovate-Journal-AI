# Finovate Journal AI 🧾

**AI-Powered Accounting Journal Assistant**  
**مساعد القيود المحاسبية المدعوم بالذكاء الاصطناعي**

---

## © Copyright Notice

**© 2025 Ahmed Mostafa Ibrahim — All Rights Reserved.**

**Developer:** Ahmed Mostafa Ibrahim  
**Brand:** Finovate – AHMED EG  
**Email:** GOGOM8870@GMAIL.COM  
**Phone:** 01225155329

---

## Overview

Finovate Journal AI is a modern desktop accounting application built with Python and PySide6 (Qt). It features an intelligent NLP-based transaction parser that can understand natural language descriptions of accounting operations and automatically generate balanced journal entries.

## Features

### Core Features
- 🏠 **Dashboard** - Real-time financial statistics and quick actions
- 🧠 **Smart Journal Entry** - AI-powered natural language transaction parsing
- 📝 **Manual Journal Entry** - Traditional manual entry with balance validation
- 📚 **Chart of Accounts** - Hierarchical account structure management
- 📖 **Journal Ledger** - View and filter all recorded transactions
- ⚙️ **Settings** - Comprehensive application configuration
- ℹ️ **About** - Application information and developer details

### Smart Features
- **Arabic NLP Parser** - Understands Arabic accounting terminology
- **Automatic VAT Calculation** - Handles Egyptian VAT (14%) automatically
- **Balance Validation** - Ensures debits equal credits before saving
- **Confidence Scoring** - Shows confidence level for AI-generated entries
- **Multi-currency Support** - EGP, USD, EUR, SAR

### Technical Features
- Modern dark theme UI
- Responsive design
- SQLite database backend
- SQLAlchemy ORM
- Structured logging
- Modular architecture

---

## Project Structure

```
finovate_journal_ai/
├── app/
│   ├── main.py              # Application entry point
│   ├── config/              # Configuration and settings
│   ├── database/            # Database management
│   ├── models/              # SQLAlchemy models
│   ├── repositories/        # Data access layer
│   ├── services/            # Business logic
│   ├── accounting/          # Accounting rules engine
│   ├── nlp/                 # Natural language processing
│   ├── ai/                  # AI integration
│   ├── ui/                  # User interface
│   │   ├── main_window.py
│   │   └── screens/         # Screen components
│   ├── utils/               # Utilities and helpers
│   └── ...
├── data/                    # Application data
├── logs/                    # Log files
├── requirements.txt         # Dependencies
└── README.md
```

---

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Steps

1. Clone the repository:
```bash
git clone <repository-url>
cd finovate_journal_ai
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python -m app.main
```

---

## Usage

### Smart Journal Entry Example

Type a natural language description like:
- "شراء بضاعة نقدًا بمبلغ 10000 جنيه"
- "دفعت إيجار المكتب 5000 جنيه من البنك"
- "استلمت من العميل أحمد 15000 جنيه نقدًا"
- "اشتريت بضاعة من شركة النور بمبلغ 11400 شامل ضريبة القيمة المضافة"

The system will:
1. Parse the transaction type
2. Extract the amount and currency
3. Detect the payment method
4. Generate balanced journal entries
5. Calculate VAT if applicable
6. Show confidence score

### Manual Entry

For precise control, use the manual entry screen to:
- Select accounts from chart of accounts
- Enter debit/credit amounts
- Validate balance in real-time
- Add multiple line items

---

## Technology Stack

- **Language:** Python 3.8+
- **GUI Framework:** PySide6 (Qt for Python)
- **Database:** SQLite
- **ORM:** SQLAlchemy
- **Styling:** Qt Stylesheets (QSS)
- **Logging:** Python logging module

---

## Disclaimer ⚠️

**English:**  
The program is an auxiliary tool for analysis and preparation of accounting entries, and does not replace professional review or accounting, legal, or tax consultation. Users must review and approve entries before final posting and ensure compliance with applicable laws and standards.

**العربية:**  
البرنامج أداة مساعدة في التحليل وإعداد القيود المحاسبية، ولا يُعد بديلًا عن المراجعة المهنية أو الاستشارة المحاسبية أو القانونية أو الضريبية. يجب على المستخدم مراجعة واعتماد القيود قبل تسجيلها نهائيًا، والتأكد من توافق المعالجة مع القوانين والمعايير المطبقة على منشأته.

---

## License

**Proprietary Software - All Rights Reserved**

This software is proprietary and confidential. Unauthorized copying, distribution, modification, or use is strictly prohibited.

© 2025 Ahmed Mostafa Ibrahim - Finovate – AHMED EG

---

## Support

For support, please contact:
- **Email:** GOGOM8870@GMAIL.COM
- **Phone:** 01225155329

---

## Version

**Current Version:** 1.0.0  
**Release Date:** 2025

---

## Acknowledgments

Developed by Ahmed Mostafa Ibrahim under the Finovate brand.
