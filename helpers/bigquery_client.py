"""
BigQuery Client — unified interface for BigQuery data access.

Manages BigQuery client lifecycle, SQL loading, query cost estimation,
and query execution. Designed for notebook and script workflows that
query BigQuery directly.

Usage:
    from helpers.bigquery_client import BigQueryClient

    bq = BigQueryClient()
    print(bq.project)

    # Run a query from a SQL file
    df = bq.run_query("working/sql/q1_sessions.sql", label="Session snapshot")

    # Run raw SQL
    df = bq.query("SELECT 1 AS test")

    # Check cost before running
    cost = bq.estimate_cost("SELECT * FROM `my_project.my_dataset.big_table`")
    print(cost)

    # Load SQL from file
    sql = bq.load_sql("working/sql/q1_sessions.sql")
"""

import logging
import os
from pathlib import Path

import pandas as pd

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed — environment must be set externally

try:
    from google.cloud import bigquery
    from google.api_core.exceptions import BadRequest

    _BQ_AVAILABLE = True
except ImportError:
    _BQ_AVAILABLE = False


logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Cost thresholds (GB processed)
# ---------------------------------------------------------------------------

GB_WARNING_LIMIT = 10
GB_ERROR_LIMIT = 50
GB_CANCEL_LIMIT = 100

# Default SQL directory (relative to caller's working directory)
_DEFAULT_SQL_DIR = "working/sql"


class BigQueryClient:
    """Convenience wrapper around ``google.cloud.bigquery.Client``.

    Handles project resolution from environment variables, SQL file loading,
    automatic cost estimation before query execution, and friendly logging.

    Args:
        project: GCP project ID. If ``None``, reads from the
            ``GOOGLE_CLOUD_PROJECT`` or ``GCP_PROJECT`` env vars,
            falling back to ``"coolblue-webandapp-dev"``.
        sql_dir: Root directory for ``.sql`` files used by
            :meth:`load_sql` and :meth:`run_query`. Defaults to
            ``working/sql``.
        warning_gb: Print a warning when estimated scan exceeds this (GB).
        error_gb: Log an error when estimated scan exceeds this (GB).
        cancel_gb: Raise an exception when estimated scan exceeds this (GB).
    """

    def __init__(
        self,
        project: str | None = None,
        sql_dir: str = _DEFAULT_SQL_DIR,
        warning_gb: float = GB_WARNING_LIMIT,
        error_gb: float = GB_ERROR_LIMIT,
        cancel_gb: float = GB_CANCEL_LIMIT,
    ):
        if not _BQ_AVAILABLE:
            raise ImportError(
                "google-cloud-bigquery is required. "
                "Install it with: pip install google-cloud-bigquery"
            )

        self._project = project or os.getenv(
            "GOOGLE_CLOUD_PROJECT",
            os.getenv("GCP_PROJECT", "coolblue-webandapp-dev"),
        )
        self._client = bigquery.Client(project=self._project)
        self.sql_dir = sql_dir
        self.warning_gb = warning_gb
        self.error_gb = error_gb
        self.cancel_gb = cancel_gb

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def project(self) -> str:
        """The active GCP project ID."""
        return self._client.project

    @property
    def client(self) -> "bigquery.Client":
        """The underlying ``google.cloud.bigquery.Client``."""
        return self._client

    # ------------------------------------------------------------------
    # SQL loading
    # ------------------------------------------------------------------

    def load_sql(self, path: str) -> str:
        """Read a ``.sql`` file and return its contents.

        If *path* is not absolute and does not exist relative to the current
        directory, it is resolved relative to :attr:`sql_dir`.
        """
        p = Path(path)
        if not p.is_absolute() and not p.exists():
            p = Path(self.sql_dir) / p
        if not p.exists():
            raise FileNotFoundError(f"SQL file not found: {p}")
        return p.read_text(encoding="utf-8")

    # ------------------------------------------------------------------
    # Cost estimation
    # ------------------------------------------------------------------

    def estimate_cost(self, query: str) -> dict:
        """Dry-run *query* and return estimated bytes / GB to be scanned.

        Returns:
            dict with keys ``bytes_processed``, ``gb_processed``, and
            ``status`` (one of ``"ok"``, ``"warning"``, ``"error"``,
            ``"cancel"``).

        Raises:
            BadRequest: If the query itself is invalid.
            RuntimeError: If the estimated scan exceeds :attr:`cancel_gb`.
        """
        job_config = bigquery.QueryJobConfig(dry_run=True, use_query_cache=False)
        try:
            job = self._client.query(query, job_config=job_config)
        except BadRequest as exc:
            logger.error("Query failed validation: %s", exc)
            raise

        bytes_processed = job.total_bytes_processed or 0
        gb_processed = bytes_processed / 1e9

        status = "ok"
        if gb_processed > self.cancel_gb:
            status = "cancel"
            msg = (
                f"Query will scan {gb_processed:.1f} GB — "
                f"exceeds cancel limit ({self.cancel_gb} GB). Aborting."
            )
            logger.error(msg)
            raise RuntimeError(msg)
        elif gb_processed > self.error_gb:
            status = "error"
            logger.error(
                "Query will scan %.1f GB (error threshold: %s GB).",
                gb_processed,
                self.error_gb,
            )
        elif gb_processed > self.warning_gb:
            status = "warning"
            logger.warning(
                "Query will scan %.1f GB (warning threshold: %s GB).",
                gb_processed,
                self.warning_gb,
            )

        return {
            "bytes_processed": bytes_processed,
            "gb_processed": round(gb_processed, 3),
            "status": status,
        }

    # ------------------------------------------------------------------
    # Query execution
    # ------------------------------------------------------------------

    def query(self, sql: str, *, check_cost: bool = True) -> pd.DataFrame:
        """Execute raw *sql* and return a DataFrame.

        Args:
            sql: The SQL string to execute.
            check_cost: If ``True`` (default), run :meth:`estimate_cost`
                first; abort if the cancel threshold is exceeded.
        """
        if check_cost:
            cost = self.estimate_cost(sql)
            print(
                f"  Cost estimate: {cost['gb_processed']:.2f} GB "
                f"({cost['status']})"
            )

        df = self._client.query(sql).to_dataframe()
        return df

    def run_query(
        self,
        sql_path: str,
        label: str = "",
        *,
        check_cost: bool = True,
    ) -> pd.DataFrame:
        """Load a SQL file, estimate cost, execute, and return a DataFrame.

        Args:
            sql_path: Path to a ``.sql`` file (absolute, relative, or
                relative to :attr:`sql_dir`).
            label: Human-readable label for console output.
            check_cost: If ``True`` (default), run a dry-run cost check
                before executing.
        """
        sql = self.load_sql(sql_path)
        display_label = label or sql_path
        print(f"Running: {display_label}...")

        if check_cost:
            cost = self.estimate_cost(sql)
            print(
                f"  Cost estimate: {cost['gb_processed']:.2f} GB "
                f"({cost['status']})"
            )

        df = self._client.query(sql).to_dataframe()
        print(f"  OK: {len(df):,} rows, {df.shape[1]} columns")
        return df

    # ------------------------------------------------------------------
    # Convenience
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return f"BigQueryClient(project={self.project!r}, sql_dir={self.sql_dir!r})"
