import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from datetime import datetime
from typing import Optional
import sys
from .database import get_session
from . import transactions, budgets, reports, settings
from .utils import validate_amount, validate_date

app = typer.Typer(help="Terminal-based budget tracker", add_completion=False)
console = Console()

def show_welcome():
    welcome_art = """
[bold cyan]
  ∧,,,∧
 (• ⩊ •)
|￣U U￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣|
|                                           |
|  Type [bold green]budget --help[/bold green] to get started        |
|  or [bold green]budget help[/bold green] for detailed commands     |
|                                           |
 ￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣
[/bold cyan]
"""
    console.print(welcome_art)

@app.callback(invoke_without_command=True)
def main_callback(ctx: typer.Context):
    """Budget Tracker - Manage your finances from terminal"""
    if ctx.invoked_subcommand is None:
        show_welcome()

@app.command()
def add(
    type: str = typer.Argument(..., help="Type: expense or income"),
    amount: str = typer.Argument(..., help="Transaction amount"),
    category: str = typer.Argument(..., help="Transaction category"),
    description: str = typer.Argument("", help="Transaction description"),
    date: Optional[str] = typer.Option(None, "--date", "-d", help="Date (YYYY-MM-DD, MM/DD/YYYY, or DD/MM/YYYY)")
):
    """Add a new transaction"""
    session = get_session()
    try:
        validated_amount = validate_amount(amount)
        transaction = transactions.add_transaction(
            session, type, validated_amount, category, description, date
        )
        currency_symbol = settings.get_currency_symbol(session)
        console.print(f"[green]✓ Added {type}: {currency_symbol}{validated_amount:.2f} to {category}[/green]")
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")
    finally:
        session.close()

@app.command(name="list")
def list_transactions(
    limit: int = typer.Option(20, "--limit", "-l", help="Number of transactions to show (default: 20)"),
    category: Optional[str] = typer.Option(None, "--category", "-c", help="Filter by category"),
    type: Optional[str] = typer.Option(None, "--type", "-t", help="Filter by type: expense or income")
):
    """List recent transactions with optional filtering"""
    session = get_session()
    try:
        reports.show_category_report(session, category, type, limit)
    finally:
        session.close()

@app.command()
def delete(transaction_id: int = typer.Argument(..., help="ID of transaction to delete")):
    """Delete a transaction by ID"""
    session = get_session()
    try:
        if transactions.delete_transaction(session, transaction_id):
            console.print(f"[green]✓ Deleted transaction #{transaction_id}[/green]")
        else:
            console.print(f"[red]Transaction #{transaction_id} not found[/red]")
    finally:
        session.close()

@app.command()
def summary(
    all_time: bool = typer.Option(False, "--all-time", "-a", help="Show all-time summary instead of current month")
):
    """Show budget summary with spending progress"""
    session = get_session()
    try:
        budgets.show_budget_summary(session, all_time)
    finally:
        session.close()

@app.command()
def set_budget(amount: float = typer.Argument(..., help="Monthly budget amount")):
    """Set monthly budget amount"""
    session = get_session()
    try:
        budgets.set_monthly_budget(session, amount)
        currency_symbol = settings.get_currency_symbol(session)
        console.print(f"[green]✓ Monthly budget set to {currency_symbol}{amount:.2f}[/green]")
    finally:
        session.close()

@app.command()
def set_goal(
    amount: float = typer.Argument(..., help="Savings goal amount"),
    name: str = typer.Option("Savings Goal", "--name", "-n", help="Savings goal name")
):
    """Set savings goal with optional name"""
    session = get_session()
    try:
        budgets.set_savings_goal(session, amount, name)
        currency_symbol = settings.get_currency_symbol(session)
        console.print(f"[green]✓ Savings goal '{name}' set to {currency_symbol}{amount:.2f}[/green]")
    finally:
        session.close()

@app.command()
def report(
    report_type: str = typer.Argument("monthly", help="Report type: monthly or categories")
):
    """Generate financial reports"""
    session = get_session()
    try:
        if report_type == "monthly":
            reports.generate_monthly_report(session)
        elif report_type == "categories":
            reports.show_category_report(session)
        else:
            console.print("[red]Invalid report type. Use 'monthly' or 'categories'[/red]")
    finally:
        session.close()

@app.command()
def export(
    filename: str = typer.Option("budget_export.csv", "--filename", "-f", help="Export filename")
):
    """Export transactions to CSV file"""
    session = get_session()
    try:
        reports.export_to_csv(session, filename)
    finally:
        session.close()

@app.command()
def set_currency(
    symbol: str = typer.Argument(..., help="Currency symbol ($, €, £, ¥, MAD, etc.)")
):
    """Set default currency symbol"""
    session = get_session()
    try:
        settings.set_currency_symbol(session, symbol)
        console.print(f"[green]✓ Currency symbol set to '{symbol}'[/green]")
    finally:
        session.close()

@app.command()
def version():
    """Show version information"""
    from . import __version__
    console.print(f"Budget Tracker v{__version__}")

@app.command()
def help():
    """Show comprehensive guide with examples"""
    console.print(Panel.fit(
        "[bold green]💰 Budget Tracker - Complete Command Guide[/bold green]\n\n"
        
        "[bold]📝 ADD TRANSACTIONS:[/bold]\n"
        "  budget add [type] [amount] [category] [description] [--date]\n"
        "  budget add expense 25.00 Food \"Lunch\"\n"
        "  budget add income 1200.00 Salary \"Monthly\" --date 2024-01-15\n"
        "  budget add expense 15.50 Coffee --date 01/15/2024\n\n"
        
        "[bold]👀 VIEW TRANSACTIONS:[/bold]\n"
        "  budget list [--limit N] [--category NAME] [--type TYPE]\n"
        "  budget list --limit 50\n"
        "  budget list --category Food --type expense\n"
        "  budget list -c Food -t expense -l 30\n\n"
        
        "[bold]🗑️  DELETE TRANSACTIONS:[/bold]\n"
        "  budget delete [ID]\n"
        "  budget delete 5\n\n"
        
        "[bold]📊 BUDGET MANAGEMENT:[/bold]\n"
        "  budget set-budget [amount]\n"
        "  budget set-budget 2000\n"
        "  budget summary [--all-time]\n"
        "  budget summary -a\n\n"
        
        "[bold]🎯 SAVINGS GOALS:[/bold]\n"
        "  budget set-goal [amount] [--name NAME]\n"
        "  budget set-goal 5000 --name \"New Laptop\"\n\n"
        
        "[bold]⚙️  CONFIGURATION:[/bold]\n"
        "  budget set-currency [symbol]\n"
        "  budget set-currency \"€\"\n"
        "  budget set-currency \"MAD\"\n\n"
        
        "[bold]📈 REPORTS & EXPORT:[/bold]\n"
        "  budget report monthly\n"
        "  budget report categories\n"
        "  budget export [--filename NAME]\n"
        "  budget export -f my_data.csv\n\n"
        
        "[bold]ℹ️  INFORMATION:[/bold]\n"
        "  budget version\n"
        "  budget help\n\n"
        
        "[bold]🎨 DATE FORMATS:[/bold] YYYY-MM-DD, MM/DD/YYYY, DD/MM/YYYY\n"
        "[bold]💡 TIP:[/bold] Use consistent category names for better reports!",
        title="📖 Complete Command Reference",
        border_style="blue",
        box=box.ROUNDED
    ))

def main():
    """Main entry point"""
    if len(sys.argv) == 1:
        show_welcome()
    else:
        app(prog_name="budget")

if __name__ == "__main__":
    main()
