# Refactoring Plan - Story Builder App

## Overview
This document outlines potential refactors to reduce technical debt. Each item includes justification and estimated impact for prioritization.

---

## 1. Extract Repetitive CSS Class Strings

**Location**: `components.py`, `forms.py`, `main.py`

**Issue**: Tailwind/DaisyUI classes are hardcoded as strings throughout components (e.g., `"btn btn-xs btn-primary mr-1"`, `"card border-2 p-3"`). This violates DRY and makes UI updates brittle.

**Refactor**: Create a `styles.py` module with semantic constants:
```python
# styles.py
BUTTON_PRIMARY_SMALL = "btn btn-xs btn-primary mr-1"
BUTTON_ERROR_SMALL = "btn btn-xs btn-error"
CARD_BASE = "card border-2 p-3"
```

**Impact**:
- **Benefit**: Single source of truth for styling; bulk style changes require 1 edit vs 10+
- **Cost**: Low - simple string extraction, no logic changes
- **Risk**: Very low - purely cosmetic refactor

**Priority**: Medium - Only worth doing if UI styling changes are anticipated. Current duplication is manageable (~15 occurrences).

---

## 2. Consolidate Form Field Builder Logic

**Location**: `forms.py:8-14`, `forms.py:83-103`, `forms.py:229-276`

**Issue**: `_form_field()` helper exists but only used 5 times in edit forms. Create forms duplicate the pattern 10+ times without using the helper.

**Refactor**:
- Make `_form_field()` more flexible to handle all form field cases
- Apply consistently across both create and edit forms
- Consider parameterizing common input types (textarea, select, number)

**Impact**:
- **Benefit**: Reduces ~50 lines of repetitive code; ensures consistent form field structure
- **Cost**: Medium - requires parameterizing the helper and updating 15+ call sites
- **Risk**: Low - well-isolated logic, easy to test

**Priority**: Low - The current duplication is acceptable for a small app with only 2 form types. Only refactor if adding more form types.

---

## 3. Abstract Database Session Management Pattern

**Location**: `main.py:73-75`, `main.py:169-170`, `main.py:190-191` (repeated 12 times)

**Issue**: Every route handler repeats the pattern:
```python
with Session(engine) as session:
    db.some_operation(session, ...)
```

**Refactor Options**:

**Option A - Dependency Injection (FastAPI-style)**:
```python
from fastapi import Depends

def get_session():
    with Session(engine) as session:
        yield session

@app.get("/")
def index(session: Session = Depends(get_session)):
    mice_cards = db.get_all_mice_cards(session)
```

**Option B - Decorator Pattern**:
```python
def with_session(func):
    def wrapper(*args, **kwargs):
        with Session(engine) as session:
            return func(session, *args, **kwargs)
    return wrapper

@app.get("/")
@with_session
def index(session):
    mice_cards = db.get_all_mice_cards(session)
```

**Impact**:
- **Benefit**: Eliminates 12+ repetitions; centralizes session lifecycle management
- **Cost**: High - Option A requires FastAPI upgrade/integration; Option B adds indirection
- **Risk**: Medium - Session lifecycle is critical; errors could affect all routes

**Priority**: Low - Current pattern is explicit and safe. Only refactor if adding connection pooling, transaction management, or complex session lifecycle needs.

---

## 4. Extract Template Modal Builder

**Location**: `main.py:24-68`

**Issue**: 45-line `_templates_modal()` function embedded in main.py with repetitive button structures. Three nearly identical buttons differ only in emoji, title, description, template name.

**Refactor**:
```python
# components.py
def _template_button(emoji: str, title: str, description: str, template_name: str):
    return air.Button(
        air.H4(f"{emoji} {title}", class_="text-xl font-bold mb-2"),
        air.P(description, class_="text-sm"),
        class_="btn btn-outline w-full text-left h-auto py-4 mb-3",
        hx_post=f"/load-template/{template_name}",
        hx_target="body",
        hx_swap="outerHTML",
        onclick="document.getElementById('templates-modal').close()"
    )

def templates_modal():
    templates = [
        ("🔍", "Mystery", "A detective investigates a murder...", "mystery"),
        ("🗺️", "Adventure", "A hero embarks on a quest...", "adventure"),
        ("💕", "Romance", "Two people find love...", "romance"),
    ]
    return air.Dialog(
        air.Div(
            air.H3("Story Templates", class_="text-2xl font-bold mb-4"),
            air.P("Choose a template...", class_="mb-4"),
            air.Div(*[_template_button(*t) for t in templates]),
            air.Button("Cancel", class_="btn btn-ghost mt-2",
                      onclick="document.getElementById('templates-modal').close()"),
            class_="modal-box"
        ),
        id="templates-modal",
        class_="modal"
    )
```

