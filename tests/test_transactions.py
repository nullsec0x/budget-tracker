import pytest
from datetime import date
from sqlalchemy.orm import Session
from budget_tracker.database import Transaction, init_db
from budget_tracker.transactions import add_transaction, get_transactions, delete_transaction

@pytest.fixture
def test_session():
    """Create a test database session"""
    engine = init_db()
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.rollback()
    session.close()

def test_add_transaction(test_session: Session):
    """Test adding a transaction"""
    transaction = add_transaction(
        test_session, 'expense', 25.50, 'Food', 'Lunch'
    )

    assert transaction.type == 'expense'
    assert transaction.amount == 25.50
    assert transaction.category == 'Food'
    assert transaction.description == 'Lunch'
    assert transaction.date == date.today()

def test_get_transactions(test_session: Session):
    """Test retrieving transactions"""
    add_transaction(test_session, 'expense', 25.50, 'Food', 'Lunch')
    add_transaction(test_session, 'income', 100.00, 'Salary', 'Monthly salary')

    transactions = get_transactions(test_session)
    assert len(transactions) == 2
    assert transactions[0].type == 'income'
    assert transactions[1].type == 'expense'

def test_delete_transaction(test_session: Session):
    """Test deleting a transaction"""
    transaction = add_transaction(test_session, 'expense', 25.50, 'Food', 'Lunch')

    result = delete_transaction(test_session, transaction.id)
    assert result == True

    transactions = get_transactions(test_session)
    assert len(transactions) == 0
