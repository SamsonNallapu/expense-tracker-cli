# 💰 Expense Tracker CLI

A clean, modern Command Line Expense Tracker built with Python.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Tests](https://img.shields.io/badge/Tests-pytest-brightgreen)

## ✨ Features

- Add expenses with category & description
- List & filter expenses (by recency and category)
- Monthly & all-time summary with per-category breakdown
- Delete expenses by ID
- Export to CSV
- Beautiful terminal UI (Rich tables)
- SQLite storage via SQLAlchemy ORM
- Tested with pytest

## 🛠️ Tech stack

- [Typer](https://typer.tiangolo.com/) — CLI framework
- [Rich](https://rich.readthedocs.io/) — terminal formatting
- [SQLAlchemy](https://www.sqlalchemy.org/) — ORM over SQLite
- [pytest](https://docs.pytest.org/) — test suite

## 🚀 Installation

```bash
# 1. Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux

# 2. Install
pip install -e .
```

## 📖 Usage

```bash
# Add expenses
expense add 15.50 --cat Food --desc "Lunch"
expense add 2.80 --cat Transport --desc "Bus fare"

# List recent expenses (last 30 days by default)
expense list
expense list --days 7
expense list --cat Food

# Monthly & all-time summary with category breakdown
expense summary

# Delete an expense by its ID (shown in the list table)
expense delete 3

# Export everything to CSV
expense export
expense export --out my_expenses.csv
```

Example output:

```
                       📋 Your Expenses
┏━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━┓
┃ ID ┃ Date       ┃ Category  ┃ Description     ┃ Amount ┃
┡━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━┩
│  2 │ 2026-06-10 │ Transport │ Bus fare        │  £2.80 │
│  1 │ 2026-06-10 │ Food      │ Lunch           │ £15.50 │
└────┴────────────┴───────────┴─────────────────┴────────┘
```

## 🧪 Running the tests

```bash
pip install pytest
python -m pytest expense_tracker/tests/ -v
```

The tests use a temporary database (via the `EXPENSE_TRACKER_DB`
environment variable), so they never touch your real expense data.

## 📁 Project structure

```
expense-tracker-cli/
├── expense_tracker/
│   ├── cli.py         # Typer commands (add, list, summary, delete, export)
│   ├── models.py      # SQLAlchemy Expense model
│   ├── database.py    # Engine, session, init
│   ├── utils.py       # Category validation, Rich table rendering
│   └── tests/
│       └── test_cli.py
├── pyproject.toml     # Package config + `expense` entry point
├── requirements.txt
└── LICENSE
```

## 📝 License

MIT — see [LICENSE](LICENSE).
