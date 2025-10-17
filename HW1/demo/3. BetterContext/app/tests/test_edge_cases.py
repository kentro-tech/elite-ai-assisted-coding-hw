"""Edge case tests to discover bugs and test boundary conditions."""

import pytest
from sqlmodel import Session
import db


# ==================== Validation and Invalid Input Tests ====================

def test_create_mice_card_empty_fields(test_session):
    """Test creating a MICE card with empty string fields."""
    card = db.create_mice_card(
        session=test_session,
        code="",
        opening="",
        closing="",
        nesting_level=1
    )
    
    # Should create successfully - no validation in place
    assert card is not None
    assert card.code == ""
    assert card.opening == ""


def test_create_mice_card_invalid_code(test_session):
    """Test creating a MICE card with invalid code (not M/I/C/E)."""
    # Should accept any string - no validation in place
    card = db.create_mice_card(
        session=test_session,
        code="X",  # Invalid code
        opening="Test opening",
        closing="Test closing",
        nesting_level=1
    )
    
    assert card is not None
    assert card.code == "X"


def test_create_mice_card_negative_nesting(test_session):
    """Test creating a MICE card with negative nesting level."""
    card = db.create_mice_card(
        session=test_session,
        code="M",
        opening="Test opening",
        closing="Test closing",
        nesting_level=-1  # Negative nesting
    )
    
    # Should accept negative values - no validation in place
    assert card is not None
    assert card.nesting_level == -1


def test_create_try_card_empty_fields(test_session):
    """Test creating a Try card with empty string fields."""
    card = db.create_try_card(
        session=test_session,
        type="",
        order_num=1,
        attempt="",
        failure="",
        consequence=""
    )
    
    # Should create successfully - no validation in place
    assert card is not None
    assert card.type == ""


def test_create_try_card_invalid_type(test_session):
    """Test creating a Try card with invalid cycle type."""
    # Should accept any string - no validation in place
    card = db.create_try_card(
        session=test_session,
        type="InvalidType",
        order_num=1,
        attempt="Test attempt",
        failure="Test failure",
        consequence="Test consequence"
    )
    
    assert card is not None
    assert card.type == "InvalidType"


def test_create_try_card_negative_order(test_session):
    """Test creating a Try card with negative order number."""
    card = db.create_try_card(
        session=test_session,
        type="Failure",
        order_num=-5,  # Negative order
        attempt="Test attempt",
        failure="Test failure",
        consequence="Test consequence"
    )
    
    # Should accept negative values - no validation in place
    assert card is not None
    assert card.order_num == -5


# ==================== Special Characters and Long Text Tests ====================

def test_mice_card_special_characters(test_session):
    """Test MICE card with HTML special characters."""
    special_text = '<script>alert("XSS")</script> & "quotes" & \'apostrophes\''
    
    card = db.create_mice_card(
        session=test_session,
        code="M",
        opening=special_text,
        closing=special_text,
        nesting_level=1
    )
    
    assert card is not None
    assert card.opening == special_text
    assert card.closing == special_text


def test_mice_card_very_long_text(test_session):
    """Test MICE card with very long text (10,000 characters)."""
    long_text = "A" * 10000
    
    card = db.create_mice_card(
        session=test_session,
        code="M",
        opening=long_text,
        closing=long_text,
        nesting_level=1
    )
    
    assert card is not None
    assert len(card.opening) == 10000


def test_try_card_special_characters(test_session):
    """Test Try card with HTML special characters in all fields."""
    special_text = '<b>Bold</b> & <i>Italic</i> "quoted"'
    
    card = db.create_try_card(
        session=test_session,
        type="Failure <script>",
        order_num=1,
        attempt=special_text,
        failure=special_text,
        consequence=special_text
    )
    
    assert card is not None
    assert card.attempt == special_text


def test_try_card_multiline_text(test_session):
    """Test Try card with newlines in text fields."""
    multiline_text = "Line 1\nLine 2\nLine 3\n\nLine 5"
    
    card = db.create_try_card(
        session=test_session,
        type="Failure",
        order_num=1,
        attempt=multiline_text,
        failure=multiline_text,
        consequence=multiline_text
    )
    
    assert card is not None
    assert "\n" in card.attempt


# ==================== Duplicate and Ordering Issues ====================

def test_duplicate_try_card_order_numbers(test_session):
    """Test creating multiple Try cards with the same order_num."""
    # Create two cards with same order number
    card1 = db.create_try_card(
        session=test_session,
        type="Failure",
        order_num=1,
        attempt="First",
        failure="First fail",
        consequence="First consequence"
    )
    
    card2 = db.create_try_card(
        session=test_session,
        type="Success",
        order_num=1,  # Duplicate order number
        attempt="Second",
        failure="Second fail",
        consequence="Second consequence"
    )
    
    # Both should be created - no uniqueness constraint
    assert card1 is not None
    assert card2 is not None
    
    # When retrieved, ordering might be unpredictable
    cards = db.get_all_try_cards(test_session)
    assert len(cards) == 2


