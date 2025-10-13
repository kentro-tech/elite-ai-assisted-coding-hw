"""Form builders for MICE and Try/Fail cards."""

import air
from models import MiceCard, TryCard
from components import MICE_COLORS
from styles import BUTTON_STYLES, FORM_STYLES, SPACING_STYLES, CONTAINER_STYLES


def _form_field(label: str, input_element):
    """Helper to create a labeled form field."""
    return air.Div(
        air.Label(label, class_=FORM_STYLES["label"]),
        input_element,
        class_=FORM_STYLES["control"]
    )


def _mice_edit_form(card: MiceCard) -> air.Form:
    """Build edit form for MICE card."""
    return air.Form(
        _form_field(
            "Type:",
            air.Select(
                air.Option("Milieu", value="M", selected=(card.code == "M")),
                air.Option("Idea", value="I", selected=(card.code == "I")),
                air.Option("Character", value="C", selected=(card.code == "C")),
                air.Option("Event", value="E", selected=(card.code == "E")),
                name="code",
                class_=f"{FORM_STYLES['select']} mb-1"
            )
        ),
        _form_field(
            "Opening:",
            air.Textarea(
                card.opening,
                name="opening",
                class_=f"{FORM_STYLES['textarea']} mb-1",
                rows="2"
            )
        ),
        _form_field(
            "Closing:",
            air.Textarea(
                card.closing,
                name="closing",
                class_=f"{FORM_STYLES['textarea']} mb-1",
                rows="2"
            )
        ),
        _form_field(
            "Nesting Level:",
            air.Input(
                type="number",
                name="nesting_level",
                value=str(card.nesting_level),
                class_=f"{FORM_STYLES['input']} mb-1"
            )
        ),
        air.Button(
            "Save",
            type="submit",
            class_=f"{BUTTON_STYLES['success_xs']} {SPACING_STYLES['mr_2']}"
        ),
        air.Button(
            "Cancel",
            type="button",
            class_=BUTTON_STYLES["ghost_xs"],
            hx_get=f"/mice-card/{card.id}",
            hx_target=f"#mice-card-{card.id}",
            hx_swap="outerHTML"
        ),
        hx_put=f"/mice-cards/{card.id}",
        hx_target=f"#mice-card-{card.id}",
        hx_swap="outerHTML",
        class_=f"card border-2 p-3 {MICE_COLORS[card.code]} overflow-auto",
        style="width: 100%; height: auto; min-height: 200px;",
        id=f"mice-card-{card.id}"
    )


def _mice_create_form() -> air.Form:
    """Build create form for MICE card."""
    return air.Form(
        air.Div(
            air.Label("Type:", class_=FORM_STYLES["label"]),
            air.Select(
                air.Option("Milieu", value="M"),
                air.Option("Idea", value="I"),
                air.Option("Character", value="C"),
                air.Option("Event", value="E"),
                name="code",
                class_=f"{FORM_STYLES['select']} {SPACING_STYLES['mb_2']}"
            ),
            class_=FORM_STYLES["control"]
        ),
        air.Div(
            air.Label("Opening:", class_=FORM_STYLES["label"]),
            air.Textarea(
                name="opening",
                class_=f"{FORM_STYLES['textarea']} {SPACING_STYLES['mb_2']}",
                rows="3"
            ),
            class_=FORM_STYLES["control"]
        ),
        air.Div(
            air.Label("Closing:", class_=FORM_STYLES["label"]),
            air.Textarea(
                name="closing",
                class_=f"{FORM_STYLES['textarea']} {SPACING_STYLES['mb_2']}",
                rows="3"
            ),
            class_=FORM_STYLES["control"]
        ),
        air.Div(
            air.Label("Nesting Level:", class_=FORM_STYLES["label"]),
            air.Input(
                type="number",
                name="nesting_level",
                value="1",
                class_=f"{FORM_STYLES['input']} {SPACING_STYLES['mb_2']}"
            ),
            class_=FORM_STYLES["control"]
        ),
        air.Button(
            "Save",
            type="submit",
            class_=f"{BUTTON_STYLES['success']} {SPACING_STYLES['mr_2']}"
        ),
        air.Button(
            "Cancel",
            type="button",
            class_=BUTTON_STYLES["ghost"],
            hx_get="/clear-form",
            hx_target="#mice-form-container",
            hx_swap="innerHTML"
        ),
        hx_post="/mice-cards",
        hx_target="body",
        hx_swap="outerHTML",
        class_=CONTAINER_STYLES["card"]
    )


def mice_card_form(card: MiceCard | None = None) -> air.Form:
    """Build MICE card form for create or edit."""
    if card is not None:
        return _mice_edit_form(card)
    else:
        return _mice_create_form()


