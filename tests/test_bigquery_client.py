"""Tests for helpers/bigquery_client.py.

All tests mock the google.cloud.bigquery client — no real GCP calls are made.
"""

import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch, PropertyMock

import pandas as pd
import pytest


# ---------------------------------------------------------------------------
# Skip entire module if google-cloud-bigquery is not installed
# ---------------------------------------------------------------------------

bq_lib = pytest.importorskip("google.cloud.bigquery", reason="google-cloud-bigquery not installed")


from helpers.bigquery_client import BigQueryClient, GB_WARNING_LIMIT, GB_ERROR_LIMIT, GB_CANCEL_LIMIT


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def mock_bq_client():
    """Patch bigquery.Client so no real connection is created."""
    with patch("helpers.bigquery_client.bigquery.Client") as MockClient:
        instance = MockClient.return_value
        instance.project = "test-project"
        yield instance


@pytest.fixture()
def bq(mock_bq_client):
    """A BigQueryClient backed by a mocked google client."""
    return BigQueryClient(project="test-project")


@pytest.fixture()
def sql_dir(tmp_path):
    """A temp directory with a sample .sql file."""
    sql_file = tmp_path / "test_query.sql"
    sql_file.write_text("SELECT 1 AS col")
    return tmp_path


# ---------------------------------------------------------------------------
# Construction / project resolution
# ---------------------------------------------------------------------------


class TestInit:
    def test_explicit_project(self, mock_bq_client):
        bq = BigQueryClient(project="my-project")
        assert bq.project == "test-project"  # comes from mock

    def test_env_var_google_cloud_project(self, mock_bq_client, monkeypatch):
        monkeypatch.setenv("GOOGLE_CLOUD_PROJECT", "env-project")
        monkeypatch.delenv("GCP_PROJECT", raising=False)
        bq = BigQueryClient()
        # The mock always returns "test-project", but we verify the
        # constructor passed the env value to Client()
        from helpers.bigquery_client import bigquery
        bigquery.Client.assert_called_with(project="env-project")

    def test_env_var_gcp_project_fallback(self, mock_bq_client, monkeypatch):
        monkeypatch.delenv("GOOGLE_CLOUD_PROJECT", raising=False)
        monkeypatch.setenv("GCP_PROJECT", "fallback-project")
        bq = BigQueryClient()
        from helpers.bigquery_client import bigquery
        bigquery.Client.assert_called_with(project="fallback-project")

    def test_default_project(self, mock_bq_client, monkeypatch):
        monkeypatch.delenv("GOOGLE_CLOUD_PROJECT", raising=False)
        monkeypatch.delenv("GCP_PROJECT", raising=False)
        bq = BigQueryClient()
        from helpers.bigquery_client import bigquery
        bigquery.Client.assert_called_with(project="coolblue-webandapp-dev")

    def test_repr(self, bq):
        r = repr(bq)
        assert "BigQueryClient" in r
        assert "test-project" in r


# ---------------------------------------------------------------------------
# SQL loading
# ---------------------------------------------------------------------------


class TestLoadSql:
    def test_load_absolute_path(self, bq, tmp_path):
        sql_file = tmp_path / "my_query.sql"
        sql_file.write_text("SELECT 42")
        result = bq.load_sql(str(sql_file))
        assert result == "SELECT 42"

    def test_load_relative_to_sql_dir(self, bq, sql_dir):
        bq.sql_dir = str(sql_dir)
        result = bq.load_sql("test_query.sql")
        assert result == "SELECT 1 AS col"

    def test_file_not_found_raises(self, bq):
        with pytest.raises(FileNotFoundError, match="SQL file not found"):
            bq.load_sql("nonexistent.sql")


# ---------------------------------------------------------------------------
# Cost estimation
# ---------------------------------------------------------------------------


