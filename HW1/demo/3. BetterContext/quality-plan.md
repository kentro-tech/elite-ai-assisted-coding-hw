# Quality Plan: MICE Story Builder Testing Strategy

## Overview
This document outlines the plan for adding comprehensive testing to the MICE Story Builder application. The goal is to establish a solid test suite that validates existing functionality and helps discover any bugs in the current implementation.

## Current State Analysis

### Technology Stack
- **Backend**: FastAPI with `air` framework (Python-based UI library)
- **Frontend**: Server-rendered HTML with HTMX for dynamic interactions
- **Database**: SQLite with SQLModel ORM
- **Styling**: DaisyUI (Tailwind CSS components)

### Application Structure
```
app/
├── main.py          # FastAPI routes and HTMX endpoints
├── db.py            # Database CRUD operations
├── models.py        # SQLModel data models (MiceCard, TryCard)
├── components.py    # UI component rendering functions
├── forms.py         # Form builders for create/edit operations
├── layouts.py       # Page layout functions
├── templates.py     # Story templates data
└── story_builder.db # SQLite database file
```

### Core Features to Test
1. **MICE Cards**: Create, Read, Update, Delete operations
2. **Try/Fail Cards**: Create, Read, Update, Delete operations
3. **Templates**: Loading pre-built story templates
4. **Clear All**: Deleting all cards from database
5. **HTML Fragment Generation**: Endpoints return correct HTMX responses

---

## Testing Strategy

### Phase 1: Unit Tests for Database Layer (`db.py`)
**Goal**: Verify all database operations work correctly in isolation.

#### MICE Card Tests
- ✅ Create MICE card with all fields
- ✅ Retrieve all MICE cards
- ✅ Retrieve single MICE card by ID
- ✅ Update MICE card fields
- ✅ Delete MICE card by ID
- ✅ Handle non-existent card IDs gracefully

#### Try/Fail Card Tests
- ✅ Create Try card with all fields
- ✅ Retrieve all Try cards (verify ordering by order_num)
- ✅ Retrieve single Try card by ID
- ✅ Update Try card fields
- ✅ Delete Try card by ID
- ✅ Handle non-existent card IDs gracefully

#### Bulk Operations Tests
- ✅ Clear all cards (both types)
- ✅ Load template data (clear + bulk insert)
- ✅ Verify data persists after operations

**Approach**: 
- Use real SQLite test database file (`test_story_builder.db`)
- Create fresh database for each test via fixtures
- Simpler than in-memory - no mocking/patching needed!
- Better for learning - can inspect test database when debugging
- No dependencies on actual `story_builder.db` file

---

### Phase 2: Integration Tests for API Endpoints (`main.py`)
**Goal**: Verify HTTP endpoints return correct responses and HTML fragments.

#### MICE Card Endpoints
- `GET /` - Home page loads with all sections
- `GET /mice-form` - Returns create form HTML
- `POST /mice-cards` - Creates card and redirects
- `GET /mice-edit/{card_id}` - Returns edit form HTML
- `PUT /mice-cards/{card_id}` - Updates card and redirects
- `GET /mice-card/{card_id}` - Returns card display HTML
- `DELETE /mice-cards/{card_id}` - Deletes card

#### Try/Fail Card Endpoints
- `GET /try-form` - Returns create form HTML
- `POST /try-cards` - Creates card and redirects
- `GET /try-edit/{card_id}` - Returns edit form HTML
- `PUT /try-cards/{card_id}` - Updates card and returns HTML
- `GET /try-card/{card_id}` - Returns card display HTML
- `DELETE /try-cards/{card_id}` - Deletes card

#### Template & Utility Endpoints
- `POST /load-template/mystery` - Loads mystery template
- `POST /load-template/adventure` - Loads adventure template
- `POST /load-template/romance` - Loads romance template
- `POST /load-template/invalid` - Returns 404 for invalid template
- `POST /clear-data` - Clears all data and redirects
- `GET /clear-form` - Returns empty string (clears form)
- `GET /clear-try-form` - Returns empty string (clears form)

**Approach**:
- Use FastAPI `TestClient` for HTTP testing
- Use real test database file (simpler than mocking!)
- Temporarily swap engine in main.py for test duration
- Verify response status codes and HX-Redirect headers
- Basic HTML structure validation (not full DOM testing)

---

### Phase 3: Bug Discovery and Edge Cases
**Goal**: Find and document bugs through comprehensive testing.

#### Areas to Investigate
1. **Validation**: What happens with invalid/missing form data?
2. **Edge Cases**: 
   - Empty strings in required fields
   - Negative nesting levels
   - Duplicate order numbers in Try cards
   - Very long text inputs
3. **State Consistency**:
   - Deleting non-existent cards
   - Updating after deletion
   - Concurrent operations (if applicable)
4. **Template Loading**:
   - Loading template when cards already exist
   - Invalid template names
5. **HTML Generation**:
   - Cards render correctly with special characters
   - Empty card lists display properly
   - Tooltips contain correct text

