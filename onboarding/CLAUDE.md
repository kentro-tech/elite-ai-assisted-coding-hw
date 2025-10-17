# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an onboarding project for the Air framework - a Python web framework designed for building HTMX-powered applications. The project demonstrates the basics of Air with a simple web application.

## Running the Application

```bash
# Run the development server directly
python main.py

# Or use uv to run in the virtual environment
uv run python main.py
```

The server runs on `http://0.0.0.0:8000` by default.

## Air Framework Architecture

Air is a web framework that integrates seamlessly with HTMX for building interactive web applications without complex JavaScript.

### Route Structure

Routes are defined using decorators on the `app` instance:

```python
@app.get("/")          # HTTP GET requests
@app.post("/endpoint") # HTTP POST requests
def handler():
    return html_string  # Return HTML directly
```

### Key Components

- **Air instance**: The main `app = Air()` object that handles routing and requests
- **Decorators**: `@app.get()`, `@app.post()`, etc. for defining routes
- **Return values**: Functions return HTML strings that are sent to the browser
- **Server**: Uses `uvicorn` to run the ASGI application

### Frontend Stack

The application uses:
- **HTMX** (1.9.10): For dynamic HTML interactions without JavaScript
- **Pico CSS** (1.5.7): Classless CSS framework for styling

Both are loaded via CDN in the HTML templates.

## Project Structure

- `main.py`: Main application file containing the Air app and route definitions
- `pyproject.toml`: Project dependencies and metadata (requires Python 3.13+)
- `uv.lock`: Locked dependency versions (managed by uv)
- `.specstory/`: SpecStory CLI integration for tracking development sessions

## Dependencies

Main dependency: `air[standard]>=0.33.1`

This includes:
- The Air framework core
- FastAPI/Starlette (underlying ASGI framework)
- Uvicorn (ASGI server)
- Standard Air extras for common functionality

## Development Notes

When adding new routes:
1. Use the appropriate HTTP method decorator (`@app.get`, `@app.post`, etc.)
2. Return HTML strings directly from handler functions
3. HTMX attributes can be added to HTML elements for dynamic behavior
4. The server auto-reloads when running via uvicorn in development mode
