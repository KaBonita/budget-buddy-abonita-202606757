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

st.markdown(
    """
    <style>
    /* Add subtle border under each row to look like a table */
    div[data-testid="column"] {
        display: flex;
        align-items: center;
    }
    .table-row {
        padding: 8px 0px;
        border-bottom: 1px solid rgba(49, 51, 63, 0.2);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

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

table_data = [ [dictionary["category"], dictionary["income_source"], dictionary["planned_amount"]] for dictionary in month_budget_data 
]


col_ratios = [2, 2, 2, 1]
header_cols = st.columns(col_ratios)
for col, header in zip(header_cols, ["Category", "Income Source", "Planned Amount", "Actions"]):
    col.markdown(f"**{header}**")
for index, row in enumerate(table_data):
    cols = st.columns(col_ratios)

    cols[0].write(row[0])
    cols[1].write(row[1])
    cols[2].write(row[2])

    if cols[3].button("Edit", key = row):

        new_category = cols[0].text_input("Edit Category", value = row[0], on_change = "ignore")
        new_income_source = cols[1].selectbox("Edit Income Source", 
                          (income_source[0] for income_source in income_sources),
                          index = [income_source[0] for income_source in income_sources].index(row[1]),
                          on_change = "ignore")
        new_planned_amount = cols[2].number_input("Edit Planned Amount", value = row[2],
                           on_change = "ignore", step = 100.0)
        if cols[3].button("Save"):
            month_budget_data[index]["category"] = new_category
            month_budget_data[index]["income_source"] = new_income_source
            month_budget_data[index]["planned_amount"] = new_planned_amount
            st.rerun()
        
st.write(month_budget_data)
st.write(income_sources)