class TestEstimateCost:
    def test_ok_status(self, bq, mock_bq_client):
        mock_job = MagicMock()
        mock_job.total_bytes_processed = 1_000_000_000  # 1 GB
        mock_bq_client.query.return_value = mock_job

        result = bq.estimate_cost("SELECT 1")
        assert result["gb_processed"] == 1.0
        assert result["status"] == "ok"

    def test_warning_status(self, bq, mock_bq_client):
        mock_job = MagicMock()
        mock_job.total_bytes_processed = int((GB_WARNING_LIMIT + 1) * 1e9)
        mock_bq_client.query.return_value = mock_job

        result = bq.estimate_cost("SELECT 1")
        assert result["status"] == "warning"

    def test_error_status(self, bq, mock_bq_client):
        mock_job = MagicMock()
        mock_job.total_bytes_processed = int((GB_ERROR_LIMIT + 1) * 1e9)
        mock_bq_client.query.return_value = mock_job

        result = bq.estimate_cost("SELECT 1")
        assert result["status"] == "error"

    def test_cancel_raises(self, bq, mock_bq_client):
        mock_job = MagicMock()
        mock_job.total_bytes_processed = int((GB_CANCEL_LIMIT + 1) * 1e9)
        mock_bq_client.query.return_value = mock_job

        with pytest.raises(RuntimeError, match="cancel limit"):
            bq.estimate_cost("SELECT 1")

    def test_bad_request_propagated(self, bq, mock_bq_client):
        from google.api_core.exceptions import BadRequest

        mock_bq_client.query.side_effect = BadRequest("invalid SQL")

        with pytest.raises(BadRequest):
            bq.estimate_cost("INVALID SQL")

    def test_zero_bytes(self, bq, mock_bq_client):
        mock_job = MagicMock()
        mock_job.total_bytes_processed = 0
        mock_bq_client.query.return_value = mock_job

        result = bq.estimate_cost("SELECT 1")
        assert result["gb_processed"] == 0.0
        assert result["status"] == "ok"


# ---------------------------------------------------------------------------
# Query execution
# ---------------------------------------------------------------------------


class TestQuery:
    def test_query_returns_dataframe(self, bq, mock_bq_client):
        expected_df = pd.DataFrame({"col": [1]})

        # Cost check: dry run
        mock_dry_job = MagicMock()
        mock_dry_job.total_bytes_processed = 1_000_000  # 0.001 GB
        # Actual query
        mock_query_job = MagicMock()
        mock_query_job.to_dataframe.return_value = expected_df

        mock_bq_client.query.side_effect = [mock_dry_job, mock_query_job]

        result = bq.query("SELECT 1 AS col")
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 1

    def test_query_skip_cost_check(self, bq, mock_bq_client):
        expected_df = pd.DataFrame({"col": [1]})
        mock_query_job = MagicMock()
        mock_query_job.to_dataframe.return_value = expected_df
        mock_bq_client.query.return_value = mock_query_job

        result = bq.query("SELECT 1", check_cost=False)
        assert len(result) == 1
        # Only one call — no dry run
        assert mock_bq_client.query.call_count == 1


class TestRunQuery:
    def test_run_query_from_file(self, bq, mock_bq_client, sql_dir):
        bq.sql_dir = str(sql_dir)

        expected_df = pd.DataFrame({"col": [1]})
        mock_dry_job = MagicMock()
        mock_dry_job.total_bytes_processed = 500_000
        mock_query_job = MagicMock()
        mock_query_job.to_dataframe.return_value = expected_df

        mock_bq_client.query.side_effect = [mock_dry_job, mock_query_job]

        result = bq.run_query("test_query.sql", label="test")
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 1

    def test_run_query_file_not_found(self, bq):
        with pytest.raises(FileNotFoundError):
            bq.run_query("does_not_exist.sql", label="missing")

    def test_run_query_skip_cost(self, bq, mock_bq_client, sql_dir):
        bq.sql_dir = str(sql_dir)

        expected_df = pd.DataFrame({"col": [1]})
        mock_query_job = MagicMock()
        mock_query_job.to_dataframe.return_value = expected_df
        mock_bq_client.query.return_value = mock_query_job

        result = bq.run_query("test_query.sql", label="test", check_cost=False)
        assert len(result) == 1
