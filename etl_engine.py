"""
Clinician ETL Engine
--------------------
Extract, Transform, and Load pipeline for clinician data.
Standardizes names, dates, phones, states, and flags data-quality issues.
"""

import re
import pandas as pd
from datetime import datetime

# ── US state mapping ──────────────────────────────────────────────────────────
STATE_MAP = {
    "alabama": "AL", "alaska": "AK", "arizona": "AZ", "arkansas": "AR",
    "california": "CA", "colorado": "CO", "connecticut": "CT", "delaware": "DE",
    "florida": "FL", "georgia": "GA", "hawaii": "HI", "idaho": "ID",
    "illinois": "IL", "indiana": "IN", "iowa": "IA", "kansas": "KS",
    "kentucky": "KY", "louisiana": "LA", "maine": "ME", "maryland": "MD",
    "massachusetts": "MA", "michigan": "MI", "minnesota": "MN",
    "mississippi": "MS", "missouri": "MO", "montana": "MT", "nebraska": "NE",
    "nevada": "NV", "new hampshire": "NH", "new jersey": "NJ",
    "new mexico": "NM", "new york": "NY", "north carolina": "NC",
    "north dakota": "ND", "ohio": "OH", "oklahoma": "OK", "oregon": "OR",
    "pennsylvania": "PA", "rhode island": "RI", "south carolina": "SC",
    "south dakota": "SD", "tennessee": "TN", "texas": "TX", "utah": "UT",
    "vermont": "VT", "virginia": "VA", "washington": "WA",
    "west virginia": "WV", "wisconsin": "WI", "wyoming": "WY",
    "district of columbia": "DC",
}
# Also accept 2-letter abbreviations as-is
VALID_ABBREVS = set(STATE_MAP.values())

# ── Credential suffixes to strip from names ───────────────────────────────────
CREDENTIAL_PATTERNS = [
    r"\bm\.?\s?d\.?\b",   # MD, M.D., M D
    r"\bd\.?\s?o\.?\b",   # DO, D.O.
    r"\bph\.?\s?d\.?\b",  # PhD, Ph.D.
    r"\bnp\b",            # NP
    r"\bpa\b",            # PA
    r"\brn\b",            # RN
]


# ═══════════════════════════════════════════════════════════════════════════════
# Individual transform functions
# ═══════════════════════════════════════════════════════════════════════════════

def clean_name(raw: str) -> tuple[str, str]:
    """Return (cleaned_name, credentials_found)."""
    if pd.isna(raw) or not str(raw).strip():
        return ("", "")

    name = str(raw).strip()

    # Strip leading "Dr." / "DR" etc.
    name = re.sub(r"^dr\.?\s*", "", name, flags=re.IGNORECASE).strip()

    # Extract credentials
    found_creds: list[str] = []
    for pat in CREDENTIAL_PATTERNS:
        match = re.search(pat, name, re.IGNORECASE)
        if match:
            found_creds.append(match.group().upper().replace(" ", "").replace(".", ""))
            name = re.sub(pat, "", name, flags=re.IGNORECASE)

    # Collapse whitespace and title-case
    name = re.sub(r"\s+", " ", name).strip().title()

    credentials = ", ".join(found_creds) if found_creds else ""
    return (name, credentials)


def standardize_state(raw: str) -> str:
    """Convert state name / abbreviation to 2-letter code."""
    if pd.isna(raw) or not str(raw).strip():
        return ""
    val = str(raw).strip()
    upper = val.upper()
    if upper in VALID_ABBREVS:
        return upper
    lookup = STATE_MAP.get(val.lower(), "")
    return lookup if lookup else upper  # Keep original if unmapped


def parse_expiry(raw: str) -> str:
    """Normalize expiry date to YYYY-MM-DD or flag."""
    if pd.isna(raw) or not str(raw).strip():
        return ""
    val = str(raw).strip().lower()
    if val == "expired":
        return "EXPIRED"

    for fmt in ("%Y-%m-%d", "%m/%Y", "%m/%d/%Y", "%d/%m/%Y", "%Y/%m/%d"):
        try:
            dt = datetime.strptime(val, fmt)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue
    return str(raw).strip()  # Return as-is if unparseable


def format_phone(raw: str) -> str:
    """Strip to digits and format as (XXX) XXX-XXXX."""
    if pd.isna(raw) or not str(raw).strip():
        return ""
    digits = re.sub(r"\D", "", str(raw))
    if digits.startswith("1") and len(digits) == 11:
        digits = digits[1:]
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    return str(raw).strip()  # Return original if unexpected length


def validate_npi(raw) -> tuple[str, bool]:
    """Return (npi_string, is_valid). Valid = exactly 10 digits."""
    if pd.isna(raw) or str(raw).strip() == "":
        return ("", False)
    npi = str(int(float(raw))) if isinstance(raw, float) else str(raw).strip()
    is_valid = bool(re.fullmatch(r"\d{10}", npi))
    return (npi, is_valid)


