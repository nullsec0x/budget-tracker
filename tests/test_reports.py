import pytest
import os
from budget_tracker.database import init_db
from budget_tracker.reports import export_to_csv

@pytest.fixture
def test_session():
    """Create a test database session"""
    engine = init_db()
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.rollback()
    session.close()

def test_export_to_csv(test_session, tmp_path):
    """Test exporting to CSV"""
    test_file = tmp_path / "test_export.csv"
    export_to_csv(test_session, str(test_file))

    assert test_file.exists()
    assert test_file.stat().st_size > 0

    # Clean up
    if test_file.exists():
        os.remove(test_file)
