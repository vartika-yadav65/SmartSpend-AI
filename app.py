import os
import json
import hashlib
from datetime import date

import pandas as pd
import streamlit as st

from prediction import (
    predict_next_month,
    prediction_comparison,
    spending_trend,
    category_breakdown,
    top_spending_category,
    monthly_average_by_category,
    detect_anomalies,
    budget_forecast,
)


# ============================================================
# PAGE SETTINGS
# ============================================================

st.set_page_config(
    page_title="SmartSpend AI",
    page_icon="💰",
    layout="wide",
)


# ============================================================
# FOLDERS
# ============================================================

DATA_DIR = "data"

os.makedirs(DATA_DIR, exist_ok=True)

USERS_FILE = os.path.join(DATA_DIR, "users.json")


# ============================================================
# USER FUNCTIONS
# ============================================================

def hash_password(password):
    return hashlib.sha256(
        password.encode()
    ).hexdigest()


def load_users():
    if not os.path.exists(USERS_FILE):
        return {}

    try:
        with open(USERS_FILE, "r") as file:
            return json.load(file)
    except:
        return {}


def save_users(users):
    with open(USERS_FILE, "w") as file:
        json.dump(users, file, indent=4)


def safe_username(username):
    return "".join(
        c for c in username
        if c.isalnum() or c in "_-"
    )


def expense_file(username):
    return os.path.join(
        DATA_DIR,
        f"{safe_username(username)}_expenses.csv"
    )


def budget_file(username):
    return os.path.join(
        DATA_DIR,
        f"{safe_username(username)}_budget.txt"
    )


# ============================================================
# AUTHENTICATION
# ============================================================

if "user" not in st.session_state:
    st.session_state.user = None


if st.session_state.user is None:

    st.title("💰 SmartSpend AI")
    st.subheader("Smart Personal Expense Management")

    login_tab, register_tab = st.tabs(
        ["🔐 Login", "📝 Register"]
    )

    with login_tab:

        username = st.text_input(
            "Username",
            key="login_username"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button(
            "Login",
            use_container_width=True
        ):

            users = load_users()

            if (
                username in users
                and users[username]
                == hash_password(password)
            ):
                st.session_state.user = username
                st.success("Login successful!")
                st.rerun()

            else:
                st.error(
                    "Invalid username or password."
                )

    with register_tab:

        new_username = st.text_input(
            "Create username",
            key="register_username"
        )

        new_password = st.text_input(
            "Create password",
            type="password",
            key="register_password"
        )

        confirm_password = st.text_input(
            "Confirm password",
            type="password"
        )

        if st.button(
            "Create Account",
            use_container_width=True
        ):

            users = load_users()

            if not new_username or not new_password:
                st.warning(
                    "Please enter username and password."
                )

            elif new_password != confirm_password:
                st.error(
                    "Passwords do not match."
                )

            elif new_username in users:
                st.error(
                    "Username already exists."
                )

            else:

                users[new_username] = hash_password(
                    new_password
                )

                save_users(users)

                st.success(
                    "Account created! Go to Login."
                )

    st.stop()


# ============================================================
# CURRENT USER
# ============================================================

username = st.session_state.user


# ============================================================
# LOAD EXPENSES
# ============================================================

def load_expenses():

    file = expense_file(username)

    if os.path.exists(file):

        try:
            df = pd.read_csv(file)

            if not df.empty:
                df["Date"] = pd.to_datetime(
                    df["Date"],
                    errors="coerce"
                )

            return df

        except:
            pass

    return pd.DataFrame(
        columns=[
            "Date",
            "Category",
            "Amount",
            "Payment_Method",
            "Description",
        ]
    )


def save_expenses(df):

    file = expense_file(username)

    df.to_csv(
        file,
        index=False
    )


expenses = load_expenses()


# ============================================================
# BUDGET
# ============================================================

def load_budget():

    file = budget_file(username)

    if os.path.exists(file):

        try:
            with open(file, "r") as f:
                return float(f.read())
        except:
            pass

    return 5000.0


budget = load_budget()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("💰 SmartSpend AI")

    st.write(
        f"Welcome, **{username}** 👋"
    )

    st.divider()

    st.subheader("💵 Monthly Budget")

    new_budget = st.number_input(
        "Budget (₹)",
        min_value=0.0,
        value=float(budget),
        step=500.0
    )

    if st.button(
        "Save Budget",
        use_container_width=True
    ):

        with open(
            budget_file(username),
            "w"
        ) as f:

            f.write(str(new_budget))

        st.success("Budget saved!")
        st.rerun()

    st.divider()

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        st.session_state.user = None
        st.rerun()


# ============================================================
# HEADER
# ============================================================

st.title("💰 SmartSpend AI")

st.caption(
    "AI-powered personal expense tracking, analytics and prediction."
)


# ============================================================
# BASIC CALCULATIONS
# ============================================================

if expenses.empty:

    total_spending = 0

else:

    total_spending = pd.to_numeric(
        expenses["Amount"],
        errors="coerce"
    ).fillna(0).sum()


remaining = budget - total_spending

prediction = predict_next_month(
    expenses
)


# ============================================================
# TOP METRICS
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "💸 Total Spending",
        f"₹{total_spending:,.0f}"
    )

