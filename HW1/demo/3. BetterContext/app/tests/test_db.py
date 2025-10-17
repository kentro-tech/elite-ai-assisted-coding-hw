"""Unit tests for database operations in db.py"""

import pytest
from sqlmodel import select
from models import MiceCard, TryCard
import db


# ==================== MICE Card CRUD Tests ====================

def test_create_mice_card(test_session, sample_mice_card):
    """Test creating a MICE card and verifying all fields are saved correctly."""
    card = db.create_mice_card(
        session=test_session,
        **sample_mice_card
    )
    
    assert card is not None
    assert card.id is not None  # ID should be auto-generated
    assert card.code == sample_mice_card["code"]
    assert card.opening == sample_mice_card["opening"]
    assert card.closing == sample_mice_card["closing"]
    assert card.nesting_level == sample_mice_card["nesting_level"]
    assert card.story_id == 1  # Default story_id


def test_get_all_mice_cards(test_session, multiple_mice_cards):
    """Test retrieving all MICE cards from the database."""
    # Create multiple cards
    for card_data in multiple_mice_cards:
        db.create_mice_card(session=test_session, **card_data)
    
    # Retrieve all cards
    cards = db.get_all_mice_cards(test_session)
    
    assert len(cards) == len(multiple_mice_cards)
    assert all(isinstance(card, MiceCard) for card in cards)


def test_get_all_mice_cards_empty(test_session):
    """Test getting all MICE cards when database is empty."""
    cards = db.get_all_mice_cards(test_session)
    assert cards == []


def test_get_mice_card_by_id(test_session, sample_mice_card):
    """Test retrieving a single MICE card by its ID."""
    # Create a card
    created_card = db.create_mice_card(session=test_session, **sample_mice_card)
    
    # Retrieve it by ID
    retrieved_card = db.get_mice_card(test_session, created_card.id)
    
    assert retrieved_card is not None
    assert retrieved_card.id == created_card.id
    assert retrieved_card.code == created_card.code
    assert retrieved_card.opening == created_card.opening


def test_get_mice_card_not_found(test_session):
    """Test that getting a non-existent MICE card returns None."""
    card = db.get_mice_card(test_session, 99999)
    assert card is None


def test_update_mice_card(test_session, sample_mice_card):
    """Test updating all fields of a MICE card."""
    # Create a card
    created_card = db.create_mice_card(session=test_session, **sample_mice_card)
    original_id = created_card.id
    
    # Update it
    updated_card = db.update_mice_card(
        session=test_session,
        card_id=original_id,
        code="C",
        opening="Updated opening",
        closing="Updated closing",
        nesting_level=5
    )
    
    assert updated_card is not None
    assert updated_card.id == original_id  # ID should not change
    assert updated_card.code == "C"
    assert updated_card.opening == "Updated opening"
    assert updated_card.closing == "Updated closing"
    assert updated_card.nesting_level == 5


def test_update_mice_card_not_found(test_session):
    """Test that updating a non-existent MICE card returns None."""
    result = db.update_mice_card(
        session=test_session,
        card_id=99999,
        code="M",
        opening="test",
        closing="test",
        nesting_level=1
    )
    assert result is None


def test_delete_mice_card(test_session, sample_mice_card):
    """Test deleting a MICE card and verifying it's gone."""
    # Create a card
    created_card = db.create_mice_card(session=test_session, **sample_mice_card)
    card_id = created_card.id
    
    # Delete it
    result = db.delete_mice_card(test_session, card_id)
    
    assert result is True
    
    # Verify it's deleted
    deleted_card = db.get_mice_card(test_session, card_id)
    assert deleted_card is None


def test_delete_mice_card_not_found(test_session):
    """Test that deleting a non-existent MICE card returns False."""
    result = db.delete_mice_card(test_session, 99999)
    assert result is False


# ==================== Try Card CRUD Tests ====================

def test_create_try_card(test_session, sample_try_card):
    """Test creating a Try card and verifying all fields are saved correctly."""
    card = db.create_try_card(
        session=test_session,
        **sample_try_card
    )
    
    assert card is not None
    assert card.id is not None  # ID should be auto-generated
    assert card.type == sample_try_card["type"]
    assert card.order_num == sample_try_card["order_num"]
    assert card.attempt == sample_try_card["attempt"]
    assert card.failure == sample_try_card["failure"]
    assert card.consequence == sample_try_card["consequence"]
    assert card.story_id == 1  # Default story_id


def test_get_all_try_cards(test_session, multiple_try_cards):
    """Test retrieving all Try cards and verifying they're ordered by order_num."""
    # Create cards in non-sequential order
    for card_data in reversed(multiple_try_cards):  # Create in reverse order
        db.create_try_card(session=test_session, **card_data)
    
    # Retrieve all cards
    cards = db.get_all_try_cards(test_session)
    
    assert len(cards) == len(multiple_try_cards)
    assert all(isinstance(card, TryCard) for card in cards)
    
    # Verify they're ordered by order_num
    order_nums = [card.order_num for card in cards]
    assert order_nums == sorted(order_nums)


def test_get_all_try_cards_empty(test_session):
    """Test getting all Try cards when database is empty."""
    cards = db.get_all_try_cards(test_session)
    assert cards == []


