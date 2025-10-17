# Story Builder with MICE Quotient — Product Requirements

This document defines the product requirements for a web-based story outlining tool that helps writers structure narratives using the MICE Quotient framework (Milieu, Inquiry, Character, Event) with Try/Fail cycles.

## Product Vision

A single-page web application that enables novice writers to visually construct story outlines using the MICE Quotient framework. The tool provides an educational, card-based interface where users can create nested story elements and see their narrative structure visualized in real-time.

## Core User Experience

The application presents a three-column layout:

1. **MICE Cards (Left)**: Visual cards representing the four story elements (Milieu, Inquiry, Character, Event). Each card captures both an opening (Act 1) and closing (Act 3) for that narrative thread, plus a nesting level indicating story structure depth.

2. **Try/Fail Cycles (Center)**: Cards representing Act 2 story beats where characters attempt and fail/succeed in various ways. Four types supported:
   - Escalation (No, AND): Failure makes things worse
   - Complication (Yes, BUT): Success creates new problems
   - Revelation (No, BUT): Failure reveals opportunity
   - Resolution (Yes, AND): Success builds momentum

3. **Generated Outline (Right)**: Real-time visualization showing both a nested structure diagram and a linear story flow from Act 1 through Act 3.

### 1. MICE Card Management

**Card Types**: Four distinct types representing narrative elements:
- **Milieu (M)**: Stories about exploring a place/setting
- **Inquiry (I)**: Stories driven by seeking answers to questions
- **Character (C)**: Stories about personal transformation
- **Event (E)**: Stories about external conflicts/actions

**Card Properties**:
- MICE type indicator (M, I, C, or E)
- Opening text: What begins this narrative thread (Act 1)
- Closing text: How this thread resolves (Act 3)
- Nesting level: Integer 1-4+ indicating structural depth

**Visual Design**:
- Each MICE type has distinct color coding and icon
- Cards display abbreviated content with tooltips showing full educational details
- Cards are fixed-height (approximately 200px) and fixed-width (approximately 290px)
- Opening and closing text are both visible but truncated with ellipsis

**Card Operations**:
- Add new MICE card via form with type selector, opening/closing textareas, and nesting level input
- Edit existing card inline (replaces card with form)
- Delete card permanently
- No drag-and-drop reordering for MICE cards

### 2. Try/Fail Cycle Management

**Cycle Types**: Four patterns of story progression:
- **Escalation (No, AND)**: Failure that makes things worse
- **Complication (Yes, BUT)**: Success that creates new problems
- **Revelation (No, BUT)**: Failure that reveals opportunity
- **Resolution (Yes, AND)**: Success that builds momentum

**Card Properties**:
- Cycle type indicator
- Order number (explicit sequencing)
- Attempt: What the character tries to do
- Outcome: What actually happens (failure/success)
- Consequence: The result or what's learned

**Visual Design**:
- Each cycle type has distinct color coding and icon
- Cards show drag handle (⋮⋮) for reordering
- Cards display order number prominently
- Fixed-height (approximately 175px) and fixed-width
- All three fields (Try/Result/Learn) visible but truncated

**Card Operations**:
- Add new Try card via form with type selector and three text fields
- Edit existing card inline
- Delete card permanently
- Drag-and-drop reordering within the Try cards section only
- Order numbers update automatically after drag-and-drop

### 3. Story Outline Generation & Visualization

**Nesting Structure Diagram**:
- Visual representation showing MICE cards organized by nesting level
- Nested boxes indicating structural depth (level 1 contains level 2, etc.)
- Each box shows abbreviated card content with arrows (↓ for opening, ↑ for closing)
- Automatically updates when MICE cards are added, edited, or deleted

**Story Flow Timeline**:
- Linear three-act view showing narrative progression
- Act 1: Lists all MICE card openings in nesting order (outside-in: 1→2→3→4)
- Act 2: Lists all Try/Fail cycles in order with icon, attempt, and outcome
- Act 3: Lists all MICE card closings in reverse nesting order (inside-out: 4→3→2→1)
- Color-coded sections (green for Act 1, blue for Act 2, purple for Act 3)

**AI-Generated Outline**:
- "Generate Outline" button triggers AI processing
- Sends all cards to AI service with structured prompt
- Returns formatted prose outline displayed in dedicated area
- Outline persists until regenerated

### 4. Educational Features

**MICE Theory Panel**:
- Expandable/collapsible panel explaining the MICE Quotient framework
- Grid display of all four MICE types with:
  - Full name, description, and real-world examples (e.g., "Lord of the Rings" for Milieu)
  - Color-coded boxes matching card design
