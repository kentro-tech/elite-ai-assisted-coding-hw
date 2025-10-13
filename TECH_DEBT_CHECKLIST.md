# Tech Debt Reduction - Implementation Checklist

This checklist provides step-by-step instructions for implementing the tech debt recommendations from [TECH_DEBT_ANALYSIS.md](./TECH_DEBT_ANALYSIS.md).

## 📋 Phase 1: Quick Wins (1-2 hours total)

### ✅ Task 1.1: Add Type Hints to tzconverter (15 min)

**File:** `Wk1-RecordedLessonContents/tzconverter/main.py`

- [ ] Add return type to `generate_time_options()`
  ```python
  def generate_time_options() -> list[str]:
  ```

- [ ] Add explicit type to `times` variable
  ```python
  times: list[str] = []
  ```

- [ ] Verify types with mypy: `mypy Wk1-RecordedLessonContents/tzconverter/main.py`

**Acceptance:** All functions have complete type hints, mypy passes

---

### ✅ Task 1.2: Complete Type Hints in Demo 2 Database (15 min)

**File:** `HW1/demo/2. Requirements/app/database.py`

- [ ] Verify all function parameters have type hints
- [ ] Verify all function return types are specified
- [ ] Check that types match actual usage

**Current state check:**
```bash
grep "def " HW1/demo/2.\ Requirements/app/database.py
```

**Acceptance:** Every function parameter and return value has explicit type annotation

---

### ✅ Task 1.3: Add Docstrings to Demo 2 Functions (30 min)

**File:** `HW1/demo/2. Requirements/app/database.py`

For each function, add docstring explaining:
- What the function does (business purpose)
- Why it matters (domain context - MICE quotient)
- NOT implementation details (code is self-evident)

**Example:**
```python
def get_mice_cards(story_id: int = 1) -> List[Dict[str, Any]]:
    """Retrieve all MICE cards for a story, ordered by nesting level.
    
    MICE cards represent narrative structure elements (Milieu, Inquiry, 
    Character, Event) that open in Act 1 and close in Act 3 in nested order.
    Nesting level determines the opening/closing sequence.
    """
    # ... implementation
```

**Functions to document:**
- [ ] `get_db()`
- [ ] `init_db()`
- [ ] `get_mice_cards()`
- [ ] `get_try_cards()`
- [ ] `add_mice_card()`
- [ ] `add_try_card()`
- [ ] `update_mice_card()`
- [ ] `update_try_card()`
- [ ] `delete_mice_card()`
- [ ] `delete_try_card()`
- [ ] `clear_all_data()`

**Acceptance:** All database functions have clear docstrings explaining business purpose

---

## 📋 Phase 2: CSS Extraction (2-3 hours total)

### ✅ Task 2.1: Create CSS Files (30 min)

**Demo 2:**
- [ ] Create `HW1/demo/2. Requirements/app/static/styles.css`
- [ ] Update `main.py` to mount static files if not already done
- [ ] Verify static file serving works

**Demo 3:**
- [ ] Check if `static/` directory exists
- [ ] Create or expand `styles.css` file

---

### ✅ Task 2.2: Extract Inline Styles from Demo 2 Components (1 hour)

**File:** `HW1/demo/2. Requirements/app/components.py`

Inline styles found (use search: `style="`):

- [ ] Line ~23: `air.P(f"Opens: {opens}", style="font-style: italic;")`
  - Replace with: `class_="theory-opens"`
  - Add to CSS: `.theory-opens { font-style: italic; }`

- [ ] Line ~24: `air.P(f"Closes: {closes}", style="font-style: italic;")`
  - Replace with: `class_="theory-closes"`
  - Add to CSS: `.theory-closes { font-style: italic; }`

- [ ] Line ~25: `air.P(f"Example: {example}", style="color: #666;")`
  - Replace with: `class_="theory-example"`
  - Add to CSS: `.theory-example { color: #666; }`

- [ ] Search for remaining `style=` attributes:
  ```bash
  grep -n "style=" HW1/demo/2.\ Requirements/app/components.py
  ```

