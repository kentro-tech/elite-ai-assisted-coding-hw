"""Pytest configuration and shared fixtures for testing."""

import pytest
import os
from pathlib import Path
from sqlmodel import SQLModel, Session, create_engine
from fastapi.testclient import TestClient
from models import MiceCard, TryCard
import main

# Test database file path
TEST_DB_PATH = Path(__file__).parent / "test_story_builder.db"
TEST_DATABASE_URL = f"sqlite:///{TEST_DB_PATH}"


@pytest.fixture(scope="function")
def test_engine():
    """
    Create a real SQLite test database file for testing.
    The database is created fresh for each test and cleaned up after.
    
    Using a real file instead of in-memory makes debugging easier and
    avoids complex mocking - better for learning!
    """
    # Remove test database if it exists
    if TEST_DB_PATH.exists():
        TEST_DB_PATH.unlink()
    
    # Create new engine and tables
    engine = create_engine(TEST_DATABASE_URL, echo=False)
    SQLModel.metadata.create_all(engine)
    
    yield engine
    
    # Cleanup: close all connections and remove test database
    engine.dispose()
    if TEST_DB_PATH.exists():
        TEST_DB_PATH.unlink()


@pytest.fixture
def test_session(test_engine):
    """
    Create a database session with fresh tables for each test.
    Automatically commits and closes after the test completes.
    """
    with Session(test_engine) as session:
        yield session
        # Session automatically commits and closes after yield


@pytest.fixture
def test_client(test_engine):
    """
    Create a FastAPI TestClient that uses the test database.
    
    This is much simpler than the in-memory approach!
    We just temporarily replace the DATABASE_URL in main.py.
    """
    # Replace the app's engine with our test engine
    original_engine = main.engine
    main.engine = test_engine
    
    # Create test client
    client = TestClient(main.app)
    
    yield client
    
    # Restore original engine after test
    main.engine = original_engine


@pytest.fixture
def sample_mice_card():
    """
    Returns sample data for creating a MICE card (as a dict).
    Useful for testing create operations.
    """
    return {
        "code": "M",
        "opening": "The detective arrives in a mysterious small town",
        "closing": "The detective leaves the town with answers",
        "nesting_level": 1
    }


@pytest.fixture
def sample_try_card():
    """
    Returns sample data for creating a Try card (as a dict).
    Useful for testing create operations.
    """
    return {
        "type": "Failure",
        "order_num": 1,
        "attempt": "Detective interviews the suspect",
        "failure": "Suspect has an airtight alibi",
        "consequence": "Must look for other suspects"
    }


@pytest.fixture
def populated_session(test_session, sample_mice_card, sample_try_card):
    """
    Returns a database session pre-populated with sample data.
    Contains one MICE card and one Try card.
    """
    # Add sample MICE card
    mice_card = MiceCard(**sample_mice_card)
    test_session.add(mice_card)
    
    # Add sample Try card
    try_card = TryCard(**sample_try_card)
    test_session.add(try_card)
    
    test_session.commit()
    test_session.refresh(mice_card)
    test_session.refresh(try_card)
    
    return test_session


@pytest.fixture
def multiple_mice_cards():
    """
    Returns a list of multiple MICE cards for testing ordering and bulk operations.
    """
    return [
        {
            "code": "M",
            "opening": "Enter the world",
            "closing": "Leave the world",
            "nesting_level": 1
        },
        {
            "code": "I",
            "opening": "Question is posed",
            "closing": "Question is answered",
            "nesting_level": 2
        },
        {
            "code": "C",
            "opening": "Character is dissatisfied",
            "closing": "Character is transformed",
            "nesting_level": 3
        },
        {
            "code": "E",
            "opening": "Disruption occurs",
            "closing": "New order established",
            "nesting_level": 2
        }
    ]


@pytest.fixture
def multiple_try_cards():
    """
    Returns a list of multiple Try cards for testing ordering.
    """
    return [
        {
            "type": "Failure",
            "order_num": 1,
            "attempt": "First attempt",
            "failure": "First failure",
            "consequence": "First consequence"
        },
        {
            "type": "Success",
            "order_num": 2,
            "attempt": "Second attempt",
            "failure": "Partial failure",
            "consequence": "Second consequence"
        },
        {
            "type": "Trade-off",
            "order_num": 3,
            "attempt": "Third attempt",
            "failure": "Win something, lose something",
            "consequence": "Third consequence"
        }
    ]