def test_mice_cards_same_nesting_level(test_session):
    """Test multiple MICE cards at the same nesting level."""
    for i in range(3):
        card = db.create_mice_card(
            session=test_session,
            code=["M", "I", "C"][i],
            opening=f"Opening {i}",
            closing=f"Closing {i}",
            nesting_level=1  # All at same level
        )
        assert card is not None
    
    cards = db.get_all_mice_cards(test_session)
    assert len(cards) == 3


def test_try_cards_out_of_order(test_session):
    """Test creating Try cards in non-sequential order."""
    # Create cards with order: 5, 1, 3
    for order in [5, 1, 3]:
        card = db.create_try_card(
            session=test_session,
            type="Failure",
            order_num=order,
            attempt=f"Attempt {order}",
            failure=f"Failure {order}",
            consequence=f"Consequence {order}"
        )
        assert card is not None
    
    # Verify they're returned sorted by order_num
    cards = db.get_all_try_cards(test_session)
    order_nums = [card.order_num for card in cards]
    assert order_nums == [1, 3, 5]  # Should be sorted


# ==================== State Consistency Tests ====================

def test_delete_then_get(test_session, sample_mice_card):
    """Test that getting a card after deletion returns None."""
    # Create and delete
    card = db.create_mice_card(test_session, **sample_mice_card)
    card_id = card.id
    
    db.delete_mice_card(test_session, card_id)
    
    # Try to get deleted card
    result = db.get_mice_card(test_session, card_id)
    assert result is None


def test_delete_then_update(test_session, sample_mice_card):
    """Test that updating a deleted card returns None."""
    # Create and delete
    card = db.create_mice_card(test_session, **sample_mice_card)
    card_id = card.id
    
    db.delete_mice_card(test_session, card_id)
    
    # Try to update deleted card
    result = db.update_mice_card(
        test_session,
        card_id,
        code="I",
        opening="New",
        closing="New",
        nesting_level=2
    )
    assert result is None


def test_load_template_multiple_times(test_session):
    """Test loading the same template twice - should replace data."""
    template_data_mice = [
        {"code": "M", "opening": "First", "closing": "First", "nesting_level": 1}
    ]
    template_data_try = [
        {"type": "Failure", "order_num": 1, "attempt": "First", "failure": "First", "consequence": "First"}
    ]
    
    # Load template first time
    db.load_template_data(test_session, template_data_mice, template_data_try)
    
    # Load same template again
    db.load_template_data(test_session, template_data_mice, template_data_try)
    
    # Should still only have one of each card (not duplicated)
    mice_cards = db.get_all_mice_cards(test_session)
    try_cards = db.get_all_try_cards(test_session)
    
    assert len(mice_cards) == 1
    assert len(try_cards) == 1


def test_load_different_templates(test_session):
    """Test loading different templates in sequence - should replace data."""
    template1_mice = [
        {"code": "M", "opening": "Template 1", "closing": "Template 1", "nesting_level": 1}
    ]
    template1_try = []
    
    template2_mice = [
        {"code": "I", "opening": "Template 2", "closing": "Template 2", "nesting_level": 1}
    ]
    template2_try = [
        {"type": "Success", "order_num": 1, "attempt": "Template 2", "failure": "T2", "consequence": "T2"}
    ]
    
    # Load first template
    db.load_template_data(test_session, template1_mice, template1_try)
    
    # Load second template
    db.load_template_data(test_session, template2_mice, template2_try)
    
    # Should only have data from second template
    mice_cards = db.get_all_mice_cards(test_session)
    try_cards = db.get_all_try_cards(test_session)
    
    assert len(mice_cards) == 1
    assert mice_cards[0].opening == "Template 2"
    assert len(try_cards) == 1


# ==================== Boundary Conditions ====================

def test_mice_card_zero_nesting_level(test_session):
    """Test MICE card with nesting level = 0."""
    card = db.create_mice_card(
        session=test_session,
        code="M",
        opening="Test",
        closing="Test",
        nesting_level=0
    )
    
    assert card is not None
    assert card.nesting_level == 0


def test_mice_card_large_nesting_level(test_session):
    """Test MICE card with very large nesting level (100+)."""
    card = db.create_mice_card(
        session=test_session,
        code="M",
        opening="Test",
        closing="Test",
        nesting_level=999
    )
    
    assert card is not None
    assert card.nesting_level == 999


def test_try_card_zero_order(test_session):
    """Test Try card with order number = 0."""
    card = db.create_try_card(
        session=test_session,
        type="Failure",
        order_num=0,
        attempt="Test",
        failure="Test",
        consequence="Test"
    )
    
    assert card is not None
    assert card.order_num == 0


def test_empty_database_operations(test_session):
    """Test all read operations on empty database."""
    # All should return empty lists or None without errors
    assert db.get_all_mice_cards(test_session) == []
    assert db.get_all_try_cards(test_session) == []
    assert db.get_mice_card(test_session, 1) is None
    assert db.get_try_card(test_session, 1) is None
    
    # Clear on empty database should work
    db.clear_all_cards(test_session)
    
    # Still empty
    assert db.get_all_mice_cards(test_session) == []

