import streamlit as st
def init_session_state() -> None:
    """Initialize required Streamlit session state keys per SDD Section 5.1."""
    defaults = {
        "raw_df": None,
        "cleaned_df": None,
        "file_id": None
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value