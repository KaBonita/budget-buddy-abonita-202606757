from data_loader import load_budget_data, save_budget_data
from main import ask_month_year, help_button

import streamlit as st

# =============================================================================
# DATA LOADING FUNCTIONS
# =============================================================================

def load_month_budget(month_year):
    """
    Loads all budget data of budget_data.csv filtered by a specific month.

    month_year: string of a month and a year, e.g., "January 2027"
    Returns a list of dictionaries
    """
    budget_data = load_budget_data()
    month_budget = []

    for line in budget_data:
        if line["month"] == month_year:
            month_budget.append(line)

    return month_budget

def get_budget_table_data(month_budget_data):
    """
    Formats each line of month_budget_data into the form [category, income source, planned amount]
    for proper displaying in the expense table.

    month_budget_data: list of dictionaries
    returns a list of lists.
    """
    budget_table_data = [[line["category"], 
                          line["income_source"], 
                          line["planned_amount"]] 
                          for line in month_budget_data ]

    return budget_table_data

def get_income_sources(month_year):
    """
    Returns all income sources used in a specific month. Returns a list of lists, where
    all inner lists have the form [income source, income amount]

    month_year: string of a month and a year, e.g., "January 2027"
    """
    month_budget_data = load_month_budget(month_year)
    income_sources = []

    for line in month_budget_data:
        if [line["income_source"], line["income"]] not in income_sources:
            new_income_source = [line["income_source"], line["income"]]
            income_sources.append(new_income_source)

    return income_sources

def get_total_income(month_year):
    """
    Retuns the total income used in a specific month. 

    month_year: string of a month and a year, e.g., "January 2027"
    """
    income_sources = get_income_sources(month_year)
    total_income = 0

    for income_source in income_sources:
        total_income += income_source[1]

    return total_income

def get_total_planned(month_year):
    """
    Returns the total planned amount used in a specific month.

    month_year: string of a month and a year, e.g., "January 2027"
    """
    month_budget_data = load_month_budget(month_year)
    total_planned = 0

    for line in month_budget_data:
        total_planned += line["planned_amount"]

    return total_planned

def get_budget_categories(month_year = "all"):
    """
    Returns a list of all budget categories used in a specific month. If no month
    was given, it returns all budget categories used across all months.

    month_year: string of a month and a year, e.g., "January 2027"
    """
    if month_year == "all":
        budget_data = load_budget_data()
    elif month_year:
        budget_data = load_month_budget(month_year)

    budget_categories = []
    for line in budget_data:
        category = line["category"]
        if category not in budget_categories:
            budget_categories.append(category)

    return budget_categories

def get_budget_months():
    """
    Returns a list all months with planned budget buckets, ordered by the recency of the
    month's bucket creation.
    """
    budget_data = load_budget_data()
    months = []

    for line in budget_data:
        month = line["month"]
        if month not in months:
            months.append(month)

    return months

# =============================================================================
# DATA SAVING FUNCTIONS
# =============================================================================

def check_bucket_validity(month_year ,income_source, category, planned_amount):
    """
    An input handling method that ensures the newly bucket data is valid. Checks income sources,
    category, planned amount which are the values of the new bucket, and if any of them are
    invalid, displays a corresponding error message. 

    Returns False if the new log is invalid, and True if valid.
    """
    budget_categories = get_budget_categories(month_year)

    if not income_source:
        st.error("Your income source cannot be empty. Select an income source then try again. ")
        return False
    elif not category:
        st.error("Your category must have a name. Type a category name then try again.")
        return False
    elif planned_amount == 0:
        st.error("The value of the planned amount cannot be 0. Please try again.")
        return False
    elif planned_amount < 0:
        st.error("The value of the planned amount cannot be negative. Please try again.")
    else:
        return True

def replace_budget_entry(replace_item, with_item):
    """
    Finds the item with value replace_item in the budget file then puts with_item in its place.
    """
    budget_data = load_budget_data()

    if with_item:
        index = budget_data.index(replace_item)
        budget_data[index] = with_item
    else:
        budget_data.remove(replace_item)

    save_budget_data(budget_data)

def replace_income_values(month_year, income_category, new_value):
    """
    Replaces all set income values for a specific income category in a specific month.

    month_year: string of a month and a year, e.g., "January 2027"
    income_category: string of the name of the income category
    new_value: floating point number of the new value. 
    """
    budget_data = load_budget_data()
    
    for line in budget_data:
        if line["month"] == month_year and line["income_source"] == income_category:
            line["income"] = new_value

    save_budget_data(budget_data)

