"""
Coolblue Chart Library — Standardized visualization functions.

Simple, clean charts using the Coolblue brand palette.
Supports: horizontal bar, vertical bar, line graph, and YoY time-series.

Usage:
    from helpers.coolblue_charts import (
        bar_chart, line_chart, yoy_line_chart, apply_coolblue_style,
        COLORS,
    )

    apply_coolblue_style()

    # Horizontal bar chart
    bar_chart(df, x="revenue", y="segment", title="Revenue by segment")

    # Line chart
    line_chart(df, x="date", y="sessions", title="Sessions over time")

    # Year-over-year comparison with MoM/YoY table
    fig, ax, comparison_df = yoy_line_chart(
        df, date_col="date", value_col="sessions",
        title="Sessions by month — Year over Year",
    )
"""

from __future__ import annotations

import calendar
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Coolblue brand palette
# ---------------------------------------------------------------------------

COLORS = {
    "orange":     "#FF6600",   # Primary highlight — most important element
    "fact_blue":  "#285DAB",   # Secondary highlight
    "coolblue":   "#0090E3",   # Coolblue Blue
    "light_blue": "#CCE9F9",   # Tertiary / supporting data
    "grey":       "#F7F6F2",   # Subtle background fill (not chart bg)
    "white":      "#FFFFFF",   # Chart background
    "text_dark":  "#1F2937",   # Titles
    "text_mid":   "#4B5563",   # Axis labels
    "text_light": "#6B7280",   # Tick labels
    "grid":       "#E5E7EB",   # Gridlines
}

# Ordered color cycle: orange (most important) → fact_blue → light_blue
_COLOR_CYCLE = [COLORS["orange"], COLORS["fact_blue"], COLORS["light_blue"]]


# ---------------------------------------------------------------------------
# Style application
# ---------------------------------------------------------------------------

def apply_coolblue_style() -> None:
    """Apply the Coolblue chart style globally via matplotlib rcParams.

    Call once at the start of a notebook or script. Sets white background,
    clean spines, and brand typography defaults.
    """
    plt.rcParams.update({
        "figure.figsize": (10, 6),
        "figure.dpi": 150,
        "figure.facecolor": COLORS["white"],
        "figure.edgecolor": COLORS["white"],
        "axes.facecolor": COLORS["white"],
        "axes.edgecolor": COLORS["grid"],
        "axes.linewidth": 0.5,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.titlesize": 14,
        "axes.titleweight": "bold",
        "axes.titlepad": 14,
        "axes.labelsize": 10,
        "axes.labelcolor": COLORS["text_mid"],
        "axes.labelpad": 8,
        "axes.grid": False,
        "axes.prop_cycle": plt.cycler(color=_COLOR_CYCLE),
        "font.family": "sans-serif",
        "font.sans-serif": [
            "Helvetica Neue", "Helvetica", "Arial",
            "DejaVu Sans", "sans-serif",
        ],
        "font.size": 10,
        "xtick.color": COLORS["text_light"],
        "xtick.labelsize": 9,
        "xtick.major.size": 0,
        "ytick.color": COLORS["text_light"],
        "ytick.labelsize": 9,
        "ytick.major.size": 0,
        "lines.linewidth": 2.0,
        "lines.markersize": 0,
        "legend.frameon": False,
        "legend.fontsize": 9,
        "patch.edgecolor": COLORS["white"],
        "patch.linewidth": 0.5,
        "savefig.dpi": 150,
        "savefig.bbox": "tight",
        "savefig.facecolor": COLORS["white"],
        "savefig.edgecolor": COLORS["white"],
    })


# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------

def _fmt_number(val: float, prefix: str = "", suffix: str = "") -> str:
    """Format a number compactly (K / M) with optional prefix/suffix."""
    if abs(val) >= 1e6:
        return f"{prefix}{val / 1e6:.1f}M{suffix}"
    elif abs(val) >= 1e3:
        return f"{prefix}{val / 1e3:.0f}K{suffix}"
    else:
        return f"{prefix}{val:,.0f}{suffix}"


def _pick_color(index: int) -> str:
    """Return a color from the Coolblue cycle by index."""
    return _COLOR_CYCLE[index % len(_COLOR_CYCLE)]


# ---------------------------------------------------------------------------
# Bar chart
# ---------------------------------------------------------------------------

