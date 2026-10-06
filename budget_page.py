from data_loader import load_budget_data, save_budget_data
from main import load_month_budget
import streamlit as st
import datetime
import time

def replace_income_values(month_year, income_category, new_value):
    budget_data = load_budget_data()
    for line in budget_data:
        if line["month"] == month_year and line["income_source"] == income_category:
            line["income"] = new_value

    save_budget_data(budget_data)

def replace_budget_entry(replace_item, with_item):
    budget_data = load_budget_data()
    index = budget_data.index(replace_item)
    budget_data[index] = with_item

    save_budget_data(budget_data)

curr_month = datetime.datetime.now().month
curr_year = datetime.datetime.now().year


#Ask month and year
st.header("Manage budget for")
month_col, year_col = st.columns(2)
with month_col:
    month = st.selectbox("", ("January", "February",
                        "March", "April", "May", "June", "July", "August",
                        "September", "October", "November", "December"),
                        index = curr_month - 1)
with year_col:
    year = str(st.selectbox("", (tuple(range(1, 10000))),
                             index = curr_year - 1))
st.divider()
month_year = month + " " + year

month_budget_data = load_month_budget(month_year)


income_sources = []
for line in month_budget_data:
    if [line["income_source"], line["income"]] not in income_sources:
        new_income_source = [line["income_source"], line["income"]]
        income_sources.append(new_income_source)

st.subheader("Income Sources")
income_source_col, income_col = st.columns(2)
with income_source_col:
    for line in income_sources:
        income_source = line[0]
        st.write("")
        st.write("")
        st.write(income_source)
        st.write("")

with income_col:
    for income_source in income_sources:
        income_source[1] = st.number_input(None, value = income_source[1], step = 100.0, key = income_source)

if income_sources:
    if st.button("Save Changes", key = "Save_Income"):
        for income_source in income_sources:
            replace_income_values(month_year, income_source[0], income_source[1])
        st.rerun()

st.divider()


#Whole table + editing

table_data = [[dictionary["category"], dictionary["income_source"], dictionary["planned_amount"]] for dictionary in month_budget_data ]

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
        if st.button("Save Changes", use_container_width=True):
            new_item = month_budget_data[idx].copy()
            new_item["category"] = edit_category
            new_item["income_source"] = edit_income_source
            new_item["planned_amount"] = edit_planned_amount
            for income_source in income_sources:
                if new_item["income_source"] == income_source[0]:
                    new_item["income"] = income_source[1]

            replace_budget_entry(month_budget_data[idx], new_item)


            st.session_state.editing_index = None
            st.rerun()
    with col_cancel:
        if st.button("Cancel", use_container_width=True):
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
    st.subheader("Add New Budget Entry")

    add_category = st.text_input("New Category", placeholder="e.g., Side Hustle")
    add_income_source = st.selectbox("Income Source", options=income_options)
    add_planned_amount = st.number_input("Planned Amount", value=0.0, step=100.0)

    col_add_confirm, col_add_cancel = st.columns([1, 1])

    if col_add_confirm.button("Add Entry", use_container_width=True):
        st.session_state.adding_entry = False
        st.rerun()

    if col_add_cancel.button("Cancel Add", use_container_width=True):
        st.session_state.adding_entry = False
        st.rerun()

else:
    if st.session_state.editing_index is None:
        if st.button("Add Entry", use_container_width=True):
            st.session_state.adding_entry = True
            st.rerun()

st.divider()

st.write(month_budget_data)
st.write(income_sources)