def new_budget_entry(new_value):
    """
    Saves the new budget entry into the csv file. Ensures that the new entry is inserted below
    other entries of the same month to keep them grouped for file organization.

    new_value: dict
    """
    budget_data = load_budget_data()
    month_year = new_value["month"]
    r_index = 0

    for line in list(reversed(budget_data)):
        if line["month"] == month_year:
            break
        r_index += 1

    index = len(budget_data) - r_index
    budget_data.insert(index, new_value)

    save_budget_data(budget_data)

# =============================================================================
# UI COMPONENT FUNCTIONS
# =============================================================================

def render_income_section(month_year, income_sources):
    """
    Renders the income sources management section.
    """
    st.subheader("Income")
    st.write("")
    income_source_col, income_col = st.columns(2)
    
    with income_source_col:
        st.markdown("**Income Source**")

        for line in income_sources:
            income_source = line[0]
            st.write("")
            st.write("")
            st.write(income_source)
            st.write("")

    with income_col:
        st.markdown("**Expected Amount**")

        for income_source in income_sources:
            income_source[1] = st.number_input(
                None, 
                value=income_source[1], 
                step=100.0, 
                key=f"inc_input_{income_source[0]}"
            )

    st.write("")
    col_save, col_help = st.columns([10, 1])

    with col_save:
        if income_sources:
            if st.button("Save Changes", key="Save_Income"):
                for income_source in income_sources:
                    replace_income_values(month_year, income_source[0], income_source[1])
                st.rerun()
    
    help_button("income_sources", col_help)
    st.divider()


def render_edit_bucket_form(month_year, month_budget_data, income_sources, income_options):
    """
    Renders the edit form for an existing budget bucket.
    """
    st.session_state.adding_entry = False
    index = st.session_state.editing_index
    current_item = month_budget_data[index]

    st.subheader("Editing Budget Bucket")
    edit_category = st.text_input("Edit Category", value=current_item["category"])

    current_source = current_item["income_source"]
    source_index = (income_options.index(current_source)
        if current_source in income_options
        else 0)
    edit_income_source = st.selectbox("Edit Income Source", 
        options=income_options, 
        index=source_index,
        accept_new_options=True)

    edit_planned_amount = st.number_input("Edit Planned Amount",
        value=float(current_item["planned_amount"]),
        step=100.0,)
    
    col_save, col_cancel = st.columns([1, 1])

    if col_save.button("Save Changes", width="stretch"):
        new_item = month_budget_data[index].copy()
        new_item["category"] = edit_category
        new_item["income_source"] = edit_income_source
        new_item["planned_amount"] = edit_planned_amount
        
        for income_source in income_sources:
            if new_item["income_source"] == income_source[0]:
                new_item["income"] = income_source[1]
                break
            else:
                new_item["income"] = 100.0
                
        if check_bucket_validity(month_year, edit_income_source, edit_category, edit_planned_amount):
            replace_budget_entry(month_budget_data[index], new_item)
            st.session_state.editing_index = None
            st.rerun()

    with col_cancel:
        if st.button("Remove Budget Bucket", width="stretch", type="primary"):
            replace_budget_entry(month_budget_data[index], None)
            st.session_state.editing_index = None
            st.rerun()
            
    if st.button("Cancel", width="stretch"):
        st.session_state.editing_index = None
        st.rerun()


def render_bucket_table(month_budget_data):
    """
    Renders the table of planned budget buckets with Edit action buttons.
    """
    st.subheader("Planned Budget Buckets")
    st.write("")
    
    table_data = [[line["category"], line["income_source"], line["planned_amount"]] for line in month_budget_data]
    col_ratios = [2, 2, 2, 1]
    header_cols = st.columns(col_ratios)
    
    for col, header in zip(header_cols, ["Category", "Income Source", "Planned Amount", "Actions"]):
        col.markdown(f"**{header}**")
        
    st.write("")
    for index, row in enumerate(table_data):
        cols = st.columns(col_ratios)
        cols[0].write(row[0])
        cols[1].write(row[1])
        cols[2].write(f"₱{str(row[2])}")

        if cols[3].button("Edit", key=f"edit_btn_{index}"):
            st.session_state.editing_index = index
            st.rerun()


