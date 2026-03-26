# Agent Index

## System Variables (auto-resolved)
| Variable | Value | Used in |
|----------|-------|---------|
| `{{DATE}}` | Current date, YYYY-MM-DD | All agent output filenames |
| `{{DATASET_NAME}}` | Short name derived from data path or user input | File naming, report headers |
| `{{BUSINESS_CONTEXT_TITLE}}` | Short title derived from `{{BUSINESS_CONTEXT}}` | Question brief header |
| `{{RUN_ID}}` | Unique run identifier (YYYY-MM-DD_question-slug) | Run Pipeline, Resume Pipeline |
| `{{RUN_DIR}}` | Per-run output directory path | All agents during pipeline |
| `{{SQL_PATTERNS}}` | Archaeology-retrieved SQL patterns | Analysis agents |
| `{{CORRECTIONS}}` | Logged corrections for current context | Analysis agents |
| `{{LEARNINGS}}` | Category-specific learnings | Question Framing, Storytelling |
| `{{ENTITY_INDEX}}` | Disambiguation index | Question Router |
| `{{ORG_CONTEXT}}` | Business context (glossary, products, teams) | Question Framing, Storytelling |
| `{{THEME}}` | Active theme name | Chart Maker, Deck Creator |
| `{{CONTEXT}}` | Presentation context (workshop/talk/analysis) | Story Architect, Deck Creator |
| `{{STORYBOARD}}` | Story Architect output | Chart Maker, Storytelling |
| `{{FIX_REPORT}}` | Visual Design Critic feedback | Chart Maker (fix pass) |
| `{{DECK_FILE}}` | Generated deck path | Visual Design Critic |
| `{{CONFIDENCE_GRADE}}` | Validation confidence score (A-F) | Storytelling, Deck Creator |

## Agents
| Agent | Path | Invoke When |
|-------|------|-------------|
| Question Framing | `.github/agents/question-framing.agent.md` | User provides a business problem to analyze |
| Hypothesis | `.github/agents/hypothesis.agent.md` | Questions are framed, need testable hypotheses |
| Data Explorer | `.github/agents/data-explorer.agent.md` | Need to understand what data exists in a source |
| Descriptive Analytics | `.github/agents/descriptive-analytics.agent.md` | Need to analyze a dataset (segmentation, funnels, drivers) |
| Overtime / Trend | `.github/agents/overtime-trend.agent.md` | Need time-series analysis or trend identification |
| Cohort Analysis | `.github/agents/cohort-analysis.agent.md` | Need cohort retention curves, LTV analysis, or vintage comparison |
| Root Cause Investigator | `.github/agents/root-cause-investigator.agent.md` | Initial analysis found an anomaly — need to drill down iteratively to find the specific root cause |
| Opportunity Sizer | `.github/agents/opportunity-sizer.agent.md` | Root cause identified or opportunity found — quantify the business impact with sensitivity analysis |
| Experiment Designer | `.github/agents/experiment-designer.agent.md` | Need to test a causal hypothesis — designs A/B tests or quasi-experimental analyses with power estimation and decision rules |
| Story Architect | `.github/agents/story-architect.agent.md` | Analysis is complete — designs the storyboard (narrative beats + visual mapping) before any charting. Pass `{{CONTEXT}}` for workshop/talk closing sequences. |
| Chart Maker | `.github/agents/chart-maker.agent.md` | Need to generate a specific chart. |
| Visual Design Critic | `.github/agents/visual-design-critic.agent.md` | After Chart Maker generates charts — reviews against SWD checklist. After Deck Creator — reviews slide-level design with `{{DECK_FILE}}` and `{{THEME}}`. |
| Narrative Coherence Reviewer | `.github/agents/narrative-coherence-reviewer.agent.md` | After Story Architect produces the storyboard, before charting — reviews story flow, beat structure, and Closing beats if present |
| Storytelling | `.github/agents/storytelling.agent.md` | Analysis and charts are complete, need a narrative |
| Validation | `.github/agents/validation.agent.md` | Need to verify findings before presenting |
| Deck Creator | `.github/agents/deck-creator.agent.md` | Need to create a presentation from analysis. Uses `coolblue` theme by default. Supports `{{THEME}}` override and `{{CONTEXT}}` (workshop/talk closing sequence). |
| Comms Drafter | `.github/agents/comms-drafter.agent.md` | Need stakeholder communications (Slack summary, email brief, exec summary). Non-critical — pipeline continues if this fails. |
| BigQuery Notebook Builder | `.github/agents/bigquery-notebook-builder.agent.md` | Need to create or refactor BigQuery Jupyter notebooks so SQL lives in separate `.sql` files and notebook cells load SQL files before execution. |
| Notebook Analyst | `.github/agents/notebook-analyst.agent.md` | End-to-end notebook-based analysis — takes Phase 1 framing, asks user for analysis type (descriptive/cohort/trend), writes SQL to working/sql/, builds a Jupyter notebook with queries + analysis + charts + validation + recommendations. |
