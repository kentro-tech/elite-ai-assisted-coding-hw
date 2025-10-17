# Story Builder Development Plan

Each step below adds one complete, testable feature. After each step, you should test the feature as a user would before proceeding.

## Step 1: Verify starter app runs

- [x] Ensure the Air starter app runs successfully
- [x] Verify you can access the homepage in a browser
- [x] Confirm the app uses the correct Python environment

## Step 2: Set up database with MICE cards table

- [x] Create SQLite database (`story_builder.db`)
- [x] Add `mice_cards` table with schema: id, story_id, code, opening, closing, nesting_level
- [x] Add a basic endpoint to insert one sample MICE card
- [x] Verify database file exists and contains the sample data

## Step 3: Set up Try cards table

- [x] Add `try_cards` table with schema: id, story_id, type, attempt, failure, consequence, order_num
- [x] Add a basic endpoint to insert one sample Try card
- [x] Verify the table exists and contains the sample data

## Step 4: Create three-column page layout

- [x] Update home.html with a three-column CSS grid layout
- [x] Left column: "MICE Cards" header
- [x] Center column: "Try/Fail Cycles" header
- [x] Right column: "Generated Outline" header
- [x] Add basic CSS styling for the grid (fixed widths, borders)
- [x] Verify the three columns display side-by-side

## Step 5: Display MICE cards from database

- [x] Create endpoint to fetch all MICE cards from database
- [x] Display MICE cards in left column as styled cards (200px height, 290px width)
- [x] Show card type, opening text (truncated), closing text (truncated), nesting level
- [x] Add color coding for M, I, C, E types
- [x] Verify cards display correctly with proper styling

## Step 6: Add "Create MICE Card" form and functionality

- [x] Add "Add MICE Card" button above MICE cards
- [x] Create form with: type selector (M/I/C/E), opening textarea, closing textarea, nesting level input
- [x] Create POST endpoint to save new MICE card to database
- [x] Form saves card and refreshes display
- [x] Verify you can add new MICE cards and see them appear

## Step 7: Add Edit and Delete for MICE cards

- [x] Add "Edit" button on each MICE card (replaces card with filled form)
- [x] Add "Delete" button on each MICE card (removes immediately)
- [x] Create PUT and DELETE endpoints
- [x] Verify you can edit and delete MICE cards

## Step 8: Display Try cards from database

- [x] Create endpoint to fetch all Try cards from database
- [x] Display Try cards in center column as styled cards (175px height)
- [x] Show cycle type, order number, attempt, outcome, consequence (all truncated)
- [x] Add color coding for the four cycle types
- [x] Prevent duplicate order numbers for Try cards
- [x] Determine the order of the Try cards by the order number, and display them in that order
- [x] Add drag handle icon (⋮⋮) to each card and automatically update the order number when the order changes
- [x] Verify cards display correctly with proper styling

## Step 9: Add "Create Try Card" form and functionality

- [x] Add "Add Try Card" button above Try cards
- [x] Create form with: cycle type selector, order number input, attempt textarea, failure textarea, consequence textarea
- [x] Create POST endpoint to save new Try card
- [x] Form saves card and refreshes display
- [x] Verify you can add new Try cards and see them appear

## Step 10: Add "Seed Sample Data" button

- [-] Add button to populate database with example story - NOTE: Replaced by Templates feature
- [-] Create sample MICE cards at different nesting levels - NOTE: Replaced by Templates feature
- [-] Create sample Try/Fail cycles - NOTE: Replaced by Templates feature
- [-] Button clears existing data first, then adds sample - NOTE: Replaced by Templates feature
- [-] Verify sample data loads and displays correctly - NOTE: Replaced by Templates feature

## Step 11: Add "Clear All Data" button

- [x] Add button to delete all cards from database
- [x] Add confirmation dialog before clearing
- [x] Verify all data is cleared and displays update

## Step 12: Add Edit and Delete for Try cards

- [x] Add "Edit" button on each Try card
- [x] Add "Delete" button on each Try card
- [x] Create PUT and DELETE endpoints
- [x] Verify you can edit and delete Try cards

## Step 13: Generate nesting structure diagram

- [x] In right column, create visual nesting diagram
- [x] Display MICE cards organized by nesting level (nested boxes)
- [x] Show abbreviated content with ↓ for opening, ↑ for closing
- [x] Diagram updates automatically when MICE cards change
- [x] Verify diagram displays correctly and updates

## Step 14: Generate story flow timeline (Act 1, 2, 3)

- [x] Below nesting diagram in right column, create three-act timeline
- [x] Act 1: List MICE openings in nesting order (1→2→3→4)
- [x] Act 2: List Try/Fail cycles in order with icons
- [x] Act 3: List MICE closings in reverse order (4→3→2→1)
- [x] Color-code sections (green, blue, purple)
- [x] Verify timeline displays correctly and updates

## Step 15: Add MICE Theory educational panel

- [x] Create expandable/collapsible panel explaining MICE Quotient
- [x] Display grid of all four MICE types with descriptions and examples
- [x] Explain nesting concept and Try/Fail cycles
- [x] Match color coding from cards
- [x] Verify panel displays and toggles correctly

## Step 16: Add tooltips to cards

