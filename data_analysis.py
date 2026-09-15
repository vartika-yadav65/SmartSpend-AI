import pandas as pd
import numpy as np


def clean_data(df):

    data = df.copy()

    if "Amount" in data.columns:

        data["Amount"] = pd.to_numeric(
            data["Amount"],
            errors="coerce"
        )

    if "Date" in data.columns:

        data["Date"] = pd.to_datetime(
            data["Date"],
            errors="coerce"
        )

    data = data.dropna(
        subset=["Amount"]
    )

    return data


def total_spending(df):

    data = clean_data(df)

    if data.empty:
        return 0.0

    return round(
        float(data["Amount"].sum()),
        2
    )


def average_expense(df):

    data = clean_data(df)

    if data.empty:
        return 0.0

    return round(
        float(data["Amount"].mean()),
        2
    )


def category_totals(df):

    data = clean_data(df)

    if data.empty:
        return {}

    if "Category" not in data.columns:
        return {}

    result = (
        data
        .groupby("Category")["Amount"]
        .sum()
        .sort_values(
            ascending=False
        )
    )

    return result.to_dict()


def monthly_totals(df):

    data = clean_data(df)

    if data.empty:
        return {}

    if "Date" not in data.columns:
        return {}

    data = data.dropna(
        subset=["Date"]
    )

    result = (
        data
        .groupby(
            data["Date"].dt.to_period("M")
        )["Amount"]
        .sum()
    )

    result.index = (
        result.index.astype(str)
    )

    return result.to_dict()


def payment_method_totals(df):

    data = clean_data(df)

    if data.empty:
        return {}

    if "Payment_Method" not in data.columns:
        return {}

    result = (
        data
        .groupby(
            "Payment_Method"
        )["Amount"]
        .sum()
        .sort_values(
            ascending=False
        )
    )

    return result.to_dict()