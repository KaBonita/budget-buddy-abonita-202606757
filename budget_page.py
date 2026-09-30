from data_loader import load_budget_data
from main import load_month_budget
import streamlit as st
import datetime

curr_month = datetime.datetime.now().month
curr_year = datetime.datetime.now().year

#Ask month and year
st.divider()
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
income_source_col, income_col = st.columns(2)
with income_source_col:
    for line in income_sources:
        income_source = list(line.keys())[0]
        st.write("")
        st.write("")
        st.write(income_source)
        st.write("")

with income_col:
    for line in income_sources:
        income = st.number_input(None, value = list(line.values())[0], step = 100.0, key = line)
st.divider()

st.write(month_budget_data)