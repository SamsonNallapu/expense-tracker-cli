from rich.console import Console
from rich.table import Table

console = Console()

CATEGORIES = ["Food", "Transport", "Rent", "Utilities", "Entertainment", "Shopping", "Health", "Other"]

def validate_category(category: str) -> str:
    cat = category.capitalize()
    return cat if cat in CATEGORIES else "Other"

def print_expenses(expenses):
    table = Table(title="📋 Your Expenses")
    table.add_column("ID", justify="right")
    table.add_column("Date")
    table.add_column("Category")
    table.add_column("Description")
    table.add_column("Amount", justify="right", style="green")

    for exp in expenses:
        table.add_row(
            str(exp.id),
            exp.date.strftime("%Y-%m-%d"),
            exp.category,
            exp.description or "-",
            f"£{exp.amount:.2f}"
        )
    console.print(table)