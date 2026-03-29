# clinician-etl
AI-powered clinician data cleaning ETL pipeline
# 🏥 Clinician ETL — AI-Powered Healthcare Data Cleaning

> A lightweight prototype that solves a real problem in healthcare operations: messy clinician data.

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)](https://clinician-etl.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Google Gemini](https://img.shields.io/badge/AI-Google%20Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev)

---

## 🔍 The Problem

Healthcare organizations routinely receive clinician roster files from hospitals, staffing agencies, and credentialing bodies — and they're almost always messy. Names in wrong case, expired licenses buried in spreadsheets, malformed NPIs, inconsistent specialty labels, and bad phone formats are the norm, not the exception.

Manual cleaning is slow, error-prone, and doesn't scale.

---

## 💡 The Solution

**Clinician ETL** is an end-to-end data pipeline wrapped in a clean web dashboard. Upload a CSV of clinician records, click one button, and get back:

- A fully normalized, cleaned dataset
- A structured issue report flagging every data quality problem
- Downloadable outputs in CSV and Excel format

AI assistance (Google Gemini) handles ambiguous fields that rules alone can't resolve — like freeform specialty descriptions or non-standard name formats.

---

## ✨ Features

| Feature | Description |
|---|---|
| 📤 CSV / XLSX Upload | Drag-and-drop file ingestion |
| 🧪 Sample Data Mode | One-click demo with built-in messy dataset |
| 🤖 AI-Assisted Cleaning | Google Gemini normalizes ambiguous fields |
| 🔎 Issue Detection | Flags license expiry, bad NPIs, format errors, missing fields |
| 📊 Quality Metrics | Summary cards: total records, issue count, clean rate |
| 🔽 Filtered Issue View | Browse issues by field category |
| 📥 3 Download Options | Cleaned CSV, Issues CSV, Excel workbook with both sheets |

---

## 📸 Screenshots

<!-- Replace the placeholder paths below with your actual screenshot filenames after uploading to GitHub -->

### Dashboard Overview
![Dashboard Overview](screenshots/dashboard.png)

### Data Quality Summary
![Data Quality Summary](screenshots/quality_summary.png)

### Issue Details Table
![Issue Details](screenshots/issue_details.png)

---

## 🛠 Tech Stack

- **Frontend / UI** — [Streamlit](https://streamlit.io)
- **Data Processing** — [Pandas](https://pandas.pydata.org)
- **AI Cleaning** — [Google Gemini API](https://ai.google.dev) via `google-generativeai`
- **Excel Export** — [openpyxl](https://openpyxl.readthedocs.io)
- **Deployment** — [Streamlit Cloud](https://streamlit.io/cloud)

---

## 📁 Project Structure

```
clinician-etl/
├── app.py              # Streamlit dashboard UI
├── etl_engine.py       # Core ETL logic and data cleaning rules
├── sample_data.csv     # 10-row demo dataset with intentional data quality issues
├── requirements.txt    # Python dependencies
└── README.md
```

---

## 🚀 Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/vkoneru7-gif/clinician-etl.git
cd clinician-etl
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add your Gemini API key
Create a file at `.streamlit/secrets.toml`:
```toml
GEMINI_API_KEY = "your-api-key-here"
```

### 4. Run the app
```bash
streamlit run app.py
```

Then open `http://localhost:8501` in your browser.

---

## 📊 Sample Results

Running the pipeline on the included `sample_data.csv` (10 records) produces:

| Metric | Value |
|---|---|
| Total Records | 10 |
| Issues Found | 12 |
| Clean Records | 1 |
| Issue Rate | 90% |
| Issue Categories | license_expiry, license_number, specialty, npi |

---

## 🗺 Roadmap

- [ ] Batch processing for large rosters (1,000+ records)
- [ ] NPPES NPI registry live lookup
- [ ] CAQH / CRED integration
- [ ] Role-based access for credentialing teams
- [ ] Audit trail / change log per record

---

## 👤 Author

**Venkat Koneru**
[GitHub](https://github.com/vkoneru7-gif) • [LinkedIn](#) <!-- Replace # with your LinkedIn URL -->

---

*This project is a prototype demonstrating applied AI in healthcare data operations. Not intended for production clinical use.*
