from sqlmodel import SQLModel, Field
from typing import Optional

class MiceCard(SQLModel, table=True):
    __tablename__ = "mice_cards"

    id: int | None = Field(default=None, primary_key=True)
    story_id: int = Field(default=1)
    code: str = Field(max_length=1)
    opening: str
    closing: str
    nesting_level: int
    act1_icon: Optional[bytes] = Field(default=None, nullable=True)  # AI-generated icon for Act 1 (opening)
    act3_icon: Optional[bytes] = Field(default=None, nullable=True)  # AI-generated icon for Act 3 (closing)

class TryCard(SQLModel, table=True):
    __tablename__ = "try_cards"

    id: int | None = Field(default=None, primary_key=True)
    story_id: int = Field(default=1)
    type: str
    attempt: str
    failure: str
    consequence: str
    order_num: int
    consequence_icon: Optional[bytes] = Field(default=None, nullable=True)  # AI-generated icon for consequence
