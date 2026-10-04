from data_loader import load_budget_data
from main import load_month_budget, replace_csv_row, read_csv_row, len_csv
import streamlit as st
import datetime
import time

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
        income_source[1] = st.number_input(None, value = income_source[1], step = 100.0, key = income_source, format = "Php")


if "is_processing" not in st.session_state:
    st.session_state.is_processing = False
def start_processing():
    st.session_state.is_processing = True

if income_sources:
    if not st.session_state.is_processing:
        st.button("Save Changes", on_click=start_processing)
    else:
        st.info("Saving changes, please wait...")
        for income_source in income_sources:
            replace_income_val(month_year, income_source[0], income_source[1])
        time.sleep(1)
        st.session_state.is_processing = False
        st.rerun()

st.divider()

st.write(month_budget_data)
st.write(income_sources)
