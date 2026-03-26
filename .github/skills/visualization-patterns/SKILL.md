---
name: visualization-patterns
description: "Ensures every chart follows Coolblue brand standards: simple chart types (bar/line only), Coolblue colors, white background, and YoY time-series conventions."
user-invocable: false
---
# Visualization Patterns

## Purpose
Ensure every chart the assistant produces follows Coolblue brand standards with simple chart types, consistent Coolblue colors, and clean design.

## When to Use
Apply this skill whenever generating a chart, graph, or data visualization. Always apply the Coolblue style. Default and only theme: `coolblue`.

## Instructions

### Pre-flight: Load Learnings
Before executing, check `.knowledge/learnings/index.md` for relevant entries:
- Read the file. If it doesn't exist or is empty, skip silently.
- Scan for entries under **"Chart Style"** and **"General"** headings (or related categories like "Visualization Insights").
- If entries exist, incorporate them as constraints for this execution (e.g., preferred chart types, color overrides, annotation preferences).
- Never block execution if learnings are unavailable.

### Core Principle: Coolblue Visualization Standards

Every chart follows the Coolblue simplicity standard:

> **Keep it simple. Use only bar charts and line charts. Use only Coolblue colors. White background always.**

#### Allowed Chart Types
- **Horizontal bar chart** — for comparing categories (default, preferred)
- **Vertical bar chart** — for comparing a few categories (≤6)
- **Line chart** — for time series and trends
- **No other chart types** — heatmaps, matrices, scatter plots, pie charts, donut charts, area charts, waterfall charts, stacked bars, and all other complex visualizations are banned

#### Color Palette (Coolblue Brand)
```python
COLORS = {
    "orange":     "#FF6600",   # Most important element
    "fact_blue":  "#285DAB",   # Second most important
    "coolblue":   "#0090E3",   # Coolblue Blue (axis labels, ticks)
    "light_blue": "#CCE9F9",   # Supporting/context data
    "grey":       "#F7F6F2",   # Subtle fill only
    "white":      "#FFFFFF",   # Chart background — ALWAYS white
}
```

**Color hierarchy:**
- **Orange `#FF6600`** — the primary/most important data element
- **Fact Blue `#285DAB`** — the secondary data element
- **Light Blue `#CCE9F9`** — supporting/context data (non-highlighted bars, older time series)
- **No other colors** — no reds, greens, ambers, purples, or grays outside this palette
- Background is always white (`#FFFFFF`), never off-white or colored

#### Time Series Convention (YoY / MoM data)
When data spans multiple years (e.g., monthly data from 2023-2026):
1. **Each year is a separate line** on one chart (NOT separate charts per year)
2. **Most recent year** → Orange `#FF6600` (thicker line, optional small markers)
3. **2nd most recent year** → Fact Blue `#285DAB`
4. **3rd and older years** → Light Blue `#CCE9F9`
5. **Every time series chart must include a companion DataFrame** with: Year, Month, Value, MoM difference, MoM % change, YoY difference, YoY % change

Use `yoy_line_chart()` from `helpers/coolblue_charts.py` for this pattern.

**Implementation:** Apply the Coolblue style before generating any chart:
```python
from helpers.coolblue_charts import apply_coolblue_style, bar_chart, line_chart, yoy_line_chart, COLORS

apply_coolblue_style()  # Sets white bg, Coolblue color cycle, clean spines
```

Or using the core helpers:
```python
from helpers.chart_helpers import swd_style, highlight_bar, highlight_line, action_title, save_chart

colors = swd_style()  # Loads style + returns Coolblue color palette
```

### Declutter Checklist

Before finalizing **any** chart, verify each item:

- [ ] Chart border / box — removed entirely
- [ ] Top and right spines — removed (keep only bottom and left)
- [ ] Heavy gridlines — removed or very light gray (`#E5E7EB`), y-axis only
- [ ] Data markers — removed from line charts (except most recent year in YoY)
- [ ] Legend — present and clean for multi-series; use direct labels where practical
- [ ] Rotated axis text — if labels need rotation, switch to horizontal bars
- [ ] Trailing zeros — use `€45` not `€45.00`; use `12%` not `12.0%`
- [ ] 3D effects — never
- [ ] Background color — always white (`#FFFFFF`)
- [ ] Colors — only Coolblue palette (orange, fact_blue, light_blue)
- [ ] Chart type — only bar (horizontal/vertical) or line chart
- [ ] No distracting elements — no annotations, arrows, shaded regions unless essential
- [ ] Redundant axis labels — if the title says "Revenue (€M)", the y-axis doesn't need "Revenue in Millions of Euros"
- [ ] Excessive tick marks — reduce to 4-6 ticks maximum
- [ ] Decimal precision — match the precision to the decision (`12%` not `12.347%`)

