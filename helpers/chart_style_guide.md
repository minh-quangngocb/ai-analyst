# Analytics Chart Style Guide

**Internal reference for all chart visualizations.**
Coolblue brand standards with clean, simple design.

---

## Philosophy

Every chart follows one rule: **keep it simple.**

- Use only bar charts (horizontal/vertical) and line charts
- Use only Coolblue brand colors
- Background is always white
- Title is simple and clear
- No distracting elements — the data speaks for itself

---

## Color Palette

Only Coolblue brand colors. No exceptions.

| Name | Hex | Usage |
|------|-----|-------|
| **Orange** | `#FF6600` | Most important element — primary highlight |
| **Fact Blue** | `#285DAB` | Second most important element |
| **Coolblue Blue** | `#0090E3` | Axis labels, tick marks |
| **Light Blue** | `#CCE9F9` | Supporting/context data — non-highlighted bars/lines |
| **Grey** | `#F7F6F2` | Subtle fills only (never as chart background) |
| **White** | `#FFFFFF` | Chart background — always white |
| **Text Dark** | `#1F2937` | Titles |
| **Text Mid** | `#4B5563` | Axis labels |
| **Text Light** | `#6B7280` | Tick labels |
| **Grid** | `#E5E7EB` | Gridlines (if used) |

### Rules

- **Only Coolblue colors** — no reds, greens, purples, ambers, or other colors
- **Color hierarchy**: Orange (most important) → Fact Blue (secondary) → Light Blue (supporting)
- **Background**: Always white (`#FFFFFF`)
- **No semantic colors** — no red for "bad" or green for "good"
- **Rainbow palettes are banned**

### Accessibility

The Orange / Fact Blue / Light Blue palette provides good visual separation.

- Always pair color with a second visual channel (direct labels, position, weight)
- Never rely on color alone to convey meaning

#### Font Size Minimums

All text in charts must meet minimum size requirements for legibility at
standard viewing distance and when projected:

| Element | Minimum Size | Recommended Size |
|---------|-------------|-----------------|
| **Chart titles** | 14pt | 17-18pt |
| **Axis labels** | 11pt | 11-12pt |
| **Tick labels** | 9pt | 10pt |
| **Data labels / annotations** | 9pt | 9-10pt |
| **Legend text** | 8pt | 9pt |

#### Chart Dimensions for Slides

Charts are rendered at standard figsize `(10, 6)` (~1500×900 @ 150 DPI) and
embedded directly on slides. CSS `object-fit: contain` in the theme handles
all containment — no chart-side resizing needed.

```python
from helpers.chart_helpers import CHART_FIGSIZE

fig, ax = plt.subplots(figsize=CHART_FIGSIZE)  # (10, 6)
# ... build chart ...
save_chart(fig, "outputs/charts/my_chart.png")
```

#### Date Axis Formatting

Time-series charts must show readable date labels. Matplotlib's default
`AutoDateFormatter` often produces fragments like "-01, -02" instead of
month names. Use `format_date_axis()` after plotting:

```python
from helpers.chart_helpers import format_date_axis

# After plotting time-series data:
format_date_axis(ax)           # Default: abbreviated month (Jan, Feb, Mar)
format_date_axis(ax, "%b %Y")  # Month + year (Jan 2024)
format_date_axis(ax, "%b '%y") # Short year (Jan '24)
```

The function handles both datetime-typed axes and string date axes. For
string axes, it attempts to parse labels with `pd.to_datetime()` and
re-format them. If parsing fails, the axis is left unchanged.

**Rule:** Every chart with a date/time x-axis MUST call `format_date_axis(ax)`
before saving. This is checked in the declutter checklist (Step 5b, item 10).

#### Title Spacing Rules

`action_title()` positions the title and subtitle using `transAxes`
coordinates:

| Element | Y-position | Font Size |
|---------|-----------|-----------|
| Title | `y=1.12` | 17pt bold |
| Subtitle | `y=1.06` | 12pt regular |

The 0.06 gap (1.12 − 1.06) provides sufficient separation.

#### Contrast Ratio Requirements

Text and visual elements must meet WCAG 2.1 contrast ratios:

| Element Type | Minimum Contrast Ratio | Notes |
|-------------|----------------------|-------|
| **Body text** (axis labels, annotations, data labels) | 4.5:1 | Against background color |
| **Large text** (titles, big numbers ≥18pt) | 3:1 | Against background color |
| **Non-text elements** (bars, lines, data points) | 3:1 | Against adjacent elements |
| **Heatmap cell text** | 4.5:1 | Against cell background — auto-switch white/dark |

