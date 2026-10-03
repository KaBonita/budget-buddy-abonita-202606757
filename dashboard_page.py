import streamlit as st

st.title("Dashboard")

st.markdown(
    """
    <style>
    /* Target Streamlit buttons to scale them down to text height */
    div.stButton > button {
        padding: 2px 10px !important;
        font-size: 14px !important;
        line-height: 1.2 !important;
        min-height: 0px !important;
        height: auto !important;
        border-radius: 4px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

col1, col2 = st.columns([2, 1])

with col1:
    st.write("This is a standard line of text right next to a small button ->")

with col2:
    if st.button("Click me"):
        st.write("Button clicked!")