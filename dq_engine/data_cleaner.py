import pandas as pd
import numpy as np
import re

def preprocess_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans up raw dataset before validation.
    Converts null-like strings to NaN, trims spaces,
    normalizes date columns, and standardizes string casing.
    """
    df = df.copy()

    # --- 1. Convert null-like strings to np.nan ---
    null_like = [
        "null", "none", "nan", "na", "n/a", "", "-", "--", "not available", "missing"
    ]
    df = df.replace(to_replace=r"^\s*$", value=np.nan, regex=True)  # empty strings
    df = df.replace(to_replace=r"(?i)^(null|none|nan|na|n/a|missing|--|-)$", value=np.nan, regex=True)

    # --- 2. Trim spaces from string columns ---
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype(str).str.strip()

    # --- 3. Normalize text casing for categorical fields like kyc_type or kyc_mode ---
    text_like_cols = [c for c in df.columns if any(x in c.lower() for x in ['type', 'mode', 'status', 'category'])]
    for col in text_like_cols:
        df[col] = df[col].str.lower()

    # --- 4. Convert date-like columns to proper datetime ---
    date_like_cols = [c for c in df.columns if 'date' in c.lower() or 'expiry' in c.lower()]
    for col in date_like_cols:
        df[col] = pd.to_datetime(df[col], errors='coerce',dayfirst=True)

    # --- 5. Drop duplicates if any ---
    df = df.drop_duplicates()

    return df
