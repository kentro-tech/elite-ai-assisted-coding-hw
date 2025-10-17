# Story Builder Development Plan

Each step below adds one complete, testable feature. After each step, you should test the feature as a user would before proceeding.

## Step 1: Verify starter app runs
- Ensure the Air starter app runs successfully
- Verify you can access the homepage in a browser
- Confirm the app uses the correct Python environment

## Step 2: Set up database with MICE cards table
- Create SQLite database (`story_builder.db`)
- Add `mice_cards` table with schema: id, story_id, code, opening, closing, nesting_level
- Add a basic endpoint to insert one sample MICE card
- Verify database file exists and contains the sample data

## Step 3: Set up Try cards table
- Add `try_cards` table with schema: id, story_id, type, attempt, failure, consequence, order_num
- Add a basic endpoint to insert one sample Try card
- Verify the table exists and contains the sample data

## Step 4: Create three-column page layout
- Update home.html with a three-column CSS grid layout
- Left column: "MICE Cards" header
- Center column: "Try/Fail Cycles" header
- Right column: "Generated Outline" header
- Add basic CSS styling for the grid (fixed widths, borders)
- Verify the three columns display side-by-side

## Step 5: Display MICE cards from database
- Create endpoint to fetch all MICE cards from database
- Display MICE cards in left column as styled cards (200px height, 290px width)
- Show card type, opening text (truncated), closing text (truncated), nesting level
- Add color coding for M, I, C, E types
- Verify cards display correctly with proper styling

## Step 6: Add "Create MICE Card" form and functionality
- Add "Add MICE Card" button above MICE cards
- Create form with: type selector (M/I/C/E), opening textarea, closing textarea, nesting level input
- Create POST endpoint to save new MICE card to database
- Form saves card and refreshes display
- Verify you can add new MICE cards and see them appear

## Step 7: Add Edit and Delete for MICE cards
- Add "Edit" button on each MICE card (replaces card with filled form)
- Add "Delete" button on each MICE card (removes immediately)
- Create PUT and DELETE endpoints
- Verify you can edit and delete MICE cards

## Step 8: Display Try cards from database
- Create endpoint to fetch all Try cards from database
- Display Try cards in center column as styled cards (175px height)
- Show cycle type, order number, attempt, outcome, consequence (all truncated)
- Add color coding for the four cycle types
- Add drag handle icon (⋮⋮) to each card
- Verify cards display correctly with proper styling

## Step 9: Add "Create Try Card" form and functionality
- Add "Add Try Card" button above Try cards
- Create form with: cycle type selector, order number input, attempt textarea, failure textarea, consequence textarea
- Create POST endpoint to save new Try card
- Form saves card and refreshes display
- Verify you can add new Try cards and see them appear

## Step 10: Add "Seed Sample Data" button
- Add button to populate database with example story
- Create sample MICE cards at different nesting levels
- Create sample Try/Fail cycles
- Button clears existing data first, then adds sample
- Verify sample data loads and displays correctly

## Step 11: Add "Clear All Data" button
- Add button to delete all cards from database
- Add confirmation dialog before clearing
- Verify all data is cleared and displays update

## Step 12: Add Edit and Delete for Try cards
- Add "Edit" button on each Try card
- Add "Delete" button on each Try card
- Create PUT and DELETE endpoints
- Verify you can edit and delete Try cards

## Step 13: Generate nesting structure diagram
- In right column, create visual nesting diagram
- Display MICE cards organized by nesting level (nested boxes)
- Show abbreviated content with ↓ for opening, ↑ for closing
- Diagram updates automatically when MICE cards change
- Verify diagram displays correctly and updates

## Step 14: Generate story flow timeline (Act 1, 2, 3)
- Below nesting diagram in right column, create three-act timeline
- Act 1: List MICE openings in nesting order (1→2→3→4)
- Act 2: List Try/Fail cycles in order with icons
- Act 3: List MICE closings in reverse order (4→3→2→1)
- Color-code sections (green, blue, purple)
- Verify timeline displays correctly and updates

## Step 15: Add MICE Theory educational panel
- Create expandable/collapsible panel explaining MICE Quotient
- Display grid of all four MICE types with descriptions and examples
- Explain nesting concept and Try/Fail cycles
- Match color coding from cards
- Verify panel displays and toggles correctly

## Step 16: Add tooltips to cards
- Add tooltips to MICE cards showing detailed type info and examples
- Add tooltips to Try cards showing pattern and example
- Verify tooltips appear on hover

## Step 17: Add story templates feature
- Create "Templates" button that opens a modal
- Add three templates: Mystery, Adventure, Romance
- Each template has 4 MICE cards and 3 Try cycles
- Loading template clears data and populates with template
- Verify templates load correctly

## Step 18: Add AI outline generation
- Add "Generate Outline" button in right column
- Create endpoint that sends all cards to AI service
- Display returned prose outline in dedicated area
- Add loading state while AI processes
- Verify outline generates and displays

## Step 10: Polish and refinement
- Review all features for consistency
- Ensure all automatic updates work correctly
- Verify color coding and styling throughout
- Test full user workflow from empty to complete story
- Final verification of all features
