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
    card = TryCard(
        type=type,
        order_num=order_num,
        attempt=attempt,
        failure=failure,
        consequence=consequence
    )
    session.add(card)
    session.commit()
    session.refresh(card)
    return card


# ==================== Update Functions ====================

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
        card.type = type
        card.order_num = order_num
        card.attempt = attempt
        card.failure = failure
        card.consequence = consequence
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
