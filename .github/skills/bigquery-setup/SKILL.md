---
name: bigquery-setup
description: "Sets up the BigQuery client for notebooks and scripts using helpers/bigquery_client.py. Use when creating a new notebook that queries BigQuery, setting up a BigQuery connection, or when the user asks to run queries against BigQuery."
user-invocable: false
disable-model-invocation: false
---

# BigQuery Setup

## When to Use

Apply this skill when:
- Creating a new Jupyter notebook that queries BigQuery
- The user asks to "set up BigQuery", "connect to BigQuery", or "run a query"
- A notebook or script needs to execute SQL against BigQuery
- The data source is a BigQuery dataset (PFA, GA4, transaction_margin, etc.)

## Prerequisites

Before writing any BigQuery code, verify these prerequisites in order:

### 1. Environment Variable

The GCP project used for authentication and billing is **always
`coolblue-marketing-dev`**. This is NOT the same as the BigQuery dataset
project (e.g., `cb-data-hub-prod`) where the data lives — that project is
referenced only in fully-qualified table names inside SQL queries.

`BigQueryClient` reads `GOOGLE_CLOUD_PROJECT` from the environment. The
variable is already set in the user's shell profile or `.env` file.

**Do NOT create, modify, or overwrite the `.env` file.** The `.env` file is
managed by the user. If `GOOGLE_CLOUD_PROJECT` is not set, instruct the user
to run:
```bash
export GOOGLE_CLOUD_PROJECT="coolblue-marketing-dev"
```

Never set `GOOGLE_CLOUD_PROJECT` to a dataset project like `cb-data-hub-prod`.

### 2. Dependencies

The following packages must be installed:
- `google-cloud-bigquery`
- `db-dtypes` (for BigQuery-specific dtypes in pandas)
- `python-dotenv` (optional but recommended — auto-loads `.env`)

Check `requirements.txt` — these should already be listed.

### 3. Authentication

The user must have valid GCP credentials. This is typically handled by:
- `gcloud auth application-default login` (local development)
- A service account key via `GOOGLE_APPLICATION_CREDENTIALS` env var
- Workload identity (CI/CD)

If the client raises an authentication error, suggest:
```bash
gcloud auth application-default login
```

## Setup Pattern

### Standard Notebook Setup

When setting up BigQuery in a notebook, use exactly this pattern:

```python
from helpers.bigquery_client import BigQueryClient

bq = BigQueryClient()
print(f"Project: {bq.project}")
```

**Do NOT:**
- Import `google.cloud.bigquery` directly in notebooks
- Hardcode project IDs — let `BigQueryClient` resolve from env vars
- Create `bigquery.Client()` manually — always use the wrapper

### With Custom SQL Directory

If SQL files live somewhere other than `working/sql/`:

```python
bq = BigQueryClient(sql_dir="path/to/sql")
```

### With Custom Cost Thresholds

For exploratory work with potentially large scans:

```python
bq = BigQueryClient(warning_gb=20, error_gb=100, cancel_gb=200)
```

## Running Queries

### From a SQL File

The primary pattern — keeps SQL out of notebook cells:

```python
df = bq.run_query("q1_session_snapshot.sql", label="Q1: Session Metrics")
```

- `run_query()` resolves the file relative to `bq.sql_dir` (default: `working/sql/`)
- Automatically runs a dry-run cost estimate before executing
- Prints row count and column count on success

### Raw SQL

For quick one-off queries or validation checks:

```python
df = bq.query("SELECT COUNT(*) AS n FROM `project.dataset.table`")
```

### Skip Cost Check

When re-running a known-safe query or in tight iteration loops:

```python
df = bq.run_query("q1.sql", label="Q1", check_cost=False)
df = bq.query("SELECT 1", check_cost=False)
```

### Cost Estimation Only

To check scan size without executing:

```python
cost = bq.estimate_cost("SELECT * FROM `project.dataset.big_table`")
print(f"{cost['gb_processed']} GB — status: {cost['status']}")
```

**Cost thresholds (defaults):**

| Threshold | GB | Behavior |
|-----------|----|----------|
| Warning   | 10 | Logs a warning, continues |
| Error     | 50 | Logs an error, continues |
| Cancel    | 100 | Raises `RuntimeError`, query does NOT execute |

### Loading SQL Without Executing

To inspect or manipulate SQL before running:

```python
sql = bq.load_sql("q1_session_snapshot.sql")
print(sql)
```

## SQL File Organization

Place `.sql` files in `working/sql/` (or the notebook's local `sql/` directory). Name them descriptively:

```
working/sql/
  q1_session_snapshot.sql
  q2_sales_snapshot.sql
  q3_weekly_sessions.sql
```

The `load_sql()` and `run_query()` methods resolve paths in this order:
1. Absolute path (if provided)
2. Relative to current working directory
3. Relative to `bq.sql_dir`

## Accessing the Raw Client

If you need the underlying `google.cloud.bigquery.Client` for advanced operations:

```python
raw_client = bq.client
```

## Notebook Template

When creating a new BigQuery analysis notebook, use this cell structure:

**Cell 1 — Imports:**
```python
import pandas as pd
from helpers.bigquery_client import BigQueryClient
```

**Cell 2 — Client Setup:**
```python
bq = BigQueryClient()
print(f"Project: {bq.project}")
```

**Cell 3+ — Queries:**
```python
df = bq.run_query("q1_snapshot.sql", label="Q1: Snapshot")
df.head()
```

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `ImportError: google-cloud-bigquery` | Package not installed | `pip install google-cloud-bigquery` |
| `DefaultCredentialsError` | No GCP auth | `gcloud auth application-default login` |
| `BadRequest` | Invalid SQL | Check query syntax; error is logged with details |
| `RuntimeError: exceeds cancel limit` | Query scans > 100 GB | Optimize query (add filters, limit partitions) or raise `cancel_gb` threshold |
| `FileNotFoundError: SQL file not found` | Wrong path or missing file | Check `bq.sql_dir` and file name |
