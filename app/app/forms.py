"""Form builders for MICE and Try/Fail cards."""

import air
from models import MiceCard, TryCard
from components import MICE_COLORS


def _form_field(label: str, input_element):
    """Helper to create a labeled form field."""
    return air.Div(
        air.Label(label, class_="label"),
        input_element,
        class_="form-control"
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
                class_="select select-bordered w-full mb-1"
            )
        ),
        _form_field(
            "Opening:",
            air.Textarea(
                card.opening,
                name="opening",
                class_="textarea textarea-bordered w-full mb-1",
                rows="2"
            )
        ),
        _form_field(
            "Closing:",
            air.Textarea(
                card.closing,
                name="closing",
                class_="textarea textarea-bordered w-full mb-1",
                rows="2"
            )
        ),
        _form_field(
            "Nesting Level:",
            air.Input(
                type="number",
                name="nesting_level",
                value=str(card.nesting_level),
                class_="input input-bordered w-full mb-1"
            )
        ),
        air.Button(
            "Save",
            type="submit",
            class_="btn btn-success btn-xs mr-2"
        ),
        air.Button(
            "Cancel",
            type="button",
            class_="btn btn-ghost btn-xs",
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
            air.Label("Type:", class_="label"),
            air.Select(
                air.Option("Milieu", value="M"),
                air.Option("Idea", value="I"),
                air.Option("Character", value="C"),
                air.Option("Event", value="E"),
                name="code",
                class_="select select-bordered w-full mb-2"
            ),
            class_="form-control"
        ),
        air.Div(
            air.Label("Opening:", class_="label"),
            air.Textarea(
                name="opening",
                class_="textarea textarea-bordered w-full mb-2",
                rows="3"
            ),
            class_="form-control"
        ),
        air.Div(
            air.Label("Closing:", class_="label"),
            air.Textarea(
                name="closing",
                class_="textarea textarea-bordered w-full mb-2",
                rows="3"
            ),
            class_="form-control"
        ),
        air.Div(
            air.Label("Nesting Level:", class_="label"),
            air.Input(
                type="number",
                name="nesting_level",
                value="1",
                class_="input input-bordered w-full mb-2"
            ),
            class_="form-control"
        ),
        air.Button(
            "Save",
            type="submit",
            class_="btn btn-success mr-2"
        ),
        air.Button(
            "Cancel",
            type="button",
            class_="btn btn-ghost",
            hx_get="/clear-form",
            hx_target="#mice-form-container",
            hx_swap="innerHTML"
        ),
        hx_post="/mice-cards",
        hx_target="body",
        hx_swap="outerHTML",
        class_="card bg-base-100 shadow-lg p-4 mb-3"
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
                class_="select select-bordered select-sm w-full"
            )
        ),
        _form_field(
            "Order #:",
            air.Input(
                type="number",
                name="order_num",
                value=str(card.order_num),
                class_="input input-bordered input-sm w-full"
            )
        ),
        _form_field(
            "Attempt:",
            air.Textarea(
                card.attempt,
                name="attempt",
                class_="textarea textarea-bordered textarea-sm w-full",
                rows="1"
            )
        ),
        _form_field(
            "Failure:",
            air.Textarea(
                card.failure,
                name="failure",
                class_="textarea textarea-bordered textarea-sm w-full",
                rows="1"
            )
        ),
        _form_field(
            "Consequence:",
            air.Textarea(
                card.consequence,
                name="consequence",
                class_="textarea textarea-bordered textarea-sm w-full",
                rows="1"
            )
        ),
        air.Div(
            air.Button(
                "Save",
                type="submit",
                class_="btn btn-success btn-xs mr-2"
            ),
            air.Button(
                "Cancel",
                type="button",
                class_="btn btn-ghost btn-xs",
                hx_get=f"/try-card/{card.id}",
                hx_target=f"#try-card-{card.id}",
                hx_swap="outerHTML"
            ),
            class_="mt-2"
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
            air.Label("Cycle Type:", class_="label"),
            air.Select(
                air.Option("Success", value="Success"),
                air.Option("Failure", value="Failure"),
                air.Option("Trade-off", value="Trade-off"),
                air.Option("Moral", value="Moral"),
                name="type",
                class_="select select-bordered w-full mb-2"
            ),
            class_="form-control"
        ),
        air.Div(
            air.Label("Order Number:", class_="label"),
            air.Input(
                type="number",
                name="order_num",
                value="1",
                class_="input input-bordered w-full mb-2"
            ),
            class_="form-control"
        ),
        air.Div(
            air.Label("Attempt:", class_="label"),
            air.Textarea(
                name="attempt",
                class_="textarea textarea-bordered w-full mb-2",
                rows="2"
            ),
            class_="form-control"
        ),
        air.Div(
            air.Label("Failure:", class_="label"),
            air.Textarea(
                name="failure",
                class_="textarea textarea-bordered w-full mb-2",
                rows="2"
            ),
            class_="form-control"
        ),
        air.Div(
            air.Label("Consequence:", class_="label"),
            air.Textarea(
                name="consequence",
                class_="textarea textarea-bordered w-full mb-2",
                rows="2"
            ),
            class_="form-control"
        ),
        air.Button(
            "Save",
            type="submit",
            class_="btn btn-success mr-2"
        ),
        air.Button(
            "Cancel",
            type="button",
            class_="btn btn-ghost",
            hx_get="/clear-try-form",
            hx_target="#try-form-container",
            hx_swap="innerHTML"
        ),
        hx_post="/try-cards",
        hx_target="body",
        hx_swap="outerHTML",
        class_="card bg-base-100 shadow-lg p-4 mb-3"
    )


def try_card_form(card: TryCard | None = None) -> air.Form:
    """Build Try/Fail card form for create or edit."""
    if card is not None:
        return _try_edit_form(card)
    else:
        return _try_create_form()
