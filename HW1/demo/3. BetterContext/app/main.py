import air
from fastapi import Form, Response, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from sqlmodel import SQLModel, Session, create_engine
from models import MiceCard, TryCard
from layouts import story_builder_layout
from templates import TEMPLATES
from components import render_mice_card, render_try_card, render_nesting_diagram, render_story_timeline, render_mice_help_panel
import db
from forms import mice_card_form, try_card_form
import hf_api

# Database setup
DATABASE_URL = "sqlite:///story_builder.db"
engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)

# Initialize database on startup
init_db()

app = air.Air()
app.mount("/static", StaticFiles(directory="static"), name="static")


def _templates_modal():
    """Render the story templates selection modal dialog."""
    return air.Dialog(
        air.Div(
            air.H3("Story Templates", class_="text-2xl font-bold mb-4"),
            air.P("Choose a template to get started with a pre-built story structure:", class_="mb-4"),
            air.Div(
                air.Button(
                    air.H4("🔍 Mystery", class_="text-xl font-bold mb-2"),
                    air.P("A detective investigates a murder in a small town", class_="text-sm"),
                    class_="btn btn-outline w-full text-left h-auto py-4 mb-3",
                    hx_post="/load-template/mystery",
                    hx_target="body",
                    hx_swap="outerHTML",
                    onclick="document.getElementById('templates-modal').close()"
                ),
                air.Button(
                    air.H4("🗺️ Adventure", class_="text-xl font-bold mb-2"),
                    air.P("A hero embarks on a quest to save their homeland", class_="text-sm"),
                    class_="btn btn-outline w-full text-left h-auto py-4 mb-3",
                    hx_post="/load-template/adventure",
                    hx_target="body",
                    hx_swap="outerHTML",
                    onclick="document.getElementById('templates-modal').close()"
                ),
                air.Button(
                    air.H4("💕 Romance", class_="text-xl font-bold mb-2"),
                    air.P("Two people find love against all odds", class_="text-sm"),
                    class_="btn btn-outline w-full text-left h-auto py-4 mb-3",
                    hx_post="/load-template/romance",
                    hx_target="body",
                    hx_swap="outerHTML",
                    onclick="document.getElementById('templates-modal').close()"
                ),
            ),
            air.Button(
                "Cancel",
                class_="btn btn-ghost mt-2",
                onclick="document.getElementById('templates-modal').close()"
            ),
            class_="modal-box"
        ),
        id="templates-modal",
        class_="modal"
    )


@app.get("/")
def index():
    with Session(engine) as session:
        mice_cards = db.get_all_mice_cards(session)
        try_cards = db.get_all_try_cards(session)

        return story_builder_layout(
            air.Title("Story Builder"),
            air.Div(
                air.Button(
                    "Templates",
                    class_="btn btn-sm btn-info mr-3",
                    onclick="document.getElementById('templates-modal').showModal()"
                ),
                air.Button(
                    "Test HuggingFace Connection",
                    class_="btn btn-sm btn-success mr-3",
                    hx_get="/test-hf-api",
                    hx_target="body",
                    hx_swap="outerHTML"
                ),
                air.Button(
                    "Clear All Data",
                    class_="btn btn-sm btn-error",
                    hx_post="/clear-data",
                    hx_target="body",
                    hx_swap="outerHTML",
                    hx_confirm="Are you sure you want to delete all cards? This cannot be undone."
                ),
                class_="mb-6 flex gap-3"
            ),
            _templates_modal(),
            render_mice_help_panel(),
            air.Div(
                air.Div(
                    air.H2("MICE Cards", class_="text-2xl font-bold mb-4"),
                    air.Button(
                        "Add MICE Card",
                        class_="btn btn-primary mb-3",
                        hx_get="/mice-form",
                        hx_target="#mice-form-container",
                        hx_swap="innerHTML"
                    ),
                    air.Div(id="mice-form-container"),
                    air.Div(
                        *[render_mice_card(card) for card in mice_cards],
                        class_="flex flex-col gap-3",
                        id="mice-cards-list"
                    ),
                    class_="border border-base-300 p-4"
                ),
                air.Div(
                    air.H2("Try/Fail Cycles", class_="text-2xl font-bold mb-4"),
                    air.Button(
                        "Add Try Card",
                        class_="btn btn-primary mb-3",
                        hx_get="/try-form",
                        hx_target="#try-form-container",
                        hx_swap="innerHTML"
                    ),
                    air.Div(id="try-form-container"),
                    air.Div(
                        *[render_try_card(card) for card in try_cards],
                        class_="flex flex-col gap-3",
                        id="try-cards-list"
                    ),
                    class_="border border-base-300 p-4"
                ),
                air.Div(
                    air.H2("Generated Outline", class_="text-2xl font-bold mb-4"),
                    air.H3("Nesting Structure", class_="text-lg font-semibold mb-2"),
                    render_nesting_diagram(mice_cards),
                    air.H3("Story Timeline", class_="text-lg font-semibold mb-2 mt-6"),
                    render_story_timeline(mice_cards, try_cards),
                    class_="border border-base-300 p-4"
                ),
                class_="grid grid-cols-3 gap-4 w-full"
            )
        )


