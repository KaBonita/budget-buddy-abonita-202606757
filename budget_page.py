from data_loader import load_budget_data
import streamlit as st

st.title("Budget")

#Ask month and year
st.divider()
st.header("Manage budget for")
monthcol, yrcol = st.columns(2)
with monthcol:
    month = st.selectbox("", ("January", "February",
                "March", "April", "May", "June", "July", "August",
                    "September", "October", "November", "December"))
with yrcol:
    year = str(st.selectbox("", (tuple(range(1000, 10000))), index = 1027))
st.divider()

st.write(month + " " + year)
