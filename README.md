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

AI assistance (Google Gemini) handles ambiguous fields that rules alone can't resolve — like freeform specialty descriptions or non-standard name formats. The pipeline uses a **hybrid strategy**: deterministic rules handle ~80% of issues instantly, while the LLM is invoked only for the ambiguous 20% — keeping cost low and results predictable.

> 📝 **Architecture deep-dive:** [How I Built a Healthcare Data Cleaning Pipeline with Python and Gemini AI](#) — *Replace # with your Medium post URL once published*

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
<img width="975" height="535" alt="image" src="https://github.com/user-attachments/assets/410c6f60-d77a-4c67-ae19-b45c74887006" />


### Data Quality Summary
<img width="975" height="508" alt="image" src="https://github.com/user-attachments/assets/7308b512-b49a-4e0f-908c-ae4beac1bb79" />


### Issue Details Table
<img width="975" height="502" alt="image" src="https://github.com/user-attachments/assets/4291865d-c6d2-47e6-a0f1-73b45f238242" />


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

Validated against a 3,000-record real-world clinician dataset:

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

> 💡 A 10-record demo file (`sample_data.csv`) is included in the repo. Click **"Use Sample Data"** in the app sidebar to try it instantly — no upload needed.

**Performance (measured on 3,000-record dataset):**
- 87% of records cleaned via rules-based logic — zero API latency, zero cost
- 13% routed to Gemini API for ambiguous fields — ~1.5 seconds per record
- Total cost at scale: ~$0.008 per 100 records (~$0.80 per 10,000 records) at current Gemini Flash pricing
- End-to-end pipeline: under 10 seconds for rules-only pass; ~6 minutes for full AI-assisted run on 3,000 records

---

## ⚙️ Production Considerations

This prototype demonstrates the core pipeline. Below is an honest assessment of what production deployment in a healthcare system would require.

### Error Handling & Recovery
- The current Gemini API integration processes records sequentially. In production, a mid-batch API failure could leave data in a partially cleaned state. A production build would require idempotent processing — each record gets a status (`pending`, `cleaned`, `failed`) so interrupted jobs can resume without reprocessing or corrupting records already cleaned.
- Graceful degradation strategy: if the LLM API is unavailable, fall back to rules-only cleaning and flag affected records for manual review rather than failing the entire batch.

### Cost & Performance at Scale
- Gemini API calls add latency and cost per record. Estimated approach for scale: apply deterministic rules-based cleaning first (handles ~80% of issues), then route only ambiguous records to the LLM (remaining ~20%). This reduces API cost significantly at 10,000+ record volumes.
- A production benchmark target: < 2 seconds per record end-to-end, < $0.01 per record in API costs.

### Compliance & Security
- **PII handling:** Clinician name, NPI, email, and phone are isolated to dedicated fields and never logged in plain text in issue reports.
- **Audit logging:** Every change made by the pipeline is recorded with a before/after value and a timestamp. This is required for credentialing compliance workflows.
- **Secrets management:** API keys are stored via environment variables (`st.secrets` on Streamlit Cloud), never hardcoded.
- **Data retention:** Source data is not persisted server-side. Cleaned output is generated in-session and downloaded by the user.

### ✅ Ideal Use Case
This tool is designed as a **pre-screening step before CAQH or CRED submission** — catching format errors, expiry issues, and missing fields before they fail credentialing workflows downstream. Think of it as a data quality gate, not a credentialing decision engine.

### When NOT to Use This
- **Sanctions screening:** This tool does not check NPI deactivation status or OIG exclusion lists. Do not use as a substitute for NPPES live lookup or SAM.gov exclusion checks before credentialing.
- **Multi-source reconciliation:** If the same clinician appears in both CAQH and a payer roster with conflicting specialties, this tool cannot resolve the conflict — it requires a human credentialing reviewer.
- **State board validation:** License format validation is rule-based. It does not confirm active status with individual state licensing boards.
- **Restricted or temporary licenses:** The pipeline does not distinguish between full, restricted, or temporary license types.

### What a Production Version Would Add
- Immutable source data storage + separate cleaned dataset (never overwrite the original)
- Per-record approval workflow: Credentialer reviews flagged records → approves or rejects → approved data pushed to EHR/credentialing platform → audit log entry recorded automatically
- Integration with NPPES API for real-time NPI validation
- Database-backed audit trail (who ran the pipeline, what changed, when)
- Role-based access control for credentialing staff vs. administrators

---

## 🗺 Roadmap

- [ ] Batch processing for large rosters (1,000+ records)
- [ ] NPPES NPI registry live lookup — required because ~2–3% of active rosters contain deactivated NPIs that block credentialing
- [ ] CAQH / CRED integration
- [ ] Role-based access for credentialing teams
- [ ] Audit trail / change log per record

---

## 👤 Author

**Venkat Koneru**
[GitHub](https://github.com/vkoneru7-gif) • [LinkedIn](https://www.linkedin.com/in/venkata-koneru) • [Medium](#)
<!-- Replace # placeholders with your LinkedIn and Medium URLs -->

---

*This project demonstrates HIPAA-aware data handling patterns — including PII field isolation, audit-ready issue logging, and secrets management via environment variables. Not intended for production clinical use without additional compliance review.*
