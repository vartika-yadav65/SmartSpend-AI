import pandas as pd


def predict_next_month(expenses):
    if expenses is None or len(expenses) == 0:
        return 0.0

    df = expenses.copy()

    # Find the amount column
    amount_col = None

    for col in ["Amount", "amount", "Expense", "expense"]:
        if col in df.columns:
            amount_col = col
            break

    if amount_col is None:
        return 0.0

    df[amount_col] = pd.to_numeric(df[amount_col], errors="coerce")
    df = df.dropna(subset=[amount_col])

    if df.empty:
        return 0.0

    # Find date column
    date_col = None

    for col in ["Date", "date"]:
        if col in df.columns:
            date_col = col
            break

    if date_col:
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
        df = df.dropna(subset=[date_col])

        if not df.empty:
            monthly = df.groupby(
                df[date_col].dt.to_period("M")
            )[amount_col].sum()

            if len(monthly) > 0:
                return round(float(monthly.mean()), 2)

    return round(float(df[amount_col].mean()), 2)