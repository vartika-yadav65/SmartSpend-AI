import pandas as pd
import numpy as np


def load_data(file_path="expenses.csv"):
    """Load and prepare expense data."""
    df = pd.read_csv(file_path)
    
    df["Date"] = pd.to_datetime(df["Date"])
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")

    df = df.dropna(subset=["Date", "Amount"])
    df = df[df["Amount"] >= 0]

    return df


def get_summary(df):
    """Calculate basic spending statistics."""
    total_spending = df["Amount"].sum()
    average_spending = df["Amount"].mean()
    highest_expense = df["Amount"].max()

    highest_category = (
        df.groupby("Category")["Amount"]
        .sum()
        .idxmax()
    )

    return {
        "total_spending": total_spending,
        "average_spending": average_spending,
        "highest_expense": highest_expense,
        "highest_category": highest_category
    }


def category_analysis(df):
    """Calculate spending by category."""
    return (
        df.groupby("Category")["Amount"]
        .sum()
        .sort_values(ascending=False)
    )


def monthly_analysis(df):
    """Calculate monthly spending."""
    df = df.copy()
    df["Month"] = df["Date"].dt.to_period("M").astype(str)

    return (
        df.groupby("Month")["Amount"]
        .sum()
        .sort_index()
    )


if __name__ == "__main__":
    df = load_data()

    summary = get_summary(df)

    print("\n===== SMARTSPEND AI =====")
    print(f"Total Spending: ₹{summary['total_spending']:.2f}")
    print(f"Average Expense: ₹{summary['average_spending']:.2f}")
    print(f"Highest Expense: ₹{summary['highest_expense']:.2f}")
    print(f"Highest Spending Category: {summary['highest_category']}")

    print("\n===== CATEGORY ANALYSIS =====")
    print(category_analysis(df))

    print("\n===== MONTHLY ANALYSIS =====")
    print(monthly_analysis(df))
