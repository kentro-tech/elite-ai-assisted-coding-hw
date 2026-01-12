import air

def story_builder_layout(*children):
    """Custom layout for Story Builder app."""
    # Separate head and body content
    head_tags = air.layouts.filter_head_tags(children)
    body_tags = air.layouts.filter_body_tags(children)

    # Build custom structure
    return air.Html(
        air.Head(
            air.Meta(charset="utf-8"),
            air.Meta(name="viewport", content="width=device-width, initial-scale=1"),
            air.Link(href="https://cdn.jsdelivr.net/npm/daisyui@latest/dist/full.css", rel="stylesheet", type="text/css"),
            air.Script(src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"),
            air.Script(
                src="https://unpkg.com/htmx.org@2.0.7"
            ),
            *head_tags
        ),
        air.Body(
            air.Main(
                *body_tags,
                class_="min-h-screen bg-base-200 p-4"
            ),
            data_theme = 'light'
        )
    ).render()