### Chart Sequencing (Multi-Chart Analyses)

When producing multiple charts for a deep dive or root cause investigation, follow **Context → Tension → Resolution**:

| Phase | Charts | Purpose | Example |
|-------|--------|---------|---------|
| **Context** | 1-2 | Set the baseline. What does normal look like? | "[Dataset] processes ~4,000 support tickets per month" |
| **Tension** | 2-3 | Reveal the problem. Progressively zoom in. | "June spiked to 6,200" → "The spike was iOS payment issues" |
| **Resolution** | 1-2 | Explain why and recommend action. | "iOS v2.3 introduced a bug → fix eliminates ~2,200 tickets/mo" |

- Each chart builds on the previous one
- Never show a chart that makes the audience ask "so what?"
- The number of charts is determined by the storyboard. Each narrative beat that requires a visualization becomes a chart.
- The final chart should make the recommended action obvious

### Chart Helper Functions Reference

All chart helpers live in `helpers/chart_helpers.py`. The style file is `helpers/analytics_chart_style.mplstyle`. The full style guide with before/after examples is in `helpers/chart_style_guide.md`.

| Function | Purpose | Key Args |
|----------|---------|----------|
| `swd_style()` | Apply Coolblue matplotlib style, return color palette | — |
| `highlight_bar()` | Bar chart with one bar highlighted (orange), rest light_blue | `highlight=`, `horizontal=True`, `sort=True` |
| `highlight_line()` | Line chart with one line colored (orange), rest light_blue | `highlight=`, `y_dict={}` |
| `action_title()` | Bold title + optional subtitle | `title`, `subtitle=` |
| `annotate_point()` | Clean annotation with arrow | `x`, `y`, `text`, `offset=` |
| `save_chart()` | Tight layout + white background + correct DPI | `fig`, `path`, `dpi=150` |

#### Coolblue Chart Library (preferred for new charts)

| Function | Purpose | Key Args |
|----------|---------|----------|
| `apply_coolblue_style()` | Apply Coolblue rcParams globally (white bg, brand colors) | — |
| `bar_chart()` | Bar chart from DataFrame | `df`, `x`, `y`, `highlight=`, `horizontal=True` |
| `line_chart()` | Line chart from DataFrame | `df`, `x`, `y` (str or list) |
| `yoy_line_chart()` | YoY overlay: each year as separate line + comparison table | `df`, `date_col`, `value_col` |
| `save_chart()` | Save with white background | `fig`, `path` |

### Theme Definition

#### Theme: `coolblue` (Default — only theme)
```python
COOLBLUE_THEME = {
    "colors": {
        "primary": "#FF6600",      # Orange — most important
        "secondary": "#285DAB",    # Fact Blue — second most important
        "tertiary": "#CCE9F9",     # Light Blue — supporting data
        "accent": "#0090E3",       # Coolblue Blue — axis labels, ticks
        "palette": ["#FF6600", "#285DAB", "#CCE9F9"],
        "background": "#FFFFFF",   # Always white
        "grid": "#E5E7EB",
    },
    "fonts": {
        "title": {"family": "sans-serif", "size": 14, "weight": "bold"},
        "subtitle": {"family": "sans-serif", "size": 10, "weight": "normal", "color": "#4B5563"},
        "axis_label": {"family": "sans-serif", "size": 10},
        "annotation": {"family": "sans-serif", "size": 9},
    },
    "grid": {"show": False, "axis": "y", "style": "-", "alpha": 0.15},
    "annotations": {"style": "minimal", "direct_labels": True},
    "title": {"position": "left-aligned", "include_subtitle": False},
}
```

All other themes (nyt, economist, minimal, corporate) are deprecated. Use the Coolblue theme for all charts.

