# Bugs Discovered During Testing

This document lists bugs and issues found during comprehensive testing of the MICE Story Builder application.

---

## Bug #1: No Validation on MICE Code Field

**Severity**: Important  
**Test**: `test_create_mice_card_invalid_code`

**Description**: The MICE card `code` field accepts any string value, not just the valid MICE codes (M, I, C, E).

**How to Reproduce**:
1. Create a MICE card with `code="X"` or any other invalid value
2. The card is created successfully without validation error

**Expected Behavior**: 
- Should only accept "M", "I", "C", or "E"
- Should raise validation error for invalid codes

**Actual Behavior**:
- Accepts any string value including empty strings, numbers, special characters

**Impact**: 
- Users can create cards with meaningless codes
- Breaks the MICE methodology structure
- Could cause UI display issues with unexpected values

**Recommendation**: Add validation to restrict code to valid MICE values.

---

## Bug #2: No Validation on Try Card Type Field

**Severity**: Important  
**Test**: `test_create_try_card_invalid_type`

**Description**: The Try card `type` field accepts any string value, not just "Failure" or "Success".

**How to Reproduce**:
1. Create a Try card with `type="InvalidType"` or any other value
2. The card is created successfully without validation error

**Expected Behavior**:
- Should only accept "Failure" or "Success"
- Should raise validation error for invalid types

**Actual Behavior**:
- Accepts any string value including empty strings

**Impact**:
- Users can create cards with meaningless types
- Could cause UI display issues or incorrect story structure

**Recommendation**: Add validation to restrict type to "Failure" or "Success".

---

## Bug #3: Empty Fields Accepted Without Validation

**Severity**: Minor  
**Tests**: `test_create_mice_card_empty_fields`, `test_create_try_card_empty_fields`

**Description**: All text fields accept empty strings without validation.

**How to Reproduce**:
1. Create a MICE card with all empty strings: `code=""`, `opening=""`, `closing=""`
2. Create a Try card with empty `type`, `attempt`, `failure`, `consequence`
3. Cards are created successfully

**Expected Behavior**:
- Should require non-empty values for key fields
- Should provide user-friendly error message

**Actual Behavior**:
- Empty fields are accepted
- Cards appear in UI with no content

**Impact**:
- Users can accidentally create empty/useless cards
- Clutters the UI with blank cards
- Reduces data quality

**Recommendation**: Add validation to require non-empty strings for key fields.

---

## Bug #4: Negative Numbers Accepted for Nesting Level and Order

**Severity**: Minor  
**Tests**: `test_create_mice_card_negative_nesting`, `test_create_try_card_negative_order`

**Description**: Nesting level and order number fields accept negative values.

**How to Reproduce**:
1. Create a MICE card with `nesting_level=-1`
2. Create a Try card with `order_num=-5`
3. Both are accepted

**Expected Behavior**:
- Should require positive integers (>= 0 or >= 1)
- Should raise validation error for negative values

**Actual Behavior**:
- Negative values are accepted and stored

**Impact**:
- Could cause unexpected sorting/display behavior
- Nesting diagram might render incorrectly with negative indentation
- Timeline might be out of order

**Recommendation**: Add validation to ensure positive values.

---

## Bug #5: Duplicate Try Card Order Numbers Allowed

**Severity**: Important  
**Test**: `test_duplicate_try_card_order_numbers`

**Description**: Multiple Try cards can have the same `order_num` value, leading to ambiguous ordering.

**How to Reproduce**:
1. Create Try card with `order_num=1`
2. Create another Try card with `order_num=1`
3. Both are created successfully

**Expected Behavior**:
- Order numbers should be unique within a story
- Should prevent duplicates or auto-increment
- Or show validation error

**Actual Behavior**:
- Duplicate order numbers are allowed
- Ordering in UI becomes unpredictable when duplicates exist

**Impact**:
- Users can't reliably sequence their Try/Fail cycles
- Story timeline becomes ambiguous
- Database query ordering is undefined for duplicates

**Recommendation**: Add unique constraint or auto-increment order numbers.

---

## Bug #6: No HTML Escaping for User Input (Potential XSS)

