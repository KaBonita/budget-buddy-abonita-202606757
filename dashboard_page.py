import streamlit as st

st.title("Dashboard")

if "button_disabled" not in st.session_state:
    st.session_state.button_disabled = False


# Callback function to handle the click
def disable_button():
    st.session_state.button_disabled = True


# Render the button with the disabled state and callback
st.button(
    "Click Me to Disable",
    disabled=st.session_state.button_disabled,
    on_click=disable_button,
)

# Optional: Add a button to reset the state
if st.session_state.button_disabled:
    st.success("Button has been pressed and disabled!")
    if st.button("Reset"):
        st.session_state.button_disabled = False
        st.rerun()