def test_get_try_card_by_id(test_session, sample_try_card):
    """Test retrieving a single Try card by its ID."""
    # Create a card
    created_card = db.create_try_card(session=test_session, **sample_try_card)
    
    # Retrieve it by ID
    retrieved_card = db.get_try_card(test_session, created_card.id)
    
    assert retrieved_card is not None
    assert retrieved_card.id == created_card.id
    assert retrieved_card.type == created_card.type
    assert retrieved_card.attempt == created_card.attempt


def test_get_try_card_not_found(test_session):
    """Test that getting a non-existent Try card returns None."""
    card = db.get_try_card(test_session, 99999)
    assert card is None


def test_update_try_card(test_session, sample_try_card):
    """Test updating all fields of a Try card."""
    # Create a card
    created_card = db.create_try_card(session=test_session, **sample_try_card)
    original_id = created_card.id
    
    # Update it
    updated_card = db.update_try_card(
        session=test_session,
        card_id=original_id,
        type="Success",
        order_num=10,
        attempt="Updated attempt",
        failure="Updated failure",
        consequence="Updated consequence"
    )
    
    assert updated_card is not None
    assert updated_card.id == original_id  # ID should not change
    assert updated_card.type == "Success"
    assert updated_card.order_num == 10
    assert updated_card.attempt == "Updated attempt"
    assert updated_card.failure == "Updated failure"
    assert updated_card.consequence == "Updated consequence"


def test_update_try_card_not_found(test_session):
    """Test that updating a non-existent Try card returns None."""
    result = db.update_try_card(
        session=test_session,
        card_id=99999,
        type="Success",
        order_num=1,
        attempt="test",
        failure="test",
        consequence="test"
    )
    assert result is None


def test_delete_try_card(test_session, sample_try_card):
    """Test deleting a Try card and verifying it's gone."""
    # Create a card
    created_card = db.create_try_card(session=test_session, **sample_try_card)
    card_id = created_card.id
    
    # Delete it
    result = db.delete_try_card(test_session, card_id)
    
    assert result is True
    
    # Verify it's deleted
    deleted_card = db.get_try_card(test_session, card_id)
    assert deleted_card is None


def test_delete_try_card_not_found(test_session):
    """Test that deleting a non-existent Try card returns False."""
    result = db.delete_try_card(test_session, 99999)
    assert result is False


# ==================== Bulk Operations Tests ====================

def test_clear_all_cards(test_session, sample_mice_card, sample_try_card):
    """Test clearing all cards from both tables."""
    # Create some cards
    db.create_mice_card(session=test_session, **sample_mice_card)
    db.create_mice_card(session=test_session, code="I", opening="test", closing="test", nesting_level=2)
    db.create_try_card(session=test_session, **sample_try_card)
    db.create_try_card(session=test_session, type="Success", order_num=2, attempt="t", failure="t", consequence="t")
    
    # Verify cards exist
    assert len(db.get_all_mice_cards(test_session)) == 2
    assert len(db.get_all_try_cards(test_session)) == 2
    
    # Clear all
    db.clear_all_cards(test_session)
    
    # Verify all are gone
    assert len(db.get_all_mice_cards(test_session)) == 0
    assert len(db.get_all_try_cards(test_session)) == 0


def test_clear_all_cards_empty_db(test_session):
    """Test clearing cards when database is already empty."""
    # Should not raise an error
    db.clear_all_cards(test_session)
    
    assert len(db.get_all_mice_cards(test_session)) == 0
    assert len(db.get_all_try_cards(test_session)) == 0


def test_load_template_data(test_session):
    """Test loading template data into the database."""
    mice_data = [
        {"code": "M", "opening": "Enter world", "closing": "Leave world", "nesting_level": 1},
        {"code": "I", "opening": "Question posed", "closing": "Answer found", "nesting_level": 2}
    ]
    
    try_data = [
        {"type": "Failure", "order_num": 1, "attempt": "Try 1", "failure": "Fail 1", "consequence": "Con 1"},
        {"type": "Success", "order_num": 2, "attempt": "Try 2", "failure": "Fail 2", "consequence": "Con 2"}
    ]
    
    # Load template
    db.load_template_data(test_session, mice_data, try_data)
    
    # Verify data loaded
    mice_cards = db.get_all_mice_cards(test_session)
    try_cards = db.get_all_try_cards(test_session)
    
    assert len(mice_cards) == 2
    assert len(try_cards) == 2
    assert mice_cards[0].code == "M"
    assert try_cards[0].type == "Failure"


def test_load_template_replaces_existing(test_session, sample_mice_card, sample_try_card):
    """Test that loading a template clears existing data first."""
    # Create some cards
    db.create_mice_card(session=test_session, **sample_mice_card)
    db.create_try_card(session=test_session, **sample_try_card)
    
    # Verify they exist
    assert len(db.get_all_mice_cards(test_session)) == 1
    assert len(db.get_all_try_cards(test_session)) == 1
    
    # Load new template
    new_mice_data = [
        {"code": "E", "opening": "Event", "closing": "Resolution", "nesting_level": 1}
    ]
    new_try_data = []
    
    db.load_template_data(test_session, new_mice_data, new_try_data)
    
    # Verify old data is gone and new data exists
    mice_cards = db.get_all_mice_cards(test_session)
    try_cards = db.get_all_try_cards(test_session)
    
    assert len(mice_cards) == 1
    assert mice_cards[0].code == "E"  # New card
    assert len(try_cards) == 0  # Old try card is gone