with col2:

    st.metric(
        "💰 Monthly Budget",
        f"₹{budget:,.0f}"
    )

with col3:

    st.metric(
        "💵 Remaining",
        f"₹{remaining:,.0f}"
    )

with col4:

    st.metric(
        "🔮 Next Month Prediction",
        f"₹{prediction:,.0f}"
    )


# ============================================================
# BUDGET ALERT
# ============================================================

if budget > 0:

    usage = total_spending / budget

    if usage >= 1:

        st.error(
            "🚨 You have exceeded your monthly budget!"
        )

    elif usage >= 0.8:

        st.warning(
            "⚠️ You have used more than 80% of your budget."
        )

    else:

        st.success(
            f"✅ You have used {usage * 100:.1f}% of your budget."
        )


# ============================================================
# TABS
# ============================================================

(
    dashboard_tab,
    add_tab,
    analytics_tab,
    prediction_tab,
    anomaly_tab,
    ai_tab,
    data_tab,
) = st.tabs(
    [
        "📊 Dashboard",
        "➕ Add Expense",
        "📈 Analytics",
        "🔮 Prediction",
        "🚨 Anomalies",
        "🤖 AI Assistant",
        "📁 Data",
    ]
)


# ============================================================
# DASHBOARD
# ============================================================

with dashboard_tab:

    st.subheader("📊 Spending Dashboard")

    if expenses.empty:

        st.info(
            "No expenses yet. Add your first expense!"
        )

    else:

        # Budget progress

        st.write("### 💰 Budget Usage")

        progress = min(
            max(
                total_spending / budget
                if budget > 0 else 0,
                0
            ),
            1
        )

        st.progress(progress)

        st.write(
            f"{(total_spending / budget * 100) if budget else 0:.1f}% used"
        )

        st.divider()

        # Monthly chart

        st.write("### 📅 Monthly Spending")

        monthly = expenses.copy()

        monthly["Date"] = pd.to_datetime(
            monthly["Date"],
            errors="coerce"
        )

        monthly["Amount"] = pd.to_numeric(
            monthly["Amount"],
            errors="coerce"
        )

        monthly["Month"] = (
            monthly["Date"]
            .dt.to_period("M")
            .astype(str)
        )

        monthly_chart = (
            monthly
            .groupby("Month")["Amount"]
            .sum()
        )

        st.line_chart(monthly_chart)

        # Category chart

        st.write("### 🛍️ Category Spending")

        categories = category_breakdown(
            expenses
        )

        if categories:

            category_series = pd.Series(
                categories
            ).sort_values(
                ascending=False
            )

            st.bar_chart(category_series)

        st.divider()

        # Smart insights

        st.write("### 🧠 Smart Insights")

        st.info(
            f"📌 Spending Trend: {spending_trend(expenses)}"
        )

        st.info(
            f"🏆 Top Spending Category: "
            f"{top_spending_category(expenses)}"
        )

        st.info(
            f"🔮 Predicted Next Month Spending: "
            f"₹{prediction:,.0f}"
        )