@app.get("/mice-form")
def mice_form():
    return mice_card_form()

@app.get("/clear-form")
def clear_form():
    return ""

@app.get("/try-form")
def try_form():
    return try_card_form()

@app.get("/clear-try-form")
def clear_try_form():
    return ""

def _generate_try_card_icon(card_id: int, consequence_text: str):
    """Background task to generate icon for a Try card."""
    try:
        # Generate prompt from consequence text
        prompt = hf_api.generate_image_prompt(consequence_text, context="story consequence")
        
        # Generate the image
        image_bytes = hf_api.generate_icon_image(prompt)
        
        if image_bytes:
            # Save to database (overwrites the loading placeholder)
            with Session(engine) as session:
                card = db.get_try_card(session, card_id)
                if card:
                    card.consequence_icon = image_bytes
                    session.commit()
                    print(f"✅ Generated icon for Try card {card_id}")
        else:
            print(f"⚠️ Failed to generate icon for Try card {card_id}: No image data returned")
            
    except Exception as e:
        print(f"❌ Error generating icon for Try card {card_id}: {e}")


def _generate_mice_card_icons(card_id: int, opening_text: str, closing_text: str):
    """Background task to generate icons for a MICE card (both Act 1 and Act 3)."""
    try:
        # Generate Act 1 icon from opening text
        act1_prompt = hf_api.generate_image_prompt(opening_text, context="story opening")
        act1_image_bytes = hf_api.generate_icon_image(act1_prompt)
        
        if act1_image_bytes:
            with Session(engine) as session:
                card = db.get_mice_card(session, card_id)
                if card:
                    card.act1_icon = act1_image_bytes
                    session.commit()
                    print(f"✅ Generated Act 1 icon for MICE card {card_id}")
        else:
            print(f"⚠️ Failed to generate Act 1 icon for MICE card {card_id}: No image data returned")
        
        # Generate Act 3 icon from closing text
        act3_prompt = hf_api.generate_image_prompt(closing_text, context="story closing")
        act3_image_bytes = hf_api.generate_icon_image(act3_prompt)
        
        if act3_image_bytes:
            with Session(engine) as session:
                card = db.get_mice_card(session, card_id)
                if card:
                    card.act3_icon = act3_image_bytes
                    session.commit()
                    print(f"✅ Generated Act 3 icon for MICE card {card_id}")
        else:
            print(f"⚠️ Failed to generate Act 3 icon for MICE card {card_id}: No image data returned")
            
    except Exception as e:
        print(f"❌ Error generating icons for MICE card {card_id}: {e}")


@app.post("/try-cards")
def create_try_card(
    background_tasks: BackgroundTasks,
    type: str = Form(...),
    order_num: int = Form(...),
    attempt: str = Form(...),
    failure: str = Form(...),
    consequence: str = Form(...)
):
    with Session(engine) as session:
        card = db.create_try_card(session, type, order_num, attempt, failure, consequence)
        
        # Trigger async icon generation
        background_tasks.add_task(_generate_try_card_icon, card.id, consequence)

    return Response(status_code=200, headers={"HX-Redirect": "/"})


@app.post("/clear-data")
def clear_data():
    with Session(engine) as session:
        db.clear_all_cards(session)

    return Response(status_code=200, headers={"HX-Redirect": "/"})