The palette is pre-validated against the `#FFFFFF` white background:
- Text Dark (`#1F2937`) on white: ~16:1 (passes)
- Text Mid (`#4B5563`) on white: ~8:1 (passes)
- Orange (`#FF6600`) on white: ~4.6:1 (passes)
- Fact Blue (`#285DAB`) on white: ~7:1 (passes)
- Text Light (`#6B7280`) on white: ~5:1 (passes)
- Light Blue (`#CCE9F9`) on white: decorative use only — never for text

#### Alt Text Guidelines for Charts

Every chart saved to `outputs/` should have an accompanying alt text
description. Alt text enables screen reader access and serves as documentation.

**Structure:** Type + Data + Insight

1. **Chart type:** State what kind of chart it is (bar chart, line chart, etc.)
2. **Data description:** Summarize what data is shown (axes, categories, time range)
3. **Key insight:** State the main takeaway (matches the action title)

**Examples:**

- "Horizontal bar chart showing support ticket volume by category. Payment
  issues lead with 2,450 tickets, followed by shipping (1,200) and account
  (890). Payment issues drove the June spike."
- "Line chart showing monthly active users from Jan-Dec 2024. iOS usage
  spiked to 45,000 in June while Android remained stable at 28,000."
- "Slope chart comparing NPS scores before and after the redesign across 5
  product segments. Enterprise NPS improved from 32 to 58, the largest
  change."

**Rules:**
- Keep alt text under 150 words
- Always include the numeric values for highlighted data points
- Do not describe colors — describe the relationship or pattern
- Include the time range or date context when applicable
- Match the alt text takeaway to the chart's action title

---

## Declutter Checklist

Before finalizing any chart, remove or reduce:

