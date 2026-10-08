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

def check_item_validity(date, month_year, category, description, amount):
    year = int(month_year.split()[1])
    month = month_year.split()[0]
    month_number = {"January": 1, "February": 2, "March": 3,
                     "April":4, "May":5, "June":6, "July":7,
                     "August":8, "September":9, "October":10,
                     "November":11, "December":12}.get(month)
    input_month = int(date[5:7])
    input_year = int(date[0:4])

    if (month_number, year) != (input_month, input_year):
        st.warning(f"{date} is not within {month_year}. Change your inputted date to match that of your selected month range then try again.")
        return False
    elif not category:
        st.warning(f"Your category cannot be empty. Select a category then try again. If there are no categories, you must first set up your budget categories for {month_year} in the budget panel.")
        return False
    elif not description:
        st.warning("Your description is empty. Write something in the log description then try again.")
        return False
    elif amount == 0:
        st.warning("The value of the expense cannot be 0. Please try again.")
        return False
    elif amount < 0:
        st.warning("The value of the expense cannot be negative. Please try again.")
    else:
        return True

def new_expense_entry(new_value):
    expense_data = load_expense_data()
    month_year = new_value["month"]
    r_index = 0
    entry_day = int(new_value["date"][8:10])
    for line in list(reversed(expense_data)):
        if line["month"] == month_year:
            break
        r_index += 1
    index = len(expense_data) - r_index
    while expense_data[index-1]["month"] == month_year and entry_day < int(expense_data[index-1]["date"][8:10]):
        index -= 1
    
    expense_data.insert(index, new_value)

    save_expense_data(expense_data)


st.header("Manage expenses for:")
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
    st.subheader(f"{month_year} Expense Log:")
    st.write("")
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
    amount = st.number_input("Amount", step = 10.0, value = 10.0)

    new_log = {"date":expense_date,
               "month":month_year,
               "category":category,
               "description":description,
               "amount":amount}

    col_add_confirm, col_add_cancel = st.columns([1, 1])

    if col_add_confirm.button("Add Entry", width = "stretch"):
        if check_item_validity(expense_date, month_year, category, description, amount):
            new_expense_entry(new_log)
            st.session_state.adding_entry = False
            st.rerun()

    if col_add_cancel.button("Cancel Add", width = "stretch"):
        st.session_state.adding_entry = False
        st.rerun()

else:
    if st.session_state.adding_entry is False:
        if st.button("Log New Expense", width = "stretch"):
            st.session_state.adding_entry = True
            st.rerun()

st.divider()