@app.post("/load-template/{template_name}")
def load_template(template_name: str, background_tasks: BackgroundTasks):
    """Load a story template from templates.py into the database."""
    if template_name not in TEMPLATES:
        return Response(status_code=404, content=f"Template '{template_name}' not found")

    template = TEMPLATES[template_name]

    with Session(engine) as session:
        db.load_template_data(session, template["mice_cards"], template["try_cards"])
        
        # Trigger icon generation for all Try cards
        try_cards = db.get_all_try_cards(session)
        for card in try_cards:
            background_tasks.add_task(_generate_try_card_icon, card.id, card.consequence)
        
        # Trigger icon generation for all MICE cards
        mice_cards = db.get_all_mice_cards(session)
        for card in mice_cards:
            background_tasks.add_task(_generate_mice_card_icons, card.id, card.opening, card.closing)

    return Response(status_code=200, headers={"HX-Redirect": "/"})

@app.get("/api/mice-card-icon/{card_id}/{icon_type}")
def get_mice_card_icon(card_id: int, icon_type: str):
    """Serve the generated icon image for a MICE card from the database.
    
    Args:
        card_id: The ID of the MICE card
        icon_type: Either 'act1' or 'act3'
    """
    with Session(engine) as session:
        card = db.get_mice_card(session, card_id)
        if card:
            if icon_type == "act1" and card.act1_icon:
                return Response(content=card.act1_icon, media_type="image/png")
            elif icon_type == "act3" and card.act3_icon:
                return Response(content=card.act3_icon, media_type="image/png")
        # Return 404 if card or icon doesn't exist
        return Response(status_code=404)


@app.get("/api/mice-card-icon-element/{card_id}/{icon_type}")
def get_mice_card_icon_element(card_id: int, icon_type: str):
    """Return just the icon IMG element for polling updates.
    
    Args:
        card_id: The ID of the MICE card
        icon_type: Either 'act1' or 'act3'
    """
    with Session(engine) as session:
        card = db.get_mice_card(session, card_id)
        if not card:
            return Response(status_code=404)
        
        # Get the appropriate icon based on type
        icon_data = card.act1_icon if icon_type == "act1" else card.act3_icon
        
        # Check if it's the loading icon
        is_loading_icon = False
        if icon_data:
            try:
                with open("static/loading-icon.png", 'rb') as f:
                    loading_icon_bytes = f.read()
                is_loading_icon = (icon_data == loading_icon_bytes)
            except FileNotFoundError:
                pass
        
        # Build icon attributes - MICE cards are ~2x bigger than original placeholders (100px vs 48px)
        position_class = "top-2" if icon_type == "act1" else "bottom-2"
        icon_attrs = {
            "src": f"/api/mice-card-icon/{card.id}/{icon_type}",
            "class_": f"absolute {position_class} right-2 rounded-md border border-gray-300 object-cover",
            "alt": f"{icon_type.upper()} Icon",
            "style": "width: 100px; height: 100px;",
            "id": f"mice-icon-{icon_type}-{card.id}"
        }
        
        # If still loading, keep polling
        if is_loading_icon:
            icon_attrs["hx_get"] = f"/api/mice-card-icon-element/{card.id}/{icon_type}"
            icon_attrs["hx_trigger"] = "every 2s"
            icon_attrs["hx_swap"] = "outerHTML"
            print(f"🔄 Still loading {icon_type} icon, continuing to poll MICE card {card.id}")
        else:
            print(f"✅ Real {icon_type} icon ready for MICE card {card.id}, stopping poll")
        
        return air.Img(**icon_attrs)


@app.post("/api/mice-card-icon/{card_id}/generate")
def generate_mice_card_icons_endpoint(card_id: int, background_tasks: BackgroundTasks):
    """Manually trigger icon generation for a MICE card."""
    with Session(engine) as session:
        card = db.get_mice_card(session, card_id)
        if card:
            # Read the loading icon placeholder and save it immediately for both icons
            loading_icon_path = "static/loading-icon.png"
            try:
                with open(loading_icon_path, 'rb') as f:
                    loading_icon_bytes = f.read()
                card.act1_icon = loading_icon_bytes
                card.act3_icon = loading_icon_bytes
                session.commit()
                session.refresh(card)
            except FileNotFoundError:
                print(f"⚠️ Loading icon not found at {loading_icon_path}")
            
            # Trigger async icon generation (will overwrite the loading icons)
            background_tasks.add_task(_generate_mice_card_icons, card.id, card.opening, card.closing)
            # Return the card with the loading icons
            return render_mice_card(card)
        else:
            return Response(status_code=404)


