---
name: resume-pipeline
description: "Detect existing artifacts, determine last completed step, and resume analysis."
disable-model-invocation: true
---
# Resume Pipeline

## Purpose
Resume an interrupted analysis pipeline by reading `working/pipeline_state.json`, determining which phase and agents completed, and continuing from the next phase using the run-pipeline orchestrator.

## When to Use
Invoke as `/resume-pipeline` when:
- A previous analysis session was interrupted (context limit, user break, connection issue)
- The user wants to continue an analysis started in a prior conversation
- Pipeline state file exists from a partially completed run
- A pipeline failed and the underlying issue has been fixed

## Instructions

### Step 1: Locate pipeline state (per-run directory aware)

Search for the most recent pipeline state in this order:

1. **Per-run directory (preferred):** Check `working/latest/pipeline_state.json` (symlink to latest run).
   If found, set `RUN_DIR` from the symlink target and proceed to Step 2.
2. **Specific run:** If the user passed a run ID (e.g., `/resume-pipeline 2026-02-23_pfa_why-revenue-dropped`),
   look in `working/runs/{id}/pipeline_state.json`. Set `RUN_DIR` accordingly.
3. **Legacy location:** Check `working/pipeline_state.json` (pre-run-directory pipelines).
   If found, read it and proceed to Step 2 without a `RUN_DIR`.
4. **No state found:** Fall back to artifact scanning (Step 1b).

**Pipeline state fields to extract (V2):**
- `run_id` — identifies this run
- `run_dir` — per-run directory path (may be absent for legacy runs)
- `dataset` — active dataset
- `question` — the business question
- `plan` — execution plan (`full_presentation`, `deep_dive`, `quick_chart`, `refresh_deck`, `validate_only`)
- `status` — `running`, `paused`, or `failed`
- `agents` — map of agent-name to agent state (status, output_file, timestamps)
- `phase_completed` — highest completed phase number (0–4)

### Step 1a: V1-to-V2 state migration

After loading the state file and before any processing, check whether the state
uses the V1 (step-number keyed) format and migrate it to V2 if needed.

```python
from helpers.pipeline_state import detect_schema_version, migrate_v1_to_v2

if detect_schema_version(state) < 2:
    # Resolve dataset from active.yaml or fall back to "unknown"
    dataset = state.get("dataset") or resolve_active_dataset() or "unknown"
    state = migrate_v1_to_v2(state, dataset=dataset)
    # Write migrated state back to disk (same location it was read from)
    write_pipeline_state(state_path, state)
    print("Migrated pipeline state from V1 -> V2 format")
```

**Migration details** (handled by `helpers/pipeline_state.py`):
- `pipeline_id` (ISO timestamp) → `started_at`; generate `run_id` from date + dataset + question slug
- `steps.{n}.agent` keys → `agents.{agent_name}` keys
- `steps.{n}.output_files[0]` → `agents.{name}.output_file` (take first)
- Status values are preserved as-is (compatible between V1 and V2)
- Adds `schema_version: 2` and `updated_at` set to current time
- If any V1 step had `status: running`, it becomes `paused` at the pipeline level (was interrupted)

After migration, continue with the V2 fields listed above.

### Step 1b: Artifact-based fallback (no pipeline_state.json)

If no state file exists, scan `working/` and `outputs/` for artifacts to
determine which phases completed. Walk top-to-bottom; if an artifact exists and
looks complete (not empty, no "NEEDS REVISION" markers), mark that agent as
completed.

**Phase 0 — Knowledge Bootstrap (metadata only):**

Phase 0 does not produce pipeline artifacts. It is always re-run on resume
(see Step 2a). No artifact scan needed.

**Phase 1 — Framing & Exploration:**

| Agent | Expected Artifact | Directory |
|-------|-------------------|-----------|
| question-framing | `question_brief_*.md` | `outputs/` |
| data-explorer | `data_feasibility_*.md` | `outputs/` |
| hypothesis | `hypothesis_doc_*.md` | `outputs/` |