# ============================================================
# ADD EXPENSE
# ============================================================

with add_tab:

    st.subheader("➕ Add New Expense")

    with st.form("expense_form"):

        expense_date = st.date_input(
            "Date",
            value=date.today()
        )

        category = st.selectbox(
            "Category",
            [
                "Food",
                "Travel",
                "Shopping",
                "Education",
                "Entertainment",
                "Bills",
                "Healthcare",
                "Other",
            ]
        )

        amount = st.number_input(
            "Amount (₹)",
            min_value=0.0,
            step=10.0
        )

        payment_method = st.selectbox(
            "Payment Method",
            [
                "UPI",
                "Cash",
                "Card",
                "Net Banking",
                "Other",
            ]
        )

        description = st.text_input(
            "Description"
        )

        submitted = st.form_submit_button(
            "💾 Save Expense",
            use_container_width=True
        )

        if submitted:

            if amount <= 0:

                st.error(
                    "Please enter an amount greater than ₹0."
                )

            else:

                new_row = pd.DataFrame(
                    [{
                        "Date": expense_date,
                        "Category": category,
                        "Amount": amount,
                        "Payment_Method": payment_method,
                        "Description": description,
                    }]
                )

                expenses = pd.concat(
                    [
                        expenses,
                        new_row
                    ],
                    ignore_index=True
                )

                save_expenses(expenses)

                st.success(
                    "Expense added successfully! 🎉"
                )

                st.rerun()


# ============================================================
# ANALYTICS
# ============================================================

with analytics_tab:

    st.subheader(
        "📈 Financial Analytics"
    )

    if expenses.empty:

        st.info(
            "Add expenses to see analytics."
        )

    else:

        col1, col2 = st.columns(2)

        with col1:

            st.write(
                "### 🛍️ Category Breakdown"
            )

            breakdown = category_breakdown(
                expenses
            )

            st.dataframe(
                pd.DataFrame(
                    list(breakdown.items()),
                    columns=[
                        "Category",
                        "Total Spending"
                    ]
                ),
                use_container_width=True
            )

        with col2:

            st.write(
                "### 💳 Payment Methods"
            )

            payment_data = (
                expenses
                .groupby("Payment_Method")["Amount"]
                .sum()
                .sort_values(
                    ascending=False
                )
            )

            st.bar_chart(
                payment_data
            )

        st.divider()

        st.write(
            "### 📊 Monthly Average by Category"
        )

        monthly_category = (
            monthly_average_by_category(
                expenses
            )
        )

        if not monthly_category.empty:

            st.dataframe(
                monthly_category,
                use_container_width=True
            )

        st.divider()

        st.write(
            "### 📅 Monthly Summary"
        )

        monthly_summary = (
            expenses.assign(
                Month=pd.to_datetime(
                    expenses["Date"]
                ).dt.to_period("M").astype(str)
            )
            .groupby("Month")["Amount"]
            .agg(
                ["sum", "mean", "count"]
            )
            .reset_index()
        )

        monthly_summary.columns = [
            "Month",
            "Total",
            "Average",
            "Transactions"
        ]

        st.dataframe(
            monthly_summary,
            use_container_width=True
        )


# ============================================================
# PREDICTION
# ============================================================

with prediction_tab:

    st.subheader(
        "🔮 Advanced Spending Prediction"
    )

    if expenses.empty:

        st.info(
            "Add expenses first to generate predictions."
        )

    else:

        forecast = budget_forecast(
            expenses,
            budget
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Predicted Spending",
                f"₹{forecast['prediction']:,.0f}"
            )

        with col2:

            st.metric(
                "Budget",
                f"₹{budget:,.0f}"
            )

        with col3:

            difference = forecast["difference"]

            st.metric(
                "Difference",
                f"₹{abs(difference):,.0f}",
                "Above" if difference > 0 else "Below"
            )

        st.divider()

        st.write(
            "### 🔬 Prediction Method Comparison"
        )

        comparison = prediction_comparison(
            expenses
        )

        comparison["Prediction"] = (
            comparison["Prediction"]
            .round(2)
        )

        st.dataframe(
            comparison,
            use_container_width=True,
            hide_index=True
        )

        st.bar_chart(
            comparison.set_index("Method")
            ["Prediction"]
        )

        st.divider()

        st.write(
            "### 🧠 How SmartSpend AI Predicts"
        )

        st.write(
            """
            **Weighted Trend Prediction**

            • 60% Linear spending trend  
            • 40% Recency-weighted spending  
            • Recent months receive more importance  
            • Negative predictions are prevented  

            The app also compares this result with:
            Historical Average, Last Month and Exponential forecasting.
            """
        )


