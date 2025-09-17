from sqlalchemy.orm import Session
from datetime import date, datetime
from typing import List, Dict
import csv
from rich.table import Table
from rich.console import Console
from rich import box
from .database import Transaction, Settings
from .utils import get_current_month_range, format_currency

console = Console()

def generate_monthly_report(session: Session):
    start_date, end_date = get_current_month_range()
    transactions = session.query(Transaction).filter(
        Transaction.date >= start_date,
        Transaction.date < end_date
    ).all()

    category_totals: Dict[str, float] = {}
    for transaction in transactions:
        if transaction.category not in category_totals:
            category_totals[transaction.category] = 0.0
        if transaction.type == 'expense':
            category_totals[transaction.category] += transaction.amount
        else:
            category_totals[transaction.category] -= transaction.amount

    settings = session.query(Settings).first()
    currency_symbol = settings.currency_symbol if settings else '$'

    table = Table(title=f"Monthly Report - {start_date.strftime('%B %Y')}")
    table.add_column("Category", style="cyan")
    table.add_column("Amount", style="green")
    table.add_column("Type", style="magenta")

    total_income = sum(t.amount for t in transactions if t.type == 'income')
    total_expenses = sum(t.amount for t in transactions if t.type == 'expense')

    for category, amount in sorted(category_totals.items(), key=lambda x: abs(x[1]), reverse=True):
        trans_type = "Expense" if amount > 0 else "Income"
        table.add_row(category, format_currency(amount, currency_symbol), trans_type)

    console.print(table)
    console.print(f"\nTotal Income: [green]{format_currency(total_income, currency_symbol)}[/green]")
    console.print(f"Total Expenses: [red]{format_currency(total_expenses, currency_symbol)}[/red]")
    console.print(f"Net: [blue]{format_currency(total_income - total_expenses, currency_symbol)}[/blue]")

def export_to_csv(session: Session, filename: str = "budget_export.csv"):
    transactions = session.query(Transaction).order_by(Transaction.date.desc()).all()

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['id', 'type', 'amount', 'category', 'description', 'date']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for transaction in transactions:
            writer.writerow({
                'id': transaction.id,
                'type': transaction.type,
                'amount': transaction.amount,
                'category': transaction.category,
                'description': transaction.description,
                'date': transaction.date.isoformat()
            })

    console.print(f"[green]✓ Exported {len(transactions)} transactions to {filename}[/green]")

def show_category_report(session: Session, category: str = None, type_filter: str = None, limit: int = 20):
    from .transactions import get_transactions

    transactions = get_transactions(session, category=category, type=type_filter, limit=limit)
    settings = session.query(Settings).first()
    currency_symbol = settings.currency_symbol if settings else '$'

    if not transactions:
        console.print("[yellow]No transactions found[/yellow]")
        return

    total_income = sum(t.amount for t in transactions if t.type == 'income')
    total_expenses = sum(t.amount for t in transactions if t.type == 'expense')

    table = Table(
        title=f"Transactions ({len(transactions)} found)" +
              (f" - Category: {category}" if category else "") +
              (f" - Type: {type_filter}" if type_filter else ""),
        box=box.ROUNDED
    )
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Date", style="yellow", no_wrap=True)
    table.add_column("Type", style="magenta", no_wrap=True)
    table.add_column("Category", style="blue", no_wrap=True)
    table.add_column("Amount", style="green", justify="right")
    table.add_column("Description", style="white")

    for transaction in transactions:
        amount_style = "red" if transaction.type == 'expense' else "green"
        amount_prefix = "-" if transaction.type == 'expense' else "+"
        amount_display = f"{amount_prefix}{format_currency(transaction.amount, currency_symbol)}"

        table.add_row(
            str(transaction.id),
            transaction.date.strftime('%Y-%m-%d'),
            transaction.type.capitalize(),
            transaction.category,
            f"[{amount_style}]{amount_display}[/{amount_style}]",
            transaction.description or "-"
        )

    console.print(table)

    if total_income > 0 or total_expenses > 0:
        console.print(f"\n[bold]Summary:[/bold]")
        console.print(f"Income: [green]+{format_currency(total_income, currency_symbol)}[/green]")
        console.print(f"Expenses: [red]-{format_currency(total_expenses, currency_symbol)}[/red]")
        console.print(f"Net: [blue]{format_currency(total_income - total_expenses, currency_symbol)}[/blue]")
