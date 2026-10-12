import streamlit as st
import datetime

BUDGET_FILENAME = "budget_data.csv"
EXPENSE_FILENAME = "expense_data.csv"

def ask_month_year():
    """
    Asks the user to select a month and a year, then returns it as a string.
    """
    now = datetime.datetime.now()
    curr_month = now.month
    curr_year = now.year

    months = (    "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December")
    
    years = [str(y) for y in range(curr_year - 5, curr_year + 11)]
    default_year_index = years.index(str(curr_year))

    month_col, year_col = st.columns(2)
    
    with month_col:
        selected_month = st.selectbox("",
            months, 
            index=curr_month - 1, 
            label_visibility="collapsed",
            key="selected_month_picker")
        
    with year_col:
        selected_year = st.selectbox("", 
            years, 
            index=default_year_index, 
            label_visibility="collapsed",
            key="selected_year_picker")

    month_year = f"{selected_month} {selected_year}"

    """Reset streamlit session states to prevent errors when switching months while editing."""
    if "previous_month_year" not in st.session_state:
        st.session_state.previous_month_year = month_year
    elif st.session_state.previous_month_year != month_year:
        st.session_state.previous_month_year = month_year
        st.session_state.editing_index = None
        st.session_state.adding_entry = False

    return month_year

# =============================================================================
#                                 EXTRA FEATURE
# =============================================================================

def help_button(type, col = st):
    """
    Writes a button that, once pressed, will give an info message informing the user what 
    a specific section does. 

    type: string determining what type of info message will be displayed.
    col = specific location or column the help button will be in. Set to st as default.
    """
    messages = {"income_sources": "This is where the amount coming from your income sources are edited. If you want to add another income source, you can do this by typing a new one on the income source select box when adding or editing a budget bucket. Don't forget to press the save changes button to prevent your changes from being lost later on.",
                "budget_buckets": "Budget buckets are the different budget categories which you will be spending your income. This is where you can edit your existing budget buckets or add a new one. ",
                "default_buckets": "You can choose the use default buckets button to use the pre-loaded default budget buckets. Alternatively, you can press the generate auto buckets option which will generate a budget bucket based on trends from your recent buckets. Note: You can only use this option if you have already created at least two budget buckets",
                "expense_log": "This is where you log every expense you make. When you log an expense, select the budget bucket where this expense belongs to, write a short description about the expense, the amount spent, then click save once you are done"}
    message = messages[type]

    if col.button("help?", type = "tertiary", key = type):
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
    col1, col2, col3 = st.columns([1, 2, 1])
    col2.image("logo.png", use_container_width=True)
    st.divider()

    curr_page = st.navigation([dashboard, budget, expenses])
    curr_page.run()
    