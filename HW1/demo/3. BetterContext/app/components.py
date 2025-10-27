"""UI components for rendering MICE cards, Try/Fail cards, and story structure visualizations."""

import air
from models import MiceCard, TryCard
from styles import (
    BUTTON_STYLES, HEADING_STYLES, TEXT_STYLES, SPACING_STYLES,
    ACT_STYLES, LIST_STYLES, UTILITY_STYLES
)

# Tooltip content for MICE card types
MICE_TOOLTIPS = {
    "M": "Milieu: Story about a place/environment. Character enters → explores → leaves. Example: Alice falls down rabbit hole, explores Wonderland, returns home.",
    "I": "Idea: Story about a question/mystery. Question posed → investigated → answered. Example: Whodunit mystery starts with murder, detective investigates, reveals killer.",
    "C": "Character: Story about internal change. Character dissatisfied → struggles → transforms. Example: Scrooge is miserly, faces ghosts, becomes generous.",
    "E": "Event: Story about external problem. World order disrupted → crisis → new order. Example: Alien invasion threatens Earth, heroes fight back, peace restored."
}

# Tooltip content for Try/Fail cycle types
TRY_TOOLTIPS = {
    "Success": "Yes, but... - Character succeeds at immediate goal but the larger problem persists. Example: Hero defeats minion but villain escapes.",
    "Failure": "No, and... - Character fails and situation worsens. Example: Detective's suspect has alibi AND another murder occurs.",
    "Trade-off": "Yes, but at a cost - Character wins something but loses something else. Example: Hero saves city but loses their powers.",
    "Moral": "Success with ethical compromise - Character succeeds but violates their values. Example: Detective catches killer by breaking the law."
}

# Color classes for MICE card types
MICE_COLORS = {
    "M": "bg-blue-100 border-blue-300",
    "I": "bg-green-100 border-green-300",
    "C": "bg-yellow-100 border-yellow-300",
    "E": "bg-purple-100 border-purple-300"
}

# Color classes for Try/Fail cycle types
TRY_COLORS = {
    "Success": "bg-green-100 border-green-300",
    "Failure": "bg-red-100 border-red-300",
    "Trade-off": "bg-orange-100 border-orange-300",
    "Moral": "bg-blue-100 border-blue-300"
}


def render_mice_card(card: MiceCard):
    """Render a single MICE card with opening, closing, and controls."""
    def info_span(icon: str, text: str, extra_class: str = ""):
        return air.Div(
            air.Span(icon, class_=TEXT_STYLES["bold"]),
            air.Span(text),
            class_=f"{SPACING_STYLES['mb_2']} {TEXT_STYLES['small']} {extra_class}"
        )

    return air.Div(
        air.Div(
            air.Span(f"{card.code}", class_=f"text-lg {TEXT_STYLES['bold']} tooltip tooltip-right", data_tip=MICE_TOOLTIPS.get(card.code, "")),
            air.Span(f" Level {card.nesting_level}", class_=TEXT_STYLES["small"]),
            class_=SPACING_STYLES["mb_2"]
        ),
        info_span("↓ ", card.opening),
        info_span("↑ ", card.closing),
        air.Div(
            air.Button(
                "Edit",
                class_=f"{BUTTON_STYLES['primary_xs']} {SPACING_STYLES['mr_1']}",
                hx_get=f"/mice-edit/{card.id}",
                hx_target=f"#mice-card-{card.id}",
                hx_swap="outerHTML"
            ),
            air.Button(
                "Delete",
                class_=BUTTON_STYLES["error_xs"],
                hx_delete=f"/mice-cards/{card.id}",
                hx_target=f"#mice-card-{card.id}",
                hx_swap="outerHTML"
            ),
            class_=SPACING_STYLES["mt_2"]
        ),
        class_=f"card border-2 p-3 {MICE_COLORS[card.code]}",
        style="height: auto; min-height: 200px;",
        id=f"mice-card-{card.id}"
    )