- [x] Add tooltips to MICE cards showing detailed type info and examples
- [x] Add tooltips to Try cards showing pattern and example
- [x] Verify tooltips appear on hover

## Step 17: Add story templates feature

- [x] Create "Templates" button that opens a modal
- [x] Add three templates: Mystery, Adventure, Romance
- [x] Each template has 4 MICE cards and 3 Try cycles
- [x] Loading template clears data and populates with template
- [x] Verify templates load correctly

## Step 18: Add database columns for AI-generated icons

- [x] Add migration or update script to add `act1_icon` column (BLOB, nullable) to `mice_cards` table
- [x] Add migration or update script to add `act3_icon` column (BLOB, nullable) to `mice_cards` table
- [x] Add migration or update script to add `consequence_icon` column (BLOB, nullable) to `try_cards` table
- [x] Update database helper functions to handle the new columns
- [x] Verify database schema changes are applied correctly
- [x] Test that existing cards still work with the new nullable columns

## Step 19: Add placeholder icons to all cards

- [x] Create or select a placeholder icon image (40x40px)
- [x] Update MICE card display to show placeholder in top-right corner (Act 1 position)
- [x] Update MICE card display to show placeholder in bottom-right corner (Act 3 position)
- [x] Update Try card display to show placeholder in center or top-right corner (consequence position)
- [x] Add CSS styling for icons: rounded corners, subtle border, proper positioning
- [x] Verify all cards display placeholder icons correctly
- [x] Test that placeholders don't break existing card layouts

## Step 20: Set up HuggingFace API integration

- [x] Set up HF_TOKEN environment variable for authentication
- [x] Create helper function to call HuggingFace text-to-image models via Inference API
- [x] Implement basic prompt generation function that creates image prompts from text
- [x] Create test endpoint to verify API connection works
- [x] Add error handling for API failures (timeout, rate limits, invalid token)
- [x] Test API integration with a simple test prompt
- [x] Verify generated images can be retrieved and stored as BLOBs
- [x] Added Pillow dependency for image processing
- [x] Documented that text-to-image requires HuggingFace Pro subscription or credits
- [x] Implemented dual API mode support:
  - [x] Added Gradio API integration for free image generation (uses public HF Spaces)
  - [x] Added gradio-client dependency
  - [x] Created USE_GRADIO_API environment variable to switch between modes
  - [x] Updated test endpoint to show which API mode is active
  - [x] Added "Test HuggingFace Connection" button to main page using HTMX
  - [x] Enhanced test page with live status updates and clear API mode indicator
  - [x] Updated documentation to explain both API modes (Gradio free vs Inference paid)
  - [x] Configured Gradio API as default for testing (USE_GRADIO_API=true)

## Step 21: Add icon generation for Try cards

- [x] Create endpoint to serve images from database BLOBs (e.g., `/api/try-card-icon/<id>`)
- [x] Update Try card POST endpoint to trigger async icon generation after saving:
  - [x] Generate prompt from consequence text
  - [x] Call HuggingFace API to generate image
  - [x] Save image BLOB to database
- [x] Update Try card display to show generated icon instead of placeholder when available
- [x] Update Try card PUT endpoint to regenerate icon when consequence text changes
- [x] Added automatic icon generation when loading templates
- [x] Made placeholder icon clickable to manually trigger icon generation
- [x] Added clear "Image Generating" message with refresh instruction
- [x] Made generated icons clickable to regenerate
- [x] Added loading icon display when editing consequence text
- [x] Test creating new Try cards and verify icons generate and display
- [x] Test editing Try cards and verify icons update

## Step 22: Add icon generation for MICE cards

- [x] Create endpoint to serve MICE card images from database BLOBs (e.g., `/api/mice-card-icon/<id>/<type>`)
- [x] Update MICE card POST endpoint to trigger async icon generation after saving:
  - [x] Generate prompt from opening text for Act 1 icon
  - [x] Generate prompt from closing text for Act 3 icon
  - [x] Call HuggingFace API to generate both images
  - [x] Save both image BLOBs to database
- [x] Update MICE card display to show generated icons instead of placeholders when available
- [x] Add loading/generation status indicator on cards during generation
- [x] Update MICE card PUT endpoint to regenerate icons when opening/closing text changes
- [x] Test creating new MICE cards and verify both icons generate and display
- [x] Test editing MICE cards and verify icons update appropriately

## Step 23: Add AI outline generation

- [ ] Add "Generate Outline" button in right column
- [ ] Create endpoint that sends all cards to AI service
- [ ] Display returned prose outline in dedicated area
- [ ] Add loading state while AI processes
- [ ] Verify outline generates and displays

## Step 24: Polish and refinement

- [x] Review all features for consistency
- [x] Ensure all automatic updates work correctly
- [x] Verify color coding and styling throughout
- [ ] Verify all icon styling is consistent (rounded corners, borders, sizing)
- [ ] Test icon generation performance and user experience
- [ ] Ensure placeholder-to-generated-icon transitions are smooth
- [ ] Test error scenarios (API failures, network issues)
- [x] Test full user workflow from empty to complete story
- [ ] Final verification of all features - NOTE: Mostly complete, but AI icon generation and outline generation not yet implemented