- Explanation of nesting concept: how stories open outside-in and close inside-out
- Try/Fail cycle explanation with all four types, patterns, and examples

**In-Context Help**:
- Tooltips on MICE cards showing detailed type information and examples
- Tooltips on Try cards showing pattern and example scenario
- Form fields include helper text guiding content creation

### 5. Data Management & Templates

**Sample Data**:
- "Seed Sample Data" button populates database with example story
- Sample includes multiple MICE cards at different nesting levels
- Sample includes 3 Try/Fail cycles demonstrating different types
- Demonstrates a complete story arc (e.g., child at summer camp overcoming shyness)

**Story Templates**:
- Template modal with pre-built story structures:
  - Mystery Story: I-M-C-E structure with detection-focused Try cycles
  - Adventure Story: M-E-C-I structure with quest-focused Try cycles
  - Romance Story: C-M-E-I structure with relationship-focused Try cycles
- Loading template clears existing data and populates with template cards
- Each template includes 4 MICE cards and 3 Try cycles

**Data Reset**:
- "Clear All Data" button with confirmation dialog
- Removes all cards from database
- No undo mechanism

### 6. Data Model

**MICE Cards Table** (`mice_cards`):
- `id`: Auto-incrementing primary key
- `story_id`: Foreign key (currently defaults to 1, multi-story support deferred)
- `code`: MICE type (M, I, C, or E)
- `opening`: Act 1 content (text)
- `closing`: Act 3 content (text)
- `nesting_level`: Integer indicating structural depth

**Try Cards Table** (`try_cards`):
- `id`: Auto-incrementing primary key
- `story_id`: Foreign key (currently defaults to 1)
- `type`: Try/Fail type (full string like "Escalation (No, AND)")
- `attempt`: What character tries (text)
- `failure`: What actually happens (text)
- `consequence`: Result/learning (text)
- `order_num`: Explicit sequence number

**Persistence Requirements**:
- All card operations (add/edit/delete/reorder) persist immediately to SQLite
- Database survives server restart
- No user accounts or authentication
- Single-user assumption (no concurrency handling needed)

## Interaction Patterns

### MICE Card Workflow
1. User clicks "Add MICE Card" button
2. Form appears above existing cards with type selector, two textareas (opening/closing), and nesting level input
3. User fills form and clicks Save
4. Form disappears, new card appears in grid
5. Nesting diagram automatically updates

### Try Card Workflow
1. User clicks "Add Try Card" button
2. Form appears with cycle type selector, order number input, and three textareas
3. User fills form and clicks Save
4. Form disappears, new card appears in grid
5. Story flow timeline automatically updates

### Drag-and-Drop Workflow
1. User grabs drag handle (⋮⋮) on Try card
2. Card becomes semi-transparent while dragging
3. Other cards shift to show drop position
4. On drop, positions update visually
5. Background request updates database order numbers
6. Story flow timeline automatically updates

### Edit Card Workflow
1. User clicks "Edit" button on card
2. Card is replaced by filled-out form
3. Other cards remain visible
4. User modifies fields and clicks Save
5. Form disappears, updated card appears
6. Relevant visualizations automatically update

### Delete Card Workflow
1. User clicks "Delete" button
2. Card immediately disappears (no confirmation for MVP)
3. Relevant visualizations automatically update

### Outline Generation Workflow
1. User arranges cards as desired
2. User clicks "Generate Outline" button
3. Loading state appears (button disabled or spinner)
4. AI service processes all cards
5. Formatted prose outline appears in dedicated section
6. Outline remains until "Generate Outline" clicked again

## Technical Constraints

- **Browser Support**: Modern evergreen browsers (Chrome, Firefox, Safari, Edge)
- **Database**: SQLite with two tables (mice_cards, try_cards)
- **No Export**: No PDF, document, or data export functionality
- **No Collaboration**: Single user editing at a time
- **No History**: No undo/redo, no version history
- **No Mobile Optimization**: Desktop-first design (responsive not required)
- **AI Dependency**: Outline generation requires external AI service access

## Out of Scope (MVP)

- Multiple stories/projects (story_id exists but only ID=1 used)
- User accounts, authentication, authorization
- Sharing or collaboration features
- Export to PDF, Word, or other formats
- Mobile-responsive design
- Undo/redo functionality
- Auto-save indicators or status
- Offline mode
- Print-friendly views
- Keyboard shortcuts
- Accessibility features beyond basic HTML semantics
- Admin interface or analytics