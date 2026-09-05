import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
from datetime import date

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="SmartSpend AI",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

DATA_FILE = "expenses.csv"
BUDGET_FILE = "budget.txt"

CATEGORIES = [
    "Food",
    "Travel",
    "Shopping",
    "Education",
    "Entertainment",
    "Bills",
    "Other"
]

PAYMENT_METHODS = [
    "UPI",
    "Cash",
    "Card"
]

# =========================================================
# DARK PROFESSIONAL UI
# =========================================================

st.markdown(
    """
    <style>

    .stApp {
        background: #050509;
        color: #F5F7FF;
    }

    [data-testid="stHeader"] {
        background: #050509;
    }

    .block-container {
        max-width: 1500px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF !important;
    }

    p, span, label {
        color: #D0D3DE;
    }

    [data-testid="stMetric"] {
        background: #11111A;
        border: 1px solid #29293A;
        border-radius: 18px;
        padding: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.25);
    }

    [data-testid="stMetricLabel"] {
        color: #AEB2C4 !important;
    }

    [data-testid="stMetricValue"] {
        color: #FFFFFF !important;
    }

    div[data-baseweb="tab-list"] {
        background: #0D0D14;
        border: 1px solid #29293A;
        border-radius: 15px;
        padding: 7px;
        gap: 5px;
    }

    button[data-baseweb="tab"] {
        color: #AEB2C4 !important;
        background: transparent !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
    }

    button[data-baseweb="tab"]:hover {
        background: #191923 !important;
        color: white !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        background: #6252D9 !important;
        color: white !important;
    }

    div[data-baseweb="input"] {
        background: #11111A !important;
        border: 1px solid #303040 !important;
        border-radius: 10px !important;
    }

    input {
        color: white !important;
    }

    div[data-baseweb="select"] > div {
        background: #11111A !important;
        border: 1px solid #303040 !important;
        color: white !important;
    }

    div[data-baseweb="select"] span {
        color: white !important;
    }

    textarea {
        background: #11111A !important;
        color: white !important;
    }

    .stButton > button,
    .stFormSubmitButton > button {
        background: #6252D9 !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
    }

    .stButton > button:hover,
    .stFormSubmitButton > button:hover {
        background: #7567ED !important;
    }

    [data-testid="stAlert"] {
        border-radius: 12px !important;
    }

    hr {
        border-color: #29293A !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# DATA FUNCTIONS
# =========================================================

def empty_dataframe():

    return pd.DataFrame(
        columns=[
            "Date",
            "Category",
            "Amount",
            "Payment_Method",
            "Description"
        ]
    )


def load_data():

    if not os.path.exists(DATA_FILE):
        return empty_dataframe()

    try:
        data = pd.read_csv(DATA_FILE)
    except Exception:
        return empty_dataframe()

    required = [
        "Date",
        "Category",
        "Amount",
        "Payment_Method",
        "Description"
    ]

    for column in required:

        if column not in data.columns:
            data[column] = ""

    data = data[required]

    data["Date"] = pd.to_datetime(
        data["Date"],
        errors="coerce"
    )

    data["Amount"] = pd.to_numeric(
        data["Amount"],
        errors="coerce"
    )

    data["Category"] = (
        data["Category"]
        .fillna("Other")
        .astype(str)
    )

    data["Payment_Method"] = (
        data["Payment_Method"]
        .fillna("Other")
        .astype(str)
    )

    data["Description"] = (
        data["Description"]
        .fillna("")
        .astype(str)
    )

    data = data.dropna(
        subset=["Date", "Amount"]
    )

    return data


def save_data(data):

    save_df = data.copy()

    save_df["Date"] = pd.to_datetime(
        save_df["Date"]
    ).dt.strftime("%Y-%m-%d")

    save_df.to_csv(
        DATA_FILE,
        index=False
    )


def load_budget():

    if not os.path.exists(BUDGET_FILE):
        return 5000.0

    try:

        with open(BUDGET_FILE, "r") as file:
            return float(file.read())

    except Exception:

        return 5000.0


def save_budget(value):

    with open(BUDGET_FILE, "w") as file:
        file.write(str(value))


df = load_data()

# =========================================================
# HEADER
# =========================================================

st.title("💰 SmartSpend AI")

st.subheader(
    "Intelligent Personal Finance Management"
)

st.caption(
    "Track • Analyze • Detect • Predict • Optimize"
)

st.divider()

# =========================================================
# NAVIGATION
# =========================================================

(
    dashboard_tab,
    add_tab,
    budget_tab,
    monthly_tab,
    category_tab,
    unusual_tab,
    prediction_tab,
    assistant_tab,
    reports_tab
) = st.tabs(
    [
        "🏠 Dashboard",
        "➕ Add Expense",
        "🎯 Budget",
        "📅 Monthly",
        "🛒 Categories",
        "🚨 Unusual",
        "🔮 Prediction",
        "🤖 AI Assistant",
        "📥 Reports"
    ]
)

# =========================================================
# DASHBOARD
# =========================================================

with dashboard_tab:

    st.header("📊 Financial Overview")

    if df.empty:

        st.info(
            "No expenses available yet. "
            "Go to Add Expense to begin."
        )

    else:

        # -------------------------------------------------
        # FILTERS
        # -------------------------------------------------

        col1, col2, col3 = st.columns(3)

        with col1:

            selected_category = st.selectbox(
                "🛒 Category",
                ["All"] +
                sorted(
                    df["Category"]
                    .unique()
                    .tolist()
                ),
                key="dashboard_category"
            )

        with col2:

            selected_payment = st.selectbox(
                "💳 Payment Method",
                ["All"] +
                sorted(
                    df["Payment_Method"]
                    .unique()
                    .tolist()
                ),
                key="dashboard_payment"
            )

        with col3:

            min_date = df["Date"].min().date()
            max_date = df["Date"].max().date()

            selected_dates = st.date_input(
                "📅 Date Range",
                value=(min_date, max_date),
                key="dashboard_dates"
            )

        filtered = df.copy()

        if selected_category != "All":

            filtered = filtered[
                filtered["Category"]
                == selected_category
            ]

        if selected_payment != "All":

            filtered = filtered[
                filtered["Payment_Method"]
                == selected_payment
            ]

        if isinstance(selected_dates, tuple) and len(selected_dates) == 2:

            start_date, end_date = selected_dates

            filtered = filtered[
                (filtered["Date"].dt.date >= start_date)
                &
                (filtered["Date"].dt.date <= end_date)
            ]

        if filtered.empty:

            st.warning(
                "No transactions match the selected filters."
            )

        else:

            total_spending = filtered["Amount"].sum()
            transaction_count = len(filtered)
            average_expense = filtered["Amount"].mean()
            highest_expense = filtered["Amount"].max()

            budget = load_budget()

            current_month = pd.Timestamp.today().to_period("M")

            current_month_spending = df[
                df["Date"].dt.to_period("M")
                == current_month
            ]["Amount"].sum()

            remaining = budget - current_month_spending

            # -------------------------------------------------
            # KPI CARDS
            # -------------------------------------------------

            c1, c2, c3, c4, c5 = st.columns(5)

            with c1:
                st.metric(
                    "💰 Total Spending",
                    f"₹{total_spending:,.0f}"
                )

            with c2:
                st.metric(
                    "🧾 Transactions",
                    transaction_count
                )

            with c3:
                st.metric(
                    "📊 Average",
                    f"₹{average_expense:,.0f}"
                )

            with c4:
                st.metric(
                    "🔝 Highest",
                    f"₹{highest_expense:,.0f}"
                )

            with c5:
                st.metric(
                    "🎯 Budget Left",
                    f"₹{remaining:,.0f}"
                )

            st.divider()

            # -------------------------------------------------
            # SMART INSIGHTS
            # -------------------------------------------------

            st.header("🤖 Smart Insights")

            category_totals = (
                filtered
                .groupby("Category")["Amount"]
                .sum()
                .sort_values(ascending=False)
            )

            if not category_totals.empty:

                top_category = category_totals.index[0]
                top_amount = category_totals.iloc[0]

                i1, i2, i3 = st.columns(3)

                with i1:

                    st.info(
                        f"🛒 **Top Category**\n\n"
                        f"{top_category}\n\n"
                        f"₹{top_amount:,.0f}"
                    )

                with i2:

                    largest = filtered.loc[
                        filtered["Amount"].idxmax()
                    ]

                    st.warning(
                        f"💸 **Largest Expense**\n\n"
                        f"₹{largest['Amount']:,.0f}\n\n"
                        f"{largest['Category']}"
                    )

                with i3:

                    percentage = (
                        top_amount
                        / total_spending
                        * 100
                    )

                    st.success(
                        f"📈 **Top Category Share**\n\n"
                        f"{percentage:.1f}%\n\n"
                        f"of total spending"
                    )

            st.divider()

            # -------------------------------------------------
            # INTERACTIVE MONTHLY CHART
            # -------------------------------------------------

            st.subheader("📈 Spending Trend")

            monthly = (
                filtered
                .assign(
                    Month=filtered["Date"]
                    .dt.to_period("M")
                    .astype(str)
                )
                .groupby("Month")["Amount"]
                .sum()
                .reset_index()
            )

            if not monthly.empty:

                fig = px.line(
                    monthly,
                    x="Month",
                    y="Amount",
                    markers=True,
                    title="Monthly Spending Trend"
                )

                fig.update_layout(
                    template="plotly_dark",
                    paper_bgcolor="#050509",
                    plot_bgcolor="#050509",
                    font_color="white",
                    hovermode="x unified"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            # -------------------------------------------------
            # CATEGORY CHART
            # -------------------------------------------------

            st.subheader("🛒 Spending by Category")

            category_chart = (
                filtered
                .groupby("Category")["Amount"]
                .sum()
                .reset_index()
                .sort_values(
                    "Amount",
                    ascending=False
                )
            )

            fig_category = px.bar(
                category_chart,
                x="Category",
                y="Amount",
                title="Category Spending"
            )

            fig_category.update_layout(
                template="plotly_dark",
                paper_bgcolor="#050509",
                plot_bgcolor="#050509",
                font_color="white"
            )

            st.plotly_chart(
                fig_category,
                use_container_width=True
            )

            # -------------------------------------------------
            # RECENT TRANSACTIONS
            # -------------------------------------------------

            st.subheader("🧾 Recent Transactions")

            recent = (
                filtered
                .sort_values(
                    "Date",
                    ascending=False
                )
                .head(10)
            )

            st.dataframe(
                recent,
                use_container_width=True,
                hide_index=True
            )

# =========================================================
# ADD EXPENSE
# =========================================================

with add_tab:

    st.header("➕ Add New Expense")

    st.write(
        "Record your daily transaction."
    )

    with st.form(
        "expense_form",
        clear_on_submit=True
    ):

        left, right = st.columns(2)

        with left:

            expense_date = st.date_input(
                "📅 Date",
                value=date.today()
            )

            category = st.selectbox(
                "🛒 Category",
                CATEGORIES
            )

            amount = st.number_input(
                "💰 Amount",
                min_value=1.0,
                value=100.0,
                step=10.0
            )

        with right:

            payment = st.selectbox(
                "💳 Payment Method",
                PAYMENT_METHODS
            )

            description = st.text_input(
                "📝 Description",
                placeholder="Example: College lunch"
            )

        submitted = st.form_submit_button(
            "💾 Save Expense"
        )

    if submitted:

        new_expense = pd.DataFrame(
            [{
                "Date": pd.to_datetime(
                    expense_date
                ),
                "Category": category,
                "Amount": amount,
                "Payment_Method": payment,
                "Description": description
            }]
        )

        df = pd.concat(
            [df, new_expense],
            ignore_index=True
        )

        save_data(df)

        st.success(
            "✅ Expense saved successfully!"
        )

        st.rerun()

# =========================================================
# BUDGET
# =========================================================

with budget_tab:

    st.header("🎯 Budget Tracking")

    budget = load_budget()

    current_month = pd.Timestamp.today().to_period("M")

    current_spending = df[
        df["Date"].dt.to_period("M")
        == current_month
    ]["Amount"].sum()

    remaining = budget - current_spending

    percentage_used = (
        current_spending / budget * 100
        if budget > 0
        else 0
    )

    # -------------------------------------------------
    # SET BUDGET
    # -------------------------------------------------

    st.subheader("💰 Monthly Budget")

    new_budget = st.number_input(
        "Set your monthly budget",
        min_value=100.0,
        value=float(budget),
        step=500.0
    )

    if st.button("💾 Update Budget"):

        save_budget(new_budget)

        st.success(
            f"Monthly budget updated to "
            f"₹{new_budget:,.0f}"
        )

        st.rerun()

    st.divider()

    # -------------------------------------------------
    # BUDGET METRICS
    # -------------------------------------------------

    b1, b2, b3, b4 = st.columns(4)

    with b1:
        st.metric(
            "🎯 Budget",
            f"₹{budget:,.0f}"
        )

    with b2:
        st.metric(
            "💸 Spent",
            f"₹{current_spending:,.0f}"
        )

    with b3:
        st.metric(
            "💰 Remaining",
            f"₹{remaining:,.0f}"
        )

    with b4:
        st.metric(
            "📊 Used",
            f"{percentage_used:.1f}%"
        )

    st.progress(
        min(
            percentage_used / 100,
            1.0
        )
    )

    if percentage_used >= 100:

        st.error(
            "🚨 You have exceeded your monthly budget!"
        )

    elif percentage_used >= 80:

        st.warning(
            "⚠️ You have used more than 80% "
            "of your monthly budget."
        )

    elif percentage_used >= 50:

        st.info(
            "ℹ️ You have used more than half "
            "of your monthly budget."
        )

    else:

        st.success(
            "✅ Your spending is currently within "
            "a comfortable budget range."
        )

    # -------------------------------------------------
    # BUDGET VS SPENDING
    # -------------------------------------------------

    st.subheader("📊 Budget vs Spending")

    budget_chart = pd.DataFrame(
        {
            "Type": [
                "Budget",
                "Spent"
            ],
            "Amount": [
                budget,
                current_spending
            ]
        }
    )

    fig = px.bar(
        budget_chart,
        x="Type",
        y="Amount",
        title="Current Month Budget"
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#050509",
        plot_bgcolor="#050509",
        font_color="white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =========================================================
# MONTHLY SUMMARY
# =========================================================

with monthly_tab:

    st.header("📅 Monthly Summary")

    if df.empty:

        st.info(
            "No expense data available."
        )

    else:

        monthly_df = (
            df.assign(
                Month=df["Date"]
                .dt.to_period("M")
                .astype(str)
            )
            .groupby("Month")["Amount"]
            .agg(
                Total="sum",
                Average="mean",
                Transactions="count"
            )
            .reset_index()
        )

        monthly_df["Total"] = monthly_df[
            "Total"
        ].round(2)

        monthly_df["Average"] = monthly_df[
            "Average"
        ].round(2)

        st.dataframe(
            monthly_df,
            use_container_width=True,
            hide_index=True
        )

        st.subheader("📈 Monthly Spending")

        fig = px.line(
            monthly_df,
            x="Month",
            y="Total",
            markers=True,
            title="Monthly Spending"
        )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#050509",
            plot_bgcolor="#050509",
            font_color="white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        highest = monthly_df.loc[
            monthly_df["Total"].idxmax()
        ]

        st.success(
            f"💡 Highest spending month: "
            f"{highest['Month']} — "
            f"₹{highest['Total']:,.0f}"
        )

# =========================================================
# CATEGORIES
# =========================================================

with category_tab:

    st.header("🛒 Category Analysis")

    if df.empty:

        st.info(
            "No expense data available."
        )

    else:

        category_summary = (
            df.groupby("Category")["Amount"]
            .agg(
                Total="sum",
                Average="mean",
                Transactions="count"
            )
            .reset_index()
            .sort_values(
                "Total",
                ascending=False
            )
        )

        st.dataframe(
            category_summary,
            use_container_width=True,
            hide_index=True
        )

        category_chart = (
            df.groupby("Category")["Amount"]
            .sum()
            .reset_index()
            .sort_values(
                "Amount",
                ascending=False
            )
        )

        st.subheader("📊 Category Spending")

        fig = px.bar(
            category_chart,
            x="Category",
            y="Amount",
            title="Spending by Category"
        )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#050509",
            plot_bgcolor="#050509",
            font_color="white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.subheader("💳 Payment Method")

        payment_summary = (
            df.groupby("Payment_Method")["Amount"]
            .sum()
            .reset_index()
        )

        fig2 = px.pie(
            payment_summary,
            names="Payment_Method",
            values="Amount",
            title="Payment Method Distribution"
        )

        fig2.update_layout(
            template="plotly_dark",
            paper_bgcolor="#050509",
            font_color="white"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

# =========================================================
# UNUSUAL EXPENSE DETECTION
# =========================================================

with unusual_tab:

    st.header("🚨 Unusual Expense Detection")

    if len(df) < 2:

        st.info(
            "Add at least two expenses to detect unusual spending."
        )

    else:

        mean_amount = df["Amount"].mean()

        std_amount = df["Amount"].std()

        threshold = (
            mean_amount
            + 2 * std_amount
        )

        unusual = df[
            df["Amount"] > threshold
        ].copy()

        c1, c2, c3 = st.columns(3)

        with c1:

            st.metric(
                "📊 Average",
                f"₹{mean_amount:,.0f}"
            )

        with c2:

            st.metric(
                "🚨 Threshold",
                f"₹{threshold:,.0f}"
            )

        with c3:

            st.metric(
                "⚠️ Flagged",
                len(unusual)
            )

        if unusual.empty:

            st.success(
                "✅ No unusually high expenses detected."
            )

        else:

            st.warning(
                f"⚠️ {len(unusual)} unusual "
                f"expense(s) detected."
            )

            unusual = unusual.sort_values(
                "Amount",
                ascending=False
            )

            st.dataframe(
                unusual,
                use_container_width=True,
                hide_index=True
            )

# =========================================================
# ADVANCED PREDICTION
# =========================================================

with prediction_tab:

    st.header("🔮 Advanced Spending Prediction")

    if df.empty:

        st.info(
            "Add expense data to generate predictions."
        )

    else:

        monthly_prediction = (
            df.assign(
                Month=df["Date"]
                .dt.to_period("M")
            )
            .groupby("Month")["Amount"]
            .sum()
            .reset_index()
        )

        values = monthly_prediction[
            "Amount"
        ].values

        if len(values) >= 3:

            x = np.arange(
                len(values)
            )

            # Linear trend

            linear_coefficients = np.polyfit(
                x,
                values,
                1
            )

            linear_prediction = np.polyval(
                linear_coefficients,
                len(values)
            )

            # Weighted recent average

            recent_count = min(
                3,
                len(values)
            )

            recent_values = values[
                -recent_count:
            ]

            weights = np.arange(
                1,
                recent_count + 1
            )

            weighted_prediction = np.average(
                recent_values,
                weights=weights
            )

            # Combined prediction

            prediction = (
                linear_prediction * 0.5
                +
                weighted_prediction * 0.5
            )

        elif len(values) == 2:

            prediction = np.mean(values)

        else:

            prediction = values[-1]

        prediction = max(
            0,
            float(prediction)
        )

        last_month = float(
            values[-1]
        )

        if last_month > 0:

            change = (
                prediction
                - last_month
            ) / last_month * 100

        else:

            change = 0

        p1, p2, p3 = st.columns(3)

        with p1:

            st.metric(
                "📅 Last Month",
                f"₹{last_month:,.0f}"
            )

        with p2:

            st.metric(
                "🔮 Predicted",
                f"₹{prediction:,.0f}"
            )

        with p3:

            st.metric(
                "📊 Expected Change",
                f"{change:+.1f}%"
            )

        st.divider()

        prediction_display = monthly_prediction.copy()

        prediction_display["Month"] = (
            prediction_display[
                "Month"
            ].astype(str)
        )

        next_period = (
            monthly_prediction["Month"].iloc[-1]
            + 1
        )

        prediction_display = pd.concat(
            [
                prediction_display,
                pd.DataFrame(
                    [{
                        "Month": str(next_period),
                        "Amount": prediction
                    }]
                )
            ],
            ignore_index=True
        )

        prediction_display["Type"] = (
            ["Historical"]
            * (
                len(prediction_display)
                - 1
            )
            + ["Predicted"]
        )

        fig = px.line(
            prediction_display,
            x="Month",
            y="Amount",
            color="Type",
            markers=True,
            title="Historical Spending + Forecast"
        )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#050509",
            plot_bgcolor="#050509",
            font_color="white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        if prediction > last_month:

            st.warning(
                "⚠️ Spending is expected to increase "
                "next month. Review your largest categories."
            )

        elif prediction < last_month:

            st.success(
                "✅ Spending is expected to decrease "
                "next month."
            )

        else:

            st.info(
                "ℹ️ Spending is expected to remain "
                "approximately stable."
            )

        st.caption(
            "Prediction combines a historical trend with "
            "a weighted recent-spending estimate. "
            "It is an estimate, not a guarantee."
        )

# =========================================================
# SMARTSPEND AI ASSISTANT
# =========================================================

with assistant_tab:

    st.header("🤖 SmartSpend AI Assistant")

    st.write(
        "Ask SmartSpend AI questions about your spending "
        "patterns and financial activity."
    )

    if "chat_history" not in st.session_state:

        st.session_state.chat_history = []

    # -------------------------------------------------
    # QUICK QUESTIONS
    # -------------------------------------------------

    st.subheader("💡 Quick Questions")

    q1, q2, q3, q4 = st.columns(4)

    quick_question = None

    with q1:

        if st.button(
            "💰 Total Spending",
            key="q_total"
        ):

            quick_question = (
                "How much have I spent?"
            )

    with q2:

        if st.button(
            "🛒 Top Category",
            key="q_category"
        ):

            quick_question = (
                "Which category do I spend the most on?"
            )

    with q3:

        if st.button(
            "🎯 Budget Status",
            key="q_budget"
        ):

            quick_question = (
                "How is my budget?"
            )

    with q4:

        if st.button(
            "🔮 Prediction",
            key="q_prediction"
        ):

            quick_question = (
                "What is my predicted spending?"
            )

    question = st.text_input(
        "💬 Ask SmartSpend AI",
        value=quick_question or "",
        placeholder=(
            "Example: Where am I spending the most?"
        )
    )

    ask = st.button(
        "✨ Ask SmartSpend AI",
        key="ask_ai"
    )

    if ask and question.strip():

        q = question.lower()

        if df.empty:

            response = (
                "I don't have enough expense data yet. "
                "Add some expenses and I'll analyze them."
            )

        else:

            total = df["Amount"].sum()

            average = df["Amount"].mean()

            count = len(df)

            category_totals = (
                df.groupby("Category")["Amount"]
                .sum()
                .sort_values(
                    ascending=False
                )
            )

            top_category = (
                category_totals.index[0]
            )

            top_amount = (
                category_totals.iloc[0]
            )

            largest = df.loc[
                df["Amount"].idxmax()
            ]

            budget = load_budget()

            current_month = pd.Timestamp.today().to_period("M")

            current_spending = df[
                df["Date"].dt.to_period("M")
                == current_month
            ]["Amount"].sum()

            budget_remaining = (
                budget
                - current_spending
            )

            budget_percentage = (
                current_spending
                / budget
                * 100
                if budget > 0
                else 0
            )

            # -------------------------------
            # TOTAL
            # -------------------------------

            if (
                "total" in q
                or "how much" in q
                or "spent" in q
            ):

                response = (
                    f"💰 You have recorded "
                    f"**₹{total:,.0f}** in total spending "
                    f"across **{count} transactions**."
                )

            # -------------------------------
            # TOP CATEGORY
            # -------------------------------

            elif (
                "category" in q
                or "most" in q
                or "where" in q
            ):

                response = (
                    f"🛒 Your highest spending category "
                    f"is **{top_category}**, with "
                    f"**₹{top_amount:,.0f}** spent."
                )

            # -------------------------------
            # AVERAGE
            # -------------------------------

            elif (
                "average" in q
                or "avg" in q
            ):

                response = (
                    f"📊 Your average transaction is "
                    f"**₹{average:,.0f}**."
                )

            # -------------------------------
            # LARGEST
            # -------------------------------

            elif (
                "largest" in q
                or "biggest" in q
                or "highest expense" in q
            ):

                response = (
                    f"🔝 Your largest recorded expense "
                    f"is **₹{largest['Amount']:,.0f}** "
                    f"in **{largest['Category']}**."
                )

            # -------------------------------
            # BUDGET
            # -------------------------------

            elif (
                "budget" in q
                or "remaining" in q
            ):

                if budget_percentage >= 100:

                    response = (
                        f"🚨 You have exceeded your "
                        f"monthly budget.\n\n"
                        f"Budget: **₹{budget:,.0f}**\n\n"
                        f"Spent: **₹{current_spending:,.0f}**"
                    )

                else:

                    response = (
                        f"🎯 Your current monthly budget "
                        f"is **₹{budget:,.0f}**.\n\n"
                        f"You have spent "
                        f"**₹{current_spending:,.0f}** "
                        f"({budget_percentage:.1f}%).\n\n"
                        f"Remaining: "
                        f"**₹{budget_remaining:,.0f}**."
                    )

            # -------------------------------
            # PREDICTION
            # -------------------------------

            elif (
                "predict" in q
                or "forecast" in q
                or "next month" in q
            ):

                monthly_values = (
                    df.assign(
                        Month=df["Date"]
                        .dt.to_period("M")
                    )
                    .groupby("Month")["Amount"]
                    .sum()
                    .values
                )

                if len(monthly_values) >= 2:

                    x = np.arange(
                        len(monthly_values)
                    )

                    coefficients = np.polyfit(
                        x,
                        monthly_values,
                        1
                    )

                    predicted = np.polyval(
                        coefficients,
                        len(monthly_values)
                    )

                    predicted = max(
                        0,
                        float(predicted)
                    )

                    response = (
                        f"🔮 SmartSpend estimates your "
                        f"next month's spending at around "
                        f"**₹{predicted:,.0f}**."
                    )

                else:

                    response = (
                        "I need at least two months of "
                        "data for a meaningful prediction."
                    )

            # -------------------------------
            # UNUSUAL
            # -------------------------------

            elif (
                "unusual" in q
                or "abnormal" in q
                or "high expense" in q
            ):

                mean = df["Amount"].mean()

                std = df["Amount"].std()

                threshold = mean + 2 * std

                unusual_count = len(
                    df[
                        df["Amount"]
                        > threshold
                    ]
                )

                if unusual_count:

                    response = (
                        f"🚨 I found **{unusual_count}** "
                        f"unusually high expense(s) "
                        f"based on the current detection rule."
                    )

                else:

                    response = (
                        "✅ No unusually high expenses "
                        "were detected."
                    )

            # -------------------------------
            # PAYMENT
            # -------------------------------

            elif (
                "payment" in q
                or "upi" in q
                or "cash" in q
                or "card" in q
            ):

                payment_totals = (
                    df.groupby(
                        "Payment_Method"
                    )["Amount"]
                    .sum()
                    .sort_values(
                        ascending=False
                    )
                )

                method = (
                    payment_totals.index[0]
                )

                amount = (
                    payment_totals.iloc[0]
                )

                response = (
                    f"💳 Your highest spending "
                    f"payment method is **{method}**, "
                    f"with **₹{amount:,.0f}**."
                )

            # -------------------------------
            # ADVICE
            # -------------------------------

            elif (
                "advice" in q
                or "save" in q
                or "improve" in q
                or "suggest" in q
            ):

                response = (
                    f"💡 Based on your data, "
                    f"**{top_category}** is your biggest "
                    f"spending category.\n\n"
                    f"Review that category first and "
                    f"look for expenses that can be reduced "
                    f"without affecting your essentials."
                )

            else:

                response = (
                    "🤔 I can help with:\n\n"
                    "• Total spending\n"
                    "• Highest category\n"
                    "• Average expense\n"
                    "• Largest expense\n"
                    "• Budget status\n"
                    "• Spending prediction\n"
                    "• Unusual expenses\n"
                    "• Payment methods\n"
                    "• Spending advice"
                )

        st.session_state.chat_history.append(
            {
                "question": question,
                "answer": response
            }
        )

    # -------------------------------------------------
    # CHAT HISTORY
    # -------------------------------------------------

    if st.session_state.chat_history:

        st.divider()

        st.subheader("💬 Conversation")

        for chat in reversed(
            st.session_state.chat_history
        ):

            st.markdown(
                f"**You:** {chat['question']}"
            )

            st.info(
                chat["answer"]
            )

# =========================================================
# REPORTS
# =========================================================

with reports_tab:

    st.header("📥 Exportable Reports")

    if df.empty:

        st.info(
            "Add expenses before generating reports."
        )

    else:

        st.write(
            "Download your SmartSpend data and "
            "summary reports."
        )

        # -------------------------------------------------
        # CSV REPORT
        # -------------------------------------------------

        st.subheader("📄 Expense CSV")

        csv_data = (
            df
            .sort_values(
                "Date",
                ascending=False
            )
            .to_csv(index=False)
            .encode("utf-8")
        )

        st.download_button(
            "⬇️ Download Expense CSV",
            csv_data,
            file_name="smartspend_expenses.csv",
            mime="text/csv"
        )

        # -------------------------------------------------
        # SUMMARY
        # -------------------------------------------------

        total = df["Amount"].sum()

        average = df["Amount"].mean()

        transaction_count = len(df)

        category_totals = (
            df.groupby("Category")["Amount"]
            .sum()
            .sort_values(
                ascending=False
            )
        )

        top_category = (
            category_totals.index[0]
        )

        top_amount = (
            category_totals.iloc[0]
        )

        budget = load_budget()

        current_month = pd.Timestamp.today().to_period("M")

        current_spending = df[
            df["Date"].dt.to_period("M")
            == current_month
        ]["Amount"].sum()

        # -------------------------------------------------
        # HTML REPORT
        # -------------------------------------------------

        html_report = f"""
        <html>
        <head>
            <title>SmartSpend AI Report</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background: #050509;
                    color: white;
                    padding: 40px;
                }}

                h1 {{
                    color: #ffffff;
                }}

                .card {{
                    background: #11111A;
                    padding: 20px;
                    margin: 15px 0;
                    border-radius: 12px;
                }}

                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 20px;
                }}

                th, td {{
                    padding: 10px;
                    border-bottom: 1px solid #333;
                    text-align: left;
                }}
            </style>
        </head>

        <body>

            <h1>💰 SmartSpend AI Report</h1>

            <div class="card">
                <h2>Financial Overview</h2>
                <p>Total Spending:
                ₹{total:,.2f}</p>

                <p>Transactions:
                {transaction_count}</p>

                <p>Average Expense:
                ₹{average:,.2f}</p>

                <p>Top Category:
                {top_category}</p>

                <p>Top Category Spending:
                ₹{top_amount:,.2f}</p>

                <p>Monthly Budget:
                ₹{budget:,.2f}</p>

                <p>Current Month Spending:
                ₹{current_spending:,.2f}</p>
            </div>

            <h2>Expense Transactions</h2>

            {df.to_html(
                index=False,
                border=0
            )}

        </body>
        </html>
        """

        st.download_button(
            "🌐 Download Professional HTML Report",
            html_report.encode("utf-8"),
            file_name="smartspend_report.html",
            mime="text/html"
        )

        st.success(
            "✅ Your reports are ready to export."
        )

# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "💰 SmartSpend AI • Personal Finance Intelligence • "
    "Track • Analyze • Detect • Predict • Optimize"
)