# ============================================================
# ANOMALIES
# ============================================================

with anomaly_tab:

    st.subheader(
        "🚨 Unusual Spending Detection"
    )

    if expenses.empty:

        st.info(
            "Add expenses to detect unusual transactions."
        )

    else:

        anomalies = detect_anomalies(
            expenses
        )

        if anomalies.empty:

            st.success(
                "✅ No unusual spending detected."
            )

        else:

            st.warning(
                f"⚠️ {len(anomalies)} unusual "
                "transaction(s) detected."
            )

            st.dataframe(
                anomalies,
                use_container_width=True
            )


# ============================================================
# AI ASSISTANT
# ============================================================

with ai_tab:

    st.subheader(
        "🤖 SmartSpend AI Assistant"
    )

    st.write(
        "Ask questions about your spending."
    )

    question = st.text_input(
        "Example: Where am I spending the most?"
    )

    if st.button(
        "🤖 Ask AI",
        use_container_width=True
    ):

        if expenses.empty:

            st.info(
                "Add some expenses first."
            )

        else:

            breakdown = category_breakdown(
                expenses
            )

            top_category = (
                top_spending_category(
                    expenses
                )
            )

            total = float(
                expenses["Amount"]
                .sum()
            )

            prompt = f"""
You are SmartSpend AI, a helpful personal
finance assistant.

User spending data:
Total spending: ₹{total:.2f}
Top category: {top_category}
Category breakdown: {breakdown}

User question:
{question}

Give a short, simple and practical answer.
Do not give investment or financial advice.
"""

            api_key = None

            try:

                api_key = st.secrets[
                    "OPENAI_API_KEY"
                ]

            except:

                api_key = os.getenv(
                    "OPENAI_API_KEY"
                )

            if api_key:

                try:

                    from openai import OpenAI

                    client = OpenAI(
                        api_key=api_key
                    )

                    response = (
                        client.responses.create(
                            model="gpt-5",
                            input=prompt
                        )
                    )

                    st.success(
                        response.output_text
                    )

                except Exception as e:

                    st.error(
                        f"AI error: {e}"
                    )

            else:

                # Local AI-style fallback

                st.info(
                    f"""
                    **SmartSpend Insight 🤖**

                    Your highest spending category is
                    **{top_category}**.

                    Your total recorded spending is
                    **₹{total:,.0f}**.

                    Try reducing unnecessary spending in
                    your highest category and monitor it
                    every month.

                    💡 To activate real AI responses,
                    add an OpenAI API key later.
                    """
                )


# ============================================================
# DATA
# ============================================================

with data_tab:

    st.subheader(
        "📁 Expense Data"
    )

    if expenses.empty:

        st.info(
            "No expense data available."
        )

    else:

        display_data = expenses.copy()

        display_data["Date"] = (
            pd.to_datetime(
                display_data["Date"],
                errors="coerce"
            ).dt.strftime("%Y-%m-%d")
        )

        st.dataframe(
            display_data,
            use_container_width=True,
            hide_index=True
        )

        csv = expenses.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            "📥 Download Expenses CSV",
            csv,
            "smartspend_expenses.csv",
            "text/csv",
            use_container_width=True
        )

        st.divider()

        if st.button(
            "🗑️ Clear My Expense Data"
        ):

            os.remove(
                expense_file(username)
            )

            st.success(
                "Expense data cleared."
            )

            st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "SmartSpend AI • Personal Expense Analytics & Prediction"
)