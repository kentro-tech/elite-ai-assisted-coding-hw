# Tech Debt Reduction - Visual Guide

## 📊 Priority Matrix

```
                                HIGH VALUE
                                    │
                    Type Hints (Wk1)│
                    Type Hints (D2) │
                                    │
                                    │Extract CSS
                                    │
    LOW                             │                        HIGH
    EFFORT ─────────────────────────┼─────────────────────── EFFORT
                                    │
                    Documentation   │      Extract JS
                                    │      (HTMX migration)
                    Docstrings      │
                                    │
                                    │
                                LOW VALUE
```

## 🔄 Guideline Compliance Flow

```
Current State          →    Refactored State
─────────────────────────────────────────────────

❌ No type hints       →    ✅ Comprehensive type hints
   (tzconverter)            def foo() -> list[str]:

❌ Inline CSS          →    ✅ External stylesheet
   style="color: red"       class="error-text"
                            /* .error-text { color: red; } */

❌ Inline JS           →    ✅ HTMX attributes
   onclick="doThing()"      hx-get="/endpoint"
                            hx-target="#element"

⚠️ Missing docs        →    ✅ Business logic explained
   def get_cards():         def get_cards():
                                """Retrieve MICE cards..."""
```

## 🏗️ Architecture Evolution

### Demo Progression (Intentional!)

```
Demo 1: NoContext          Demo 2: Requirements       Demo 3: BetterContext
─────────────────          ─────────────────────      ─────────────────────
├── Jinja templates        ├── SQLite3 (raw SQL)      ├── SQLModel (ORM)
├── Pydantic models        ├── Dict-based data        ├── Type-safe models
├── Basic routing          ├── Inline JS/CSS ❌       ├── HTMX ✅
└── No persistence         ├── database.py            ├── db.py
                           └── components.py          ├── forms.py
                                                      ├── components.py
                                                      ├── layouts.py
                                                      └── templates.py

    SIMPLE                    INTERMEDIATE               ADVANCED
    (35 lines)                (99 lines)                 (280 lines)
```

**Note:** Demo 3 is the **GOLD STANDARD** - follow its patterns!

## 🎯 Refactoring Targets by Demo

### Demo 2: Requirements
```
Issues Found:
├── ❌ Type hints incomplete (database.py)
├── ❌ Inline CSS (3 instances in components.py)
├── ❌ Inline JS (onclick handlers)
└── ⚠️ Missing docstrings

Recommended Actions:
├── ✅ Complete type hints → 15 min
├── ✅ Extract CSS to styles.css → 1 hour
├── ✅ Migrate to HTMX (like Demo 3) → 2 hours
└── ✅ Add business logic docstrings → 30 min
```

### Demo 3: BetterContext
```
Issues Found:
└── ❌ Minor inline CSS (background colors)

Recommended Actions:
└── ✅ Extract to CSS classes → 30 min
```

### Wk1: tzconverter
```
Issues Found:
└── ❌ No type hints

Recommended Actions:
└── ✅ Add return types and param types → 15 min
```

## 📈 Impact Analysis

### Before Refactoring
```python
# ❌ Hard to understand, maintain, and test
def get_mice_cards(story_id = 1):  # No types!
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM mice_cards WHERE story_id = ? ORDER BY nesting_level", (story_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

# In components.py
air.P(f"Opens: {opens}", style="font-style: italic;")  # Inline CSS!
air.Button("Edit", onclick=f"editCard({id})")  # Inline JS!
```

### After Refactoring
```python
# ✅ Clear, type-safe, maintainable
def get_mice_cards(story_id: int = 1) -> List[Dict[str, Any]]:
    """Retrieve all MICE cards for a story, ordered by nesting level.
    
    MICE cards represent narrative structure elements that open in Act 1
    and close in Act 3 in nested order.
    """
    with db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM mice_cards WHERE story_id = ? ORDER BY nesting_level", 
            (story_id,)
        )
        return [dict(row) for row in cursor.fetchall()]

# In components.py
air.P(f"Opens: {opens}", class_="theory-opens")  # CSS class!
air.Button("Edit",  # HTMX!
    hx_get=f"/mice-edit/{id}",
    hx_target=f"#card-{id}"
)
```

### In styles.css
```css
.theory-opens {
    font-style: italic;
}
```

## 🚀 Quick Wins vs Long-term Improvements