- [ ] Extract each to semantic CSS class

**Acceptance:** Zero `style=` attributes in components.py, all styles in CSS file

---

### ✅ Task 2.3: Extract Inline Styles from Demo 3 Components (1 hour)

**File:** `HW1/demo/3. BetterContext/app/components.py`

- [ ] Search for inline styles: `grep -n "style=" components.py`
- [ ] For each style attribute:
  1. Create semantic CSS class name
  2. Move style to CSS file
  3. Replace style= with class=
  
**Common patterns to extract:**
- Background colors for acts/sections
- Padding/margin values
- Border styles
- Any remaining inline styles

**Acceptance:** Zero inline `style=` attributes in any Python file

---

## 📋 Phase 3: JavaScript Cleanup (2-4 hours total)

### ✅ Task 3.1: Audit Inline JavaScript (30 min)

**Find all inline JavaScript:**
```bash
grep -rn "onclick=" HW1/demo/2.\ Requirements/app/
```

**Document findings:**
- [ ] List all `onclick=` handlers
- [ ] List all other inline JS (onchange, etc.)
- [ ] Determine which can use HTMX instead

---

### ✅ Task 3.2: Migrate Demo 2 to HTMX (Recommended) (2 hours)

**Why:** Demo 3 already uses HTMX successfully - proven pattern

**Steps:**

1. [ ] Add HTMX to Demo 2 if not present
   - Check if HTMX script tag exists in templates
   - Add if needed: `<script src="https://unpkg.com/htmx.org@1.9.10"></script>`

2. [ ] Replace `onclick="editMiceCard(...)"` patterns with HTMX:
   ```python
   # Before
   air.Button("Edit", onclick=f"editMiceCard({card['id']}, ...)")
   
   # After (like Demo 3)
   air.Button("Edit",
       hx_get=f"/mice-edit/{card['id']}",
       hx_target=f"#mice-card-{card['id']}",
       hx_swap="outerHTML"
   )
   ```

3. [ ] Replace delete handlers:
   ```python
   # Before
   air.Button("Delete", onclick=f"deleteMiceCard({card['id']})")
   
   # After
   air.Button("Delete",
       hx_delete=f"/api/mice-cards/{card['id']}",
       hx_target=f"#mice-card-{card['id']}",
       hx_swap="outerHTML",
       hx_confirm="Are you sure?"
   )
   ```

4. [ ] Update routes to return appropriate HTML fragments
5. [ ] Test all interactions still work

**Acceptance:** All inline `onclick=` handlers replaced with HTMX attributes

---

### ✅ Task 3.3: Alternative - Extract to JavaScript File (2 hours)

**If HTMX migration not desired:**

1. [ ] Create `HW1/demo/2. Requirements/app/static/app.js`

2. [ ] Extract functions:
   ```javascript
   // app.js
   function editMiceCard(id, code, opening, closing, nesting_level) {
       // ... implementation
   }
   
   function deleteMiceCard(id) {
       // ... implementation  
   }
   ```

3. [ ] Use data attributes instead of inline handlers:
   ```python
   # Before
   onclick=f"editMiceCard({card['id']}, '{card['code']}', ...)"
   
   # After
   class_="edit-mice-btn",
   data_card_id=str(card['id']),
   data_card_code=card['code'],
   # ...
   ```

4. [ ] Add event listeners in app.js:
   ```javascript
   document.addEventListener('DOMContentLoaded', () => {
       document.querySelectorAll('.edit-mice-btn').forEach(btn => {
           btn.addEventListener('click', function() {
               const id = this.dataset.cardId;
               // ...
           });
       });
   });
   ```

**Acceptance:** All JavaScript in .js files, no inline onclick handlers

---

## 📋 Phase 4: Documentation (1 hour total)

### ✅ Task 4.1: Create Demo READMEs (45 min)

