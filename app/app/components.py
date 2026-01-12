"""UI components for rendering MICE cards, Try/Fail cards, and story structure visualizations."""

import air
from models import MiceCard, TryCard

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
            air.Span(icon, class_="font-bold"),
            air.Span(text),
            class_=f"mb-2 text-sm {extra_class}"
        )

    return air.Div(
        air.Div(
            air.Span(f"{card.code}", class_="text-lg font-bold tooltip tooltip-right", data_tip=MICE_TOOLTIPS.get(card.code, "")),
            air.Span(f" Level {card.nesting_level}", class_="text-sm"),
            class_="mb-2"
        ),
        info_span("↓ ", card.opening),
        info_span("↑ ", card.closing),
        air.Div(
            air.Button(
                "Edit",
                class_="btn btn-xs btn-primary mr-1",
                hx_get=f"/mice-edit/{card.id}",
                hx_target=f"#mice-card-{card.id}",
                hx_swap="outerHTML"
            ),
            air.Button(
                "Delete",
                class_="btn btn-xs btn-error",
                hx_delete=f"/mice-cards/{card.id}",
                hx_target=f"#mice-card-{card.id}",
                hx_swap="outerHTML"
            ),
            class_="mt-2"
        ),
        class_=f"card border-2 p-3 {MICE_COLORS[card.code]}",
        style="height: auto; min-height: 200px;",
        id=f"mice-card-{card.id}"
    )


def render_try_card(card: TryCard):
    """Render a single Try/Fail card with attempt, failure, consequence, and controls."""
    return air.Div(
        air.Div(
            air.Span(f"{card.type} #{card.order_num}", class_="font-bold tooltip", data_tip=TRY_TOOLTIPS.get(card.type, "")),
            class_="mb-2"
        ),
        air.Div(
            air.Span("Attempt: ", class_="font-bold text-xs"),
            air.Span(card.attempt, class_="text-xs"),
            class_="mb-1"
        ),
        air.Div(
            air.Span("Failure: ", class_="font-bold text-xs"),
            air.Span(card.failure, class_="text-xs"),
            class_="mb-1"
        ),
        air.Div(
            air.Span("Consequence: ", class_="font-bold text-xs"),
            air.Span(card.consequence, class_="text-xs"),
            class_="mb-2"
        ),
        air.Div(
            air.Button(
                "Edit",
                class_="btn btn-xs btn-primary mr-2",
                hx_get=f"/try-edit/{card.id}",
                hx_target=f"#try-card-{card.id}",
                hx_swap="outerHTML"
            ),
            air.Button(
                "Delete",
                class_="btn btn-xs btn-error",
                hx_delete=f"/try-cards/{card.id}",
                hx_target="body",
                hx_swap="outerHTML",
                hx_confirm="Are you sure you want to delete this Try card?"
            ),
            class_="flex gap-2"
        ),
        class_=f"card border-2 p-3 {TRY_COLORS[card.type]}",
        style="height: auto; max-height: 250px; overflow-auto;",
        id=f"try-card-{card.id}"
    )


