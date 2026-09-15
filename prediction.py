import pandas as pd
import numpy as np


def _get_amount_col(df):
    for col in ["Amount", "amount", "Expense", "expense", "Price", "price"]:
        if col in df.columns:
            return col
    return None


def _get_date_col(df):
    for col in ["Date", "date", "DATE"]:
        if col in df.columns:
            return col
    return None


def _get_category_col(df):
    for col in ["Category", "category", "CATEGORY"]:
        if col in df.columns:
            return col
    return None


def _clean_expenses(expenses):
    if expenses is None or len(expenses) == 0:
        return pd.DataFrame()

    df = expenses.copy()

    amount_col = _get_amount_col(df)
    date_col = _get_date_col(df)

    if amount_col:
        df[amount_col] = pd.to_numeric(df[amount_col], errors="coerce")
        df = df.dropna(subset=[amount_col])

    if date_col:
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
        df = df.dropna(subset=[date_col])

    return df


def _monthly_totals(expenses):
    df = _clean_expenses(expenses)

    if df.empty:
        return pd.Series(dtype=float)

    amount_col = _get_amount_col(df)
    date_col = _get_date_col(df)

    if not amount_col or not date_col:
        return pd.Series(dtype=float)

    monthly = (
        df.set_index(date_col)[amount_col]
        .resample("MS")
        .sum()
    )

    return monthly


def monthly_totals(expenses):
    return _monthly_totals(expenses)


def predict_next_month(expenses, method="weighted_trend"):
    monthly = _monthly_totals(expenses)

    if monthly.empty:
        return 0.0

    values = monthly.values.astype(float)

    if method == "average":
        return float(np.mean(values))

    if method == "last_month":
        return float(values[-1])

    if method == "exponential":
        series = pd.Series(values)
        return float(
            series.ewm(span=min(3, len(series)), adjust=False).mean().iloc[-1]
        )

    # Weighted Trend Prediction
    if len(values) >= 2:
        x = np.arange(len(values))
        slope, intercept = np.polyfit(x, values, 1)

        next_x = len(values)
        linear_prediction = slope * next_x + intercept

        weights = np.arange(1, len(values) + 1)
        weighted_prediction = np.average(values, weights=weights)

        prediction = (
            0.60 * linear_prediction
            + 0.40 * weighted_prediction
        )
    else:
        prediction = values[-1]

    return max(0.0, float(prediction))


def prediction_comparison(expenses):
    weighted = predict_next_month(expenses, "weighted_trend")
    average = predict_next_month(expenses, "average")
    last_month = predict_next_month(expenses, "last_month")
    exponential = predict_next_month(expenses, "exponential")

    return pd.DataFrame({
        "Method": [
            "Weighted Trend",
            "Historical Average",
            "Last Month",
            "Exponential"
        ],
        "Prediction": [
            weighted,
            average,
            last_month,
            exponential
        ]
    })


def spending_trend(expenses):
    monthly = _monthly_totals(expenses)

    if monthly.empty:
        return "No spending data available."

    if len(monthly) < 2:
        return "Not enough data to determine a trend."

    first = monthly.iloc[0]
    last = monthly.iloc[-1]

    if last > first * 1.10:
        return "Spending is increasing 📈"
    elif last < first * 0.90:
        return "Spending is decreasing 📉"
    else:
        return "Spending is relatively stable ➡️"


def category_breakdown(expenses):
    df = _clean_expenses(expenses)

    if df.empty:
        return {}

    amount_col = _get_amount_col(df)
    category_col = _get_category_col(df)

    if not amount_col or not category_col:
        return {}

    result = (
        df.groupby(category_col)[amount_col]
        .sum()
        .sort_values(ascending=False)
    )

    return result.to_dict()


def top_spending_category(expenses):
    breakdown = category_breakdown(expenses)

    if not breakdown:
        return "No data"

    return max(breakdown, key=breakdown.get)


def monthly_average_by_category(expenses):
    df = _clean_expenses(expenses)

    if df.empty:
        return pd.DataFrame()

    amount_col = _get_amount_col(df)
    date_col = _get_date_col(df)
    category_col = _get_category_col(df)

    if not amount_col or not date_col or not category_col:
        return pd.DataFrame()

    df["Month"] = df[date_col].dt.to_period("M").astype(str)

    result = (
        df.groupby(["Month", category_col])[amount_col]
        .sum()
        .reset_index()
    )

    return result


def detect_anomalies(expenses):
    df = _clean_expenses(expenses)

    if df.empty:
        return pd.DataFrame()

    amount_col = _get_amount_col(df)

    if not amount_col:
        return pd.DataFrame()

    q1 = df[amount_col].quantile(0.25)
    q3 = df[amount_col].quantile(0.75)

    iqr = q3 - q1

    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    result = df[
        (df[amount_col] < lower)
        | (df[amount_col] > upper)
    ].copy()

    return result


def budget_forecast(expenses, budget):
    prediction = predict_next_month(
        expenses,
        method="weighted_trend"
    )

    difference = prediction - float(budget)

    return {
        "prediction": prediction,
        "budget": float(budget),
        "difference": difference,
        "status": "Above Budget" if difference > 0 else "Within Budget"
    }