### Quick Wins (< 1 hour each) 🏃
```
✅ Add type hints to tzconverter       → 15 min
✅ Complete Demo 2 type hints          → 15 min  
✅ Add docstrings to Demo 2            → 30 min
✅ Create demo README files            → 30 min
─────────────────────────────────────────────────
   TOTAL                               → 1.5 hours
   IMPACT                              → Immediate compliance
```

### Medium Effort (1-3 hours each) 🚶
```
✅ Extract CSS to stylesheets          → 2 hours
✅ Migrate to HTMX or extract JS       → 2-3 hours
─────────────────────────────────────────────────
   TOTAL                               → 4-5 hours
   IMPACT                              → Clean separation of concerns
```

### Long-term (4+ hours) 🐌
```
🔵 Add example test suite              → 4 hours
🔵 Migrate Demo 2 to SQLModel          → 4 hours
🔵 Set up pre-commit hooks             → 1 hour
─────────────────────────────────────────────────
   TOTAL                               → 9 hours
   IMPACT                              → Optional enhancements
```

## 📝 Guideline Adherence Score

### Current Score: 75/100

| Criterion | Current | Target | Gap |
|-----------|---------|--------|-----|
| Type Safety | 60% | 100% | ⚠️ 40% |
| File Structure | 70% | 100% | ⚠️ 30% |
| Abstraction Quality | 90% | 90% | ✅ 0% |
| Function Size | 95% | 95% | ✅ 0% |
| Error Handling | 100% | 100% | ✅ 0% |
| Readability | 85% | 100% | ⚠️ 15% |
| Documentation | 60% | 90% | ⚠️ 30% |

### After Phase 1-3: 95/100

| Criterion | After | Target | Gap |
|-----------|-------|--------|-----|
| Type Safety | 100% | 100% | ✅ 0% |
| File Structure | 100% | 100% | ✅ 0% |
| Abstraction Quality | 90% | 90% | ✅ 0% |
| Function Size | 95% | 95% | ✅ 0% |
| Error Handling | 100% | 100% | ✅ 0% |
| Readability | 95% | 100% | ⚠️ 5% |
| Documentation | 90% | 90% | ✅ 0% |

## 🔍 What's Already Good ✅

Don't change these - they follow guidelines perfectly:

```
✅ Error Handling Strategy
   ├── No defensive try/except
   ├── Fail fast with stack traces
   └── Fix bugs at source

✅ Abstraction Thickness
   ├── db.py is thick, cohesive (not thin wrapper)
   ├── forms.py consolidates UI logic
   └── components.py groups rendering

✅ Function Design
   ├── Longer functions are single, cohesive tasks
   ├── Form builders are 60-85 lines but clear
   └── Complexity is justified

✅ Architecture Decisions
   ├── story_id field enables future features
   ├── Demo progression shows learning path
   └── Separation of concerns maintained
```

## 🎓 Educational Value Map

```
What Students Learn:

Demo 1                  Demo 2                    Demo 3
──────                  ──────                    ──────
Basic concepts     →    Database integration  →   Best practices
                        
• Routing               • Raw SQL                 • ORM (SQLModel)
• Templates             • Dict data               • Type-safe models
• Forms                 • File organization       • Thick abstractions
                        • State persistence       • HTMX patterns
                                                  • Clean architecture

                        ⚠️ Has tech debt          ✅ Gold standard
                        (teaching moment)         (follow this!)
```

**Key Insight:** Demo 2's tech debt is a **teaching opportunity** - show what NOT to do, then show Demo 3 as the solution!

## 📚 Related Documents

- [TECH_DEBT_ANALYSIS.md](./TECH_DEBT_ANALYSIS.md) - Detailed analysis with pros/cons
- [TECH_DEBT_SUMMARY.md](./TECH_DEBT_SUMMARY.md) - Quick reference table
- [TECH_DEBT_CHECKLIST.md](./TECH_DEBT_CHECKLIST.md) - Step-by-step implementation guide
- [.github/copilot-instructions.md](./.github/copilot-instructions.md) - Original guidelines

## 🎯 Recommended Action Plan

1. **Week 1:** Phase 1 - Quick wins (type hints, docstrings)
2. **Week 2:** Phase 2 - CSS extraction
3. **Week 3:** Phase 3 - JavaScript cleanup (HTMX migration)
4. **Week 4:** Phase 4 - Documentation
5. **Optional:** Phase 5 - Tests and automation

**Start Here:** Type hints in tzconverter.py (15 minutes, immediate value!)