**Severity**: Critical (Security Issue)  
**Tests**: `test_mice_card_special_characters`, `test_try_card_special_characters`

**Description**: User input containing HTML/JavaScript is stored and potentially rendered without escaping.

**How to Reproduce**:
1. Create a card with `opening='<script>alert("XSS")</script>'`
2. The value is stored as-is in the database
3. When rendered to HTML, script could execute

**Expected Behavior**:
- User input should be HTML-escaped before rendering
- JavaScript should be stripped or escaped
- Output should be safe for HTML rendering

**Actual Behavior**:
- Raw HTML/JavaScript is stored
- If rendered without escaping, could execute malicious code

**Impact**:
- **Security vulnerability**: Cross-site scripting (XSS) attack possible
- Malicious users could inject JavaScript
- Could steal session data or perform actions as other users

**Recommendation**: 
- HTML-escape all user input when rendering
- Consider using a template engine with auto-escaping
- Test that `air` framework properly escapes output

---

## Bug #7: Very Long Text Not Limited

**Severity**: Minor  
**Test**: `test_mice_card_very_long_text`

**Description**: Text fields accept extremely long values (10,000+ characters) without limits.

**How to Reproduce**:
1. Create a card with 10,000 character string in opening field
2. Card is created successfully

**Expected Behavior**:
- Should have reasonable length limits (e.g., 500-2000 characters)
- Should show validation error for excessive length

**Actual Behavior**:
- Unlimited text length accepted
- Stored in database without truncation

**Impact**:
- Could cause UI layout issues with very long text
- Database storage inefficiency
- Performance issues rendering large text blocks

**Recommendation**: Add maximum length validation (e.g., 2000 characters).

---

## Bug #8: Multiline Text Might Not Render Properly

**Severity**: Minor  
**Test**: `test_try_card_multiline_text`

**Description**: Newline characters (`\n`) in text fields are stored but might not display correctly in HTML.

**How to Reproduce**:
1. Create a card with text containing `\n` characters
2. View the card in the UI

**Expected Behavior**:
- Newlines should be preserved and displayed
- Or text should be rendered in a `<pre>` tag or with `white-space: pre-wrap`

**Actual Behavior**:
- Newlines are stored in database
- HTML collapses multiple whitespace/newlines by default

**Impact**:
- User's formatting is lost
- Text appears as one continuous line
- Reduces readability

**Recommendation**: 
- Either convert `\n` to `<br>` tags when rendering
- Or use CSS `white-space: pre-wrap` for text display
- Or provide a rich text editor

---

## Summary Statistics

**Total Bugs Found**: 8

- **Critical (Security)**: 1 (HTML/XSS)
- **Important**: 3 (Invalid codes, invalid types, duplicate orders)
- **Minor**: 4 (Empty fields, negative numbers, long text, multiline)

**Test Coverage**: All bugs discovered through automated edge case testing.

**Database Tests**: Passed (no crashes on edge cases)  
**API Tests**: Passed (no crashes on edge cases)  
**Application Stability**: Good (handles edge cases without crashing)  
**Data Validation**: Poor (no validation in place)

---

## Recommendations Priority

### High Priority
1. **Fix Bug #6**: Add HTML escaping to prevent XSS vulnerabilities
2. **Fix Bug #1**: Validate MICE codes to maintain methodology integrity
3. **Fix Bug #2**: Validate Try card types
4. **Fix Bug #5**: Prevent duplicate order numbers

### Medium Priority
5. **Fix Bug #3**: Require non-empty fields
6. **Fix Bug #4**: Validate positive numbers

### Low Priority
7. **Fix Bug #7**: Add reasonable length limits
8. **Fix Bug #8**: Improve multiline text rendering

---

## Notes

- All bugs were discovered through systematic edge case testing
- The application is stable and doesn't crash on invalid input
- Main issue is lack of validation, not application crashes
- These bugs are typical for early-stage development
- Easy to fix by adding validation at the model or API level

---

**Testing Completed**: October 17, 2025  
**Tester**: Automated Test Suite  
**Total Tests Run**: 83 tests (62 core + 21 edge cases)

