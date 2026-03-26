---
marp: true
theme: coolblue
size: 16:9
paginate: true
html: true
footer: "{{DATE}}"
---

<!-- _class: cb-title -->

<div class="logo"><img src="../templates/coolblue_logo.png" alt="Coolblue"></div>

# {{DECK_TITLE}}

## {{SUBTITLE}}

<!--
Speaker Notes:
"Opening context. What question are we answering today? [PAUSE] [ADVANCE]"
-->

---

<!-- _class: cb-agenda -->

<div class="logo"><img src="../templates/coolblue_logo.png" alt="Coolblue"></div>

## Agenda

1. Context & background
2. Key findings
3. Deep dive
4. Recommendations
5. Next steps

<!--
Speaker Notes:
"Here's what we'll cover today. [ADVANCE]"
-->

---

<!-- _class: section-opener -->

## Context

The setup — what happened and why we looked into it

<!--
Speaker Notes:
"Before diving into findings, let me set the stage. [ADVANCE]"
-->

---

<!-- _class: kpi -->

## The headline finding with specific numbers

<div class="kpi-row">
  <div class="kpi-card">
    <div class="kpi-value negative">-59%</div>
    <div class="kpi-label">Conversion Rate</div>
    <div class="kpi-delta down">Feb → Dec 2024</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-value">250K</div>
    <div class="kpi-label">Monthly Sessions</div>
    <div class="kpi-delta up">+28x growth</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-value accent">81%</div>
    <div class="kpi-label">Returning Users</div>
    <div class="kpi-delta flat">of session mix</div>
  </div>
</div>

<!--
Speaker Notes:
"Three numbers that tell the story. [PAUSE] Each card is one metric — no chart needed. [ADVANCE]"
-->

---

<!-- _class: chart-full -->

## Conversion declined steadily across all segments

<div class="chart-container">
  <img src="../outputs/charts/beat1_example.png" alt="Line chart showing conversion decline by segment">
</div>

<!--
Speaker Notes:
"One chart, maximum space. The chart tells the story — no extra text needed. [PAUSE] [ADVANCE]"
-->

---

<!-- _class: chart-full -->

## A short statement supported by the evidence

<div class="chart-container">
  <img src="charts/beat2_example.png" alt="Chart supporting the statement">
</div>

<!--
Speaker Notes:
"Let the chart do the talking. One statement, one visual. [ADVANCE]"
-->

---

<!-- _class: takeaway -->

## The blended conversion rate is misleading

- The mix shifted toward low-converting segments
- Every segment improved individually
- Aggregate decline is a composition effect, not a real decline

<!--
Speaker Notes:
"Concise bullet points for deeper context. Keep it simple for stakeholders. [ADVANCE]"
-->

---

<!-- _class: chart-right -->

## Narrative on the left, chart on the right

- **Segment A:** declined from 9.2% to 6.1%
- **Segment B:** stable at ~2.2%
- Mix shifted 38% toward low-conversion users

<div class="chart-container">
  <img src="charts/beat3_example.png" alt="Chart showing segment comparison">
</div>

<!--
Speaker Notes:
"Left side: concise bullet points. Right side: visual evidence. [ADVANCE]"
-->

---

<!-- _class: impact -->

## What should we do about this?

<!--
Speaker Notes:
"[PAUSE for effect] This is the pivot from diagnosis to action. [ADVANCE]"
-->

---

<!-- _class: recommendation -->

## Recommendations

<div class="rec-row">
  <div class="rec-number">1</div>
  <div class="rec-content">
    <div class="rec-action">Highest-confidence action item</div>
    <div class="rec-rationale">Why this matters and expected impact</div>
  </div>
  <div class="rec-confidence high">HIGH</div>
</div>

<div class="rec-row">
  <div class="rec-number">2</div>
  <div class="rec-content">
    <div class="rec-action">Second priority action</div>
    <div class="rec-rationale">Supporting rationale</div>
  </div>
  <div class="rec-confidence medium">MEDIUM</div>
</div>

<div class="rec-row">
  <div class="rec-number">3</div>
  <div class="rec-content">
    <div class="rec-action">Lower confidence exploration</div>
    <div class="rec-rationale">Requires additional data</div>
  </div>
  <div class="rec-confidence low">LOW</div>
</div>

<!--
Speaker Notes:
"Three recommendations, ordered by confidence. [Walk through each] [ADVANCE]"
-->

---

<!-- _class: appendix -->

## Appendix: Methodology & Caveats

- **Data source:** {{DISPLAY_NAME}} analytics warehouse, {{DATE_RANGE}}
- **Cohort definition:** Users with at least one session in the analysis period
- **Exclusions:** Bot traffic filtered via User-Agent rules (< 0.3% of sessions)
- **Statistical tests:** Two-proportion z-test for segment comparisons (p < 0.01)

<!--
Speaker Notes:
"Reference slide — not presented live unless asked. [END]"
-->
