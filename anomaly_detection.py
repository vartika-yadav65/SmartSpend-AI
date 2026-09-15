import pandas as pd
import numpy as np


def detect_anomalies(df):

    if df is None or df.empty:
        return pd.DataFrame()

    data = df.copy()

    if "Amount" not in data.columns:
        return pd.DataFrame()

    data["Amount"] = pd.to_numeric(
        data["Amount"],
        errors="coerce"
    )

    data = data.dropna(
        subset=["Amount"]
    )

    if len(data) < 4:
        return pd.DataFrame()

    q1 = data["Amount"].quantile(
        0.25
    )

    q3 = data["Amount"].quantile(
        0.75
    )

    iqr = q3 - q1

    lower_limit = q1 - 1.5 * iqr
    upper_limit = q3 + 1.5 * iqr

    anomalies = data[
        (data["Amount"] < lower_limit)
        |
        (data["Amount"] > upper_limit)
    ].copy()

    return anomalies


def anomaly_count(df):

    anomalies = detect_anomalies(df)

    return len(anomalies)