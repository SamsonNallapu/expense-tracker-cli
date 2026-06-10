import csv
from datetime import datetime, timedelta

import typer
from rich import print as rprint

from .database import init_db, get_db
from .models import Expense
from .utils import print_expenses, validate_category

app = typer.Typer(help="💰 Expense Tracker CLI")


@app.callback()
def callback():
    init_db()


@app.command()
def add(
    amount: float = typer.Argument(...),
    category: str = typer.Option(..., "--cat"),
    description: str = typer.Option("", "--desc"),
):
    """Add new expense"""
    db = next(get_db())
    category = validate_category(category)

    expense = Expense(amount=amount, category=category, description=description)
    db.add(expense)
    db.commit()
    rprint(f"✅ Added £{amount:.2f} → {category}")


@app.command()
def list(
    days: int = typer.Option(30, "--days", help="Only show expenses from the last N days"),
    category: str = typer.Option(None, "--cat", help="Filter by category"),
):
    """List expenses (filter by days and/or category)"""
    db = next(get_db())
    cutoff = datetime.now() - timedelta(days=days)
    query = db.query(Expense).filter(Expense.date >= cutoff)
    if category:
        query = query.filter(Expense.category == validate_category(category))
    expenses = query.order_by(Expense.date.desc()).all()
    if not expenses:
        rprint("[yellow]No expenses found for these filters.[/]")
        return
    print_expenses(expenses)


@app.command()
def summary():
    """Show monthly and all-time summary"""
    db = next(get_db())
    expenses = db.query(Expense).all()
    if not expenses:
        rprint("[yellow]No expenses recorded yet.[/]")
        return

    now = datetime.now()
    this_month = [
        e for e in expenses if e.date.year == now.year and e.date.month == now.month
    ]

    rprint(f"\n📅 This month ({now.strftime('%B %Y')}): "
           f"[green bold]£{sum(e.amount for e in this_month):.2f}[/] "
           f"({len(this_month)} expenses)")
    rprint(f"💰 All-time total: [green bold]£{sum(e.amount for e in expenses):.2f}[/] "
           f"({len(expenses)} expenses)")

    # Per-category breakdown (all-time)
    by_category: dict[str, float] = {}
    for e in expenses:
        by_category[e.category] = by_category.get(e.category, 0) + e.amount
    rprint("\n[bold]By category:[/]")
    for cat, total in sorted(by_category.items(), key=lambda kv: kv[1], reverse=True):
        rprint(f"  {cat:<15} £{total:.2f}")


@app.command()
def delete(expense_id: int = typer.Argument(..., help="ID of the expense to delete")):
    """Delete an expense by its ID"""
    db = next(get_db())
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if expense is None:
        rprint(f"[red]❌ No expense found with ID {expense_id}[/]")
        raise typer.Exit(code=1)
    db.delete(expense)
    db.commit()
    rprint(f"🗑️  Deleted expense {expense_id} (£{expense.amount:.2f}, {expense.category})")


@app.command()
def export(
    out: str = typer.Option("expenses_export.csv", "--out", help="Output CSV path"),
):
    """Export all expenses to CSV"""
    db = next(get_db())
    expenses = db.query(Expense).order_by(Expense.date).all()
    with open(out, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "date", "category", "description", "amount"])
        for e in expenses:
            writer.writerow(
                [e.id, e.date.strftime("%Y-%m-%d"), e.category, e.description, f"{e.amount:.2f}"]
            )
    rprint(f"📤 Exported {len(expenses)} expenses to [bold]{out}[/]")
