---
name: presentation-themes
description: "Theme standards for slide decks: layouts, typography, color palettes, and content density."
user-invocable: false
---
# Presentation Themes

## Purpose
Generate slide decks that look professional, tell a coherent analytical story, and follow consistent theme standards matching the visualization patterns.

## When to Use
Apply this skill whenever creating a presentation, slide deck, or structured output intended for stakeholders. Always apply the Coolblue theme. Default theme: `coolblue`.

## Instructions

### Slide Structure Templates

Every presentation follows this arc:

```
Title → Executive Summary → Context → Insight Slides → Synthesis → Recommendations → Appendix
```

#### Slide Types

**1. Title Slide**
```markdown
# [Takeaway headline — not "Q3 Analysis"]
## [Subtitle: scope, date range, audience]
### [Author / Team] | [Date]
```

**2. Executive Summary Slide**
```markdown
# [Key takeaway in one sentence]

- **Finding 1:** [One sentence with key number]
- **Finding 2:** [One sentence with key number]
- **Finding 3:** [One sentence with key number]

**Recommendation:** [One clear action]
```

**3. Context / Setup Slide**
```markdown
# [Why we looked at this]

- **Question:** [The business question that triggered this analysis]
- **Data:** [What data we used, time range, scope]
- **Method:** [How we analyzed it — one sentence]
```

**4. Insight Slide (one per finding)**
```markdown
# [Finding as a headline — "Mobile conversion dropped 18% in Q3"]

[ONE chart that proves this finding]

- [Supporting detail 1]
- [Supporting detail 2]

**So what:** [Why this matters for the business]
```

**5. Synthesis Slide**
```markdown
# [So what? — The combined story]

[How the findings connect to each other and what they mean together]

- **Pattern:** [What the findings reveal as a whole]
- **Root cause:** [If identified]
- **Magnitude:** [How big is this? Revenue impact, user impact]
```

**6. Recommendation Slide**
```markdown
# [Action to take — imperative verb]

| Action | Owner | Timeline | Expected Impact |
|--------|-------|----------|-----------------|
| [Action 1] | [Team] | [When] | [Quantified if possible] |
| [Action 2] | [Team] | [When] | [Quantified if possible] |

**Next step:** [The one thing to do Monday morning]
```

**7. Appendix Slide**
```markdown
# Appendix: [Topic]

[Supporting data, methodology details, caveats, additional charts]
[This is where you put things that support the story but would slow down the main narrative]
```

### Narrative Arc

Every deck follows: **Situation → Analysis → Finding → Implication → Recommendation**

| Arc Element | Slide Types | Purpose |
|---|---|---|
| **Situation** | Context slide | Why are we here? What question are we answering? |
| **Analysis** | (Implied — the work happened) | Don't show methodology unless asked |
| **Finding** | Insight slides (1 per finding) | What did we discover? One chart, one headline per finding. |
| **Implication** | Synthesis slide | So what? Why does this matter? |
| **Recommendation** | Recommendation slide | Now what? What should we do? |

### Content Density Rules

1. **Maximum 3 bullet points per slide** — if you need more, split into two slides
2. **One chart per slide** — never stack charts; each deserves its own headline
3. **Headlines are takeaways, not labels** — "Mobile conversion dropped 18%" not "Conversion by Device"
4. **No full sentences in bullets** — fragments with key numbers
5. **Slide count guidance**: 5-8 slides for a 10-minute readout, 10-15 for a 30-minute presentation
6. **The "headline test"**: read only the headlines in sequence — they should tell the complete story

### Theme Specifications

#### Theme: `coolblue`
- Title font: Open Sans Bold, 52pt (title), 32pt (content), #FFFFFF on blue, #1A1A1A on white
- Body font: Open Sans, 24pt, #1A1A1A on white, rgba(255,255,255,0.9) on blue
- Brand color: #0090E3 (Coolblue Blue)
- Title/agenda background: #0090E3 (Coolblue Blue)
- Content background: #FFFFFF (white) with blue bottom bar (#0090E3, 1/5 of slide height)
- Slide title (h2) renders inside the blue bottom bar in white
- Logo: Coolblue logo top-right on title and agenda slides (`templates/coolblue_logo.png`)
- Footer: current date
- Positive metrics: #059669, Negative metrics: #DC2626
- Marp CSS theme: `themes/coolblue.css`
- Best for: Coolblue internal presentations, stakeholder readouts, team reviews

**Coolblue theme structure (mandatory):**
- Slide 1: `cb-title` — blue background, logo, deck title, subtitle
- Slide 2: `cb-agenda` — blue background, logo, numbered agenda
- Slides 3+: white background content slides with blue bar at bottom

**Coolblue content slide rules:**
- **Short statements:** Use `chart-full`. One chart per slide from `outputs/charts/`. No extra text — the chart tells the story. One statement can span multiple slides with different supporting charts.
- **Detailed points:** Use `takeaway`. Concise bullet points (max 4). Minimal math/numbers. Plain language for stakeholders.
- Font: Open Sans throughout. Black text on white background, white text on blue background.

**Coolblue slide classes:**

