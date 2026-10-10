from data_loader import load_budget_data, save_budget_data
from main import load_month_budget, ask_month_year
import streamlit as st
import datetime
import time

def get_budget_table_data(month_budget_data):
    budget_table_data = [[line["category"], 
                          line["income_source"], 
                          line["planned_amount"]] 
                          for line in month_budget_data ]

    return budget_table_data

def replace_income_values(month_year, income_category, new_value):
    budget_data = load_budget_data()
    for line in budget_data:
        if line["month"] == month_year and line["income_source"] == income_category:
            line["income"] = new_value

    save_budget_data(budget_data)

def replace_budget_entry(replace_item, with_item):
    budget_data = load_budget_data()
    if with_item:
        index = budget_data.index(replace_item)
        budget_data[index] = with_item
    else:
        budget_data.remove(replace_item)

    save_budget_data(budget_data)

def new_budget_entry(new_value):
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

def get_income_sources(month_year):
    month_budget_data = load_month_budget(month_year)
    income_sources = []
    for line in month_budget_data:
        if [line["income_source"], line["income"]] not in income_sources:
            new_income_source = [line["income_source"], line["income"]]
            income_sources.append(new_income_source)

    return income_sources

def get_total_income(month_year):
    income_sources = get_income_sources(month_year)
    total_income = 0
    for income_source in income_sources:
        total_income += income_source[1]

    return total_income

def get_total_planned(month_year):
    month_budget_data = load_month_budget(month_year)
    total_planned = 0
    for line in month_budget_data:
        total_planned += line["planned_amount"]

    return total_planned

def get_budget_categories(month_year):
    month_budget_data = load_month_budget(month_year)
    budget_categories = []
    for line in month_budget_data:
        category = line["category"]
        budget_categories.append(category)

    return budget_categories

def get_planned_amounts(month_year):
    month_budget_data = load_month_budget(month_year)
    planned_amounts = []
    for line in month_budget_data:
        planned = line["planned_amount"]
        planned_amounts.append(planned)

    return planned_amounts

#Ask month and year

if __name__ == "__main__":

    st.header("Manage budget for")
    month_year = ask_month_year()
    month_budget_data = load_month_budget(month_year)

    st.divider()


    #income sources section
    income_sources = get_income_sources(month_year)

    st.subheader("Income Sources")
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
            income_source[1] = st.number_input(None, value = income_source[1], step = 100.0, key = income_source)

    if income_sources:
        if st.button("Save Changes", key = "Save_Income"):
            for income_source in income_sources:
                replace_income_values(month_year, income_source[0], income_source[1])
            st.rerun()

    st.divider()


    #Whole table + editing

    table_data = get_budget_table_data(month_budget_data)

    if "editing_index" not in st.session_state:
        st.session_state.editing_index = None

    if "adding_entry" not in st.session_state:
        st.session_state.adding_entry = False

    income_options = [isrc[0] if isinstance(isrc, (list, tuple)) else isrc for isrc in income_sources]
    if st.session_state.editing_index is not None:
        st.session_state.adding_entry = False
        idx = st.session_state.editing_index
        current_item = month_budget_data[idx]

        st.subheader(f"Editing Budget Entry")
        edit_category = st.text_input("Edit Category", value=current_item["category"])

        current_source = current_item["income_source"]
        source_index = (income_options.index(current_source)
            if current_source in income_options
            else 0)
        edit_income_source = st.selectbox(
            "Edit Income Source", options=income_options, index=source_index,
            accept_new_options= True)

        edit_planned_amount = st.number_input(
            "Edit Planned Amount",
            value=float(current_item["planned_amount"]),
            step=100.0,)
        col_save, col_cancel = st.columns([1, 1])

        with col_save:
            if st.button("Save Changes", width = "stretch"):
                new_item = month_budget_data[idx].copy()
                new_item["category"] = edit_category
                new_item["income_source"] = edit_income_source
                new_item["planned_amount"] = edit_planned_amount
                for income_source in income_sources:
                    if new_item["income_source"] == income_source[0]:
                        new_item["income"] = income_source[1]
                        break
                    else:
                        new_item["income"] = 100.0

                replace_budget_entry(month_budget_data[idx], new_item)


                st.session_state.editing_index = None
                st.rerun()
        with col_cancel:
            if st.button("Remove Budget Category", width = "stretch", type = "primary" ):
                replace_budget_entry(month_budget_data[idx], None)
                st.session_state.editing_index = None
                st.rerun()
        if st.button("Cancel", width = "stretch"):
            st.session_state.editing_index = None
            st.rerun()

    else:
        table_data = [[d["category"], d["income_source"], d["planned_amount"]]
            for d in month_budget_data]
        col_ratios = [2, 2, 2, 1]
        header_cols = st.columns(col_ratios)
        for col, header in zip(
            header_cols, ["Category", "Income Source", "Planned Amount", "Actions"]):
            col.markdown(f"**{header}**")
        for index, row in enumerate(table_data):
            cols = st.columns(col_ratios)
            cols[0].write(row[0])
            cols[1].write(row[1])
            cols[2].write(row[2])
            if cols[3].button("Edit", key=f"edit_btn_{index}"):
                st.session_state.editing_index = index
                st.rerun()


    if st.session_state.adding_entry and st.session_state.editing_index == None:
        st.divider()
        st.subheader("Add New Budget Category")

        add_category = st.text_input("Category Name", placeholder="e.g., Transportation")
        add_income_source = st.selectbox("Income Source", options = income_options, accept_new_options=True)
        add_planned_amount = st.number_input("Planned Amount", value=100.0, step=100.0)
        add_income = 100.0
        for income_source in income_sources:
            if add_income_source == income_source[0]:
                add_income = income_source[1]
                break

        new_item = {"month":month_year, "income_source": add_income_source,
                    "income": add_income, "category": add_category,
                    "planned_amount": add_planned_amount}

        col_add_confirm, col_add_cancel = st.columns([1, 1])

        if col_add_confirm.button("Add Entry", width = "stretch"):
            new_budget_entry(new_item)
            st.session_state.adding_entry = False
            st.rerun()

        if col_add_cancel.button("Cancel Add", width = "stretch"):
            st.session_state.adding_entry = False
            st.rerun()

    else:
        if st.session_state.editing_index is None:
            if st.button("Add Category", width = "stretch"):
                st.session_state.adding_entry = True
                st.rerun()

    st.divider()


    #Total income, planned amount, and warning at the bottom of the screen
    total_income_col, total_planned_col = st.columns(2)
    with total_income_col:
        total_income = get_total_income(month_year)
        st.caption(f"Total Income: ₱{total_income}")
    with total_planned_col:
        total_planned = get_total_planned(month_year)
        st.caption(f"Total Planned: ₱{total_planned}")

    if total_planned > total_income:
        st.warning(f"Warning: Your planned total exceeds your total income by ₱{total_planned - total_income}. Either increase your total income or reduce your total planned amount to fix this.")
    elif total_income > total_planned:
        st.info(f"Tip: You still have ₱{total_income - total_planned} to allocate into your budget!")