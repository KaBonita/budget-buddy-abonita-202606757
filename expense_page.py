import streamlit as st
import datetime
from data_loader import load_expense_data, save_expense_data
from main import ask_month_year, load_month_expenses, load_month_budget

def get_expense_table_data(month_expenses):
    expense_table_data = [[line["date"],
                         line["category"],
                         line["description"], 
                         line["amount"]] 
                         for line in month_expenses]

    return(expense_table_data)

def get_budget_categories(month_year):
    month_budget_data = load_month_budget(month_year)
    budget_categories = []
    for line in month_budget_data:
        budget_categories.append(line["category"])

    return budget_categories


def remove_expense_log(log):
    expense_data = load_expense_data()
    expense_data.remove(log)

    save_expense_data(expense_data)


st.header("Expense History for")
month_year = ask_month_year()
st.divider()
month_expenses = load_month_expenses(month_year)

table_data = get_expense_table_data(month_expenses)

if "editing_index" not in st.session_state:
    st.session_state.editing_index = None

if "adding_entry" not in st.session_state:
    st.session_state.adding_entry = False

if st.session_state.editing_index is not None:
    st.session_state.adding_entry = False
    idx = st.session_state.editing_index
    current_item = month_expenses[idx]

else:
    col_ratios = [1.5, 2, 3, 2]
    header_cols = st.columns(col_ratios)
    for col, header in zip(
        header_cols, ["Date", "Category", "Description", "Amount"]):
        col.markdown(f"**{header}**")
    for index, row in enumerate(table_data):
        cols = st.columns(col_ratios)
        cols[0].write(row[0])
        cols[1].write(row[1])
        cols[2].caption(row[2])
        cols[3].write(row[3])

if st.session_state.adding_entry:
    st.divider()
    st.subheader("Log new expense")

    expense_date = str(st.date_input("Expense made on:"))
    budget_categories = get_budget_categories(month_year)
    category = st.selectbox("In Budget Category", options = budget_categories)
    description = st.text_input("Description:", placeholder = "Write a short description of the expense")
    amount = st.number_input("Amount", step = 10.0)

    new_log = {"date":expense_date,
               "month":month_year,
               "category":category,
               "description":description,
               "amount":amount}
    
    st.write(new_log)

    col_add_confirm, col_add_cancel = st.columns([1, 1])

    if col_add_confirm.button("Add Entry", width = "stretch"):
        st.session_state.adding_entry = False
        st.rerun()

    if col_add_cancel.button("Cancel Add", width = "stretch"):
        st.session_state.adding_entry = False
        st.rerun()

else:
    if st.session_state.adding_entry is False:
        if st.button("Log Expense", width = "stretch"):
            st.session_state.adding_entry = True
            st.rerun()


st.write(month_expenses)