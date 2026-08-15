# Finovate Journal AI

**AI-Powered Desktop Accounting & Journal Entry Assistant**

## نظرة عامة | Overview

Finovate Journal AI هو تطبيق محاسبي ذكي لسطح المكتب يحول العمليات المحاسبية المكتوبة باللغة الطبيعية إلى قيود يومية محاسبية قابلة للمراجعة والاعتماد.

Finovate Journal AI is an intelligent desktop accounting application that converts natural language accounting transactions into reviewable and approvable journal entries.

## المميزات الرئيسية | Key Features

- 🧠 **القيد الذكي (Smart Journal)**: تحليل العمليات المحاسبية بالعربية والإنجليزية
- 📚 **دليل الحسابات (Chart of Accounts)**: هيكل حسابات كامل وقابل للتخصيص
- 📖 **دفتر اليومية (Journal)**: عرض وتدقيق القيود اليومية
- 📕 **دفتر الأستاذ (Ledger)**: متابعة حركة كل حساب
- ⚖️ **ميزان المراجعة (Trial Balance)**: التحقق من توازن الحسابات
- 💰 **العملاء والموردين (Customers & Suppliers)**: إدارة الأطراف
- 🏦 **الصندوق والبنوك (Cash & Banks)**: متابعة السيولة
- 📊 **التقارير المالية (Financial Reports)**: قائمة الدخل والميزانية
- 🤖 **مساعد الذكاء الاصطناعي (AI Assistant)**: دعم اختياري للتحليل المتقدم
- 📥📤 **استيراد وتصدير Excel**: تبادل البيانات بسهولة
- 📄 **تقارير PDF**: طباعة احترافية للتقارير
- 🔐 **الأمان والصلاحيات (Security & Roles)**: حماية البيانات
- 🌐 **ثنائي اللغة (Bilingual)**: العربية والإنجليزية مع دعم RTL/LTR
- 🌓 **الوضع المظلم/الفاتح (Dark/Light Mode)**: راحة بصرية

## المتطلبات التقنية | Technical Requirements

- Python 3.12+
- PySide6 (Qt for Python)
- SQLite + SQLAlchemy
- openpyxl, pandas (Excel)
- reportlab (PDF)
- matplotlib (Charts)

## التثبيت | Installation

```bash
# استنساخ المستودع | Clone the repository
git clone <repository-url>
cd FinovateJournalAI

# إنشاء بيئة افتراضية | Create virtual environment
python -m venv venv

# تفعيل البيئة | Activate environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# تثبيت المتطلبات | Install requirements
pip install -r requirements.txt
```

## التشغيل | Running

```bash
# تشغيل التطبيق | Run the application
python -m app.main
```

## البنية المعمارية | Architecture

```
FinovateJournalAI/
├── app/
│   ├── main.py              # نقطة الدخول الرئيسية
│   ├── accounting/          # محرك القواعد المحاسبية
│   ├── ai/                  # طبقة الذكاء الاصطناعي
│   ├── config/              # الإعدادات
│   ├── database/            # قاعدة البيانات
│   ├── models/              # نماذج البيانات
│   ├── nlp/                 # محلل اللغة الطبيعية
│   ├── ui/                  # واجهة المستخدم
│   ├── utils/               # أدوات مساعدة
│   └── security/            # الأمان والصلاحيات
├── assets/                   # الأصول (صور، أيقونات)
├── backups/                  # النسخ الاحتياطية
├── data/                     # قاعدة البيانات
├── i18n/                     # ملفات الترجمة
├── logs/                     # السجلات
├── reports/                  # التقارير المولدة
├── templates/                # قوالب PDF
├── tests/                    # الاختبارات
├── requirements.txt
├── README.md
└── .gitignore
```

## بيانات المطور | Developer Information

**المطور | Developer:** Ahmed Mostafa Ibrahim  
**العلامة التجارية | Brand:** Finovate – AHMED EG  
**المكتب | Office:** Finovate – AHMED EG  
**البريد الإلكتروني | Email:** GOGOM8870@GMAIL.COM  
**الهاتف | Phone:** 01225155329  

## الترخيص | License

© 2025 Ahmed Mostafa Ibrahim — All Rights Reserved.

## إخلاء المسؤولية | Disclaimer

البرنامج أداة مساعدة في التحليل وإعداد القيود المحاسبية، ولا يُعد بديلًا عن المراجعة المهنية أو الاستشارة المحاسبية أو القانونية أو الضريبية. يجب على المستخدم مراجعة واعتماد القيود قبل تسجيلها نهائيًا، والتأكد من توافق المعالجة مع القوانين والمعايير المطبقة على منشأته.

The software is an assistive tool for analyzing and preparing accounting entries, and is not a substitute for professional review or accounting, legal, or tax consultation. Users must review and approve entries before final posting and ensure compliance with applicable laws and standards.
