"""Clear icon from a Try card for testing."""
import sys
from sqlmodel import Session, create_engine
from models import TryCard

DATABASE_URL = "sqlite:///story_builder.db"
engine = create_engine(DATABASE_URL)

if len(sys.argv) < 2:
    print("Usage: python clear_icon.py <card_id>")
    print("\nAvailable cards:")
    with Session(engine) as session:
        cards = session.query(TryCard).all()
        for card in cards:
            icon_status = "✅ Has icon" if card.consequence_icon else "❌ No icon"
            print(f"  Card {card.id}: {card.type} #{card.order_num} - {icon_status}")
    sys.exit(1)

card_id = int(sys.argv[1])

with Session(engine) as session:
    card = session.get(TryCard, card_id)
    if card:
        card.consequence_icon = None
        session.commit()
        print(f"✅ Cleared icon from card {card_id}")
    else:
        print(f"❌ Card {card_id} not found")
