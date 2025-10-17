"""API Integration tests for MICE card endpoints."""

import pytest
from fastapi.testclient import TestClient
import db


# ==================== Home Page Tests ====================

def test_home_page_loads(test_client):
    """Test that the home page loads successfully with status 200."""
    response = test_client.get("/")
    
    assert response.status_code == 200
    assert b"Story Builder" in response.content
    assert b"MICE Cards" in response.content
    assert b"Try/Fail Cycles" in response.content
    assert b"Generated Outline" in response.content


def test_home_page_empty_state(test_client):
    """Test that home page shows appropriate empty state when no cards exist."""
    response = test_client.get("/")
    
    assert response.status_code == 200
    # The lists should exist but be empty (no card elements)
    assert b"mice-cards-list" in response.content
    assert b"try-cards-list" in response.content


def test_home_page_with_data(test_client, test_session, sample_mice_card, sample_try_card):
    """Test that home page displays existing cards when data exists."""
    # Create some cards first
    db.create_mice_card(test_session, **sample_mice_card)
    db.create_try_card(test_session, **sample_try_card)
    
    response = test_client.get("/")
    
    assert response.status_code == 200
    # Check that card content appears in the response
    assert sample_mice_card["opening"].encode() in response.content
    assert sample_try_card["attempt"].encode() in response.content


# ==================== MICE Card Creation Tests ====================

def test_get_mice_form(test_client):
    """Test that GET /mice-form returns the create form HTML."""
    response = test_client.get("/mice-form")
    
    assert response.status_code == 200
    # Should contain form elements
    assert b"form" in response.content
    assert b"code" in response.content
    assert b"opening" in response.content
    assert b"closing" in response.content
    assert b"nesting_level" in response.content


def test_create_mice_card(test_client, test_session, sample_mice_card):
    """Test that POST /mice-cards creates a new card in the database."""
    response = test_client.post("/mice-cards", data=sample_mice_card)
    
    assert response.status_code == 200
    
    # Verify card was created in database
    cards = db.get_all_mice_cards(test_session)
    assert len(cards) == 1
    assert cards[0].code == sample_mice_card["code"]
    assert cards[0].opening == sample_mice_card["opening"]


def test_create_mice_card_redirect(test_client, sample_mice_card):
    """Test that creating a MICE card returns HX-Redirect header."""
    response = test_client.post("/mice-cards", data=sample_mice_card)
    
    assert response.status_code == 200
    assert "hx-redirect" in response.headers
    assert response.headers["hx-redirect"] == "/"


# ==================== MICE Card Reading Tests ====================

def test_get_mice_card(test_client, test_session, sample_mice_card):
    """Test that GET /mice-card/{id} returns the card display HTML."""
    # Create a card first
    created_card = db.create_mice_card(test_session, **sample_mice_card)
    
    response = test_client.get(f"/mice-card/{created_card.id}")
    
    assert response.status_code == 200
    # Check that card content appears in response
    assert sample_mice_card["opening"].encode() in response.content
    assert sample_mice_card["closing"].encode() in response.content


def test_get_mice_card_not_found(test_client):
    """Test that getting a non-existent MICE card returns empty response."""
    response = test_client.get("/mice-card/99999")
    
    assert response.status_code == 200
    assert response.content == b""


# ==================== MICE Card Editing Tests ====================

def test_get_mice_edit_form(test_client, test_session, sample_mice_card):
    """Test that GET /mice-edit/{id} returns the edit form HTML with pre-filled data."""
    # Create a card first
    created_card = db.create_mice_card(test_session, **sample_mice_card)
    
    response = test_client.get(f"/mice-edit/{created_card.id}")
    
    assert response.status_code == 200
    # Should contain form elements and existing data
    assert b"form" in response.content
    assert sample_mice_card["opening"].encode() in response.content


def test_get_mice_edit_form_not_found(test_client):
    """Test that getting edit form for non-existent card returns empty response."""
    response = test_client.get("/mice-edit/99999")
    
    assert response.status_code == 200
    assert response.content == b""


def test_update_mice_card(test_client, test_session, test_engine, sample_mice_card):
    """Test that PUT /mice-cards/{id} updates the card in the database."""
    # Create a card first
    created_card = db.create_mice_card(test_session, **sample_mice_card)
    card_id = created_card.id
    
    # Update it
    updated_data = {
        "code": "C",
        "opening": "Updated opening text",
        "closing": "Updated closing text",
        "nesting_level": 5
    }
    
    response = test_client.put(f"/mice-cards/{card_id}", data=updated_data)
    
    assert response.status_code == 200
    
    # Verify card was updated in database (create fresh session to see committed changes)
    from sqlmodel import Session
    with Session(test_engine) as fresh_session:
        card = db.get_mice_card(fresh_session, card_id)
        assert card.code == "C"
        assert card.opening == "Updated opening text"
        assert card.closing == "Updated closing text"
        assert card.nesting_level == 5


def test_update_mice_card_redirect(test_client, test_session, sample_mice_card):
    """Test that updating a MICE card returns HX-Redirect header."""
    # Create a card first
    created_card = db.create_mice_card(test_session, **sample_mice_card)
    
    # Update it
    updated_data = {
        "code": "I",
        "opening": "New opening",
        "closing": "New closing",
        "nesting_level": 2
    }
    
    response = test_client.put(f"/mice-cards/{created_card.id}", data=updated_data)
    
    assert response.status_code == 200
    assert "hx-redirect" in response.headers
    assert response.headers["hx-redirect"] == "/"


# ==================== MICE Card Deletion Tests ====================

def test_delete_mice_card(test_client, test_session, test_engine, sample_mice_card):
    """Test that DELETE /mice-cards/{id} removes the card from database."""
    # Create a card first
    created_card = db.create_mice_card(test_session, **sample_mice_card)
    card_id = created_card.id
    
    # Verify it exists
    assert db.get_mice_card(test_session, card_id) is not None
    
    # Delete it
    response = test_client.delete(f"/mice-cards/{card_id}")
    
    assert response.status_code == 200
    
    # Verify it's gone (create fresh session to see committed changes)
    from sqlmodel import Session
    with Session(test_engine) as fresh_session:
        assert db.get_mice_card(fresh_session, card_id) is None


def test_delete_mice_card_not_found(test_client):
    """Test that deleting a non-existent MICE card works without error."""
    response = test_client.delete("/mice-cards/99999")
    
    # Should succeed even if card doesn't exist
    assert response.status_code == 200
    assert response.content == b""