**Impact**:
- **Benefit**: Reduces 45 lines to ~20; makes adding templates trivial (append to list vs duplicate 10 lines); belongs semantically in components.py
- **Cost**: Low - straightforward extraction and parameterization
- **Risk**: Very low - purely structural

**Priority**: High - Strong abstraction (button pattern repeats exactly 3x); fits established component organization pattern; adding more templates is likely.

---

## 5. Unify Card Rendering Field Display Logic

**Location**: `components.py:86-100` (try card), `components.py:54-55` (mice card)

**Issue**: Try/Fail cards repeat the pattern 3 times:
```python
air.Div(
    air.Span("Label: ", class_="font-bold text-xs"),
    air.Span(card.field, class_="text-xs"),
    class_="mb-1"
)
```

**Refactor**:
```python
def _labeled_field(label: str, value: str, bold_class: str = "font-bold text-xs", value_class: str = "text-xs"):
    return air.Div(
        air.Span(f"{label}: ", class_=bold_class),
        air.Span(value, class_=value_class),
        class_="mb-1"
    )
```

**Impact**:
- **Benefit**: Eliminates 4+ repetitions in try_card alone; already used pattern in mice_card (see `info_span:41-46`)
- **Cost**: Very low - simple extraction; MICE card already has similar `info_span()` helper
- **Risk**: Very low

**Priority**: Medium - Duplication is limited to one function; only 3 occurrences. Consider if extending card types or adding more fields. Could merge with existing `info_span()` helper for consistency.

---

## 6. Standardize HTMX Attribute Patterns

**Location**: Throughout `main.py`, `forms.py`, `components.py`

**Issue**: HTMX attributes specified inconsistently:
- Edit buttons: `hx_get`, `hx_target`, `hx_swap` patterns repeated 6+ times
- Delete buttons: Different `hx_confirm` and redirect strategies (some use `HX-Redirect`, others swap `body`)
- Forms: Inconsistent target/swap combos (some target `body`, others target specific IDs)

**Examples**:
```python
# Edit pattern (components.py:60-63)
hx_get=f"/mice-edit/{card.id}",
hx_target=f"#mice-card-{card.id}",
hx_swap="outerHTML"

# Delete patterns differ (components.py:67-70 vs 112-115)
hx_delete=f"/mice-cards/{card.id}",  # No confirm, targets self
hx_delete=f"/try-cards/{card.id}",   # Has confirm, targets body
```

**Refactor**:
```python
# components.py or new htmx_helpers.py
def htmx_edit_attrs(entity: str, id: int):
    return {
        "hx_get": f"/{entity}-edit/{id}",
        "hx_target": f"#{entity}-card-{id}",
        "hx_swap": "outerHTML"
    }

def htmx_delete_attrs(entity: str, id: int, confirm: str = None):
    attrs = {
        "hx_delete": f"/{entity}-cards/{id}",
        "hx_target": f"#{entity}-card-{id}",
        "hx_swap": "outerHTML"
    }
    if confirm:
        attrs["hx_confirm"] = confirm
    return attrs

# Usage
air.Button("Edit", class_="...", **htmx_edit_attrs("mice", card.id))
```

**Impact**:
- **Benefit**: Enforces consistent HTMX behavior; reduces ~40 lines of boilerplate
- **Cost**: Medium - requires updating 15+ button/form definitions; may need conditional logic for edge cases
- **Risk**: Medium - HTMX targeting is subtle; bugs could break UI interactions silently

**Priority**: Low - Current inconsistency is likely intentional (different UX needs). Only refactor after establishing clear HTMX conventions. Risk outweighs benefit unless targeting bugs appear.

---

## 7. Move Template Data to JSON/YAML

**Location**: `templates.py:7-161`

**Issue**: 150+ lines of Python dictionaries for story templates. This is configuration data, not logic, but stored in code.

**Refactor**:
- Move to `templates.json` or `templates.yaml`
- Load via `json.load()` or `yaml.safe_load()` at startup
- Keep `templates.py` minimal:
  ```python
  import json
  from pathlib import Path

  TEMPLATES = json.loads(Path("templates.json").read_text())
  ```

**Impact**:
- **Benefit**: Non-developers can edit templates; cleaner separation of data/code; easier bulk editing
- **Cost**: Low - straightforward data extraction
- **Risk**: Very low - no logic changes

**Priority**: Low - Current Python format is acceptable for developer-maintained templates. Only refactor if non-technical users need to edit templates or if adding 5+ more templates.

---

## 8. Type Hint Constants and Functions in components.py

**Location**: `components.py:7-36` (constants), various functions

**Issue**: Constants `MICE_TOOLTIPS`, `MICE_COLORS`, `TRY_TOOLTIPS`, `TRY_COLORS` lack type hints. Some functions have incomplete return type annotations.

