import streamlit as st

st.title("Dashboard")

import streamlit as st

import streamlit as st

# Custom CSS to align column text vertically and add a clean row divider
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
# 1. Define table headers and data (rows stored as lists)

data_rows = [
    [101, "Alice Smith", "Developer"],
    [102, "Bob Jones", "Designer"],
    [103, "Charlie Brown", "Product Manager"],
    [104, "Diana Prince", "Data Analyst"],
]

# Column layout ratios (e.g., ID gets 1 part width, Name gets 2 parts, etc.)
col_ratios = [1, 2, 2, 1.5]

# 2. Render Table Header
header_cols = st.columns(col_ratios)
for col, header in zip(header_cols, ["ID", "Name", "Role", "Actions"]):
    col.markdown(f"**{header}**")

# 3. Render Table Rows from List Data
for index, row in enumerate(data_rows):
    cols = st.columns(col_ratios)

    # Display row values in respective columns
    cols[0].write(f"#{row[0]}")
    cols[1].write(row[1])
    cols[2].write(row[2])

    # Add interactive widgets directly inside row columns
    if cols[3].button("Edit", key=f"edit_{row[0]}"):
        st.info(f"Editing row ID: {row[0]} ({row[1]})")