def _try_edit_form(card: TryCard) -> air.Form:
    """Build edit form for Try card."""
    return air.Form(
        _form_field(
            "Type:",
            air.Select(
                air.Option("Success", value="Success", selected=(card.type == "Success")),
                air.Option("Failure", value="Failure", selected=(card.type == "Failure")),
                air.Option("Trade-off", value="Trade-off", selected=(card.type == "Trade-off")),
                air.Option("Moral", value="Moral", selected=(card.type == "Moral")),
                name="type",
                class_=FORM_STYLES["select_sm"]
            )
        ),
        _form_field(
            "Order #:",
            air.Input(
                type="number",
                name="order_num",
                value=str(card.order_num),
                class_=FORM_STYLES["input_sm"]
            )
        ),
        _form_field(
            "Attempt:",
            air.Textarea(
                card.attempt,
                name="attempt",
                class_=FORM_STYLES["textarea_sm"],
                rows="1"
            )
        ),
        _form_field(
            "Failure:",
            air.Textarea(
                card.failure,
                name="failure",
                class_=FORM_STYLES["textarea_sm"],
                rows="1"
            )
        ),
        _form_field(
            "Consequence:",
            air.Textarea(
                card.consequence,
                name="consequence",
                class_=FORM_STYLES["textarea_sm"],
                rows="1"
            )
        ),
        air.Div(
            air.Button(
                "Save",
                type="submit",
                class_=f"{BUTTON_STYLES['success_xs']} {SPACING_STYLES['mr_2']}"
            ),
            air.Button(
                "Cancel",
                type="button",
                class_=BUTTON_STYLES["ghost_xs"],
                hx_get=f"/try-card/{card.id}",
                hx_target=f"#try-card-{card.id}",
                hx_swap="outerHTML"
            ),
            class_=SPACING_STYLES["mt_2"]
        ),
        hx_put=f"/try-cards/{card.id}",
        hx_target=f"#try-card-{card.id}",
        hx_swap="outerHTML",
        class_="card bg-base-100 shadow-lg p-2",
        style="height: auto;",
        id=f"try-card-{card.id}"
    )


def _try_create_form() -> air.Form:
    """Build create form for Try card."""
    return air.Form(
        air.Div(
            air.Label("Cycle Type:", class_=FORM_STYLES["label"]),
            air.Select(
                air.Option("Success", value="Success"),
                air.Option("Failure", value="Failure"),
                air.Option("Trade-off", value="Trade-off"),
                air.Option("Moral", value="Moral"),
                name="type",
                class_=f"{FORM_STYLES['select']} {SPACING_STYLES['mb_2']}"
            ),
            class_=FORM_STYLES["control"]
        ),
        air.Div(
            air.Label("Order Number:", class_=FORM_STYLES["label"]),
            air.Input(
                type="number",
                name="order_num",
                value="1",
                class_=f"{FORM_STYLES['input']} {SPACING_STYLES['mb_2']}"
            ),
            class_=FORM_STYLES["control"]
        ),
        air.Div(
            air.Label("Attempt:", class_=FORM_STYLES["label"]),
            air.Textarea(
                name="attempt",
                class_=f"{FORM_STYLES['textarea']} {SPACING_STYLES['mb_2']}",
                rows="2"
            ),
            class_=FORM_STYLES["control"]
        ),
        air.Div(
            air.Label("Failure:", class_=FORM_STYLES["label"]),
            air.Textarea(
                name="failure",
                class_=f"{FORM_STYLES['textarea']} {SPACING_STYLES['mb_2']}",
                rows="2"
            ),
            class_=FORM_STYLES["control"]
        ),
        air.Div(
            air.Label("Consequence:", class_=FORM_STYLES["label"]),
            air.Textarea(
                name="consequence",
                class_=f"{FORM_STYLES['textarea']} {SPACING_STYLES['mb_2']}",
                rows="2"
            ),
            class_=FORM_STYLES["control"]
        ),
        air.Button(
            "Save",
            type="submit",
            class_=f"{BUTTON_STYLES['success']} {SPACING_STYLES['mr_2']}"
        ),
        air.Button(
            "Cancel",
            type="button",
            class_=BUTTON_STYLES["ghost"],
            hx_get="/clear-try-form",
            hx_target="#try-form-container",
            hx_swap="innerHTML"
        ),
        hx_post="/try-cards",
        hx_target="body",
        hx_swap="outerHTML",
        class_=CONTAINER_STYLES["card"]
    )


def try_card_form(card: TryCard | None = None) -> air.Form:
    """Build Try/Fail card form for create or edit."""
    if card is not None:
        return _try_edit_form(card)
    else:
        return _try_create_form()