**Documentation**: 
- Create `bugs-discovered.md` to track findings
- Write regression tests for each bug
- Categorize: Critical / Important / Minor

---

## Test Infrastructure

### Dependencies to Add
```toml
[project.dependencies]
pytest = "^8.0.0"
pytest-cov = "^5.0.0"
```

### Directory Structure
```
app/
├── tests/
│   ├── __init__.py
│   ├── conftest.py           # Shared fixtures
│   ├── test_db.py            # Unit tests for db.py
│   ├── test_api_mice.py      # Integration tests for MICE endpoints
│   ├── test_api_try.py       # Integration tests for Try endpoints
│   ├── test_api_templates.py # Integration tests for templates
│   └── test_edge_cases.py    # Edge case and bug regression tests
```

### Key Fixtures (in `conftest.py`)

```python
@pytest.fixture
def test_engine():
    """Create real SQLite test database file for testing.
    Cleaned up automatically after each test."""
    
@pytest.fixture
def test_session(test_engine):
    """Create database session with fresh tables."""
    
@pytest.fixture
def sample_mice_card():
    """Sample MICE card data for testing."""
    
@pytest.fixture
def sample_try_card():
    """Sample Try card data for testing."""
    
@pytest.fixture
def test_client(test_engine):
    """FastAPI TestClient with test database.
    Simple approach - just swap the engine!"""
```

---

## Success Criteria

### Must Have ✅
- [ ] All unit tests for `db.py` pass
- [ ] All integration tests for endpoints pass
- [ ] Test coverage > 80% for `db.py` and `main.py`
- [ ] Tests run via `uv run pytest` 
- [ ] Tests use isolated test database file
- [ ] At least 3 bugs discovered and documented
- [ ] Test database files added to `.gitignore`

### Nice to Have 🎯
- [ ] Coverage report generated with `pytest-cov`
- [ ] Tests for component rendering (`components.py`, `forms.py`)
- [ ] Tests complete in < 5 seconds
- [ ] Clear test naming convention (test_should_X_when_Y)

---

## Execution Plan

### Step 1: Setup (30 min)
1. ✅ Add pytest and pytest-cov to pyproject.toml
2. ✅ Create `tests/` directory structure
3. ✅ Write `conftest.py` with database fixtures
4. ✅ Write one simple test to verify setup works

### Step 2: Database Unit Tests (1-2 hours)
1. ✅ Test MICE card CRUD operations (6 tests)
2. ✅ Test Try card CRUD operations (6 tests)
3. ✅ Test bulk operations (3 tests)
4. ✅ Run tests and verify all pass

### Step 3: API Integration Tests (2-3 hours)
1. ✅ Test MICE card endpoints (7 tests)
2. ✅ Test Try card endpoints (6 tests)
3. ✅ Test template loading (4 tests)
4. ✅ Test utility endpoints (3 tests)
5. ✅ Run tests and fix any failures

### Step 4: Bug Discovery (1-2 hours)
1. ✅ Test edge cases and invalid inputs
2. ✅ Document bugs in `bugs-discovered.md`
3. ✅ Write regression tests for bugs found
4. ✅ Decide which bugs to fix vs document

### Step 5: Documentation (30 min)
1. ✅ Update README with test running instructions
2. ✅ Generate coverage report
3. ✅ Document any known limitations

**Total Estimated Time**: 5-8 hours

---

## Commands Reference

```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run specific test file
uv run pytest tests/test_db.py

# Run with coverage report
uv run pytest --cov=app --cov-report=html

# Run tests matching pattern
uv run pytest -k "test_mice"

# Stop on first failure
uv run pytest -x

# Show print statements
uv run pytest -s
```

---

## Learning Goals Alignment

This testing approach helps you learn:

1. **Pytest Fundamentals**: Fixtures, parametrize, assertions
2. **Database Testing**: Isolation, fixtures, test database files
3. **API Testing**: TestClient, status codes, headers
4. **Test-Driven Debugging**: Using tests to find bugs, inspecting test database
5. **Test Organization**: Structure for maintainability
6. **Coverage Analysis**: Understanding what's tested vs not
7. **Practical Testing**: Real database files vs in-memory trade-offs

---

## Notes

- **Real Database File**: Using actual SQLite file instead of in-memory for simplicity and debuggability
- **No Complex Mocking**: Simple engine swap - easier to understand and maintain
- **No Frontend Testing**: HTMX behavior tested via endpoint responses only
- **Incremental Approach**: Each test builds on previous understanding
- **Bug-First Mindset**: Tests should catch issues, not just pass
- **Learning-Friendly**: Can open `test_story_builder.db` to debug test failures

---

## Open Questions / Decisions Needed

1. Should we test the `components.py` rendering functions directly, or only through endpoints?
2. Do we need tests for `templates.py` constant data?
3. Should we fix bugs we find, or just document them?
4. What's the priority: coverage percentage or bug discovery?

---

**Status**: Ready for review and approval before implementation.

