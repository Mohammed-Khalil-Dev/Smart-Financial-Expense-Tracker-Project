
import streamlit as st

import sidebar
import state
import tabs






def main() -> None:
    st.set_page_config(
        page_title="Smart Financial Expense Tracker",
        layout="wide",
    )
    state.init_session_state()

    st.title("Smart Financial Expense Tracker")
    st.caption("Upload personal expense CSV records to clean, explore, and analyze spending patterns.")

    selected_categories, amount_range = sidebar.render_sidebar()

    if st.session_state.cleaned_df is None:
        st.info("Upload a CSV file from the sidebar to begin.")
        return

    filtered_df = sidebar.apply_filters(st.session_state.cleaned_df, selected_categories, amount_range)

    tab_overview, tab_visual_analytics, tab_ai, tab_export = st.tabs(
        ["Overview & Data", "Visual Analytics (EDA)", "AI Insights", "Export"]
    )

    with tab_overview:
        tabs.tab_overview(filtered_df=filtered_df)

    with tab_visual_analytics:
        tabs.tab_visual_analytics(filtered_df=filtered_df)

    with tab_ai:
        tabs.tab_ai(model_output=filtered_df)

    with tab_export:
        tabs.tab_export(filtered_df=filtered_df,
                        cleaned_df=st.session_state.cleaned_df,
                        figures=None)

if __name__ == "__main__":
    main()