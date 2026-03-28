"""
Clinician ETL — Streamlit App
------------------------------
Upload clinician data, run the ETL pipeline, review issues, download cleaned output.
"""

import io
import streamlit as st
import pandas as pd
from etl_engine import run_pipeline, get_summary

# ═══════════════════════════════════════════════════════════════════════════════
# Page config + custom CSS
# ═══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Clinician ETL Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

CUSTOM_CSS = """
<style>
/* ── Import Google Font ─────────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* ── Root variables ─────────────────────────────────────────────────────── */
:root {
    --bg-primary: #0f172a;
    --bg-secondary: #1e293b;
    --bg-card: #1e293b;
    --accent: #38bdf8;
    --accent-green: #34d399;
    --accent-amber: #fbbf24;
    --accent-red: #f87171;
    --text-primary: #f1f5f9;
    --text-secondary: #94a3b8;
    --border: #334155;
    --glass: rgba(30, 41, 59, 0.7);
}

/* ── Global ─────────────────────────────────────────────────────────────── */
html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Inter', sans-serif;
    color: var(--text-primary);
}

[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f172a 0%, #1a1a2e 50%, #16213e 100%);
}

[data-testid="stSidebar"] {
    background: var(--bg-secondary) !important;
    border-right: 1px solid var(--border);
}

[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 {
    color: var(--accent) !important;
}

/* ── Metric cards ───────────────────────────────────────────────────────── */
[data-testid="stMetric"] {
    background: var(--glass);
    backdrop-filter: blur(12px);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 16px 20px;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
[data-testid="stMetric"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(56, 189, 248, 0.15);
}
[data-testid="stMetricValue"] {
    color: var(--accent) !important;
    font-weight: 700 !important;
}

/* ── Buttons ────────────────────────────────────────────────────────────── */
.stButton > button {
    border-radius: 10px;
    font-weight: 600;
    transition: all 0.25s ease;
}
.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 15px rgba(56, 189, 248, 0.25);
}

/* ── Dataframes ─────────────────────────────────────────────────────────── */
[data-testid="stDataFrame"] {
    border-radius: 10px;
    overflow: hidden;
    border: 1px solid var(--border);
}

/* ── Expanders ──────────────────────────────────────────────────────────── */
[data-testid="stExpander"] {
    background: var(--glass);
    backdrop-filter: blur(8px);
    border: 1px solid var(--border);
    border-radius: 12px;
}

/* ── Divider tweaks ─────────────────────────────────────────────────────── */
hr {
    border-color: var(--border) !important;
}

/* ── Success / warning / error banners ──────────────────────────────────── */
.stAlert {
    border-radius: 10px;
}

/* ── Download buttons ───────────────────────────────────────────────────── */
.stDownloadButton > button {
    background: linear-gradient(135deg, #38bdf8, #818cf8) !important;
    color: white !important;
    border: none !important;
}
.stDownloadButton > button:hover {
    opacity: 0.9;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# Sidebar
# ═══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("## 🏥 Clinician ETL")
    st.markdown("---")

    st.markdown("### 📂 Data Source")
    uploaded_file = st.file_uploader(
        "Upload CSV or Excel file",
        type=["csv", "xlsx", "xls"],
        help="Upload your clinician data file for processing",
    )

    use_sample = st.button("📋 Use Sample Data", use_container_width=True)

    st.markdown("---")
    st.markdown("### ⚙️ Options")
    show_raw = st.checkbox("Show raw data preview", value=True)
    show_issues_detail = st.checkbox("Show detailed issue breakdown", value=True)

    st.markdown("---")
    st.markdown(
        "<div style='text-align:center; color: #64748b; font-size: 0.8rem;'>"
        "Clinician ETL v1.0<br>Built with Streamlit</div>",
        unsafe_allow_html=True,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# Load data into session state
# ═══════════════════════════════════════════════════════════════════════════════

if use_sample:
    st.session_state["raw_df"] = pd.read_csv("sample_data.csv")
    st.session_state.pop("cleaned_df", None)
    st.session_state.pop("issues_df", None)

if uploaded_file is not None:
    if uploaded_file.name.endswith((".xlsx", ".xls")):
        st.session_state["raw_df"] = pd.read_excel(uploaded_file)
    else:
        st.session_state["raw_df"] = pd.read_csv(uploaded_file)
    st.session_state.pop("cleaned_df", None)
    st.session_state.pop("issues_df", None)


# ═══════════════════════════════════════════════════════════════════════════════
# Main content
# ═══════════════════════════════════════════════════════════════════════════════

# ── Hero header ───────────────────────────────────────────────────────────────
st.markdown(
    """
    <div style="
        text-align: center;
        padding: 2rem 1rem 1rem;
    ">
        <h1 style="
            font-size: 2.4rem;
            font-weight: 700;
            background: linear-gradient(135deg, #38bdf8, #818cf8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.3rem;
        ">Clinician ETL Dashboard</h1>
        <p style="color: #94a3b8; font-size: 1.1rem;">
            Clean, standardize, and validate your clinician data in seconds.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")

# ── No data loaded yet ────────────────────────────────────────────────────────
if "raw_df" not in st.session_state:
    st.markdown(
        """
        <div style="
            text-align: center;
            padding: 4rem 2rem;
            background: rgba(30, 41, 59, 0.5);
            border: 2px dashed #334155;
            border-radius: 16px;
            margin: 2rem 0;
        ">
            <p style="font-size: 3rem; margin: 0;">📁</p>
            <h3 style="color: #94a3b8;">No data loaded</h3>
            <p style="color: #64748b;">
                Upload a CSV/Excel file from the sidebar or click
                <strong>"Use Sample Data"</strong> to get started.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()

raw_df = st.session_state["raw_df"]

# ── Raw data preview ─────────────────────────────────────────────────────────
if show_raw:
    with st.expander("📊 Raw Data Preview", expanded=False):
        st.dataframe(raw_df, use_container_width=True, height=300)
        st.caption(f"{len(raw_df)} rows × {len(raw_df.columns)} columns")

# ── Run ETL ───────────────────────────────────────────────────────────────────
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    run_etl = st.button(
        "🚀  Run ETL Pipeline",
        use_container_width=True,
        type="primary",
    )

if run_etl:
    with st.spinner("Running ETL pipeline…"):
        cleaned_df, issues_df = run_pipeline(raw_df)
        st.session_state["cleaned_df"] = cleaned_df
        st.session_state["issues_df"] = issues_df

# ── Results ───────────────────────────────────────────────────────────────────
if "cleaned_df" not in st.session_state:
    st.info("👆 Click **Run ETL Pipeline** to process the data.")
    st.stop()

cleaned_df = st.session_state["cleaned_df"]
issues_df = st.session_state["issues_df"]
summary = get_summary(issues_df)

st.markdown("---")

# ── Metric cards ──────────────────────────────────────────────────────────────
st.markdown("### 📈 Data Quality Summary")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Records", len(cleaned_df))
m2.metric("Issues Found", summary["total_issues"])
m3.metric(
    "Clean Records",
    len(cleaned_df) - issues_df["row"].nunique() if not issues_df.empty else len(cleaned_df),
)
m4.metric(
    "Issue Rate",
    f"{(issues_df['row'].nunique() / len(cleaned_df) * 100):.0f}%"
    if not issues_df.empty else "0%",
)

# ── Issues breakdown ─────────────────────────────────────────────────────────
if not issues_df.empty:
    st.markdown("### ⚠️ Data Quality Issues")

    if show_issues_detail and summary["by_field"]:
        cols = st.columns(min(len(summary["by_field"]), 5))
        field_icons = {
            "clinician_name": "👤",
            "specialty": "🩺",
            "license_number": "📄",
            "license_state": "🗺️",
            "license_expiry": "📅",
            "npi": "🔢",
            "email": "📧",
            "phone": "📱",
            "status": "🔘",
        }
        for i, (field, count) in enumerate(summary["by_field"].items()):
            icon = field_icons.get(field, "📌")
            cols[i % len(cols)].metric(f"{icon} {field}", count)

    with st.expander("🔍 Issue Details", expanded=True):
        # Filter
        fields_with_issues = ["All"] + sorted(issues_df["field"].unique().tolist())
        selected_field = st.selectbox("Filter by field", fields_with_issues)
        display_issues = (
            issues_df
            if selected_field == "All"
            else issues_df[issues_df["field"] == selected_field]
        )
        st.dataframe(display_issues, use_container_width=True, height=250)
else:
    st.success("✅ No data quality issues found! Your data looks great.")

# ── Cleaned data ──────────────────────────────────────────────────────────────
st.markdown("### ✅ Cleaned Data")
st.dataframe(cleaned_df, use_container_width=True, height=400)
st.caption(f"{len(cleaned_df)} rows × {len(cleaned_df.columns)} columns")

# ── Downloads ─────────────────────────────────────────────────────────────────
st.markdown("### 💾 Download Results")
dl1, dl2, dl3 = st.columns(3)

with dl1:
    csv_data = cleaned_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️  Download Cleaned CSV",
        data=csv_data,
        file_name="clinicians_cleaned.csv",
        mime="text/csv",
        use_container_width=True,
    )

with dl2:
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        cleaned_df.to_excel(writer, sheet_name="Cleaned", index=False)
        if not issues_df.empty:
            issues_df.to_excel(writer, sheet_name="Issues", index=False)
    st.download_button(
        "⬇️  Download Excel (with Issues)",
        data=buf.getvalue(),
        file_name="clinicians_cleaned.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
    )

with dl3:
    if not issues_df.empty:
        issues_csv = issues_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️  Download Issues CSV",
            data=issues_csv,
            file_name="clinicians_issues.csv",
            mime="text/csv",
            use_container_width=True,
        )
    else:
        st.markdown(
            "<div style='text-align:center; padding:0.8rem; color:#64748b;'>"
            "No issues to download</div>",
            unsafe_allow_html=True,
        )