**Phase 2 — Analysis via Notebook Analyst:**

| Agent | Expected Artifact | Directory |
|-------|-------------------|-----------|
| Notebook Analyst | `<analysis_slug>.ipynb` | `working/` |
| (SQL files) | `*.sql` | `working/sql/` |
| (charts from notebook) | `*.png` | `outputs/charts/` |

**Note:** Phase 2 uses a single **Notebook Analyst** agent — NOT individual
analysis agents (descriptive-analytics, overtime-trend, etc.). The Notebook
Analyst wraps all analysis types (descriptive, trend, cohort), root cause
investigation, validation, and opportunity sizing into one self-contained
Jupyter notebook. If a notebook exists in `working/` with executed cells and
chart outputs, Phase 2 is complete.

Also check for `working/analysis_summary.md` — this is the structured handoff
file extracted from the notebook's final markdown cell. Phase 7+ agents read
this file (not CSVs) as `{{ANALYSIS_RESULTS}}`. If the notebook exists but
`analysis_summary.md` does not, extract it from the notebook's last markdown
cell (headed `## Pipeline Handoff — Analysis Summary`) and write it to
`working/analysis_summary.md` before proceeding.

**Phase 3 — Storytelling & Charts:**

| Agent | Expected Artifact | Directory |
|-------|-------------------|-----------|
| story-architect | `storyboard_*.md` | `working/` |
| narrative-coherence-reviewer | `coherence_review_*.md` | `working/` |
| chart-maker | `charts/*.png` (from storyboard) | `outputs/` |
| visual-design-critic | `design_review_*.md` | `working/` |

**Phase 4 — Deck & Delivery:**

| Agent | Expected Artifact | Directory |
|-------|-------------------|-----------|
| storytelling | `narrative_*.md` | `outputs/` |
| deck-creator | `deck_*.md` | `outputs/` |
| visual-design-critic (slides) | `slide_review_*.md` | `working/` |
| comms-drafter | `comms_*.md` | `outputs/` |

Reconstruct a `pipeline_state.json` from this scan and save it.

### Step 2: Re-run Phase 0 (Knowledge Bootstrap — MANDATORY)

Phase 0 is **always re-run on resume**, even if it completed before. It reads
only metadata files and is fast. This ensures the agent has the correct dataset
context for all downstream work.

Follow the Phase 0 instructions from `run-pipeline.agent.md`:

1. Read `.knowledge/active.yaml` → get `active_dataset`
2. Load `.knowledge/datasets/{active_dataset}/manifest.yaml` → extract
   `dataset_project`, `dataset`, `tables`, `filters`
3. Load schema and quirks files
4. Load the dataset-specific skill (PFA, GA4, or Transaction Margin)

**IMPORTANT — GCP project distinction (from Phase 0):**
- **Dataset project** (`cb-data-hub-prod`): where tables live. Only in SQL.
- **Auth/billing project** (`coolblue-marketing-dev`): via `GOOGLE_CLOUD_PROJECT`.
- Never confuse these. Never create or modify `.env`.

Print the dataset summary and carry the resolved context forward.

### Step 3: Compute READY set from phases and agents

1. Read `.github/agents/registry.yaml` to build the dependency graph
2. For each agent in the registry, check `state["agents"][agent_name]["status"]`:
   - If status is `complete`, `skipped`, or `degraded` → leave it
   - If status is `failed` → reset to `pending` (will be retried)
   - If status is `in_progress` or `running` → reset to `pending` (was interrupted)
3. Determine which phase to resume from based on the highest completed phase
4. Compute READY agents: those with `status: pending` whose every dependency is `complete`

**Phase-to-agent mapping for the current pipeline:**