def render_try_card(card: TryCard):
    """Render a single Try/Fail card with attempt, failure, consequence, and controls."""
    return air.Div(
        air.Div(
            air.Span(f"{card.type} #{card.order_num}", class_=f"{TEXT_STYLES['bold']} tooltip", data_tip=TRY_TOOLTIPS.get(card.type, "")),
            class_=SPACING_STYLES["mb_2"]
        ),
        air.Div(
            air.Span("Attempt: ", class_=f"{TEXT_STYLES['bold']} {TEXT_STYLES['extra_small']}"),
            air.Span(card.attempt, class_=TEXT_STYLES["extra_small"]),
            class_="mb-1"
        ),
        air.Div(
            air.Span("Failure: ", class_=f"{TEXT_STYLES['bold']} {TEXT_STYLES['extra_small']}"),
            air.Span(card.failure, class_=TEXT_STYLES["extra_small"]),
            class_="mb-1"
        ),
        air.Div(
            air.Span("Consequence: ", class_=f"{TEXT_STYLES['bold']} {TEXT_STYLES['extra_small']}"),
            air.Span(card.consequence, class_=TEXT_STYLES["extra_small"]),
            class_=SPACING_STYLES["mb_2"]
        ),
        air.Div(
            air.Button(
                "Edit",
                class_=f"{BUTTON_STYLES['primary_xs']} {SPACING_STYLES['mr_2']}",
                hx_get=f"/try-edit/{card.id}",
                hx_target=f"#try-card-{card.id}",
                hx_swap="outerHTML"
            ),
            air.Button(
                "Delete",
                class_=BUTTON_STYLES["error_xs"],
                hx_delete=f"/try-cards/{card.id}",
                hx_target="body",
                hx_swap="outerHTML",
                hx_confirm="Are you sure you want to delete this Try card?"
            ),
            class_=UTILITY_STYLES["flex_gap_2"]
        ),
        class_=f"card border-2 p-3 {TRY_COLORS[card.type]}",
        style="height: auto; max-height: 250px; overflow-auto;",
        id=f"try-card-{card.id}"
    )


def render_nesting_diagram(mice_cards):
    """Render nested boxes showing MICE card structure by nesting level."""
    if not mice_cards:
        return air.Div("No MICE cards to display", class_=UTILITY_STYLES["italic_gray"])

    # Sort by nesting level
    sorted_cards = sorted(mice_cards, key=lambda c: c.nesting_level)

    def render_nested_card(card, level):
        """Render a single card with appropriate nesting indentation."""
        indent = (level - 1) * 20  # 20px per level
        return air.Div(
            air.Div(
                air.Span(f"{card.code}", class_=f"{TEXT_STYLES['bold']} {SPACING_STYLES['mr_2']}"),
                air.Span(f"Level {card.nesting_level}", class_=TEXT_STYLES["extra_small"]),
                class_="mb-1"
            ),
            air.Div(
                air.Span("↓ ", class_=f"text-green-600 {TEXT_STYLES['bold']}"),
                air.Span(card.opening, class_=TEXT_STYLES["extra_small"]),
                class_="mb-1"
            ),
            air.Div(
                air.Span("↑ ", class_=f"text-purple-600 {TEXT_STYLES['bold']}"),
                air.Span(card.closing, class_=TEXT_STYLES["extra_small"]),
            ),
            class_=f"border-l-4 pl-2 mb-2 {MICE_COLORS[card.code].replace('bg-', 'border-')}",
            style=f"margin-left: {indent}px;"
        )

    return air.Div(
        *[render_nested_card(card, card.nesting_level) for card in sorted_cards],
        class_="bg-base-100 p-3 rounded"
    )


def render_story_timeline(mice_cards, try_cards):
    """Render three-act story timeline showing the complete narrative structure."""
    sorted_mice = sorted(mice_cards, key=lambda c: c.nesting_level)
    sorted_tries = sorted(try_cards, key=lambda c: c.order_num)

    # Act 1: MICE openings in nesting order
    act1_items = [
        air.Li(
            air.Span(f"{card.code}: ", class_=TEXT_STYLES["bold"]),
            air.Span(card.opening, class_=TEXT_STYLES["small"])
        )
        for card in sorted_mice
    ]

    # Act 2: Try/Fail cycles with all fields
    act2_items = [
        air.Li(
            air.Div(
                air.Span(f"{card.type} #{card.order_num}", class_=f"{TEXT_STYLES['bold']} {TEXT_STYLES['small']}"),
                class_="mb-1"
            ),
            air.Div(
                air.Span("Attempt: ", class_=f"{TEXT_STYLES['bold']} {TEXT_STYLES['extra_small']}"),
                air.Span(card.attempt, class_=TEXT_STYLES["extra_small"]),
                class_="mb-1"
            ),
            air.Div(
                air.Span("Failure: ", class_=f"{TEXT_STYLES['bold']} {TEXT_STYLES['extra_small']}"),
                air.Span(card.failure, class_=TEXT_STYLES["extra_small"]),
                class_="mb-1"
            ),
            air.Div(
                air.Span("Consequence: ", class_=f"{TEXT_STYLES['bold']} {TEXT_STYLES['extra_small']}"),
                air.Span(card.consequence, class_=TEXT_STYLES["extra_small"])
            ),
            class_=SPACING_STYLES["mb_3"]
        )
        for card in sorted_tries
    ]

    # Act 3: MICE closings in reverse order
    act3_items = [
        air.Li(
            air.Span(f"{card.code}: ", class_=TEXT_STYLES["bold"]),
            air.Span(card.closing, class_=TEXT_STYLES["small"])
        )
        for card in reversed(sorted_mice)
    ]

    return air.Div(
        air.Div(
            air.H4("Act 1: Setup", class_=ACT_STYLES["act1_header"]),
            air.Ul(*act1_items, class_=LIST_STYLES["disc_inside"]) if act1_items else air.P("No openings", class_=UTILITY_STYLES["italic_gray"]),
            class_=ACT_STYLES["act1"]
        ),
        air.Div(
            air.H4("Act 2: Confrontation", class_=ACT_STYLES["act2_header"]),
            air.Ul(*act2_items, class_=LIST_STYLES["disc_inside"]) if act2_items else air.P("No try/fail cycles", class_=UTILITY_STYLES["italic_gray"]),
            class_=ACT_STYLES["act2"]
        ),
        air.Div(
            air.H4("Act 3: Resolution", class_=ACT_STYLES["act3_header"]),
            air.Ul(*act3_items, class_=LIST_STYLES["disc_inside"]) if act3_items else air.P("No closings", class_=UTILITY_STYLES["italic_gray"]),
            class_=ACT_STYLES["act3"]
        ),
        class_="mt-4"
    )


