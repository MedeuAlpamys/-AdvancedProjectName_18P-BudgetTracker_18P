import streamlit as st
import pandas as pd
from datetime import date

from database import init_db
from auth import register_user, login_user
from utils import add_transaction, get_transactions

st.set_page_config(page_title="Personal Budget Tracker")

init_db()

# ============== LOGIN ==============
if "user_id" not in st.session_state:
    st.title("🧾 Budget Tracker — Login")
    menu = st.radio("Choose action", ["Login", "Register"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if menu == "Register":
        if st.button("Register"):
            if not username.strip() or not password:
                st.error("Username and password cannot be empty.")
            elif not username.endswith("@stu.sdu.edu.kz"):
                st.error("Invalid username!")
            elif register_user(username, password):
                st.success("User registered! Please log in.")
            else:
                st.error("User already exists.")
    else:
        if st.button("Login"):
            if not username.strip() or not password:
                st.error("Username and password cannot be empty.")
            else:
                user_id = login_user(username, password)
                if user_id:
                    st.session_state.user_id = user_id
                    st.rerun()
                else:
                    st.error("Incorrect username or password.")
    st.stop()

# ============== MAIN SCREEN ==============
st.sidebar.success(f"Logged in as user ID: {st.session_state.user_id}")
st.title("💰 Budget Tracker")

tab1, tab2 = st.tabs(["📥 Input", "📊 Report"])

with tab1:
    st.subheader("Add Transaction")
    type_ = st.selectbox("Type", ["", "income", "expense"])
    category = st.selectbox("Category", ["", "Salary", "Food", "Housing", "Transport", "Other"])
    amount = st.number_input("Amount", min_value=0.00, step=0.01)
    date_ = st.date_input("Date", value=date.today())
    if st.button("Add"):
        if not type_ or not category:
            st.error("Please select type and category.")
        elif amount <= 0:
            st.error("Amount must be greater than 0.")
        else:
            add_transaction(st.session_state.user_id, type_, category, amount, date_.isoformat())
            st.success("Transaction added!")

with tab2:
    st.subheader("Monthly Report")
    df = get_transactions(st.session_state.user_id)
    if df.empty:
        st.info("No data available.")
    else:
        df['date'] = pd.to_datetime(df['date'])
        df['month'] = df['date'].dt.to_period('M').astype(str)

        monthly = df.groupby(['month', 'type'])['amount'].sum().unstack(fill_value=0)
        monthly['savings'] = monthly.get('income', 0) - monthly.get('expense', 0)

        st.dataframe(monthly)

        st.line_chart(monthly)

        st.write("📈 Total Savings: ", monthly['savings'].sum())