def render_add_bucket_form(month_year, income_sources, income_options):
    """
    Renders the creation form for adding a new budget bucket.
    """
    st.divider()
    st.subheader("Add New Budget Bucket")

    add_category = st.text_input("Bucket Name", placeholder="e.g., Transportation")
    add_income_source = st.selectbox("Income Source", options=income_options, accept_new_options=True)
    add_planned_amount = st.number_input("Planned Amount", value=100.0, step=100.0)
    add_income = 100.0
    
    for income_source in income_sources:
        if add_income_source == income_source[0]:
            add_income = income_source[1]
            break

    new_item = { "month": month_year, 
        "income_source": add_income_source,
        "income": add_income, 
        "category": add_category,
        "planned_amount": add_planned_amount}

    col_add_confirm, col_add_cancel = st.columns([1, 1])

    if col_add_confirm.button("Add Entry", width="stretch"):
        if check_bucket_validity(month_year, add_income_source, add_category, add_planned_amount):
            new_budget_entry(new_item)
            st.session_state.adding_entry = False
            st.rerun()

    if col_add_cancel.button("Cancel Add", width="stretch"):
        st.session_state.adding_entry = False
        st.rerun()


def render_budget_summary(month_year):
    """
    Renders total income, total planned amount, and status warnings at the bottom.
    """
    total_income_col, total_planned_col = st.columns(2)
    
    with total_income_col:
        total_income = get_total_income(month_year)
        st.caption(f"Total Income: ₱{total_income}")
        
    with total_planned_col:
        total_planned = get_total_planned(month_year)
        st.caption(f"Total Planned: ₱{total_planned}")

    if total_planned > total_income:
        st.warning(
            f"Warning: Your planned total exceeds your total income by ₱{total_planned - total_income}. "
            f"Either increase your total income or reduce your total planned amount to fix this."
        )
    elif total_income > total_planned:
        st.info(f"Tip: You still have ₱{total_income - total_planned} to allocate into your budget!")


def render_empty_budget_state(month_year):
    """
    Renders options when no budget buckets exist for the selected month.
    """
    st.info(f"No budget buckets yet for {month_year}. Use default budget bucket?")
    st.write("")
    
    default_col, auto_col = st.columns(2)
    with default_col:
        if st.button("Use default buckets", width="stretch"):
            create_default_buckets(month_year)
            st.rerun()
            
    with auto_col:
        amount_of_buckets = len(get_budget_months())

        if st.button("Generate auto bucket", width="stretch", disabled=True if amount_of_buckets < 2 else False):
            create_auto_buckets(month_year)
            st.rerun()

# =============================================================================
# BUCKET CREATION FUNCTIONS
# =============================================================================

def create_default_buckets(month_year):
    """
    A function that, once called, will insert a new set of values of default buckets for the selected month in the
    csv file.
    """
    budget_data = load_budget_data()
    default_buckets = [{"month":month_year, "income_source": "Allowance", "income": 15000, "category": "Miscellaneous", "planned_amount": 1000.0},
        {"month":month_year, "income_source": "Allowance", "income":15000, "category": "Entertainment", "planned_amount": 1500.0},
        {"month":month_year, "income_source": "Allowance", "income":15000, "category": "Savings", "planned_amount": 3000.0},
        {"month":month_year, "income_source": "Allowance", "income":15000, "category": "Utilities", "planned_amount": 1500.0},
        {"month":month_year, "income_source": "Allowance", "income":15000, "category": "Transportation", "planned_amount": 2000.0},
        {"month":month_year, "income_source": "Allowance", "income":15000, "category": "Food", "planned_amount": 4000.0}]

    for bucket in default_buckets:
        budget_data.insert(0, bucket)

    save_budget_data(budget_data)

# =============================================================================
#                                 EXTRA FEATURE
# =============================================================================

def get_highest_scored(dictionary):
    """
    Returns the highest scored item in a dictionary. each item in the dictionary is in the form
    item: score.

    EXAMPLE:
    >>>dictionary = {"CJ": 60.0 "Keith": 75.0, "Steven": 50.0}

    >>>get_highest_scored(dictionary)
    "Keith"

    """
    list_items = list(dictionary.keys())
    highest_scored = None
    highest_score = 0

    for item in list_items:
        score = dictionary[item]
        if score > highest_score:
            highest_score = score
            highest_scored = item

    return highest_scored

