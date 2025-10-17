"""API Integration tests for template loading and utility endpoints."""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session
import db


# ==================== Template Loading Tests ====================

def test_load_mystery_template(test_client, test_engine):
    """Test that POST /load-template/mystery loads the mystery template."""
    response = test_client.post("/load-template/mystery")
    
    assert response.status_code == 200
    
    # Verify data was loaded (create fresh session to see committed changes)
    with Session(test_engine) as fresh_session:
        mice_cards = db.get_all_mice_cards(fresh_session)
        try_cards = db.get_all_try_cards(fresh_session)
        
        # Mystery template should have cards
        assert len(mice_cards) > 0
        assert len(try_cards) > 0


def test_load_adventure_template(test_client, test_engine):
    """Test that POST /load-template/adventure loads the adventure template."""
    response = test_client.post("/load-template/adventure")
    
    assert response.status_code == 200
    
    # Verify data was loaded (create fresh session to see committed changes)
    with Session(test_engine) as fresh_session:
        mice_cards = db.get_all_mice_cards(fresh_session)
        try_cards = db.get_all_try_cards(fresh_session)
        
        # Adventure template should have cards
        assert len(mice_cards) > 0
        assert len(try_cards) > 0


def test_load_romance_template(test_client, test_engine):
    """Test that POST /load-template/romance loads the romance template."""
    response = test_client.post("/load-template/romance")
    
    assert response.status_code == 200
    
    # Verify data was loaded (create fresh session to see committed changes)
    with Session(test_engine) as fresh_session:
        mice_cards = db.get_all_mice_cards(fresh_session)
        try_cards = db.get_all_try_cards(fresh_session)
        
        # Romance template should have cards
        assert len(mice_cards) > 0
        assert len(try_cards) > 0


def test_load_invalid_template(test_client):
    """Test that loading an invalid template returns 404."""
    response = test_client.post("/load-template/invalid_template_name")
    
    assert response.status_code == 404
    assert b"not found" in response.content


def test_template_redirect(test_client):
    """Test that loading a template returns HX-Redirect header."""
    response = test_client.post("/load-template/mystery")
    
    assert response.status_code == 200
    assert "hx-redirect" in response.headers
    assert response.headers["hx-redirect"] == "/"


# ==================== Clear Data Operations Tests ====================

def test_clear_all_data(test_client, test_session, test_engine, sample_mice_card, sample_try_card):
    """Test that POST /clear-data removes all cards from database."""
    # Create some cards first
    db.create_mice_card(test_session, **sample_mice_card)
    db.create_try_card(test_session, **sample_try_card)
    
    # Verify they exist
    assert len(db.get_all_mice_cards(test_session)) > 0
    assert len(db.get_all_try_cards(test_session)) > 0
    
    # Clear all data
    response = test_client.post("/clear-data")
    
    assert response.status_code == 200
    
    # Verify all data is gone (create fresh session to see committed changes)
    with Session(test_engine) as fresh_session:
        assert len(db.get_all_mice_cards(fresh_session)) == 0
        assert len(db.get_all_try_cards(fresh_session)) == 0


def test_clear_data_redirect(test_client):
    """Test that clearing data returns HX-Redirect header."""
    response = test_client.post("/clear-data")
    
    assert response.status_code == 200
    assert "hx-redirect" in response.headers
    assert response.headers["hx-redirect"] == "/"


# ==================== Form Clearing Tests ====================

def test_clear_mice_form(test_client):
    """Test that GET /clear-form returns empty string."""
    response = test_client.get("/clear-form")
    
    assert response.status_code == 200
    assert response.content == b""


def test_clear_try_form(test_client):
    """Test that GET /clear-try-form returns empty string."""
    response = test_client.get("/clear-try-form")
    
    assert response.status_code == 200
    assert response.content == b""