@app.get("/mice-edit/{card_id}")
def mice_edit(card_id: int):
    with Session(engine) as session:
        card = db.get_mice_card(session, card_id)
        if not card:
            return ""
        return mice_card_form(card)

@app.get("/mice-card/{card_id}")
def mice_card(card_id: int):
    with Session(engine) as session:
        card = db.get_mice_card(session, card_id)
        if not card:
            return ""
        return render_mice_card(card)

@app.put("/mice-cards/{card_id}")
def update_mice_card(
    background_tasks: BackgroundTasks,
    card_id: int,
    code: str = Form(...),
    opening: str = Form(...),
    closing: str = Form(...),
    nesting_level: int = Form(...)
):
    with Session(engine) as session:
        # Get the old card to check if text changed
        old_card = db.get_mice_card(session, card_id)
        opening_changed = old_card.opening != opening
        closing_changed = old_card.closing != closing
        
        # Update the card
        card = db.update_mice_card(session, card_id, code, opening, closing, nesting_level)
        if not card:
            return ""
        
        # If text changed, regenerate icons
        if opening_changed or closing_changed:
            # Set loading icons immediately
            loading_icon_path = "static/loading-icon.png"
            try:
                with open(loading_icon_path, 'rb') as f:
                    loading_icon_bytes = f.read()
                if opening_changed:
                    card.act1_icon = loading_icon_bytes
                if closing_changed:
                    card.act3_icon = loading_icon_bytes
                session.commit()
            except FileNotFoundError:
                print(f"⚠️ Loading icon not found at {loading_icon_path}")
            
            # Trigger async icon generation
            background_tasks.add_task(_generate_mice_card_icons, card_id, opening, closing)

    return Response(status_code=200, headers={"HX-Redirect": "/"})

@app.delete("/mice-cards/{card_id}")
def delete_mice_card(card_id: int):
    with Session(engine) as session:
        db.delete_mice_card(session, card_id)
    return ""

@app.post("/mice-cards")
def create_mice_card(
    background_tasks: BackgroundTasks,
    code: str = Form(...),
    opening: str = Form(...),
    closing: str = Form(...),
    nesting_level: int = Form(...)
):
    with Session(engine) as session:
        card = db.create_mice_card(session, code, opening, closing, nesting_level)
        
        # Trigger async icon generation for both Act 1 and Act 3
        background_tasks.add_task(_generate_mice_card_icons, card.id, opening, closing)

    return Response(status_code=200, headers={"HX-Redirect": "/"})

@app.get("/try-edit/{card_id}")
def try_edit(card_id: int):
    with Session(engine) as session:
        card = db.get_try_card(session, card_id)
        if not card:
            return ""
        return try_card_form(card)

@app.get("/try-card/{card_id}")
def get_try_card(card_id: int):
    with Session(engine) as session:
        card = db.get_try_card(session, card_id)
        if not card:
            return ""
        return render_try_card(card)


@app.get("/try-cards/{card_id}")
def get_try_card_by_id(card_id: int):
    """Get a single Try card by ID (used for polling during icon generation)."""
    with Session(engine) as session:
        card = db.get_try_card(session, card_id)
        if not card:
            return ""
        return render_try_card(card)

@app.put("/try-cards/{card_id}")
def update_try_card(
    card_id: int,
    background_tasks: BackgroundTasks,
    type: str = Form(...),
    order_num: int = Form(...),
    attempt: str = Form(...),
    failure: str = Form(...),
    consequence: str = Form(...)
):
    with Session(engine) as session:
        # Get the old card to check if consequence changed
        old_card = db.get_try_card(session, card_id)
        old_consequence = old_card.consequence if old_card else None
        
        # Update the card
        card = db.update_try_card(session, card_id, type, order_num, attempt, failure, consequence)
        
        # Regenerate icon if consequence text changed
        if card and old_consequence != consequence:
            # Set loading icon first
            loading_icon_path = "static/loading-icon.png"
            try:
                with open(loading_icon_path, 'rb') as f:
                    card.consequence_icon = f.read()
                session.commit()
            except FileNotFoundError:
                print(f"⚠️ Loading icon not found at {loading_icon_path}")
            
            background_tasks.add_task(_generate_try_card_icon, card_id, consequence)
        
        if card:
            # Redirect to refresh the page and show the new order
            return Response(status_code=200, headers={"HX-Redirect": "/"})
    return ""

