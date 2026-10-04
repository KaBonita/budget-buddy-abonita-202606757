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

def read_csv_row(filename, target_row_num):
    with open(filename, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for current_row_num, row in enumerate(reader, start=1):
            if current_row_num == target_row_num:
                return row
    return None

def safe_replace(temp_file, filename, retries=5, delay=0.2):
    for i in range(retries):
        try:
            os.replace(temp_file, filename)
            return
        except PermissionError:
            if i == retries - 1:
                raise
            time.sleep(delay)

def replace_csv_row(filename, row_index, new_row):
    row_index -= 1
    with open(filename, "r", newline="", encoding="utf-8") as file:
        rows = list(csv.reader(file))

    if row_index < 0 or row_index >= len(rows):
        print("Invalid row index")
        return

    rows[row_index] = new_row

    temp_file = filename + ".tmp"

    with open(temp_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(rows)

    safe_replace(temp_file, filename)

def len_csv(filename):
    with open(filename, "r", newline="") as file:
        return sum(1 for line in file)

dashboard = st.Page("dashboard_page.py", title = "Dashboard")
budget = st.Page("budget_page.py", title = "Budget")
expenses = st.Page("expense_page.py", title = "Expenses")

if __name__ == "__main__":
    curr_page = st.navigation([dashboard, budget, expenses])
    curr_page.run()