"""Database operations for the Story Builder app."""

from sqlmodel import Session, select
from models import MiceCard, TryCard


# ==================== Query Functions ====================

def get_all_mice_cards(session: Session) -> list[MiceCard]:
    """Get all MICE cards from the database."""
    return session.exec(select(MiceCard)).all()


def get_all_try_cards(session: Session) -> list[TryCard]:
    """Get all Try/Fail cards from the database, ordered by order_num."""
    return session.exec(select(TryCard).order_by(TryCard.order_num)).all()


def get_mice_card(session: Session, card_id: int) -> MiceCard | None:
    """Get a single MICE card by ID."""
    return session.get(MiceCard, card_id)


def get_try_card(session: Session, card_id: int) -> TryCard | None:
    """Get a single Try/Fail card by ID."""
    return session.get(TryCard, card_id)


# ==================== Create Functions ====================

def create_mice_card(
    session: Session,
    code: str,
    opening: str,
    closing: str,
    nesting_level: int
) -> MiceCard:
    """Create a new MICE card and save it to the database."""
    card = MiceCard(
        code=code,
        opening=opening,
        closing=closing,
        nesting_level=nesting_level
    )
    session.add(card)
    session.commit()
    session.refresh(card)
    return card


def create_try_card(
    session: Session,
    type: str,
    order_num: int,
    attempt: str,
    failure: str,
    consequence: str
) -> TryCard:
    """Create a new Try/Fail card and save it to the database."""
    # Create the new card
    card = TryCard(
        type=type,
        order_num=order_num,
        attempt=attempt,
        failure=failure,
        consequence=consequence
    )
    session.add(card)
    session.flush()  # Flush to get the card ID but don't commit yet
    
    # Get all cards ordered by order_num
    all_cards = session.exec(select(TryCard).order_by(TryCard.order_num)).all()
    
    # Remove the newly created card from the list
    all_cards = [c for c in all_cards if c.id != card.id]
    
    # Insert the card at the desired position (order_num is 1-based)
    all_cards.insert(order_num - 1, card)
    
    # Reassign order numbers sequentially
    for idx, c in enumerate(all_cards, start=1):
        c.order_num = idx
    
    session.commit()
    session.refresh(card)
    return card


# ==================== Update Functions ====================

def update_try_card_order(
    session: Session,  # Database session
    card_id: int,  # ID of the card to reorder
    new_order_num: int  # New order number for the card
) -> bool:
    """Update the order number of a Try card, shifting other cards as needed."""
    card = session.get(TryCard, card_id)
    if not card:
        return False
    
    old_order = card.order_num
    
    # If order hasn't changed, nothing to do
    if old_order == new_order_num:
        return True
    
    # Get all cards to reorder
    all_cards = session.exec(select(TryCard).order_by(TryCard.order_num)).all()
    
    # Remove the card being moved from the list
    all_cards = [c for c in all_cards if c.id != card_id]
    
    # Insert the card at the new position
    all_cards.insert(new_order_num - 1, card)
    
    # Reassign order numbers sequentially
    for idx, c in enumerate(all_cards, start=1):
        c.order_num = idx
    
    session.commit()
    return True

def update_mice_card(
    session: Session,
    card_id: int,
    code: str,
    opening: str,
    closing: str,
    nesting_level: int
) -> MiceCard | None:
    """Update an existing MICE card."""
    card = session.get(MiceCard, card_id)
    if card:
        card.code = code
        card.opening = opening
        card.closing = closing
        card.nesting_level = nesting_level
        session.commit()
        session.refresh(card)
    return card


def update_try_card(
    session: Session,
    card_id: int,
    type: str,
    order_num: int,
    attempt: str,
    failure: str,
    consequence: str
) -> TryCard | None:
    """Update an existing Try/Fail card."""
    card = session.get(TryCard, card_id)
    if card:
        old_order = card.order_num
        
        # Update the card's content fields
        card.type = type
        card.attempt = attempt
        card.failure = failure
        card.consequence = consequence
        
        # If order number changed, reorder all cards
        if old_order != order_num:
            # Get all cards ordered by current order_num
            all_cards = session.exec(select(TryCard).order_by(TryCard.order_num)).all()
            
            # Remove the card being moved from the list
            all_cards = [c for c in all_cards if c.id != card_id]
            
            # Insert the card at the new position (order_num is 1-based)
            all_cards.insert(order_num - 1, card)
            
            # Reassign order numbers sequentially
            for idx, c in enumerate(all_cards, start=1):
                c.order_num = idx
        
        session.commit()
        session.refresh(card)
    return card


# ==================== Delete Functions ====================

def delete_mice_card(session: Session, card_id: int) -> bool:
    """Delete a MICE card by ID. Returns True if deleted, False if not found."""
    card = session.get(MiceCard, card_id)
    if card:
        session.delete(card)
        session.commit()
        return True
    return False


def delete_try_card(session: Session, card_id: int) -> bool:
    """Delete a Try/Fail card by ID. Returns True if deleted, False if not found."""
    card = session.get(TryCard, card_id)
    if card:
        session.delete(card)
        session.commit()
        return True
    return False


def clear_all_cards(session: Session):
    """Delete all MICE and Try/Fail cards from the database."""
    for card in session.exec(select(MiceCard)):
        session.delete(card)
    for card in session.exec(select(TryCard)):
        session.delete(card)
    session.commit()


# ==================== Template Loading ====================

def load_template_data(
    session: Session,
    mice_data: list[dict],
    try_data: list[dict]
):
    """Clear all cards and load template data into the database."""
    clear_all_cards(session)

    for data in mice_data:
        session.add(MiceCard(**data))

    for data in try_data:
        session.add(TryCard(**data))

    session.commit()