def render_nesting_diagram(mice_cards):
    """Render nested boxes showing MICE card structure by nesting level."""
    if not mice_cards:
        return air.Div("No MICE cards to display", class_="text-gray-500 italic")

    # Sort by nesting level
    sorted_cards = sorted(mice_cards, key=lambda c: c.nesting_level)

    def render_nested_card(card, level):
        """Render a single card with appropriate nesting indentation."""
        indent = (level - 1) * 20  # 20px per level
        return air.Div(
            air.Div(
                air.Span(f"{card.code}", class_=f"font-bold mr-2"),
                air.Span(f"Level {card.nesting_level}", class_="text-xs"),
                class_="mb-1"
            ),
            air.Div(
                air.Span("↓ ", class_="text-green-600 font-bold"),
                air.Span(card.opening, class_="text-xs"),
                class_="mb-1"
            ),
            air.Div(
                air.Span("↑ ", class_="text-purple-600 font-bold"),
                air.Span(card.closing, class_="text-xs"),
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
            air.Span(f"{card.code}: ", class_="font-bold"),
            air.Span(card.opening, class_="text-sm")
        )
        for card in sorted_mice
    ]

    # Act 2: Try/Fail cycles with all fields
    act2_items = [
        air.Li(
            air.Div(
                air.Span(f"{card.type} #{card.order_num}", class_="font-bold text-sm"),
                class_="mb-1"
            ),
            air.Div(
                air.Span("Attempt: ", class_="font-bold text-xs"),
                air.Span(card.attempt, class_="text-xs"),
                class_="mb-1"
            ),
            air.Div(
                air.Span("Failure: ", class_="font-bold text-xs"),
                air.Span(card.failure, class_="text-xs"),
                class_="mb-1"
            ),
            air.Div(
                air.Span("Consequence: ", class_="font-bold text-xs"),
                air.Span(card.consequence, class_="text-xs")
            ),
            class_="mb-3"
        )
        for card in sorted_tries
    ]

    # Act 3: MICE closings in reverse order
    act3_items = [
        air.Li(
            air.Span(f"{card.code}: ", class_="font-bold"),
            air.Span(card.closing, class_="text-sm")
        )
        for card in reversed(sorted_mice)
    ]

    return air.Div(
        air.Div(
            air.H4("Act 1: Setup", class_="font-bold text-green-700 mb-2"),
            air.Ul(*act1_items, class_="list-disc list-inside space-y-1") if act1_items else air.P("No openings", class_="text-gray-500 italic text-sm"),
            class_="bg-green-50 p-3 rounded mb-3"
        ),
        air.Div(
            air.H4("Act 2: Confrontation", class_="font-bold text-blue-700 mb-2"),
            air.Ul(*act2_items, class_="list-disc list-inside space-y-1") if act2_items else air.P("No try/fail cycles", class_="text-gray-500 italic text-sm"),
            class_="bg-blue-50 p-3 rounded mb-3"
        ),
        air.Div(
            air.H4("Act 3: Resolution", class_="font-bold text-purple-700 mb-2"),
            air.Ul(*act3_items, class_="list-disc list-inside space-y-1") if act3_items else air.P("No closings", class_="text-gray-500 italic text-sm"),
            class_="bg-purple-50 p-3 rounded"
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
            class_="mb-2"
        ),
        air.Div(
            air.H3("MICE Quotient Story Structure", class_="text-xl font-bold mb-3"),
            air.P("The MICE Quotient is a plotting technique by Orson Scott Card, enhanced by Mary Robinette Kowal. Each letter represents a promise you make to your reader:", class_="mb-3"),
            air.Div(
                air.Div(
                    air.H4("M - Milieu", class_="font-bold text-lg mb-1 text-blue-700"),
                    air.P("Environment, setting, atmosphere", class_="text-sm mb-1"),
                    air.P("Example: Character enters a new world → explores → leaves", class_="text-xs italic text-gray-600"),
                    class_="bg-blue-100 border-l-4 border-blue-300 p-3 rounded"
                ),
                air.Div(
                    air.H4("I - Idea", class_="font-bold text-lg mb-1 text-green-700"),
                    air.P("Question, mystery", class_="text-sm mb-1"),
                    air.P("Example: A question is posed → investigated → answered", class_="text-xs italic text-gray-600"),
                    class_="bg-green-100 border-l-4 border-green-300 p-3 rounded"
                ),
                air.Div(
                    air.H4("C - Character", class_="font-bold text-lg mb-1 text-yellow-700"),
                    air.P("Internal problems, goals, change", class_="text-sm mb-1"),
                    air.P("Example: Character is dissatisfied → struggles → transforms", class_="text-xs italic text-gray-600"),
                    class_="bg-yellow-100 border-l-4 border-yellow-300 p-3 rounded"
                ),
                air.Div(
                    air.H4("E - Event", class_="font-bold text-lg mb-1 text-purple-700"),
                    air.P("External problems, catastrophes", class_="text-sm mb-1"),
                    air.P("Example: World order disrupted → crisis → new order restored", class_="text-xs italic text-gray-600"),
                    class_="bg-purple-100 border-l-4 border-purple-300 p-3 rounded"
                ),
                class_="grid grid-cols-2 gap-3 mb-4"
            ),
            air.H4("Nesting Structure", class_="font-bold text-lg mb-2"),
            air.P("Act 1 mirrors Act 3 in opposite order - like boxes within boxes. Open them in order 1→2→3→4, then close them in reverse 4→3→2→1. This creates satisfying symmetry!", class_="mb-3 text-sm"),
            air.H4("Try/Fail Cycles (Act 2)", class_="font-bold text-lg mb-2"),
            air.P("Between setup and resolution, your character tries to achieve their goal and fails repeatedly. Each failure raises tension and makes the eventual success more satisfying. Common types:", class_="mb-2 text-sm"),
            air.Ul(
                air.Li("Success: Small win, but problem isn't solved", class_="text-sm"),
                air.Li("Failure: Clear setback", class_="text-sm"),
                air.Li("Trade-off: Win something, lose something else", class_="text-sm"),
                air.Li("Moral: Success but at a cost to character's values", class_="text-sm"),
                class_="list-disc list-inside mb-3"
            ),
            id="mice-help",
            class_="bg-base-200 p-4 rounded mb-4",
            style="display: none;"
        ),
        class_="mb-4"
    )
