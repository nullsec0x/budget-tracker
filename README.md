# Budget Tracker

A terminal-based personal finance manager written in Python.
Track your income and expenses, set budgets, monitor savings goals, and generate financial reports — all from the command line.

Created by **Nullsec0x**.

---

## Features

- Add income and expense transactions
- Set monthly budgets and savings goals
- Generate monthly and category-based reports
- Export data to CSV format
- Filter transactions by category and type
- Clean terminal interface with [Rich](https://github.com/Textualize/rich) formatting
- Support for multiple currency symbols
- Track progress for budgets and savings goals

---

## Installation

Clone the repository:

```bash
git clone https://github.com/nullsec0x/budget-tracker.git
cd budget-tracker
```

Install dependencies:

```bash
pip install -r requirements.txt
pip install -e .
pip install "click<8.1.0" "typer==0.4.1"
pip install --upgrade typer click
```

Run the application:

```bash
python -m budget_tracker.main
# or use the shorthand
budget
```

Alternatively, use the `.exe` file from the releases.

---

## Windows Usage

1. Download the `budget.exe` file from the latest release
2. Open Command Prompt or PowerShell
3. Navigate to where you downloaded the file
4. Run the application with commands like:

```bash
budget.exe --help
budget.exe add expense 25.00 Food "Lunch"
budget.exe list
budget.exe summary
```

### Quick Start (Double-Click Method)

If you double-click the executable, it will open a command window showing the welcome message.  
To use the application effectively, run it from an already open command prompt.

---

## Usage

The application provides a full CLI interface. Use `budget --help` or `budget help` for the complete command reference.

### Examples

```bash
# Add transactions
budget add expense 25.00 Food "Lunch at cafe"
budget add income 1200.00 Salary "Monthly salary"

# View transactions
budget list --limit 10
budget list --category Food --type expense

# Manage budgets
budget set-budget 2000
budget summary

# Set savings goal
budget set-goal 5000 --name "New Laptop"

# Reports
budget report monthly
budget report categories

# Export data
budget export --filename my_finances.csv
```

---

## Tech Stack

- Python 3.10+
- [Typer](https://typer.tiangolo.com/) – CLI framework
- [Rich](https://github.com/Textualize/rich) – terminal formatting
- [SQLAlchemy](https://www.sqlalchemy.org/) – database backend

---

## Author

Developed and maintained by **Nullsec0x**.
