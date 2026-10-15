from data_loader import load_expense_data, save_expense_data
from budget_page import load_month_budget, get_budget_categories
from main import ask_month_year, help_button

import streamlit as st

# =============================================================================
# DATA LOADING FUNCTIONS
# =============================================================================

def load_month_expenses(month_year):
    """
    Loads all expense records of expense_data.csv filtered by a specific month.

    month_year: string of a month and a year, e.g., "January 2027"
    Returns a list of dictionaries
    """
    expense_data = load_expense_data()
    month_expenses = []

    for line in expense_data:
        if line["month"] == month_year:
            month_expenses.append(line)

    return month_expenses

def get_expense_table_data(month_expenses):
    """
    Formats each line of month_expenses into the form [date, category, description, amount]
    for proper displaying in the expense table.

    month_expenses: list of dictionaries
    returns a list of lists.
    """
    expense_table_data = [[line["date"],
                         line["category"],
                         line["description"], 
                         line["amount"]] 
                         for line in month_expenses]

    return(expense_table_data)

def get_total_spent(month_year):
    """
    gets the total amount of money spent in a specific month.

    month_year: string of a month and a year, e.g., "January 2027"
    returns a floating point number.
    """
    month_expenses = load_month_expenses(month_year)
    total_expenses = 0
    for line in month_expenses:
        amount = line["amount"]
        total_expenses += amount

    return total_expenses

# =============================================================================
# DATA SAVING FUNCTIONS
# =============================================================================

def check_log_validity(date, month_year, category, description, amount):
    """
    An input handling method that ensures the newly created data is valid. Checks date, month_year, category,
    description, and amount, which are the values of the new log, and if any of them are invalid, displays a
    corresponding error message. 

    Returns False if the new log is invalid, and True if valid.
    """
    year = int(month_year.split()[1])
    month = month_year.split()[0]
    month_number = {"January": 1, "February": 2, "March": 3,
                     "April":4, "May":5, "June":6, "July":7,
                     "August":8, "September":9, "October":10,
                     "November":11, "December":12}.get(month)
    input_month = int(date[5:7])
    input_year = int(date[0:4])

    if (month_number, year) != (input_month, input_year):
        st.error(f"{date} is not within {month_year}. Change your inputted date to match that of your selected month range then try again.")
        return False
    elif not category:
        st.error(f"Your category cannot be empty. Select a category then try again. If there are no categories, you must first set up your budget categories for {month_year} in the budget panel.")
        return False
    elif not description:
        st.error("Your description is empty. Write something in the log description then try again.")
        return False
    elif amount == 0:
        st.error("The value of the expense cannot be 0. Please try again.")
        return False
    elif amount < 0:
        st.error("The value of the expense cannot be negative. Please try again.")
    else:
        return True

def new_expense_entry(new_value):
    """
    Saves the new expense entry into the csv file. Ensures that the new entry is inserted within other logs of the same
    month, sorted by day, to keep the organization of the file.

    new_value: dict
    """
    expense_data = load_expense_data()
    month_year = new_value["month"]
    r_index = 0
    entry_day = int(new_value["date"][8:10])

    for line in list(reversed(expense_data)):
        if line["month"] == month_year:
            break
        r_index += 1
    index = len(expense_data) - r_index

    if expense_data[index-1]["month"] == month_year and entry_day < int(expense_data[index-1]["date"][8:10]):
        index -= 1
    
    expense_data.insert(index, new_value)

    save_expense_data(expense_data)

# =============================================================================
# UI COMPONENT FUNCTIONS
# =============================================================================

def render_expense_history_table(month_year, table_data):
    """
    Renders the table displaying previously logged expenses for the selected month.
    """
    if table_data:
        st.subheader(f"{month_year} Expense Log:")
        st.write("")
        col_ratios = [1.5, 2, 3, 2]
        header_cols = st.columns(col_ratios)
        
        for col, header in zip(header_cols, ["Date", "Category", "Description", "Amount"]):
            col.markdown(f"**{header}**")
            
        for index, row in enumerate(table_data):
            cols = st.columns(col_ratios)
            cols[0].write(row[0])
            cols[1].write(row[1])
            cols[2].caption(row[2])
            cols[3].write(f"₱{str(row[3])}")
            
        st.divider()
    else:
        st.info(f"You currently have no logged expenses for {month_year}. Log one?")


# =============================================================================
# UI COMPONENT FUNCTIONS
# =============================================================================

def render_add_expense_form(month_year):
    """
    Renders the form used to log a new expense entry.
    """
    st.divider()
    st.subheader("Log new expense")

    expense_date = str(st.date_input("Expense made on:"))
    budget_categories = get_budget_categories(month_year)
    category = st.selectbox("In Budget Category", options=budget_categories)
    description = st.text_input("Description:", 
        placeholder="Write a short description of the expense")
    amount = st.number_input("Amount", step=10.0, value=10.0)

    new_log = {"date": expense_date,
        "month": month_year,
        "category": category,
        "description": description,
        "amount": amount}

    col_add_confirm, col_add_cancel = st.columns(2)

    if col_add_confirm.button("Log Expense", width="stretch"):
        while check_log_validity(expense_date, month_year, category, description, amount):
            new_expense_entry(new_log)
            st.session_state.adding_entry = False
            st.rerun()

    if col_add_cancel.button("Cancel", width="stretch"):
        st.session_state.adding_entry = False
        st.rerun()


# =============================================================================
# MAIN EXPENSE PAGE ROUTINE
# =============================================================================

if __name__ == "__main__":
        
    st.header("Manage expenses for")
    month_year = ask_month_year()
    st.divider()
    
    month_expenses = load_month_expenses(month_year)
    table_data = get_expense_table_data(month_expenses)

    # Initialize session state for
    if "adding_entry" not in st.session_state:
        st.session_state.adding_entry = False

    # 1. Expense Log History Table
    render_expense_history_table(month_year, table_data)

    # 2. Add Expense Form or Trigger Button
    if st.session_state.adding_entry:
        render_add_expense_form(month_year)
    else:
        if st.button("Log New Expense", width="stretch"):
            st.session_state.adding_entry = True
            st.rerun()

    # 3. Page Footer Help Action
    placeholder, col_help = st.columns([10, 1])
    help_button("expense_log", col_help)
