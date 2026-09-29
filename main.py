import streamlit as st

dashboard = st.Page("dashboard_page.py", title = "Dashboard")
budget = st.Page("budget_page.py", title = "Budget")
expenses = st.Page("expense_page.py", title = "Expenses")

curr_page = st.navigation([dashboard, budget, expenses])
curr_page.run()