def bar_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str = "",
    horizontal: bool = True,
    highlight: str | list[str] | None = None,
    highlight_color: str | None = None,
    base_color: str | None = None,
    sort: bool = True,
    fmt: str | None = None,
    figsize: tuple[float, float] | None = None,
    ax: plt.Axes | None = None,
) -> tuple[plt.Figure, plt.Axes]:
    """Draw a bar chart from a DataFrame.

    One bar per row. Optionally highlight specific categories.

    Args:
        df: Source DataFrame.
        x: Column name for bar lengths / heights (numeric).
        y: Column name for bar labels (categorical).
        title: Chart title.
        horizontal: If True (default), horizontal bars. If False, vertical.
        highlight: Value(s) in the *y* column to highlight with ``highlight_color``.
            When None, all bars use the ``highlight_color`` (orange).
        highlight_color: Color for highlighted bars. Default: orange.
        base_color: Color for non-highlighted bars. Default: light_blue.
        sort: Sort bars by value (ascending for horizontal, descending for vertical).
        fmt: Format string for value labels (e.g. ``"€{:,.0f}"``). Auto-detected if None.
        figsize: Figure size override.
        ax: Existing Axes to draw on. If None, a new figure is created.

    Returns:
        (fig, ax) tuple.
    """
    highlight_color = highlight_color or COLORS["orange"]
    base_color = base_color or COLORS["light_blue"]

    data = df[[y, x]].copy()
    if sort:
        data = data.sort_values(x, ascending=horizontal)

    categories = data[y].tolist()
    values = data[x].tolist()

    # Determine which bars to highlight
    if highlight is None:
        bar_colors = [highlight_color] * len(categories)
    else:
        if isinstance(highlight, str):
            highlight = [highlight]
        hl_set = set(highlight)
        bar_colors = [
            highlight_color if c in hl_set else base_color for c in categories
        ]

    if ax is None:
        fig, ax = plt.subplots(figsize=figsize or (10, max(3, len(categories) * 0.6)))
    else:
        fig = ax.figure

    max_val = max(values) if values else 1

    if horizontal:
        bars = ax.barh(categories, values, color=bar_colors)
        ax.set_xlim(0, max_val * 1.25)
        ax.xaxis.set_visible(False)
        ax.spines["bottom"].set_visible(False)

        for bar, val in zip(bars, values):
            label = fmt.format(val) if fmt else _fmt_number(val)
            ax.text(
                val + max_val * 0.02,
                bar.get_y() + bar.get_height() / 2,
                label,
                va="center",
                fontsize=9,
                color=COLORS["text_dark"],
            )
    else:
        bars = ax.bar(categories, values, color=bar_colors)
        ax.set_ylim(0, max_val * 1.20)
        ax.yaxis.set_visible(False)
        ax.spines["left"].set_visible(False)

        for bar, val in zip(bars, values):
            label = fmt.format(val) if fmt else _fmt_number(val)
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                val + max_val * 0.02,
                label,
                ha="center",
                fontsize=9,
                color=COLORS["text_dark"],
            )

    if title:
        ax.set_title(title, fontsize=14, fontweight="bold",
                     color=COLORS["text_dark"], loc="left", pad=14)

    fig.tight_layout()
    return fig, ax


# ---------------------------------------------------------------------------
# Line chart
# ---------------------------------------------------------------------------

def line_chart(
    df: pd.DataFrame,
    x: str,
    y: str | list[str],
    title: str = "",
    colors: list[str] | None = None,
    figsize: tuple[float, float] | None = None,
    ax: plt.Axes | None = None,
    show_legend: bool = True,
) -> tuple[plt.Figure, plt.Axes]:
    """Draw a line chart from a DataFrame.

    Supports one or multiple y-series. Colors follow the Coolblue hierarchy:
    first series → orange, second → fact_blue, third → light_blue.

    Args:
        df: Source DataFrame.
        x: Column name for the x-axis (typically dates).
        y: Column name (str) or list of column names for y-series.
        title: Chart title.
        colors: Optional explicit color list. Defaults to Coolblue cycle.
        figsize: Figure size override.
        ax: Existing Axes to draw on. If None, a new figure is created.
        show_legend: Whether to show a legend (default True for multi-series).

    Returns:
        (fig, ax) tuple.
    """
    if isinstance(y, str):
        y = [y]

    line_colors = colors or [_pick_color(i) for i in range(len(y))]

    if ax is None:
        fig, ax = plt.subplots(figsize=figsize or (10, 6))
    else:
        fig = ax.figure

    for i, col in enumerate(y):
        color = line_colors[i % len(line_colors)]
        ax.plot(df[x], df[col], color=color, linewidth=2.5 if i == 0 else 1.8,
                label=col)

    ax.yaxis.grid(True, color=COLORS["grid"], linewidth=0.5, alpha=0.7)
    ax.set_axisbelow(True)
    ax.spines["bottom"].set_color(COLORS["grid"])

    if title:
        ax.set_title(title, fontsize=14, fontweight="bold",
                     color=COLORS["text_dark"], loc="left", pad=14)

    if show_legend and len(y) > 1:
        ax.legend(loc="upper left", frameon=False, fontsize=9)

    fig.tight_layout()
    return fig, ax


