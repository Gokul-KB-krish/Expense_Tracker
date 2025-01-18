import streamlit as st
import pandas as pd
import plotly.express as px
from db_config import get_connection

# Queries
queries = {
    "total_spent_per_category": """
        SELECT category, SUM(amount_paid) AS total_spent
        FROM expenses_data
        GROUP BY category
        ORDER BY total_spent DESC;
    """,
    "total_spent_per_payment_mode": """
        SELECT payment_mode, SUM(amount_paid) AS total_spent
        FROM expenses_data
        GROUP BY payment_mode;
    """,
    "total_cashback_received": """
        SELECT SUM(cashback) AS total_cashback
        FROM expenses_data;
    """,
    "top_5_categories": """
        SELECT category, SUM(amount_paid) AS total_spent
        FROM expenses_data
        GROUP BY category
        ORDER BY total_spent DESC
        LIMIT 5;
    """,
    "spending_per_month": """
        SELECT MONTHNAME(date) AS month, SUM(amount_paid) AS total_spent
        FROM expenses_data
        GROUP BY MONTH(date)
        ORDER BY MONTH(date);
    """,
    "highest_spending_categories": """
        SELECT MONTHNAME(date) AS month, category, SUM(amount_paid) AS total_spent
        FROM expenses_data
        WHERE category IN ('Travel', 'Entertainment', 'Gifts')
        GROUP BY MONTH(date), category
        ORDER BY total_spent DESC;
    """,
    "transactions_with_cashback": """
        SELECT date, category, description, amount_paid, cashback
        FROM expenses_data
        WHERE cashback > 0;
    """,
    "recurring_expenses_data": """
        SELECT MONTHNAME(date) AS month, category, SUM(amount_paid) AS total_spent
        FROM expenses_data
        WHERE category IN ('Insurance', 'Property Taxes')
        GROUP BY MONTH(date), category
        ORDER BY MONTH(date);
    """,
    "monthly_cashback_rewards": """
        SELECT MONTHNAME(date) AS month, SUM(cashback) AS total_cashback
        FROM expenses_data
        GROUP BY MONTH(date)
        ORDER BY MONTH(date);
    """,
    "spending_trend": """
        SELECT MONTHNAME(date) AS month, SUM(amount_paid) AS total_spent
        FROM expenses_data
        GROUP BY MONTH(date)
        ORDER BY MONTH(date);
    """,
    "travel_expenses_data": """
        SELECT category, SUM(amount_paid) AS total_spent
        FROM expenses_data
        WHERE category = 'Transportation'
        GROUP BY category;
    """,
    "grocery_patterns": """
        SELECT DAYNAME(date) AS day, SUM(amount_paid) AS total_spent
        FROM expenses_data
        WHERE category = 'Groceries'
        GROUP BY DAY(date)
        ORDER BY FIELD(day, 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday');
    """,
    "high_low_priority_categories": """
        SELECT category, SUM(amount_paid) AS total_spent
        FROM expenses_data
        GROUP BY category
        ORDER BY total_spent DESC;
    """,
    "highest_percentage_category": """
        SELECT category, SUM(amount_paid) AS total_spent, 
        ROUND((SUM(amount_paid) / (SELECT SUM(amount_paid) FROM expenses_data) * 100), 2) AS percentage
        FROM expenses_data
        GROUP BY category
        ORDER BY percentage DESC
        LIMIT 1;
    """
}

# Helper function to fetch data
def fetch_data(query):
    conn = get_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Streamlit App
st.set_page_config(page_title="Expense Tracker", layout="wide")
st.title("Personal Expense Tracker")

# Sidebar Navigation
st.sidebar.title("Navigation")
options = [
    "Total Spending by Category",
    "Total Spending by Payment Mode",
    "Total Cashback Received",
    "Top 5 Expense Categories",
    "Monthly Spending Overview",
    "Highest Spending in Travel, Entertainment, and Gifts",
    "Transactions with Cashback",
    "Recurring expenses_data",
    "Monthly Cashback Rewards",
    "Spending Trend Over Time",
    "Travel expenses_data Breakdown",
    "Grocery Spending Patterns",
    "High and Low Priority Categories",
    "Highest Percentage Category"
]
choice = st.sidebar.radio("Select an Insight", options)