@app.delete("/try-cards/{card_id}")
def delete_try_card(card_id: int):
    with Session(engine) as session:
        db.delete_try_card(session, card_id)
    return Response(status_code=200, headers={"HX-Redirect": "/"})

@app.get("/api/try-card-icon/{card_id}")
def get_try_card_icon(card_id: int):
    """Serve the generated icon image for a Try card from the database."""
    with Session(engine) as session:
        card = db.get_try_card(session, card_id)
        if card and card.consequence_icon:
            return Response(content=card.consequence_icon, media_type="image/png")
        else:
            # Return 404 if no icon exists
            return Response(status_code=404)


@app.get("/api/try-card-icon-element/{card_id}")
def get_try_card_icon_element(card_id: int):
    """Return just the icon IMG element for polling updates."""
    with Session(engine) as session:
        card = db.get_try_card(session, card_id)
        if not card:
            return Response(status_code=404)
        
        # Check if it's the loading icon
        is_loading_icon = False
        if card.consequence_icon:
            try:
                with open("static/loading-icon.png", 'rb') as f:
                    loading_icon_bytes = f.read()
                is_loading_icon = (card.consequence_icon == loading_icon_bytes)
            except FileNotFoundError:
                pass
        
        # Build icon attributes
        icon_attrs = {
            "src": f"/api/try-card-icon/{card.id}",
            "class_": "absolute top-2 right-2 rounded-md border border-gray-300 object-cover",
            "alt": "Icon",
            "style": "width: 120px; height: 120px;",
            "id": f"try-icon-{card.id}"
        }
        
        # If still loading, keep polling
        if is_loading_icon:
            icon_attrs["hx_get"] = f"/api/try-card-icon-element/{card.id}"
            icon_attrs["hx_trigger"] = "every 2s"
            icon_attrs["hx_swap"] = "outerHTML"
            print(f"🔄 Still loading, continuing to poll card {card.id}")
        else:
            print(f"✅ Real icon ready for card {card.id}, stopping poll")
        
        return air.Img(**icon_attrs)


@app.post("/api/try-card-icon/{card_id}/generate")
def generate_try_card_icon_endpoint(card_id: int, background_tasks: BackgroundTasks):
    """Manually trigger icon generation for a Try card."""
    with Session(engine) as session:
        card = db.get_try_card(session, card_id)
        if card:
            # Read the loading icon placeholder and save it immediately
            loading_icon_path = "static/loading-icon.png"
            try:
                with open(loading_icon_path, 'rb') as f:
                    card.consequence_icon = f.read()
                session.commit()
                session.refresh(card)
            except FileNotFoundError:
                print(f"⚠️ Loading icon not found at {loading_icon_path}")
            
            # Trigger async icon generation (will overwrite the loading icon)
            background_tasks.add_task(_generate_try_card_icon, card.id, card.consequence)
            # Return the card with the loading icon
            return render_try_card(card)
        else:
            return Response(status_code=404)


@app.post("/try-cards/{card_id}/reorder")
def reorder_try_card(card_id: int, new_order: int = Form(...)):
    """Update the order of a Try card after drag and drop."""
    with Session(engine) as session:
        db.update_try_card_order(session, card_id, new_order)
    return Response(status_code=200, headers={"HX-Redirect": "/"})