- [ ] **Chart border / box** — remove entirely
- [ ] **Top and right spines** — remove (keep only bottom and left)
- [ ] **Heavy gridlines** — remove or use very light gray (`#E5E7EB`), y-axis only
- [ ] **Data markers** — remove from line charts (the line *is* the data)
- [ ] **Legend** — replace with direct labels on the data
- [ ] **Rotated axis text** — if labels need rotation, switch to horizontal bars
- [ ] **Trailing zeros** — use `$45` not `$45.00`; use `12%` not `12.0%`
- [ ] **3D effects** — never
- [ ] **Background color** — always white (`#FFFFFF`)
- [ ] **Redundant axis labels** — if the title says "Revenue ($M)", the y-axis doesn't need "Revenue in Millions of Dollars"
- [ ] **Excessive tick marks** — reduce to 4-6 ticks maximum
- [ ] **Decimal precision** — match the precision to the decision (don't show `12.347%` when `12%` suffices)

---

## Chart Type Decision Tree

Choose the simplest chart type. Only bar charts and line charts are allowed.

### Category Comparison → Horizontal Bar Chart (default)
- Sort bars by value (largest at top), not alphabetically
- Highlight the most important bar(s) in Orange (`#FF6600`), others in Light Blue (`#CCE9F9`)
- Use direct labels at end of bars (no x-axis needed)

### Few Categories → Vertical Bar Chart
- Use when comparing ≤6 categories
- Highlight the most important bar in Orange, rest in Light Blue

### Time Series → Line Chart
- For single series: use Orange (`#FF6600`)
- For multiple series: most important in Orange, secondary in Fact Blue, rest in Light Blue
- Use direct labels at the end of each line

### Year-over-Year → YoY Line Chart
- Each year is a separate line on ONE chart
- Most recent year → Orange `#FF6600` (thicker, optional markers)
- 2nd most recent → Fact Blue `#285DAB`
- Older years → Light Blue `#CCE9F9`
- MUST include companion DataFrame with MoM/YoY differences and % changes
- Use `yoy_line_chart()` from `helpers/coolblue_charts.py`

### Single Number → Big Bold Text
- Don't chart a single number — display it as large formatted text
- Add context: direction, comparison, or benchmark

### Banned Chart Types
All other chart types are banned. Convert them to bar or line charts:
- Heatmap/matrix → Horizontal bar chart
- Pie/donut → Horizontal bar chart
- Scatter → Bar chart (grouped if needed)
- Stacked bars → Grouped bars or separate charts
- Area chart → Line chart
- Waterfall → Bar chart with labels
- Funnel → Horizontal bar chart

---

## Chart Function Style Specifications

Rendering specs for the Coolblue chart library (`helpers/coolblue_charts.py`).

### bar_chart()

| Property | Value |
|----------|-------|
| **Bar color (highlighted)** | Orange `#FF6600` |
| **Bar color (non-highlighted)** | Light Blue `#CCE9F9` |
| **Sort** | By value (ascending for horizontal) |
| **Direct labels** | 9pt, at bar end, Text Dark color |
| **Background** | White `#FFFFFF` |
| **Spines** | Bottom + left only |

### line_chart()

| Property | Value |
|----------|-------|
| **Line colors** | Orange (1st), Fact Blue (2nd), Light Blue (3rd) |
| **Line width (primary)** | 2.5pt |
| **Line width (secondary)** | 1.8pt |
| **Markers** | None (line is the data) |
| **Gridlines** | Light y-axis only (Grid `#E5E7EB`, 0.5pt) |
| **Legend** | Upper left, frameless |

### yoy_line_chart()

| Property | Value |
|----------|-------|
| **Most recent year** | Orange `#FF6600`, 2.5pt, small markers (size 4) |
| **2nd most recent** | Fact Blue `#285DAB`, 1.5pt, no markers |
| **Older years** | Light Blue `#CCE9F9`, 1.5pt, no markers |
| **X-axis** | Month abbreviations (Jan, Feb, ..., Dec) |
| **Legend** | Upper left, frameless, year labels |
| **Companion table** | Year, Month, Value, MoM diff, MoM %, YoY diff, YoY % |

---

## Title & Annotation Rules

### Titles Tell the Story

Every chart title should be an **action title** — a sentence that states the takeaway.

| Type | Example |
|------|---------|
| **Descriptive (bad)** | "Monthly Support Tickets by Category" |
| **Action (good)** | "Payment issues drove the June ticket spike" |
| **Descriptive (bad)** | "Conversion Rate by Device" |
| **Action (good)** | "Mobile converts at half the rate of desktop" |
| **Action (good)** | "Ticket rate climbed 4x — independent of business growth" |

### Font Hierarchy

| Element | Weight | Size | Color |
|---------|--------|------|-------|
| **Title** | Bold | 17pt | Gray 900 (`#1F2937`) |
| **Subtitle** | Regular | 12pt | Gray 600 (`#6B7280`) |
| **Axis labels** | Regular | 10pt | Gray 600 (`#6B7280`) |
| **Annotations** | Regular | 9pt | Gray 900 or Action Amber |
| **Data labels** | Regular | 9pt | Match the data element color |

### Annotation Guidelines

- Place annotations **close to the data point** they reference
- Use a thin arrow only when the label can't sit directly on the data
- Keep annotation text short (under 10 words)
- Align annotations consistently (all left, all right, or all centered)
- Don't annotate everything — annotate only what supports the story

---

## Story Structure

Multi-chart analyses (deep dives, root cause investigations) follow **Context → Tension → Resolution**:

### Context (1-2 charts)
Set the baseline. What does normal look like?
- "[Dataset] processes ~4,000 support tickets per month"
- Use a simple time series or summary stat

### Tension (2-3 charts)
Reveal the problem. What changed, and where?
- "In June, tickets spiked to 6,200 — a 55% increase"
- "The spike was concentrated in iOS payment issues"
- Use progressively focused charts that zoom in on the anomaly

### Resolution (1-2 charts)
Explain why and recommend action.
- "iOS app version 2.3 introduced a payment processing bug"
- "Fixing the bug would eliminate ~2,200 tickets/month"
- End with the recommendation, not just the finding

### Sequencing Rules

- Each chart should build on the previous one
- Never show a chart that makes the audience ask "so what?"
- The final chart should make the recommended action obvious
- Limit to 4-6 charts for a complete analysis (not 12)

---

## Anti-Patterns

These are **banned** from all course materials:

| Anti-Pattern | Why It's Bad | Use Instead |
|--------------|-------------|-------------|
| **Pie charts** | Humans can't compare angles accurately | Horizontal bar chart |
| **Rainbow palettes** | No natural ordering, visual noise | Gray + one highlight color |
| **Spaghetti lines** | Too many colored lines, nothing stands out | Gray all lines, highlight one |
| **Dual y-axes** | Misleading — any two series can be made to "correlate" | Two separate charts, stacked vertically |
| **3D charts** | Distorts proportions, adds no information | Flat 2D versions |
| **Descriptive titles** | Don't tell the reader what to think | Action titles (state the takeaway) |
| **Legend boxes** | Force the reader to look away from the data | Direct labels on the data |
| **Excessive gridlines** | Create visual clutter | Light y-axis gridlines only, or none |
| **Truncated y-axes** | Exaggerate small differences (for bar charts) | Start at zero for bar charts |
| **Cluttered annotations** | Annotating every data point defeats the purpose | Annotate only the story |

---

## Before/After Examples

The `examples/` directory contains paired comparisons using sample data:

| Before | After | What Changed |
|--------|-------|-------------|
| ![](examples/before_bar.png) | ![](examples/after_bar.png) | Default bar chart → sorted, highlighted, action title |
| ![](examples/before_stacked.png) | ![](examples/after_stacked.png) | Rainbow stacked bars → gray + highlight |
| ![](examples/before_spaghetti.png) | ![](examples/after_spaghetti.png) | Multi-line spaghetti → focused single line |
| ![](examples/before_analysis.png) | ![](examples/after_analysis.png) | 6-panel dump → Context-Tension-Resolution |

---

## Applying the Style

### Quick Start

```python
from helpers.chart_helpers import swd_style, highlight_bar, action_title, save_chart

# Load the style
colors = swd_style()

# Create a chart
fig, ax = plt.subplots()
highlight_bar(ax, categories, values, highlight="iOS", color=colors["action"])
action_title(ax, "iOS drives 60% of all support tickets", "{{DISPLAY_NAME}}, {{DATE_RANGE}}")
save_chart(fig, "outputs/my_chart.png")
```

### Using the .mplstyle File Directly

```python
plt.style.use("helpers/analytics_chart_style.mplstyle")
```

### Color Palette Access

```python
from helpers.chart_helpers import swd_style

colors = swd_style()
# colors["action"]   → "#D97706"
# colors["accent"]   → "#DC2626"
# colors["gray200"]  → "#E5E7EB"
# colors["gray600"]  → "#6B7280"
```

---

## Common Gotchas

Practical issues discovered during chart production. Check these before finalizing.

### YoY Comparisons — Don't Use Two Similar Bars

Side-by-side bars in two shades of gray (or two muted colors) are nearly indistinguishable. For year-over-year or period-over-period comparisons:

- **Use overlaid lines** with the current period in Action Amber and the prior period in Gray 200
- **Add `fill_between`** to shade the gap between the two lines (Gray 100, alpha 0.3)
- **Use end-of-line labels** showing the period and total (e.g., "2024 (9.5M)")
- Reserve side-by-side bars for category comparisons where bars have distinct highlight colors

### Negative Bar Labels — Pad the Axis

When a bar chart has negative values, direct labels placed outside the bar end can collide with category names on the opposite axis:

- Compute `x_min` and `x_max` from the data, then set `ax.set_xlim(x_min - padding, x_max + padding)`
- For negative bars, place labels to the left of the bar end; for positive bars, to the right
- A padding of 2-3 percentage points (for % data) or ~10% of the range works well

### Contextual Events — Make Them Prominent

External events that explain anomalies (product launches, outages, wildfires, policy changes) must be visually prominent. A small gray annotation arrow is not enough:

- Use a **bbox annotation** with a colored border: `bbox=dict(boxstyle="round,pad=0.4", fc="white", ec=COLORS["accent"], lw=1.5)`
- Place the annotation where the eye naturally lands (near the affected data point)
- Short, specific text: "Lahaina wildfire (Aug 2023)" not "External event occurred"

### Annotation Collisions — Switch to Direct Labels

When multiple data points are close together (e.g., consecutive months all annotated), arrow-style annotations pile up and become unreadable:

- **Drop the arrows** — use direct labels placed just above/below each bar or point
- If only one point is the story, annotate only that one and let the rest speak for themselves
- Use semantic color (e.g., Danger Red for the worst month) to draw the eye instead of an arrow

### Annotation-Label Collisions — Check Before Saving

When using `annotate_point()` on a chart that also has direct data labels, the arrow
and text can overlap existing labels:

- Before adding an annotation, check if any existing data label occupies the same region
- If collision: (1) move the annotation offset, (2) drop the arrow and use color emphasis,
  or (3) remove the data label at the collision point
- Test at final DPI — collisions that look fine at screen resolution may overlap at 150 DPI

### Multi-Panel Charts — Bypass `tight_layout()`

`save_chart()` calls `fig.tight_layout()` internally, which overrides manual `fig.subplots_adjust()` and `fig.text()` positioning. For charts with:

- **Figure-level titles** (via `fig.text()`)
- **Manual `subplots_adjust(top=...)`** to make room for those titles
- **Multiple subplots** with their own panel headers

Use direct `fig.savefig()` instead of `save_chart()`:

```python
fig.savefig(path, dpi=150, bbox_inches="tight", facecolor="#F7F6F2", edgecolor="none")
plt.close(fig)
```

This preserves your manual spacing. Only use `save_chart()` for single-panel charts where `tight_layout()` is helpful.

---

## Review Checklist

Before including any chart in course materials:

- [ ] Title states the takeaway (not a description)
- [ ] Only 1-2 colors used (plus gray)
- [ ] No chart border, no top/right spines
- [ ] Direct labels instead of legend
- [ ] Gridlines removed or very light
- [ ] Axis labels are clean (no rotation, no trailing zeros)
- [ ] Annotations are minimal and support the story
- [ ] Chart type matches the data relationship
- [ ] A single number isn't charted — it's displayed as text
- [ ] The chart would be understood in 5 seconds
- [ ] YoY comparisons use lines (not two similar-colored bars)
- [ ] Labels don't collide with bars, axes, or other labels
- [ ] External context events have prominent bbox annotations
- [ ] Multi-panel charts with fig-level titles use direct `savefig()` (not `save_chart()`)
