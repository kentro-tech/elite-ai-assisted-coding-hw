"""Smoke tests to verify test infrastructure is working correctly."""

import pytest
from models import MiceCard, TryCard
import db


def test_pytest_works():
    """Basic test to verify pytest is installed and working."""
    assert True


def test_fixtures_available(test_session, sample_mice_card):
    """Verify that fixtures are accessible and working."""
    assert test_session is not None
    assert sample_mice_card is not None
    assert "code" in sample_mice_card


def test_database_connection(test_session):
    """Verify we can connect to the test database."""
    # Try a simple query
    from sqlmodel import select
    result = test_session.exec(select(MiceCard)).all()
    assert isinstance(result, list)


def test_create_mice_card_basic(test_session):
    """Basic smoke test for creating a MICE card."""
    card = db.create_mice_card(
        session=test_session,
        code="M",
        opening="Test opening",
        closing="Test closing",
        nesting_level=1
    )
    
    assert card is not None
    assert card.id is not None
    assert card.code == "M"
    assert card.opening == "Test opening"


def test_create_try_card_basic(test_session):
    """Basic smoke test for creating a Try card."""
    card = db.create_try_card(
        session=test_session,
        type="Failure",
        order_num=1,
        attempt="Test attempt",
        failure="Test failure",
        consequence="Test consequence"
    )
    
    assert card is not None
    assert card.id is not None
    assert card.type == "Failure"
    assert card.order_num == 1


def test_test_client_available(test_client):
    """Verify the test client is available and can make requests."""
    response = test_client.get("/")
    assert response.status_code == 200

