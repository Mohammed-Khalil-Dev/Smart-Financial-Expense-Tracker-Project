import io
import pandas as pd
from matplotlib.figure import Figure
from pathlib import Path


def save_to_outputs(file_name: str, data: bytes) -> None:
    """Persist a copy of an exported artifact into the project's outputs/ directory."""
    out_dir = Path("outputs")
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / file_name).write_bytes(data)

def build_summary_report(
    filtered_df: pd.DataFrame,
    raw_row_count: int | None = None,
) -> str:
    """Build a plain-text analytical summary report (SRS FR-17)."""
    lines = [
        "SMART FINANCIAL EXPENSE TRACKER - FILTERED SUMMARY REPORT",
        "=" * 50,
        f"Filtered Records Exported: {len(filtered_df):,}",
    ]
    if raw_row_count is not None:
        lines.append(f"Original Raw Records:      {raw_row_count:,}")

    if "amount" in filtered_df.columns and not filtered_df.empty:
        lines.extend([
            "",
            "FILTERED SPENDING METRICS",
            "-" * 50,
            f"Total Spending:     ${filtered_df['amount'].sum():,.2f}",
            f"Mean Transaction:   ${filtered_df['amount'].mean():,.2f}",
            f"Median Transaction: ${filtered_df['amount'].median():,.2f}",
            f"Min Amount:   ${filtered_df['amount'].min():,.2f}",
            f"Max Amount:   ${filtered_df['amount'].max():,.2f}"
        ])

    if {"category", "amount"}.issubset(filtered_df.columns) and not filtered_df.empty:
        lines.extend(["", "FILTERED SPENDING BY CATEGORY", "-" * 50])
        categories_totals: dict[str, float | int] = (
            filtered_df.groupby("category")["amount"]
            .sum()
            .sort_values(ascending=False)
        )
        for cat, total in categories_totals.items():
            lines.append(f"- {cat}: ${total:,.2f}")

    return "\n".join(lines)


def figure_to_png_bytes(fig: Figure, dpi: int = 300) -> bytes:
    """Render a Matplotlib Figure into PNG bytes in memory (SDD Sec 5.2)."""
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=dpi, bbox_inches="tight")
    buf.seek(0)
    return buf.getvalue()


