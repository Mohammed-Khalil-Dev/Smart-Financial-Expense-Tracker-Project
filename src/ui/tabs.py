import pandas as pd
import streamlit as st
from matplotlib import figure

from utils.export_helpers import build_summary_report, figure_to_png_bytes, save_to_outputs


def tab_overview(filtered_df: pd.DataFrame) -> None:
    if "amount" in filtered_df.columns and not filtered_df.empty:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Spending", f"${filtered_df['amount'].sum():,.2f}")
        c2.metric("Mean Transaction", f"${filtered_df['amount'].mean():,.2f}")
        c3.metric("Median Transaction", f"${filtered_df['amount'].median():,.2f}")
        c4.metric("Records", f"{len(filtered_df):,}")
    st.dataframe(filtered_df, use_container_width=True)

def tab_visual_analytics(filtered_df: pd.DataFrame) -> None:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Spending by Category")
        st.info("Connect src/visualization/plots.py here.")
    with col2:
        st.subheader("Spending Over Time")
        st.info("Connect src/visualization/plots.py here.")


def tab_ai(model_output) -> None:
    st.subheader("Expense Pattern & Anomaly Detection")
    st.info("Connect src/pipelines/ and src/models/ outputs here.")



def tab_export(
    filtered_df: pd.DataFrame,
    cleaned_df: pd.DataFrame | None = None,
    figures: dict[str, figure.Figure] | None = None,
) -> None:
    """Render download controls for CSV datasets, summary report, and PNG charts."""
    st.subheader("Download Processed Data & Reports")

    # 1. Dataset & Summary Report Downloads (3 side-by-side buttons)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**Filtered Dataset**")
        filtered_csv = filtered_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download Filtered CSV",
            data=filtered_csv,
            file_name="filtered_expenses.csv",
            mime="text/csv",
            key="dl_filtered_expenses",
            on_click=save_to_outputs,
            args=("filtered_expenses.csv", filtered_csv),
            disabled=filtered_df.empty,
            use_container_width=True,
        )

    with col2:
        st.markdown("**Full Cleaned Dataset**")
        full_df = cleaned_df if cleaned_df is not None else filtered_df
        full_csv = full_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download Full Cleaned CSV",
            data=full_csv,
            file_name="cleaned_expenses.csv",
            key="dl_cleaned_expenses",
            on_click=save_to_outputs,
            args=("cleaned_expenses.csv", full_csv),
            mime="text/csv",
            disabled=full_df.empty,
            use_container_width=True,
        )

    with col3:
        st.markdown("**Analytical Summary**")
        raw_df = st.session_state.get("raw_df")
        raw_count = len(raw_df) if isinstance(raw_df, pd.DataFrame) else None
        report_bytes = build_summary_report(filtered_df, raw_count).encode("utf-8")
        st.download_button(
            label="Download Summary Report",
            data=report_bytes,
            file_name="expense_summary_report.txt",
            mime="text/plain",
            key="dl_expense_summary_report",
            on_click=save_to_outputs,
            args=("expense_summary_report.txt", report_bytes),
            disabled=filtered_df.empty,
            use_container_width=True,
        )

    st.divider()

    # 2. Chart / Figure PNG Downloads
    st.markdown("**Export Generated Charts (High-DPI PNG)**")
    if not figures:
        st.info("No charts generated yet. Once src/visualization/ is connected, PNG download buttons will appear here.")
        return

    chart_cols = st.columns(2)
    for idx, (chart_name, fig) in enumerate(figures.items()):
        acceptable_file_name = chart_name.lower().replace(" ", "_")
        png_bytes = figure_to_png_bytes(fig)
        with chart_cols[idx % 2]:
            st.download_button(
                label=f"Download {chart_name} (.png)",
                data=png_bytes,
                file_name=f"{acceptable_file_name}.png",
                mime="image/png",
                key=f"dl_{acceptable_file_name}",
                on_click=save_to_outputs,
                args=(f"{acceptable_file_name}.png", png_bytes),
                use_container_width=True,
            )