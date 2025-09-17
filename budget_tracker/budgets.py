from sqlalchemy.orm import Session
from datetime import date
from typing import Tuple
from rich.progress import Progress, BarColumn, TextColumn
from rich.console import Console
from .database import Settings, Transaction
from .utils import get_current_month_range, format_currency

console = Console()

def set_monthly_budget(session: Session, amount: float) -> Settings:
    settings = session.query(Settings).first()
    if not settings:
        settings = Settings(monthly_budget=amount)
        session.add(settings)
    else:
        settings.monthly_budget = amount

    session.commit()
    return settings

def set_savings_goal(session: Session, amount: float, name: str = "Savings Goal") -> Settings:
    settings = session.query(Settings).first()
    if not settings:
        settings = Settings(savings_goal_amount=amount, savings_goal_name=name)
        session.add(settings)
    else:
        settings.savings_goal_amount = amount
        settings.savings_goal_name = name

    session.commit()
    return settings

def get_budget_summary(session: Session, all_time: bool = False) -> Tuple[float, float, float]:
    settings = session.query(Settings).first()
    if not settings or settings.monthly_budget == 0:
        return 0.0, 0.0, 0.0

    if all_time:
        transactions = session.query(Transaction).filter(
            Transaction.type == 'expense'
        ).all()
    else:
        start_date, end_date = get_current_month_range()
        transactions = session.query(Transaction).filter(
            Transaction.date >= start_date,
            Transaction.date < end_date,
            Transaction.type == 'expense'
        ).all()

    total_spent = sum(t.amount for t in transactions)
    remaining = settings.monthly_budget - total_spent

    return settings.monthly_budget, total_spent, remaining

def show_budget_summary(session: Session, all_time: bool = False):
    budget, spent, remaining = get_budget_summary(session, all_time)
    settings = session.query(Settings).first()
    currency_symbol = settings.currency_symbol if settings else '$'

    time_period = "All Time" if all_time else "Current Month"
    console.print(f"\n[bold blue]📊 Budget Summary ({time_period})[/bold blue]")
    console.print(f"Monthly Budget: [green]{format_currency(budget, currency_symbol)}[/green]")
    console.print(f"Total Spent: [red]{format_currency(spent, currency_symbol)}[/red]")
    console.print(f"Remaining: [green]{format_currency(remaining, currency_symbol)}[/green]")

    if budget > 0:
        progress = (spent / budget) * 100
        console.print(f"\nProgress: {progress:.1f}% spent")

        if progress <= 100:
            with Progress(
                BarColumn(bar_width=40),
                TextColumn("{task.percentage:>3.0f}%"),
                transient=True,
            ) as progress_bar:
                task = progress_bar.add_task("Spending", total=100, completed=progress)
        else:
            console.print("[red]⚠️  Budget exceeded![/red]")

def get_savings_progress(session: Session) -> Tuple[float, float, float]:
    settings = session.query(Settings).first()
    if not settings or settings.savings_goal_amount == 0:
        return 0.0, 0.0, 0.0

    start_date, end_date = get_current_month_range()
    transactions = session.query(Transaction).filter(
        Transaction.date >= start_date,
        Transaction.date < end_date
    ).all()

    total_income = sum(t.amount for t in transactions if t.type == 'income')
    total_expenses = sum(t.amount for t in transactions if t.type == 'expense')
    monthly_surplus = total_income - total_expenses

    return settings.savings_goal_amount, monthly_surplus, (monthly_surplus / settings.savings_goal_amount * 100) if settings.savings_goal_amount > 0 else 0