**Refactor**:
```python
from typing import Final

MICE_TOOLTIPS: Final[dict[str, str]] = {
    "M": "Milieu: Story about a place...",
    ...
}

MICE_COLORS: Final[dict[str, str]] = {
    "M": "bg-blue-100 border-blue-300",
    ...
}

# Function return types
def render_mice_card(card: MiceCard) -> air.Div:
    ...

def render_nesting_diagram(mice_cards: list[MiceCard]) -> air.Div | air.Div:
    ...
```

**Impact**:
- **Benefit**: Improves IDE autocomplete; catches type errors at development time; self-documenting code
- **Cost**: Very low - just add annotations
- **Risk**: Very low

**Priority**: High - Aligns with stated code quality guidelines ("Always use type hints"). Quick win for code clarity. Should have been done initially.

---

## 9. Consolidate Color Mapping Logic

**Location**: `components.py:23-36`, `components.py:73`, `components.py:119`, `components.py:151`

**Issue**: `MICE_COLORS` and `TRY_COLORS` dicts accessed directly throughout. Color selection logic duplicated when cards are rendered. Color string manipulation (e.g., `replace('bg-', 'border-')`) done inline.

**Refactor**:
```python
# components.py
from dataclasses import dataclass

@dataclass
class CardColors:
    bg: str
    border: str

    @property
    def full(self) -> str:
        return f"bg-{self.bg} border-{self.border}"

    @property
    def border_only(self) -> str:
        return f"border-{self.border}"

MICE_COLORS_NEW: Final[dict[str, CardColors]] = {
    "M": CardColors("blue-100", "blue-300"),
    "I": CardColors("green-100", "green-300"),
    "C": CardColors("yellow-100", "yellow-300"),
    "E": CardColors("purple-100", "purple-300")
}

# Usage
class_=f"card border-2 p-3 {MICE_COLORS_NEW[card.code].full}"
class_=f"border-l-4 pl-2 {MICE_COLORS_NEW[card.code].border_only}"
```

**Impact**:
- **Benefit**: Eliminates fragile string manipulation; centralized color logic; easier to add color variants (hover, active, etc.)
- **Cost**: Medium - requires updating all color access sites (~6 locations); adds abstraction
- **Risk**: Low - purely structural, but color rendering is user-visible

**Priority**: Very Low - Current approach works fine for static colors. Only refactor if adding dynamic theming, color variants, or if string manipulation bugs appear. The abstraction adds complexity without clear payoff.

---

## 10. Extract Database Engine/URL Configuration

**Location**: `main.py:12-13`, `main.py:15-16`, `main.py:19`

**Issue**: Database setup logic mixed with route definitions. `DATABASE_URL` hardcoded; no environment variable support.

**Refactor**:
```python
# config.py
import os
from sqlmodel import create_engine, SQLModel

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///story_builder.db")
engine = create_engine(DATABASE_URL, echo=bool(os.getenv("DB_ECHO", False)))

def init_db():
    SQLModel.metadata.create_all(engine)

# main.py
from config import engine, init_db

init_db()
app = air.Air()
...
```

**Impact**:
- **Benefit**: Enables environment-specific config (dev/prod databases); follows 12-factor app principles; cleaner main.py
- **Cost**: Low - straightforward extraction
- **Risk**: Very low

**Priority**: Medium - Good practice but not urgent. Only needed if deploying to multiple environments or switching database backends. Low cost makes it easy to do preemptively.

---

## Summary Prioritization

| Priority | Refactor | Lines Saved | Complexity | Urgency |
|----------|----------|-------------|------------|---------|
| **High** | #4 Template Modal | ~25 | Low | Likely to add templates |
| **High** | #8 Type Hints | 0 (adds) | Very Low | Stated requirement |
| **Medium** | #1 CSS Classes | ~10 | Low | If UI changes planned |
| **Medium** | #5 Card Fields | ~15 | Very Low | If extending cards |
| **Medium** | #10 DB Config | ~5 | Low | Good practice |
| **Low** | #2 Form Builder | ~50 | Medium | Only if adding forms |
| **Low** | #3 Session Management | ~30 | High | Only if complex needs |
| **Low** | #6 HTMX Helpers | ~40 | Medium | Risk > benefit |
| **Low** | #7 Template JSON | 0 (moves) | Low | Only if non-devs edit |
| **Very Low** | #9 Color Objects | ~5 | Medium | Premature abstraction |

**Recommended Action**:
1. **Do now**: #4 (template modal) and #8 (type hints) - low effort, clear benefit
2. **Consider**: #10 (config) if deploying, #1 (CSS) if restyling
3. **Skip**: #3, #6, #9 unless specific problems arise
