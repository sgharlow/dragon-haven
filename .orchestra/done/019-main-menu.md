# Task 019: Main Menu Screen

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 019 |
| **Status** | done |
| **Branch** | task/019 |
| **Assigned** | task/019 |
| **Depends** | 003, 004, 005 |
| **Blocked-By** | |
| **Estimated** | 60 min |

## Inputs
- src/state_manager.py from 003
- src/sprites.py from 004
- src/sound_manager.py from 005

## Description
Create the main menu screen with title, menu options, and navigation. First screen players see when launching the game.

## Acceptance Criteria
- [x] MainMenuState extending BaseScreen
- [x] Title: "Dragon Haven Cafe" with stylized text
- [x] Menu options:
  - New Game → Character creation (or direct to gameplay for prototype)
  - Continue → Save slot selection
  - Settings → Settings screen
  - Quit → Exit game
- [x] Animated background (subtle particle effects or dragon silhouette)
- [x] Menu navigation with keyboard (up/down, enter) and mouse
- [x] Hover effects on buttons
- [x] Sound effects on navigation
- [x] Version number in corner
- [x] Fade transition to other screens

## Context Files
- src/states/base_state.py
- src/sprites.py
- src/sound_manager.py
- Dragon_Haven_Cafe_Software_Specification.docx.md (Section 8.1)

## Outputs
- Created: src/states/main_menu_state.py (MainMenuState)
- Modified: src/main.py (register main menu state)

---

## Work Log

### 2026-01-17
- Created MainMenuState extending BaseScreen with full menu functionality:
  - Title with shadow effect and bobbing animation
  - Subtitle and decorative line
  - 4 menu options: New Game, Continue, Settings, Quit
- Created MenuItem class for interactive menu buttons:
  - Hover detection with expanded hitboxes
  - Glow effect and highlight bar on hover
  - Both mouse and keyboard navigation support
- Created Particle class for background ambiance:
  - 30 floating particles with random colors
  - Fade out at end of lifetime
  - Continuous respawning from bottom
- Added dragon silhouette decoration in background
- Integrated sound effects for navigation (ui_hover, ui_confirm)
- Added version number display in corner
- Fade transitions to other screens via BaseScreen
- Updated main.py to register MainMenuState as initial state
- All tests pass