| Phase | Agents | Description |
|-------|--------|-------------|
| 0 | (none — metadata only) | Knowledge Bootstrap — always re-run |
| 1 | question-framing, data-explorer, hypothesis | Framing & Exploration |
| 2 | Notebook Analyst | Analysis (wraps descriptive, trend, cohort, RCA, validation, sizing) |
| 3 | story-architect, narrative-coherence-reviewer, chart-maker, visual-design-critic | Storytelling & Charts |
| 4 | storytelling, deck-creator, visual-design-critic (slides), close-the-loop, comms-drafter | Deck & Delivery |

**Execution plan awareness:** Check `state.plan` to know which phases apply.
For example, `deep_dive` stops after Phase 2; `quick_chart` only runs
chart-maker + visual-design-critic; `refresh_deck` only runs Phase 4.

### Step 4: Build context summary

Read each completed agent's output files and extract a brief summary:
- From question brief: the framed question and decision context
- From data feasibility: available/missing data points, dataset choice
- From hypothesis doc: top hypotheses being tested
- From analysis summary (`working/analysis_summary.md`): key findings, charts
  generated, confidence grade, recommendations, opportunity sizing. This is the
  primary context source for Phase 7+ agents — never read CSV files.
- From storyboard: narrative beats and visual plan
- From validation (if separate from notebook): confidence grade

> **Rule: No CSV reading.** When resuming into Phase 3 or 4, pass
> `working/analysis_summary.md` as `{{ANALYSIS_RESULTS}}` to all agents.
> The analysis_summary.md contains all quantitative findings, metrics, chart
> references, and recommendations. Downstream agents never read `.csv` files.

### Step 5: Present resume plan

Display:

```
Resuming pipeline: {run_id}
Dataset: {active_dataset} (project: {dataset_project})
Plan: {plan}

Phase 0 — Knowledge Bootstrap: ✅ Re-loaded
Phase 1 — Framing & Exploration: {status}
Phase 2 — Notebook Analysis: {status}
Phase 3 — Storytelling & Charts: {status}
Phase 4 — Deck & Delivery: {status}

Completed agents ({count}):
  - {agent_name}: {one-line summary from outputs}
  - ...

Failed/interrupted agents (will retry): {count}
  - {agent_name}: {error or "interrupted"}

Resuming from: Phase {N} — {phase_name}
Next agents: {list}
```

Use `#tool:vscode/askQuestions` to confirm with the user before proceeding.

### Step 6: Resume execution

On confirmation:
1. Update `pipeline_state.json`: set `status: running`, reset failed/running agents to `pending`
2. Hand off to the run-pipeline orchestrator, starting from the determined phase
3. The orchestrator picks up from the READY set and continues phase-by-phase,
   running checkpoints, invoking subagents, and verifying outputs as normal
4. All existing completed outputs are preserved — only pending agents execute

## Special Cases

- **Notebook partially executed:** If the notebook exists but cells haven't all
  run, the Notebook Analyst will re-run it. The notebook is the single analysis
  deliverable — there are no separate report files to check.
- **Storyboard with "NEEDS ADDITIONS":** Mark story-architect as `pending`, not completed
- **Partial chart generation:** Count generated charts vs storyboard beats. If incomplete, mark chart-maker as `pending`
- **Stale data (>24h gap):** Warn that underlying data may have changed since the original run
- **Plan mismatch:** If the user wants a different plan than the original run
  (e.g., started with `full_presentation` but now wants `deep_dive`), update
  the plan in pipeline state and skip agents not in the new plan

## Limitations

- **Context gap:** Resuming restores artifacts but not conversational reasoning. The resumed analysis may be slightly less coherent than a single-session run.
- **No partial step recovery:** If an agent was interrupted mid-execution, the entire agent must re-run.
- **Pipeline state is authoritative:** If `pipeline_state.json` and artifacts disagree, trust `pipeline_state.json`.
- **Phase 0 is always re-run:** This is intentional — it's metadata-only and ensures correct dataset context regardless of what changed between sessions.