| Variant | Class Directive | Purpose |
|---------|----------------|---------|
| Title | `<!-- _class: cb-title -->` | Blue background, logo, opening slide |
| Agenda | `<!-- _class: cb-agenda -->` | Blue background, logo, numbered agenda |
| Section opener | `<!-- _class: section-opener -->` | Blue background, topic transition |
| Chart-full | `<!-- _class: chart-full -->` | White + blue bar, one chart, short statement |
| Takeaway | `<!-- _class: takeaway -->` | White (no bar), concise bullet points |
| Impact | `<!-- _class: impact -->` | White (no bar), centered statement |
| KPI | `<!-- _class: kpi -->` | White + blue bar, metric cards |
| Chart-left | `<!-- _class: chart-left -->` | White + blue bar, 60/40 chart + text |
| Chart-right | `<!-- _class: chart-right -->` | White + blue bar, 40/60 text + chart |
| Recommendation | `<!-- _class: recommendation -->` | White + blue bar, action items |
| Appendix | `<!-- _class: appendix -->` | White + blue bar, reference material |

### Automatic Theme Selection

The `coolblue` theme is the default and only supported theme. All decks use Coolblue brand styling.

| Condition | Theme | Rationale |
|-----------|-------|----------|
| Default | `coolblue` | All presentations use Coolblue branding |
| `{{THEME}}` explicitly provided | Use as-is | Explicit override accepted |

Pass `{{THEME}}` to override auto-selection for any context.

### Font Size Minimums for Presentations

These minimums ensure readability during screen-share and projection:

| Element | Minimum Size | Recommended |
|---------|-------------|-------------|
| h1 (title slides) | 48px | 52px |
| h1 (content slides) | 44px | 44px |
| h2 | 36px | 36px |
| h3 | 28px | 28px |
| Body / paragraphs | 24px | 24px |
| List items | 22px | 22px |
| Minimum readable | 16px | — |
| Footer / page numbers | 12-14px | 14px |

Nothing except footers and page numbers should be below 16px. If text must be smaller, it belongs in the appendix or speaker notes.

### QR Code Integration Pattern

When embedding QR codes on slides, use a clean container:

```html
<div style="background:#fff; border-radius:10px; padding:6px; display:inline-block;">
  <img src="qr-code.png" style="width:140px; height:140px; display:block;">
</div>
<div style="font-size:14px; color:#9CA3AF; margin-top:6px;">Scan for [description]</div>
```

Sizing: 120-160px for supporting QR codes, 180-220px for primary CTA QR codes.

### Workshop Closing Sequence Template

Optional slide sequence for workshop/talk decks. Add after the recommendation or appendix slides:

1. **Course overview slide** — Brief description of full course offering with QR code link
2. **Free resource slide** — Email course, community, newsletter with QR code
3. **Free workshops slide** — Upcoming dates and topics
4. **CTA / discount slide** — Discount code, enrollment link, contact info

This sequence follows an **escalating commitment pattern**: free resources first (low barrier), then paid offering (higher commitment). Never lead with the paid CTA.

### Speaker Notes Engagement Tactics

Enhance speaker notes beyond standard talking points with these engagement markers:

- **Audience polls**: `[POLL] "Drop in chat: 1, 2, or 3 — which scenario is closest to your team?"`
- **Show of hands**: `[HANDS] "Raise your hand if you've ever waited 2+ weeks for an analysis"`
- **Reflective pause**: `[PAUSE — let this sink in]`
- **Story sharing**: `[ASK] "Has anyone seen something like this at their company?"`
- **Transition cues**: `[ADVANCE]` or `[NEXT SLIDE]`
- **Chat engagement**: `[CHAT] "Type your biggest analytics pain point in the chat"`

Place engagement markers at natural breaks — after revealing a key number, before transitioning to recommendations, or when introducing a framework.

### Export Formats

**Marp PDF (Coolblue theme):**

Marp converts markdown directly to PDF via Chromium.

```markdown
---
marp: true
theme: coolblue
size: 16:9
paginate: true
html: true
footer: "March 26, 2026"
---

<!-- _class: cb-title -->

<div class="logo"><img src="templates/coolblue_logo.png" alt="Coolblue"></div>

# Slide Headline

## Subtitle

---

<!-- _class: chart-full -->

## Next Slide Headline

<div class="chart-container">
  <img src="charts/chart.png" alt="Description">
</div>

<!--
Speaker Notes:
"Notes go in HTML comments."
-->
```

Generate PDF with:
```bash
npx @marp-team/marp-cli --no-stdin --pdf --html --allow-local-files \
  --theme themes/coolblue.css \
  outputs/deck_name.marp.md \
  -o outputs/deck_name.pdf
```

**Speaker Notes Format:**
Every slide includes speaker notes with:
- Opening line (what to say when this slide appears)
- 2-3 talking points
- Transition to next slide
- Anticipated questions

## Examples

### Example 1: Correct chart slide (Coolblue)
```markdown
<!-- _class: chart-full -->

## Mobile conversion dropped 18% in Q3

<div class="chart-container">
  <img src="charts/conversion_by_device.png" alt="Conversion rate by device">
</div>
```

### Example 2: Correct takeaway slide (Coolblue)
```markdown
<!-- _class: takeaway -->

## Q3 conversion decline is fixable

- Mobile fell 18% after iOS 18 update broke checkout
- Desktop held steady, confirming the issue is mobile-specific
- Engineering estimates 2-week fix, recovering ~$340K/month
```

## Anti-Patterns

1. **Never put more than one chart on a slide** — each finding deserves its own space
2. **Never use label headlines** ("Revenue by Quarter") — use takeaway headlines ("Revenue grew 23%")
3. **Never exceed 3 bullet points** — if you need more, you need another slide
4. **Never show methodology in the main deck** — put it in the appendix
5. **Never skip the "so what"** — every insight slide must answer "why does this matter?"
6. **Never create a deck without a recommendation slide** — analysis without action is wasted
7. **Never use full sentences as bullets** — use fragments with key numbers
8. **Never present findings in the order you discovered them** — present in the order that tells the best story
