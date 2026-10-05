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
    if st.button("Save Changes"):
        for income_source in income_sources:
            replace_income_values(month_year, income_source[0], income_source[1])
        st.rerun()

st.divider()
st.write(month_budget_data)
st.write(income_sources)