def create_auto_buckets(month_year):
    """
    Generates buckets based on trends from your past month buckets, and inserts it to the budget file.
    It utilizes a category scoring algorithm to determine which categories will be used in the auto buckets.

    
    Scoring system for categories:
    Distance - an integer value which measures how many months are between some month and the current month based
        on get_budget_months.

    dis = d(month) #distance of some month to the current month_year.

    score function:
    s(dis) = 100/(x+1) #Behavior: s(d) is higher for lower "nearer" values of d then decreases for larger values.

    total score(category) = s(d(month1)) + s(d(month2)) + s(d(month3)) + ... for every month the category occurs in.

    If the total score for a category is greater than 75, it will be added as a category for auto buckets.
    """
    budget_data = load_budget_data()
    budget_categories = get_budget_categories()

    budget_months = get_budget_months()
    distance_table = {month: budget_months.index(month) + 1 for month in budget_months}
    winning_categories = []

    for budget_category in budget_categories:
        score = 0

        for line in budget_data:
            if line["category"] == budget_category:
                month = line["month"]
                distance = distance_table[month]
                score += 100/(distance + 1)

        if score >= 75:
            winning_categories.append(budget_category)

    """
    Once all auto categories have been established, we now determine what the income source and planned amount values
    it will take. Each income source and planned amount for every category will be scored with the same scoring system
    as the categories:

    total score(income source or planned amount) = s(d(month1)) + s(d(month2)) + s(d(month3)) + ... for every month the
    income source or planned amount of a specific category occurs in.

    Once all values of income sources and planned amounts have been scored, take only the highest scored values for income
    source and planned amount among all of them, and those chosen values will be used as the values correspoding to that category.

    Do this for all categories, and you have generated your auto buckets.
    """
    auto_buckets = []
    for category in winning_categories:

        income_sources = {}
        for line in budget_data:
            month = line["month"]
            distance = distance_table[month]

            if line["category"] == category:
                income_source = (line["income_source"], line["income"])

                if income_source not in income_sources:
                    score = 100/(distance + 1)
                    income_sources[income_source] = score
                else:
                    curr_score = income_sources[income_source]
                    score = 100/(distance + 1)
                    income_sources[income_source] = curr_score + score

        winning_income_source = get_highest_scored(income_sources)

        planned_amounts = {}
        for line in budget_data:
            month = line["month"]
            distance = distance_table[month]

            if line["category"] == category:
                planned_amount = line["planned_amount"]

                if planned_amount not in planned_amounts:
                    score = 100/(distance + 1)
                    planned_amounts[planned_amount] = score
                else:
                    curr_score = planned_amounts[planned_amount]
                    score = 100/(distance + 1)
                    planned_amounts[planned_amount] = curr_score + score

        winning_planned_amount = get_highest_scored(planned_amounts)

        new_item = {"month": month_year,
                    "income_source": winning_income_source[0],
                    "income": winning_income_source[1], 
                    "category": category,
                    "planned_amount": winning_planned_amount}

        auto_buckets.insert(0, new_item)

    """s
    Insert the auto buckets into the budget data file, then save.
    """
    for bucket in auto_buckets:
        budget_data.insert(0, bucket)

    save_budget_data(budget_data)


# =============================================================================
# MAIN BUDGET PAGE ROUTINE
# =============================================================================

if __name__ == "__main__":
    st.header("Manage budget for")
    month_year = ask_month_year()
    month_budget_data = load_month_budget(month_year)

    st.divider()
    table_data = get_budget_table_data(month_budget_data)

    if table_data:
        # 1. Income Sources Section
        income_sources = get_income_sources(month_year)
        render_income_section(month_year, income_sources)

        # 2. Session State Initialization
        if "editing_index" not in st.session_state:
            st.session_state.editing_index = None

        if "adding_entry" not in st.session_state:
            st.session_state.adding_entry = False

        income_options = [income_source[0] for income_source in income_sources]

        # 3. Edit Form or Table Display
        if st.session_state.editing_index is not None:
            render_edit_bucket_form(month_year, month_budget_data, income_sources, income_options)
        else:
            render_bucket_table(month_budget_data)

        # 4. Add Entry Form or Add Button Controls
        if st.session_state.adding_entry and st.session_state.editing_index is None:
            render_add_bucket_form(month_year, income_sources, income_options)
        else:
            if st.session_state.editing_index is None:
                if st.button("Add Budget Bucket", width="stretch"):
                    st.session_state.adding_entry = True
                    st.rerun()

        placeholder, col_help = st.columns([10, 1])
        help_button("budget_buckets", col_help)

        st.divider()

        # 5. Financial Summary Callout
        render_budget_summary(month_year)

    else:
        # Empty State
        render_empty_budget_state(month_year)
       
        placeholder, col_help = st.columns([10, 1])
        help_button("default_buckets", col_help)
