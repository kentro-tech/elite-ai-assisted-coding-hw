"""API Integration tests for Try card endpoints."""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session
import db


# ==================== Try Card Creation Tests ====================

def test_get_try_form(test_client):
    """Test that GET /try-form returns the create form HTML."""
    response = test_client.get("/try-form")
    
    assert response.status_code == 200
    # Should contain form elements
    assert b"form" in response.content
    assert b"type" in response.content
    assert b"order_num" in response.content
    assert b"attempt" in response.content
    assert b"failure" in response.content
    assert b"consequence" in response.content


def test_create_try_card(test_client, test_session, sample_try_card):
    """Test that POST /try-cards creates a new card in the database."""
    response = test_client.post("/try-cards", data=sample_try_card)
    
    assert response.status_code == 200
    
    # Verify card was created in database
    cards = db.get_all_try_cards(test_session)
    assert len(cards) == 1
    assert cards[0].type == sample_try_card["type"]
    assert cards[0].attempt == sample_try_card["attempt"]


def test_create_try_card_redirect(test_client, sample_try_card):
    """Test that creating a Try card returns HX-Redirect header."""
    response = test_client.post("/try-cards", data=sample_try_card)
    
    assert response.status_code == 200
    assert "hx-redirect" in response.headers
    assert response.headers["hx-redirect"] == "/"


# ==================== Try Card Reading Tests ====================

def test_get_try_card(test_client, test_session, sample_try_card):
    """Test that GET /try-card/{id} returns the card display HTML."""
    # Create a card first
    created_card = db.create_try_card(test_session, **sample_try_card)
    
    response = test_client.get(f"/try-card/{created_card.id}")
    
    assert response.status_code == 200
    # Check that card content appears in response
    assert sample_try_card["attempt"].encode() in response.content
    assert sample_try_card["failure"].encode() in response.content
    assert sample_try_card["consequence"].encode() in response.content


def test_get_try_card_not_found(test_client):
    """Test that getting a non-existent Try card returns empty response."""
    response = test_client.get("/try-card/99999")
    
    assert response.status_code == 200
    assert response.content == b""


# ==================== Try Card Editing Tests ====================

def test_get_try_edit_form(test_client, test_session, sample_try_card):
    """Test that GET /try-edit/{id} returns the edit form HTML with pre-filled data."""
    # Create a card first
    created_card = db.create_try_card(test_session, **sample_try_card)
    
    response = test_client.get(f"/try-edit/{created_card.id}")
    
    assert response.status_code == 200
    # Should contain form elements and existing data
    assert b"form" in response.content
    assert sample_try_card["attempt"].encode() in response.content


def test_get_try_edit_form_not_found(test_client):
    """Test that getting edit form for non-existent card returns empty response."""
    response = test_client.get("/try-edit/99999")
    
    assert response.status_code == 200
    assert response.content == b""


def test_update_try_card(test_client, test_session, test_engine, sample_try_card):
    """Test that PUT /try-cards/{id} updates the card in the database."""
    # Create a card first
    created_card = db.create_try_card(test_session, **sample_try_card)
    card_id = created_card.id
    
    # Update it
    updated_data = {
        "type": "Success",
        "order_num": 10,
        "attempt": "Updated attempt text",
        "failure": "Updated failure text",
        "consequence": "Updated consequence text"
    }
    
    response = test_client.put(f"/try-cards/{card_id}", data=updated_data)
    
    assert response.status_code == 200
    
    # Verify card was updated in database (create fresh session to see committed changes)
    with Session(test_engine) as fresh_session:
        card = db.get_try_card(fresh_session, card_id)
        assert card.type == "Success"
        assert card.order_num == 10
        assert card.attempt == "Updated attempt text"
        assert card.failure == "Updated failure text"
        assert card.consequence == "Updated consequence text"


def test_update_try_card_returns_html(test_client, test_session, sample_try_card):
    """Test that updating a Try card returns HTML (not redirect like MICE cards)."""
    # Create a card first
    created_card = db.create_try_card(test_session, **sample_try_card)
    
    # Update it
    updated_data = {
        "type": "Success",
        "order_num": 5,
        "attempt": "New attempt",
        "failure": "New failure",
        "consequence": "New consequence"
    }
    
    response = test_client.put(f"/try-cards/{created_card.id}", data=updated_data)
    
    assert response.status_code == 200
    # Should return HTML content (not redirect header)
    # Try cards return rendered HTML instead of redirecting
    assert b"New attempt" in response.content


# ==================== Try Card Deletion Tests ====================

def test_delete_try_card(test_client, test_session, test_engine, sample_try_card):
    """Test that DELETE /try-cards/{id} removes the card from database."""
    # Create a card first
    created_card = db.create_try_card(test_session, **sample_try_card)
    card_id = created_card.id
    
    # Verify it exists
    assert db.get_try_card(test_session, card_id) is not None
    
    # Delete it
    response = test_client.delete(f"/try-cards/{card_id}")
    
    assert response.status_code == 200
    
    # Verify it's gone (create fresh session to see committed changes)
    with Session(test_engine) as fresh_session:
        assert db.get_try_card(fresh_session, card_id) is None


def test_delete_try_card_redirect(test_client, test_session, sample_try_card):
    """Test that deleting a Try card returns HX-Redirect header."""
    # Create a card first
    created_card = db.create_try_card(test_session, **sample_try_card)
    
    response = test_client.delete(f"/try-cards/{created_card.id}")
    
    assert response.status_code == 200
    assert "hx-redirect" in response.headers
    assert response.headers["hx-redirect"] == "/"

