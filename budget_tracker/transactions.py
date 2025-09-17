from sqlalchemy.orm import Session
from datetime import date
from typing import List, Optional
from .database import Transaction
from .utils import validate_date, validate_amount

def add_transaction(
    session: Session,
    type: str,
    amount: float,
    category: str,
    description: str = "",
    transaction_date: Optional[str] = None
) -> Transaction:
    if type not in ['expense', 'income']:
        raise ValueError("Type must be 'expense' or 'income'")

    validated_amount = validate_amount(str(amount))
    validated_date = validate_date(transaction_date)

    transaction = Transaction(
        type=type,
        amount=validated_amount,
        category=category.strip(),
        description=description.strip(),
        date=validated_date
    )

    session.add(transaction)
    session.commit()
    return transaction

def get_transactions(
    session: Session,
    limit: int = 50,
    category: Optional[str] = None,
    type: Optional[str] = None
) -> List[Transaction]:
    query = session.query(Transaction)

    if category:
        query = query.filter(Transaction.category.ilike(f"%{category}%"))

    if type:
        query = query.filter(Transaction.type == type)

    return query.order_by(Transaction.date.desc()).limit(limit).all()

def delete_transaction(session: Session, transaction_id: int) -> bool:
    transaction = session.query(Transaction).filter(Transaction.id == transaction_id).first()
    if transaction:
        session.delete(transaction)
        session.commit()
        return True
    return False

def get_transactions_by_date_range(
    session: Session,
    start_date: date,
    end_date: date
) -> List[Transaction]:
    return session.query(Transaction).filter(
        Transaction.date >= start_date,
        Transaction.date < end_date
    ).order_by(Transaction.date.desc()).all()
