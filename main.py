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

def help_button(type, loc = st):
    messages = {"income_sources": "This is where the amount coming from your income sources are edited. If you want to add another income source, you can do this by typing a new one on the income source select box when adding or editing a budget bucket. Don't forget to press the save changes button to prevent your changes from being lost later on.",
                "budget_buckets": "Budget buckets are the different budget categories which you will be spending your income. This is where you can edit your existing budget buckets or add a new one. ",
                "default_buckets": "You can choose the use default buckets button to use the pre-loaded default budget buckets. Alternatively, you can press the generate auto buckets option which will generate a budget bucket based on trends from your recent buckets. Note: You can only use this option if you have already created at least two budget buckets",
                "expense_log": "This is where you log every expense you make. When you log an expense, select the budget bucket where this expense belongs to, write a short description about the expense, the amount spent, then click save once you are done"}
    message = messages[type]

    if loc.button("help?", type = "tertiary", key = type):
        message_col, done_col = st.columns([10, 1])
        with message_col:
            st.info(message)
        with done_col:
            if st.button("done"):
                st.rerun()

dashboard = st.Page("dashboard_page.py", title = "Dashboard")
budget = st.Page("budget_page.py", title = "Budget")
expenses = st.Page("expense_page.py", title = "Expenses")

if __name__ == "__main__":
    curr_page = st.navigation([dashboard, budget, expenses])
    curr_page.run()
    