@app.get("/test-hf-api")
def test_hf_api():
    """Test endpoint to verify HuggingFace API connection with live status updates."""
    return air.Html(
        air.Head(
            air.Title("Testing HuggingFace API"),
            air.Script(src="https://unpkg.com/htmx.org@1.9.10"),
        ),
        air.Body(
            air.Div(
                air.H1("HuggingFace API Connection Test", class_="text-3xl font-bold mb-6"),
                air.Div(
                    # Status container that will be updated via HTMX
                    air.Div(
                        air.Div(
                            air.Span("⏳", class_="text-4xl mr-3"),
                            air.Span("Testing HuggingFace API connection...", class_="text-xl"),
                            class_="flex items-center mb-4"
                        ),
                        air.Progress(class_="progress progress-primary w-full"),
                        id="status-container",
                        hx_get="/test-hf-api-run",
                        hx_trigger="load",
                        hx_swap="outerHTML"
                    ),
                    class_="card bg-base-200 p-8"
                ),
                class_="container mx-auto p-8 max-w-2xl"
            ),
            class_="min-h-screen bg-base-100"
        )
    )


@app.get("/test-hf-api-run")
def test_hf_api_run():
    """Actually run the HuggingFace API test and return results."""
    result = hf_api.test_api_connection()
    
    # Get API mode from result
    api_mode = result.get("api_mode", "Unknown")
    is_gradio = "Gradio" in api_mode
    
    # Check if it's a payment/credit error
    is_payment_error = "402" in result["message"] or "Payment Required" in result["message"]
    
    if result["success"]:
        status_icon = "✅"
        status_text = "Success!"
        status_class = "text-success"
        detail_class = "alert alert-success"
    elif is_payment_error:
        status_icon = "💳"
        status_text = "Payment Required"
        status_class = "text-warning"
        detail_class = "alert alert-warning"
    else:
        status_icon = "❌"
        status_text = "Failed"
        status_class = "text-error"
        detail_class = "alert alert-error"
    
    return air.Div(
        # Status header
        air.Div(
            air.Span(status_icon, class_="text-4xl mr-3"),
            air.Span(status_text, class_=f"text-2xl font-bold {status_class}"),
            class_="flex items-center mb-6"
        ),
        
        # API Mode indicator
        air.Div(
            air.Span("🔧 API Mode: ", class_="font-semibold"),
            air.Span(api_mode, class_="badge badge-lg badge-primary"),
            class_="mb-4"
        ),
        
        # Detailed message
        air.Div(
            air.Div(
                air.H3("Status Details:", class_="font-bold mb-2"),
                air.P(result["message"], class_="mb-4"),
                
                # Special message for payment errors or info about Gradio
                air.Div(
                    air.H4("💡 About HuggingFace APIs:", class_="font-bold mb-2"),
                    air.P(
                        "This application supports two API modes:",
                        class_="mb-2 font-semibold"
                    ),
                    air.Ul(
                        air.Li(
                            air.Span("🆓 Gradio API (Free): ", class_="font-semibold"),
                            "Uses public Gradio apps on HuggingFace Spaces. Free but may have rate limits. Set USE_GRADIO_API=true in .env"
                        ),
                        air.Li(
                            air.Span("💳 Inference API (Paid): ", class_="font-semibold"),
                            "Direct API access with HuggingFace Pro subscription or credits. Set USE_GRADIO_API=false in .env"
                        ),
                        class_="list-disc list-inside ml-4 space-y-2"
                    ),
                    air.P(
                        f"Currently using: {api_mode}",
                        class_="mt-3 font-semibold text-primary"
                    ) if not is_payment_error else air.Div(
                        air.P(
                            "To fix the payment error:",
                            class_="mt-3 font-semibold mb-1"
                        ),
                        air.Ul(
                            air.Li("Switch to Gradio API (free) by setting USE_GRADIO_API=true in .env, or"),
                            air.Li("Subscribe to HuggingFace Pro at https://huggingface.co/pricing"),
                            class_="list-disc list-inside ml-4"
                        )
                    ),
                    class_="mt-4 p-4 bg-base-300 rounded-lg"
                ) if (is_payment_error or result["success"]) else "",
                
                class_=f"{detail_class} shadow-lg"
            ),
            class_="mb-6"
        ),
        
        # Action buttons
        air.Div(
            air.A(
                "← Back to Story Builder",
                href="/",
                class_="btn btn-primary"
            ),
            air.Button(
                "🔄 Test Again",
                onclick="window.location.reload()",
                class_="btn btn-secondary ml-2"
            ),
            class_="flex gap-2"
        ),
        
        id="status-container"
    )