# ---------------------------------------------------------------------------
# Year-over-Year line chart with comparison table
# ---------------------------------------------------------------------------

def yoy_line_chart(
    df: pd.DataFrame,
    date_col: str,
    value_col: str,
    title: str = "",
    figsize: tuple[float, float] | None = None,
    ax: plt.Axes | None = None,
    month_format: str = "short",
) -> tuple[plt.Figure, plt.Axes, pd.DataFrame]:
    """Year-over-Year line chart: each year as a separate line, most recent in orange.

    Also returns a comparison DataFrame with MoM and YoY differences.

    Args:
        df: Source DataFrame. Must have a date column and a numeric value column.
        date_col: Name of the date column (parseable to datetime).
        value_col: Name of the numeric value column.
        title: Chart title.
        figsize: Figure size override.
        ax: Existing Axes to draw on. If None, a new figure is created.
        month_format: ``"short"`` for Jan/Feb/..., ``"number"`` for 1/2/...

    Returns:
        (fig, ax, comparison_df) where comparison_df contains columns:
        year, month, value, mom_diff, mom_pct, yoy_diff, yoy_pct.
    """
    data = df[[date_col, value_col]].copy()
    data[date_col] = pd.to_datetime(data[date_col])
    data["year"] = data[date_col].dt.year
    data["month"] = data[date_col].dt.month

    # Aggregate to year-month level (in case of duplicates)
    monthly = (
        data.groupby(["year", "month"])[value_col]
        .sum()
        .reset_index()
        .sort_values(["year", "month"])
    )

    # --- Build comparison table ---
    comparison = monthly.copy()
    comparison = comparison.rename(columns={value_col: "value"})

    # MoM diff (within each year)
    comparison["mom_diff"] = comparison.groupby("year")["value"].diff()
    comparison["mom_pct"] = comparison.groupby("year")["value"].pct_change()

    # YoY diff (same month, previous year)
    comparison = comparison.sort_values(["month", "year"])
    comparison["yoy_diff"] = comparison.groupby("month")["value"].diff()
    comparison["yoy_pct"] = comparison.groupby("month")["value"].pct_change()
    comparison = comparison.sort_values(["year", "month"]).reset_index(drop=True)

    # Month label for display
    if month_format == "short":
        comparison["month_label"] = comparison["month"].apply(
            lambda m: calendar.month_abbr[m]
        )
    else:
        comparison["month_label"] = comparison["month"]

    # --- Draw chart ---
    years = sorted(monthly["year"].unique())

    # Color assignment: most recent → orange, next → fact_blue, older → light_blue
    year_colors = {}
    for i, yr in enumerate(reversed(years)):
        year_colors[yr] = _pick_color(i)

    if ax is None:
        fig, ax = plt.subplots(figsize=figsize or (10, 6))
    else:
        fig = ax.figure

    month_ticks = list(range(1, 13))
    month_labels = [calendar.month_abbr[m] for m in month_ticks]

    # Draw older years first (behind), most recent last (on top)
    for yr in years:
        yr_data = monthly[monthly["year"] == yr].sort_values("month")
        is_latest = (yr == years[-1])
        ax.plot(
            yr_data["month"],
            yr_data[value_col],
            color=year_colors[yr],
            linewidth=2.5 if is_latest else 1.5,
            marker="o" if is_latest else None,
            markersize=4 if is_latest else 0,
            label=str(yr),
            zorder=10 if is_latest else 1,
        )

    ax.set_xticks(month_ticks)
    ax.set_xticklabels(month_labels)
    ax.yaxis.grid(True, color=COLORS["grid"], linewidth=0.5, alpha=0.7)
    ax.set_axisbelow(True)
    ax.spines["bottom"].set_color(COLORS["grid"])

    if title:
        ax.set_title(title, fontsize=14, fontweight="bold",
                     color=COLORS["text_dark"], loc="left", pad=14)

    ax.legend(loc="upper left", frameon=False, fontsize=9)

    fig.tight_layout()
    return fig, ax, comparison


# ---------------------------------------------------------------------------
# Save helper
# ---------------------------------------------------------------------------

def save_chart(fig: plt.Figure, path: str | Path, dpi: int = 150,
               close: bool = True) -> None:
    """Save a chart to file with tight layout.

    Args:
        fig: Matplotlib Figure.
        path: Output file path.
        dpi: Resolution. Default: 150.
        close: Close the figure after saving. Default: True.
    """
    fig.tight_layout()
    fig.savefig(path, dpi=dpi, bbox_inches="tight",
                facecolor=COLORS["white"], edgecolor="none")
    if close:
        plt.close(fig)