def validate_email(raw: str) -> tuple[str, bool]:
    """Return (lowered_email, is_valid)."""
    if pd.isna(raw) or not str(raw).strip():
        return ("", False)
    email = str(raw).strip().lower()
    is_valid = bool(re.fullmatch(r"[^@\s]+@[^@\s]+\.[a-z]{2,}", email))
    return (email, is_valid)


def standardize_status(raw: str) -> str:
    """Normalize status to Active / Inactive / Pending."""
    if pd.isna(raw) or not str(raw).strip():
        return ""
    return str(raw).strip().capitalize()


def standardize_specialty(raw: str) -> str:
    """Title-case the specialty."""
    if pd.isna(raw) or not str(raw).strip():
        return ""
    return str(raw).strip().title()


# ═══════════════════════════════════════════════════════════════════════════════
# Pipeline
# ═══════════════════════════════════════════════════════════════════════════════

def run_pipeline(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Run the full ETL pipeline.

    Parameters
    ----------
    df : pd.DataFrame  — raw input dataframe

    Returns
    -------
    (cleaned_df, issues_df)
    """
    out = df.copy()
    issues: list[dict] = []

    today = datetime.today().strftime("%Y-%m-%d")

    # ── Name + credentials ────────────────────────────────────────────────
    name_results = out["clinician_name"].apply(clean_name)
    out["clinician_name"] = name_results.apply(lambda x: x[0])
    out["credentials"] = name_results.apply(lambda x: x[1])

    for idx, (name, _) in name_results.items():
        if not name:
            issues.append({"row": idx + 2, "field": "clinician_name",
                           "issue": "Missing clinician name"})

    # ── Specialty ─────────────────────────────────────────────────────────
    out["specialty"] = out["specialty"].apply(standardize_specialty)
    for idx, val in out["specialty"].items():
        if not val:
            issues.append({"row": idx + 2, "field": "specialty",
                           "issue": "Missing specialty"})

    # ── License number ────────────────────────────────────────────────────
    for idx, val in out["license_number"].items():
        if pd.isna(val) or str(val).strip() == "":
            issues.append({"row": idx + 2, "field": "license_number",
                           "issue": "Missing license number"})

    # ── State ─────────────────────────────────────────────────────────────
    out["license_state"] = out["license_state"].apply(standardize_state)
    for idx, val in out["license_state"].items():
        if not val:
            issues.append({"row": idx + 2, "field": "license_state",
                           "issue": "Missing license state"})

    # ── Expiry ────────────────────────────────────────────────────────────
    out["license_expiry"] = out["license_expiry"].apply(parse_expiry)
    for idx, val in out["license_expiry"].items():
        if val == "EXPIRED":
            issues.append({"row": idx + 2, "field": "license_expiry",
                           "issue": "License marked as expired"})
        elif not val:
            issues.append({"row": idx + 2, "field": "license_expiry",
                           "issue": "Missing license expiry"})
        elif val < today:
            issues.append({"row": idx + 2, "field": "license_expiry",
                           "issue": f"License expired on {val}"})

    # ── NPI ───────────────────────────────────────────────────────────────
    npi_results = out["npi"].apply(validate_npi)
    out["npi"] = npi_results.apply(lambda x: x[0])
    for idx, (npi, valid) in npi_results.items():
        if not npi:
            issues.append({"row": idx + 2, "field": "npi",
                           "issue": "Missing NPI"})
        elif not valid:
            issues.append({"row": idx + 2, "field": "npi",
                           "issue": f"Invalid NPI format: {npi}"})

    # ── Email ─────────────────────────────────────────────────────────────
    email_results = out["email"].apply(validate_email)
    out["email"] = email_results.apply(lambda x: x[0])
    for idx, (email, valid) in email_results.items():
        if not email:
            issues.append({"row": idx + 2, "field": "email",
                           "issue": "Missing email"})
        elif not valid:
            issues.append({"row": idx + 2, "field": "email",
                           "issue": f"Invalid email format: {email}"})

    # ── Phone ─────────────────────────────────────────────────────────────
    out["phone"] = out["phone"].apply(format_phone)

    # ── Status ────────────────────────────────────────────────────────────
    out["status"] = out["status"].apply(standardize_status)

    # ── Reorder columns ──────────────────────────────────────────────────
    desired_order = [
        "id", "clinician_name", "credentials", "specialty",
        "license_number", "license_state", "license_expiry",
        "npi", "email", "phone", "status",
    ]
    existing = [c for c in desired_order if c in out.columns]
    extra = [c for c in out.columns if c not in desired_order]
    out = out[existing + extra]

    issues_df = pd.DataFrame(issues, columns=["row", "field", "issue"])

    return out, issues_df


def get_summary(issues_df: pd.DataFrame) -> dict:
    """Return summary statistics from the issues dataframe."""
    if issues_df.empty:
        return {"total_issues": 0, "by_field": {}, "by_issue_type": {}}

    return {
        "total_issues": len(issues_df),
        "by_field": issues_df["field"].value_counts().to_dict(),
        "by_issue_type": issues_df["issue"].apply(
            lambda x: x.split(":")[0] if ":" in x else x
        ).value_counts().to_dict(),
    }
