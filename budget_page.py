from data_loader import load_budget_data
from main import load_month_budget, replace_csv_row, read_csv_row, len_csv
import streamlit as st
import datetime

def replace_income_val(month_year, income_category, new_income, BUDGET_FILENAME = "budget_data.csv"):
    for index in range(1, len_csv(BUDGET_FILENAME) + 1):
        row = read_csv_row(BUDGET_FILENAME, index)
        if row[0] == month_year and row[1] == income_category:
            row[2] = new_income
            replace_csv_row(BUDGET_FILENAME, index, row)

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
    if {line["income_source"] : line["income"]} not in income_sources:
        new_income_source = {line["income_source"] : line["income"]}
        income_sources.append(new_income_source)

st.subheader("Income Sources")
income_source_col, income_col, save_inc_col = st.columns(3)
with income_source_col:
    for line in income_sources:
        income_source = list(line.keys())[0]
        st.write("")
        st.write("")
        st.write(income_source)
        st.write("")

with income_col:
    for income_source in income_sources:
        income_source[list(income_source.keys())[0]] = st.number_input(None, value = list(income_source.values())[0], step = 100.0, key = income_source)

with save_inc_col:
    for income_source in income_sources:
        st.write("")
        st.write("")
        if st.button("Save", key = str(income_source) + "button"):
            income_category = list(income_source.keys())[0]
            income_value = income_source[income_category]
            replace_income_val(month_year, income_category, income_value)
st.divider()

st.write(month_budget_data)
