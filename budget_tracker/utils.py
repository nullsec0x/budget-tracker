from datetime import datetime, date
from typing import Optional
import re

def validate_amount(amount: str) -> float:
    try:
        amount_float = float(amount)
        if amount_float <= 0:
            raise ValueError("Amount must be positive")
        return amount_float
    except ValueError:
        raise ValueError("Amount must be a valid number")

def validate_date(date_str: Optional[str]) -> date:
    if not date_str:
        return date.today()

    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        pass

    try:
        return datetime.strptime(date_str, '%m/%d/%Y').date()
    except ValueError:
        pass

    try:
        return datetime.strptime(date_str, '%d/%m/%Y').date()
    except ValueError:
        raise ValueError("Date must be in YYYY-MM-DD, MM/DD/YYYY, or DD/MM/YYYY format")

def format_currency(amount: float, currency_symbol: str = '$') -> str:
    return f"{currency_symbol}{abs(amount):.2f}"

def get_current_month_range():
    today = date.today()
    start_date = date(today.year, today.month, 1)

    if today.month == 12:
        end_date = date(today.year + 1, 1, 1)
    else:
        end_date = date(today.year, today.month + 1, 1)

    return start_date, end_date
