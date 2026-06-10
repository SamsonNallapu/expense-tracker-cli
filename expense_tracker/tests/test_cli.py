"""Tests for the expense tracker.

Uses a temporary SQLite database (via the EXPENSE_TRACKER_DB environment
variable) so tests never touch real data.
"""
import os
import tempfile

# Point the app at a throwaway database BEFORE importing it
_tmpdir = tempfile.mkdtemp()
os.environ["EXPENSE_TRACKER_DB"] = f"sqlite:///{_tmpdir}/test_expenses.db"

from typer.testing import CliRunner  # noqa: E402

from expense_tracker.cli import app  # noqa: E402
from expense_tracker.utils import validate_category  # noqa: E402

runner = CliRunner()


# ---------- utils ----------

def test_validate_category_known():
    assert validate_category("food") == "Food"
    assert validate_category("RENT") == "Rent"


def test_validate_category_unknown_falls_back_to_other():
    assert validate_category("spaceships") == "Other"


# ---------- CLI commands ----------

def test_add_expense():
    result = runner.invoke(app, ["add", "12.50", "--cat", "food", "--desc", "Lunch"])
    assert result.exit_code == 0
    assert "12.50" in result.output
    assert "Food" in result.output


def test_list_shows_added_expense():
    runner.invoke(app, ["add", "3.20", "--cat", "transport", "--desc", "Bus fare"])
    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    assert "Bus fare" in result.output


def test_list_filters_by_category():
    result = runner.invoke(app, ["list", "--cat", "transport"])
    assert result.exit_code == 0
    assert "Bus fare" in result.output
    assert "Lunch" not in result.output


def test_summary_totals():
    result = runner.invoke(app, ["summary"])
    assert result.exit_code == 0
    assert "All-time total" in result.output


def test_delete_expense():
    runner.invoke(app, ["add", "5.00", "--cat", "other", "--desc", "To delete"])
    # The new expense has the highest ID; find it via export
    result = runner.invoke(app, ["delete", "3"])
    assert result.exit_code == 0
    assert "Deleted" in result.output


def test_delete_missing_id_fails_cleanly():
    result = runner.invoke(app, ["delete", "9999"])
    assert result.exit_code == 1


def test_export_creates_csv(tmp_path):
    out = tmp_path / "out.csv"
    result = runner.invoke(app, ["export", "--out", str(out)])
    assert result.exit_code == 0
    content = out.read_text(encoding="utf-8")
    assert content.startswith("id,date,category,description,amount")
    assert "Lunch" in content
