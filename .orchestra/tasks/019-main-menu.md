# Task 019: Main Menu Screen

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 019 |
| **Status** | ready |
| **Branch** | task/019 |
| **Assigned** | |
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
- [ ] MainMenuState extending BaseScreen
- [ ] Title: "Dragon Haven Cafe" with stylized text
- [ ] Menu options:
  - New Game → Character creation (or direct to gameplay for prototype)
  - Continue → Save slot selection
  - Settings → Settings screen
  - Quit → Exit game
- [ ] Animated background (subtle particle effects or dragon silhouette)
- [ ] Menu navigation with keyboard (up/down, enter) and mouse
- [ ] Hover effects on buttons
- [ ] Sound effects on navigation
- [ ] Version number in corner
- [ ] Fade transition to other screens

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

