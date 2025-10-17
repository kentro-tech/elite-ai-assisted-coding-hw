# MICE Story Builder - BetterContext Version

## How to run

1. Set up python
2. Install [uv](https://docs.astral.sh/uv/getting-started/installation/)
3. `cd` into the app directory and run with `uv run fastapi dev`

## Running Tests

This project has comprehensive test coverage (96%!) with 83 automated tests.

### Quick Start

```bash
# Run all tests
cd app
uv run pytest

# Run with verbose output
uv run pytest -v

# Run specific test file
uv run pytest tests/test_db.py
uv run pytest tests/test_api_mice.py

# Run with coverage report
uv run pytest --cov=. --cov-report=term --cov-report=html

# View HTML coverage report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

### Test Organization

- **`tests/test_setup.py`** - Basic setup verification (6 tests)
- **`tests/test_db.py`** - Database CRUD operations (22 tests)
- **`tests/test_api_mice.py`** - MICE card API endpoints (14 tests)
- **`tests/test_api_try.py`** - Try card API endpoints (11 tests)
- **`tests/test_api_templates.py`** - Template loading & utilities (9 tests)
- **`tests/test_edge_cases.py`** - Edge cases & bug discovery (21 tests)

### Coverage Results

- **Overall**: 96% coverage
- **db.py**: 100% ✅
- **main.py**: 98% ✅
- **components.py**: 100% ✅
- **forms.py**: 100% ✅
- **models.py**: 100% ✅

### Bugs Discovered

We found 8 bugs through systematic testing! See [`bugs-discovered.md`](bugs-discovered.md) for details:
- 1 Critical (Security - XSS vulnerability)
- 3 Important (Invalid codes, duplicate orders)
- 4 Minor (Empty fields, negative numbers, long text)

### Test Documentation

- **Testing Strategy**: See [`quality-plan.md`](quality-plan.md)
- **Progress Tracking**: See [`quality-todos.md`](quality-todos.md)
- **Bugs Found**: See [`bugs-discovered.md`](bugs-discovered.md)

## Context Gathering

I did everything from the `2. Requirements` version.  As a reminder, that's this:

1. I used voicepal to transcribe my thoughts for the app.  
2. I then gave that to copilot (GPT-5) and asked it to ask me questions that it would need to know to create a requirements plan based on that.  
3. I then transcribed more.  
4. I asked claude 4.5 to put that into a plan. 
5. I read it and saw it misunderstood the structure
6. I found a blog post about it that I liked, and used the Jina AI reader to conver to markdown
7. I used that as context to improve the plan

Then I also added these additional steps for this better context version:

1. Added playwright MCP server.
2. Added git MCP server for air.
3. Gave some details on how to use tools and files in the AGENTS.md
4. Decided to use claude code for parts of it, made a symlink from `CLAUDE.md` to `AGENTS.md` so I didn't have to have duplicate context
5. Turned `plan.md` into a step by step progression I could work through one at a time.
6. Had the agent complete 1 todo at a time, checking and screenshotting with playwright.  I reviewed code before committing, then moved to each todo
7. Once all done did another refactoring pass.  Starting with creating a `refactor.md`, then went through every line of code manually for review and edits.

## Adding MCP Servers

Each tool has a slightly different way.  For the two I used

### Claude Code

`claude mcp add playwright npx @playwright/mcp@latest`

`claude mcp add air-docs npx mcp-remote https://gitmcp.io/feldroy/air` 

### Github copilot

![](imgs/Vscode-AddMCP.png)

![](imgs/Vscode-playwright.png)
