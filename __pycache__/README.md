💰 SmartSpend AI

Intelligent Personal Finance Management & Spending Analysis

SmartSpend AI is a Python and Streamlit-based personal finance application designed to help users record, analyze, monitor, and understand their spending habits.

It combines expense tracking, interactive analytics, budget monitoring, unusual-expense detection, spending prediction, and an intelligent finance assistant in one modern dashboard.

---

✨ Features

🏠 Smart Dashboard

- Total spending overview
- Number of transactions
- Average expense
- Highest expense
- Remaining budget
- Spending filters
- Recent transactions
- Smart spending insights

➕ Expense Management

- Add daily expenses
- Select expense category
- Select payment method
- Add date and description
- Automatically save expenses to CSV

🎯 Budget Tracking

- Set a monthly budget
- Monitor current-month spending
- Calculate remaining budget
- Display budget usage percentage
- Automatic budget alerts
- Budget vs actual spending visualization

📊 Interactive Analytics

- Monthly spending trends
- Category-wise spending
- Payment-method analysis
- Interactive charts
- Hover-based chart information
- Monthly summaries

🚨 Unusual Expense Detection

SmartSpend automatically identifies unusually high expenses using a statistical threshold based on the historical average and standard deviation.

🔮 Advanced Spending Prediction

The prediction system combines:

- Historical spending trend
- Recent spending behavior
- Weighted recent averages

It generates an estimated spending amount for the next month.

🤖 SmartSpend AI Assistant

The built-in assistant can answer questions about:

- Total spending
- Highest spending category
- Average expense
- Largest transaction
- Budget status
- Spending prediction
- Unusual expenses
- Payment methods
- Spending improvement suggestions

📥 Exportable Reports

Users can export:

- Expense data as CSV
- Professional HTML financial report

---

🛠️ Technologies Used

Technology| Purpose
Python| Core programming
Streamlit| Web application
Pandas| Data processing
NumPy| Numerical analysis
Plotly| Interactive visualizations
CSV| Expense data storage

---

📂 Project Structure

SmartSpend-AI/
│
├── app.py
├── expenses.csv
├── budget.txt
├── requirements.txt
├── README.md
├── .gitignore
│
└── assets/
    └── screenshots/

---

⚙️ Installation

1. Clone the repository

git clone YOUR_GITHUB_REPOSITORY_URL

2. Open the project

cd SmartSpend-AI

3. Install dependencies

pip install -r requirements.txt

4. Run the application

python -m streamlit run app.py

The application will open in your browser.

---

📊 Data Format

SmartSpend AI uses an "expenses.csv" file with the following columns:

Date
Category
Amount
Payment_Method
Description

Example:

2026-01-02,Food,250,UPI,Lunch
2026-01-05,Travel,120,Cash,Bus
2026-01-08,Shopping,800,Card,Clothes

---

🤖 How SmartSpend AI Works

                    ┌─────────────────────┐
                    │   User Adds Expense │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    expenses.csv     │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
       ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
       │   Analysis  │  │   Budget    │  │  Detection  │
       └──────┬──────┘  └──────┬──────┘  └──────┬──────┘
              │                │                │
              └────────────────┼────────────────┘
                               ▼
                    ┌─────────────────────┐
                    │  SmartSpend AI      │
                    │     Assistant       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Insights & Reports  │
                    └─────────────────────┘

---

🔮 Prediction Method

SmartSpend AI uses historical monthly spending to estimate future spending.

The prediction combines:

Historical trend + recent spending behavior

The result should be treated as an estimate rather than a guaranteed future expense.

---

🚨 Unusual Expense Detection

SmartSpend calculates:

Average Expense
        +
2 × Standard Deviation
        =
Detection Threshold

Expenses above this threshold are flagged for review.

---

🎯 Budget Monitoring

The application calculates:

Budget Used % =
(Current Month Spending / Monthly Budget) × 100

Budget status:

- 🟢 Below 50% — Comfortable
- 🔵 50–79% — Monitor spending
- 🟡 80–99% — Warning
- 🔴 100%+ — Budget exceeded

---

📸 Screenshots

Add screenshots of your application here:

![SmartSpend Dashboard](assets/screenshots/dashboard.png)

![Budget Tracking](assets/screenshots/budget.png)

![AI Assistant](assets/screenshots/assistant.png)

![Prediction](assets/screenshots/prediction.png)

---

🚀 Future Improvements

Planned improvements include:

- 🧠 LLM-powered financial assistant
- 🔐 User authentication
- ☁️ Cloud database
- 📱 Mobile-friendly interface
- 📧 Automated spending alerts
- 📈 More advanced forecasting models
- 🏦 Bank transaction integration
- 📊 Personalized financial recommendations
- 🗓️ Recurring expense detection
- 🎯 Financial goal tracking

---

🎓 Project Purpose

This project demonstrates practical applications of:

- Data Science
- Data Analysis
- Statistical Analysis
- Data Visualization
- Machine Learning concepts
- Python programming
- Streamlit application development
- AI-assisted financial analysis

---

👩‍💻 Author

Vartika Yadav

B.Sc. Data Science Student

---

⭐ Acknowledgement

SmartSpend AI was created as an educational and portfolio project to demonstrate how data analytics and intelligent automation can be combined to build a practical personal finance application.

---

📄 License

This project is intended for educational and portfolio purposes.