**Create:** `HW1/demo/1. NoContext/README.md`
```markdown
# Demo 1: No Context - Basics

This demo shows the fundamental structure of an Air/FastAPI application.

**Learning Focus:**
- Basic routing with Air
- Jinja template integration
- Simple data models with Pydantic
- Form handling

**What's NOT here:**
- No database (just in-memory models)
- No complex state management
- Minimal interactivity

**Next:** See Demo 2 for database integration
```

- [ ] Create README for Demo 1
- [ ] Create README for Demo 2 explaining raw SQL approach
- [ ] Create README for Demo 3 explaining ORM approach
- [ ] Add progression note: 1 → 2 → 3 shows increasing sophistication

---

### ✅ Task 4.2: Update Main README (15 min)

**File:** `HW1/ASSIGNMENT_OVERVIEW.md` or `README.md`

Add section explaining demo progression:
- [ ] Explain purpose of each demo
- [ ] Why they use different technologies
- [ ] Which patterns to follow in homework (Demo 3 style)

---

## 📋 Phase 5: Optional Enhancements (4-8 hours)

### 🔵 Task 5.1: Add Example Tests (4 hours)

**Create test structure:**
```
HW1/demo/3. BetterContext/tests/
├── __init__.py
├── test_database.py
├── test_routes.py
└── conftest.py
```

**Test examples:**
- [ ] Database CRUD operations (real DB, not mocks)
- [ ] Route integration tests
- [ ] Model validation

**Note:** Follow guideline - no mocks, use real database

---

### 🔵 Task 5.2: Pre-commit Hooks (1 hour)

Add type checking enforcement:

1. [ ] Create `.pre-commit-config.yaml`
   ```yaml
   repos:
   - repo: https://github.com/pre-commit/mirrors-mypy
     rev: v1.5.1
     hooks:
     - id: mypy
       additional_dependencies: [types-all]
   ```

2. [ ] Install: `pre-commit install`
3. [ ] Document in README

---

### 🔵 Task 5.3: SQLModel Migration for Demo 2 (4 hours)

**Consider tradeoffs:**
- ✅ Pro: Consistency with Demo 3
- ❌ Con: Loses educational raw SQL example

**If migrating:**
1. [ ] Add sqlmodel dependency
2. [ ] Create models like Demo 3
3. [ ] Rewrite database.py to match Demo 3 pattern
4. [ ] Update all routes
5. [ ] Test thoroughly

**Alternative:** Keep both as examples of different approaches

---

## Verification & Testing

### Final Checks

- [ ] Run type checker: `mypy .`
- [ ] Test all demos still work
- [ ] Verify no inline styles: `grep -r "style=" HW1/demo/*/app/*.py`
- [ ] Verify no inline JS: `grep -r "onclick=" HW1/demo/*/app/*.py`
- [ ] All docstrings present
- [ ] READMEs explain progression

### Success Criteria

✅ **Phase 1:** All type hints complete, docstrings added
✅ **Phase 2:** All CSS in .css files, zero inline styles
✅ **Phase 3:** All JS in .js files or HTMX, zero inline handlers
✅ **Phase 4:** Documentation explains demo progression
✅ **Optional:** Tests and automation added

---

## Time Estimates

| Phase | Tasks | Est. Time |
|-------|-------|-----------|
| Phase 1 | Type hints & docstrings | 1-2 hours |
| Phase 2 | CSS extraction | 2-3 hours |
| Phase 3 | JS cleanup | 2-4 hours |
| Phase 4 | Documentation | 1 hour |
| Phase 5 | Optional enhancements | 4-8 hours |
| **Total** | **Core work** | **6-10 hours** |
| **Total** | **With optional** | **10-18 hours** |

---

## Notes

- Start with Phase 1 (highest ROI)
- Phase 2 and 3 can be done in parallel by different people
- Phase 5 is truly optional - core work completes guideline compliance
- Demo 3 is the reference implementation - follow its patterns

See [TECH_DEBT_ANALYSIS.md](./TECH_DEBT_ANALYSIS.md) for detailed rationale and [TECH_DEBT_SUMMARY.md](./TECH_DEBT_SUMMARY.md) for quick reference.
