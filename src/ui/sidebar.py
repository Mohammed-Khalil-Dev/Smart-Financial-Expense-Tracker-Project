import pandas as pd
import streamlit as st


def mock_clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Temporary stub until src/cleaning/ is ready."""
    # TODO: Replace with real call to src.cleaning module
    return df.dropna().copy()

def render_sidebar() -> tuple[list[str], tuple[float, float] | None]:
    """Render CSV uploader and dynamic filter controls in the sidebar (UI-2, UI-3)."""
    st.sidebar.header("1. Upload Dataset")
    uploaded_file = st.sidebar.file_uploader("Choose an expense CSV file", type=["csv"])

    if uploaded_file is not None and uploaded_file.file_id != st.session_state.file_id:
        try:
            raw_df = pd.read_csv(uploaded_file)
            if not isinstance(raw_df, pd.DataFrame) or raw_df.empty:
                st.sidebar.error("The uploaded CSV file is empty.")
            else:
                st.session_state.raw_df = raw_df
                st.session_state.cleaned_df = mock_clean_data(raw_df)
                st.session_state.file_id = uploaded_file.file_id
        except Exception as exc:
            st.sidebar.error(f"Failed to read CSV file: {exc}")

    selected_categories: list[str] = []
    amount_range: tuple[float, float] | None = None

    df = st.session_state.cleaned_df
    if df is not None and not df.empty:
        st.sidebar.divider()
        st.sidebar.header("2. Filter Transactions")

        if "category" in df.columns:
            categories = sorted(str(category) for category in df["category"].dropna().unique())
            selected_categories = st.sidebar.multiselect(
                "Expense Categories", options=categories, default=categories
            )

        if "amount" in df.columns and pd.api.types.is_numeric_dtype(df["amount"]):
            min_amt = float(df["amount"].min())
            max_amt = float(df["amount"].max())
            if min_amt < max_amt:
                amount_range = st.sidebar.slider(
                    "Amount Range", min_value=min_amt, max_value=max_amt, value=(min_amt, max_amt)
                )

    return selected_categories, amount_range


def apply_filters(
    df: pd.DataFrame,
    categories: list[str],
    amount_range: tuple[float, float] | None,
) -> pd.DataFrame:
    """Filter cleaned DataFrame based on active sidebar controls (FR-8)."""
    filtered = df.copy()
    if categories is not None and "category" in filtered.columns:
        filtered = filtered[filtered["category"].isin(categories)]
    if amount_range is not None and "amount" in filtered.columns:
        filtered = filtered[
            (filtered["amount"] >= amount_range[0]) & (filtered["amount"] <= amount_range[1])
        ]
    return filtered