### Chart Type Selection

| Data Relationship | Chart Type | When to Use |
|---|---|---|
| **Comparison** (categories) | Bar chart (horizontal) | Comparing categories — **default choice** |
| **Comparison** (few categories) | Bar chart (vertical) | Comparing ≤6 categories |
| **Change over time** | Line chart | Continuous time series, trends |
| **Change over time** (few periods) | Bar chart | Discrete periods (quarters, years) |
| **Year-over-Year** | YoY line chart | Each year as separate line + comparison DataFrame |

**Banned chart types:** Scatter plots, heatmaps, matrices, pie/donut charts, box plots, violin plots, area charts, waterfall charts, stacked bars, funnel charts, bump charts, radar charts, treemaps, bubble charts, and any other complex visualization. Convert to bar or line charts instead.

### Chart Design Standards

1. **Label key data points directly** on bars and line endpoints
2. **Titles are simple and clear** — "Sessions by segment (last 28 days)" is fine
3. **Format numbers for readability** — "€1.2M" not "€1,234,567"; "23%" not "0.2345"
4. **Use Coolblue colors only** — orange (primary), fact_blue (secondary), light_blue (supporting)
5. **No distracting elements** — no annotations, arrows, shaded regions, trendlines, or event markers unless essential
6. **Legend for multi-series** — clean, no frame, positioned to not overlap data

### Standard Chart Setup

```python
from helpers.coolblue_charts import apply_coolblue_style, bar_chart, line_chart, yoy_line_chart

apply_coolblue_style()

# Bar chart
fig, ax = bar_chart(df, x="revenue", y="segment", title="Revenue by segment")

# Line chart
fig, ax = line_chart(df, x="date", y="sessions", title="Sessions over time")

# YoY time series (returns chart + comparison DataFrame)
fig, ax, comparison_df = yoy_line_chart(
    df, date_col="date", value_col="sessions",
    title="Sessions by month — Year over Year",
)
```

## Anti-Patterns (Banned)

| Anti-Pattern | Why It's Bad | Use Instead |
|--------------|-------------|-------------|
| **Heatmaps / matrices** | Too complex, hard to read at a glance | Bar chart (horizontal) |
| **Pie / donut charts** | Humans can't compare angles accurately | Horizontal bar chart |
| **Scatter plots** | Too complex for product analytics | Bar or line chart |
| **Stacked bars** | Hard to compare non-baseline segments | Grouped bars or separate charts |
| **Area charts** | Obscures individual series values | Line chart |
| **Waterfall charts** | Overly complex | Bar chart with labels |
| **Rainbow palettes** | Visual noise, not brand-compliant | Coolblue colors only |
| **Dual y-axes** | Misleading — any two series can be made to "correlate" | Two separate charts, stacked vertically |
| **3D charts** | Distorts proportions, adds no information | Flat 2D versions |
| **Non-Coolblue colors** | Off-brand, inconsistent | Orange / Fact Blue / Light Blue only |
| **Colored backgrounds** | Distracting, not brand-compliant | Always white `#FFFFFF` |
| **Excessive annotations** | Clutters the chart | Keep it clean — title + legend + labels only |
| **Truncated y-axes** | Exaggerate small differences (for bar charts) | Start at zero for bar charts |
| **Default matplotlib styling** | Looks generic, unprofessional | Always apply `apply_coolblue_style()` first |

## Review Checklist

Before including any chart in an analysis:

- [ ] Chart type is bar (horizontal/vertical) or line — nothing else
- [ ] Colors are only from the Coolblue palette (orange, fact_blue, light_blue)
- [ ] Background is white (`#FFFFFF`)
- [ ] Title is simple and clear
- [ ] No chart border, no top/right spines
- [ ] Legend is clean for multi-series charts
- [ ] Gridlines removed or very light
- [ ] Axis labels are clean (no rotation, no trailing zeros)
- [ ] No distracting elements (no arrows, shaded regions, excessive annotations)
- [ ] The chart would be understood in 5 seconds
- [ ] YoY comparisons use overlaid lines (each year = separate line)
- [ ] YoY charts have a companion MoM/YoY comparison DataFrame
- [ ] Labels don't collide with bars, axes, or other labels
