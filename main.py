import streamlit as st
import datetime
import csv
import os

from data_loader import load_budget_data, load_expense_data

BUDGET_FILENAME = "budget_data.csv"
EXPENSE_FILENAME = "expense_data.csv"

def ask_month_year():
    curr_month = datetime.datetime.now().month
    curr_year = datetime.datetime.now().year

    month_col, year_col = st.columns(2)
    with month_col:
        month = st.selectbox("", ("January", "February",
                            "March", "April", "May", "June", "July", "August",
                            "September", "October", "November", "December"),
                            index = curr_month - 1)
    with year_col:
        year = str(st.selectbox("", (tuple(range(1, 10000))),
                                index = curr_year - 1))
    month_year = month + " " + year

    return month_year

def load_month_budget(month_year):
    budget_data = load_budget_data()
    month_budget = []

    for line in budget_data:
        if line["month"] == month_year:
            month_budget.append(line)

    return month_budget

def load_month_expenses(month_year):
    expense_data = load_expense_data()
    month_expenses = []

    for line in expense_data:
        if line["month"] == month_year:
            month_expenses.append(line)

    return month_expenses

dashboard = st.Page("dashboard_page.py", title = "Dashboard")
budget = st.Page("budget_page.py", title = "Budget")
expenses = st.Page("expense_page.py", title = "Expenses")

if __name__ == "__main__":
    curr_page = st.navigation([dashboard, budget, expenses])
    curr_page.run()