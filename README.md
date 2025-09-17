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
```

Run the application:

```bash
python -m budget_tracker.main
# or use the shorthand
budget
```
Alternativelly use the .exe file in the releases.
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
