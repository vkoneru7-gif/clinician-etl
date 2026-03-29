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
<img width="975" height="535" alt="image" src="https://github.com/user-attachments/assets/118263a3-396a-4ba3-aca5-7c5365a170ba" />


### Data Quality Summary
<img width="975" height="508" alt="image" src="https://github.com/user-attachments/assets/d6b8224f-b440-46e4-a45f-88b1e0280879" />


### Issue Details Table
<img width="975" height="502" alt="image" src="https://github.com/user-attachments/assets/fb00069c-1a60-4335-9171-eb0b4f825a34" />


---

## 🛠 Tech Stack

- **Frontend / UI** — [Streamlit](https://streamlit.io)
- **Data Processing** — [Pandas](https://pandas.pydata.org)
- **AI Cleaning** — [Google Gemini API](https://ai.google.dev) via `google-generativeai`
- **Excel Export** — [openpyxl](https://openpyxl.readthedocs.io)
- **Deployment** — [Streamlit Cloud](https://streamlit.io/cloud) — deployed in under 5 minutes with zero-config secrets management via `st.secrets`

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

Validated at scale against a 3,000-record clinician dataset:

| Metric | Value |
|---|---|
| Total Records | 3,000 |
| Issues Found | 3,836 |
| Clean Records | 154 |
| Issue Rate | 95% |
| license_expiry issues | 2,783 |
| npi issues | 441 |
| license_number issues | 261 |
| license_state issues | 180 |
| specialty issues | 92 |
| email issues | 79 |

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
[GitHub](https://github.com/vkoneru7-gif) • [LinkedIn](www.linkedin.com/in/venkata-koneru) <!-- Replace # with your LinkedIn URL -->

---

*This project demonstrates HIPAA-aware data handling patterns — including PII field isolation, audit-ready issue logging, and secrets management via environment variables. Not intended for production clinical use without additional compliance review.*
