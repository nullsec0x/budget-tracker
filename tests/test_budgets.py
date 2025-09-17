import pytest
from budget_tracker.database import Settings, init_db
from budget_tracker.budgets import set_monthly_budget, get_budget_summary

@pytest.fixture
def test_session():
    """Create a test database session"""
    engine = init_db()
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.rollback()
    session.close()

def test_set_monthly_budget(test_session):
    """Test setting monthly budget"""
    settings = set_monthly_budget(test_session, 1000.0)
    assert settings.monthly_budget == 1000.0

def test_get_budget_summary(test_session):
    """Test getting budget summary"""
    set_monthly_budget(test_session, 1000.0)
    budget, spent, remaining = get_budget_summary(test_session)

    assert budget == 1000.0
    assert spent == 0.0
    assert remaining == 1000.0