def render_mice_help_panel():
    """Render the MICE Quotient educational help panel with collapsible toggle."""
    return air.Div(
        air.Div(
            air.Button(
                "📚 What is MICE Quotient?",
                class_="btn btn-sm btn-outline w-full text-left",
                onclick="const el = document.getElementById('mice-help'); el.style.display = el.style.display === 'none' ? 'block' : 'none';"
            ),
            class_=SPACING_STYLES["mb_2"]
        ),
        air.Div(
            air.H3("MICE Quotient Story Structure", class_=f"text-xl {TEXT_STYLES['bold']} {SPACING_STYLES['mb_3']}"),
            air.P("The MICE Quotient is a plotting technique by Orson Scott Card, enhanced by Mary Robinette Kowal. Each letter represents a promise you make to your reader:", class_=SPACING_STYLES["mb_3"]),
            air.Div(
                air.Div(
                    air.H4("M - Milieu", class_=f"{HEADING_STYLES['h4']} text-blue-700"),
                    air.P("Environment, setting, atmosphere", class_=f"{TEXT_STYLES['small']} mb-1"),
                    air.P("Example: Character enters a new world → explores → leaves", class_="text-xs italic text-gray-600"),
                    class_="bg-blue-100 border-l-4 border-blue-300 p-3 rounded"
                ),
                air.Div(
                    air.H4("I - Idea", class_=f"{HEADING_STYLES['h4']} text-green-700"),
                    air.P("Question, mystery", class_=f"{TEXT_STYLES['small']} mb-1"),
                    air.P("Example: A question is posed → investigated → answered", class_="text-xs italic text-gray-600"),
                    class_="bg-green-100 border-l-4 border-green-300 p-3 rounded"
                ),
                air.Div(
                    air.H4("C - Character", class_=f"{HEADING_STYLES['h4']} text-yellow-700"),
                    air.P("Internal problems, goals, change", class_=f"{TEXT_STYLES['small']} mb-1"),
                    air.P("Example: Character is dissatisfied → struggles → transforms", class_="text-xs italic text-gray-600"),
                    class_="bg-yellow-100 border-l-4 border-yellow-300 p-3 rounded"
                ),
                air.Div(
                    air.H4("E - Event", class_=f"{HEADING_STYLES['h4']} text-purple-700"),
                    air.P("External problems, catastrophes", class_=f"{TEXT_STYLES['small']} mb-1"),
                    air.P("Example: World order disrupted → crisis → new order restored", class_="text-xs italic text-gray-600"),
                    class_="bg-purple-100 border-l-4 border-purple-300 p-3 rounded"
                ),
                class_="grid grid-cols-2 gap-3 mb-4"
            ),
            air.H4("Nesting Structure", class_=f"{HEADING_STYLES['h4']} {SPACING_STYLES['mb_2']}"),
            air.P("Act 1 mirrors Act 3 in opposite order - like boxes within boxes. Open them in order 1→2→3→4, then close them in reverse 4→3→2→1. This creates satisfying symmetry!", class_=f"{SPACING_STYLES['mb_3']} {TEXT_STYLES['small']}"),
            air.H4("Try/Fail Cycles (Act 2)", class_=f"{HEADING_STYLES['h4']} {SPACING_STYLES['mb_2']}"),
            air.P("Between setup and resolution, your character tries to achieve their goal and fails repeatedly. Each failure raises tension and makes the eventual success more satisfying. Common types:", class_=f"{SPACING_STYLES['mb_2']} {TEXT_STYLES['small']}"),
            air.Ul(
                air.Li("Success: Small win, but problem isn't solved", class_=TEXT_STYLES["small"]),
                air.Li("Failure: Clear setback", class_=TEXT_STYLES["small"]),
                air.Li("Trade-off: Win something, lose something else", class_=TEXT_STYLES["small"]),
                air.Li("Moral: Success but at a cost to character's values", class_=TEXT_STYLES["small"]),
                class_=f"list-disc list-inside {SPACING_STYLES['mb_3']}"
            ),
            id="mice-help",
            class_=f"bg-base-200 p-4 rounded {SPACING_STYLES['mb_4']}",
            style="display: none;"
        ),
        class_=SPACING_STYLES["mb_4"]
    )