# Insights Display
if choice == "Total Spending by Category":
    data = fetch_data(queries["total_spent_per_category"])
    st.write("### Total Spending by Category")
    fig = px.bar(data, x="category", y="total_spent", title="Spending by Category", text="total_spent")
    st.plotly_chart(fig)

elif choice == "Total Spending by Payment Mode":
    data = fetch_data(queries["total_spent_per_payment_mode"])
    st.write("### Total Spending by Payment Mode")
    fig = px.pie(data, names="payment_mode", values="total_spent", title="Spending by Payment Mode")
    st.plotly_chart(fig)

elif choice == "Total Cashback Received":
    data = fetch_data(queries["total_cashback_received"])
    st.write("### Total Cashback Received")
    st.metric(label="Total Cashback", value=data.iloc[0, 0])

elif choice == "Top 5 Expense Categories":
    data = fetch_data(queries["top_5_categories"])
    st.write("### Top 5 Expense Categories")
    fig = px.bar(data, x="category", y="total_spent", title="Top 5 Categories", text="total_spent")
    st.plotly_chart(fig)

elif choice == "Monthly Spending Overview":
    data = fetch_data(queries["spending_per_month"])
    st.write("### Monthly Spending Overview")
    fig = px.line(data, x="month", y="total_spent", title="Monthly Spending", markers=True)
    st.plotly_chart(fig)

elif choice == "Highest Spending in Travel, Entertainment, and Gifts":
    data = fetch_data(queries["highest_spending_categories"])
    st.write("### Spending on Travel, Entertainment, and Gifts")
    fig = px.bar(data, x="month", y="total_spent", color="category", barmode="group", title="Category Spending by Month")
    st.plotly_chart(fig)

elif choice == "Transactions with Cashback":
    data = fetch_data(queries["transactions_with_cashback"])
    st.write("### Transactions with Cashback")
    st.dataframe(data)

elif choice == "Recurring expenses_data":
    data = fetch_data(queries["recurring_expenses_data"])
    st.write("### Recurring expenses_data by Month")
    fig = px.bar(data, x="month", y="total_spent", color="category", title="Recurring expenses_data")
    st.plotly_chart(fig)

elif choice == "Monthly Cashback Rewards":
    data = fetch_data(queries["monthly_cashback_rewards"])
    st.write("### Monthly Cashback Rewards")
    fig = px.line(data, x="month", y="total_cashback", title="Monthly Cashback Rewards", markers=True)
    st.plotly_chart(fig)

elif choice == "Spending Trend Over Time":
    data = fetch_data(queries["spending_trend"])
    st.write("### Spending Trend Over Time")
    fig = px.line(data, x="month", y="total_spent", title="Spending Trend", markers=True)
    st.plotly_chart(fig)

elif choice == "Travel expenses_data Breakdown":
    data = fetch_data(queries["travel_expenses_data"])
    st.write("### Travel expenses_data Breakdown")
    st.dataframe(data)

elif choice == "Grocery Spending Patterns":
    data = fetch_data(queries["grocery_patterns"])
    st.write("### Grocery Spending Patterns by Day")
    fig = px.bar(data, x="day", y="total_spent", title="Grocery Spending Patterns", text="total_spent")
    st.plotly_chart(fig)

elif choice == "High and Low Priority Categories":
    data = fetch_data(queries["high_low_priority_categories"])
    st.write("### High and Low Priority Categories")
    st.dataframe(data)

elif choice == "Highest Percentage Category":
    data = fetch_data(queries["highest_percentage_category"])
    st.write("### Category with Highest Percentage of Spending")
    st.metric(label="Highest Percentage Category", value=f"{data.iloc[0, 0]} ({data.iloc[0, 2]}%)")