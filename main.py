import streamlit as st
import time
import csv
import os

from data_loader import load_budget_data

BUDGET_FILENAME = "budget_data.csv"
EXPENSE_FILENAME = "expense_data.csv"

def load_month_budget(month_year, filename = BUDGET_FILENAME):
    budget_data = load_budget_data(BUDGET_FILENAME)
    month_budget = []

    for line in budget_data:
        if line["month"] == month_year:
            month_budget.append(line)

    return month_budget

dashboard = st.Page("dashboard_page.py", title = "Dashboard")
budget = st.Page("budget_page.py", title = "Budget")
expenses = st.Page("expense_page.py", title = "Expenses")

if __name__ == "__main__":
    curr_page = st.navigation([dashboard, budget, expenses])
    curr_page.run()