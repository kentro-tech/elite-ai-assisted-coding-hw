# Tech Debt Reduction - Quick Reference

## Overview

Analysis of codebase against `.github/copilot-instructions.md` guidelines. Full details in [TECH_DEBT_ANALYSIS.md](./TECH_DEBT_ANALYSIS.md).

## Priority Matrix

| Issue | Value | Effort | Priority | Guideline Violated? |
|-------|-------|--------|----------|---------------------|
| Type hints in tzconverter | 8/10 | Low | **HIGH** | ✅ Yes - Type Safety |
| Type hints in Demo 2 db | 9/10 | Low | **HIGH** | ✅ Yes - Type Safety |
| Extract inline CSS (20 instances) | 7/10 | Medium | **HIGH** | ✅ Yes - File Structure |
| Extract inline JS (20 instances) | 6/10 | Medium | **MEDIUM** | ✅ Yes - File Structure |
| Add docstrings to Demo 2 | 6/10 | Low | **MEDIUM** | ⚠️ Best Practice |
| Demo progression docs | 4/10 | Low | **LOW** | ⚠️ Clarity |
| Migrate Demo 2 to SQLModel | 5/10 | High | **LOW** | ❌ No - Educational tradeoff |
| Add example tests | 5/10 | Medium | **LOW** | ❌ No - Enhancement |

## Quick Action Items

### ✅ Must Do (Guideline Violations)

1. **Add type hints to Wk1-RecordedLessonContents/tzconverter/main.py**
   - Add return type to `generate_time_options()` 
   - Add parameter types to `index()`
   - ~5 minutes

2. **Complete type hints in HW1/demo/2. Requirements/app/database.py**
   - Ensure all parameters have types
   - ~10 minutes

3. **Extract inline styles to CSS classes**
   ```python
   # BAD (current)
   style="font-style: italic;"
   
   # GOOD (refactored)
   class_="theory-opens"
   ```
   - Create/expand `static/styles.css`
   - Replace ~20 style attributes
   - ~2 hours

4. **Extract inline JavaScript**
   ```python
   # BAD (current)
   onclick=f"editMiceCard({card['id']}, ...)"
   
   # GOOD (use HTMX like Demo 3)
   hx_get=f"/mice-edit/{card.id}"
   hx_target=f"#mice-card-{card.id}"
   ```
   - Migrate Demo 2 to HTMX pattern OR extract to .js file
   - ~2-4 hours

### 🟡 Should Do (Quality Improvements)

5. **Add docstrings explaining MICE quotient domain logic**
   - Focus on Demo 2 functions
   - Explain business purpose, not implementation
   - ~1 hour

6. **Add README.md to each demo**
   - Explain progression: Demo 1 → Demo 2 → Demo 3
   - Clarify why different approaches used
   - ~30 minutes

### 🔵 Consider (Optional Enhancements)

7. **Example test suite** - Educational value for students
8. **SQLModel migration for Demo 2** - But loses raw SQL examples
9. **Pre-commit hooks** - Enforce type checking

## What's Already Correct ✅

These follow guidelines perfectly - **no changes needed**:

- ✅ **Error handling** - Correctly uses fail-fast, no defensive try/except
- ✅ **Function length** - Longer functions are cohesive single tasks
- ✅ **Demo 3 structure** - Excellent abstraction (thick, justified)
- ✅ **story_id architecture** - Forward-thinking, enables future features

## Guideline Summary

From `.github/copilot-instructions.md`:

1. **Type Hinting** - Always use type hints everywhere ← *Violated in 2 files*
2. **Abstraction** - Only thick, meaningful abstractions ← *Followed well*
3. **File Structure** - CSS in .css, JS in .js, Python in .py ← *Violated (inline styles/JS)*
4. **Function Size** - Cohesive tasks over line limits ← *Followed well*
5. **Error Handling** - Fail fast, no defensive code ← *Followed perfectly*
6. **Readability** - Explicit over clever ← *Followed well*
7. **Duplication** - Refactor on 3rd occurrence or if bug-prone ← *Handled appropriately*

## Model to Follow

**Demo 3: BetterContext** is the gold standard:
- ✅ Comprehensive type hints
- ✅ Thick, cohesive abstractions (db.py, forms.py, components.py)
- ✅ HTMX instead of inline JS
- ✅ Excellent docstrings
- ✅ Clean separation of concerns

**Refactoring wisdom from Demo 3's refactor.md:**
- Thick abstractions over thin wrappers
- Clear file purposes (easy to find things)
- Educational value (shows proper patterns)
- Minimal file jumping (related code together)

## Estimated Effort

- **Tier 1 (Must Do)**: 3-5 hours
- **Tier 2 (Should Do)**: 1-2 hours  
- **Tier 3 (Optional)**: 4-8 hours

**Total: 8-15 hours** to address all priority items.

**Highest ROI**: Type hints (15 minutes) → immediate compliance and clarity.

## Notes

- Demo 2 vs Demo 3 duplication is **intentional** (educational progression)
- No defensive error handling is **correct** per guidelines
- Longer form functions are **appropriate** (cohesive UI building)
- `story_id` field is **good architecture** (future-proofing)

---

See [TECH_DEBT_ANALYSIS.md](./TECH_DEBT_ANALYSIS.md) for detailed analysis with pros/cons for each item.
