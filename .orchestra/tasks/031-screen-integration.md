# Task 031: Screen Integration

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 031 |
| **Status** | ready |
| **Branch** | task/031 |
| **Assigned** | |
| **Depends** | 019, 020, 022, 023, 024, 025, 026 |
| **Blocked-By** | |
| **Estimated** | 60 min |

## Inputs
- All screen states from 019-026

## Description
Integrate all screens into a cohesive flow. Ensure transitions work correctly and game state persists across screens.

## Acceptance Criteria
- [ ] Main menu → New Game → Exploration (with prologue trigger)
- [ ] Main menu → Continue → Save selection → Loaded game
- [ ] Main menu → Settings → (changes) → Back to menu
- [ ] Exploration → Time triggers → Cafe mode
- [ ] Cafe mode → End service → Summary → Exploration
- [ ] Any gameplay → Pause → Menu (inventory, recipes, dragon, settings)
- [ ] Pause menu → Resume → Back to gameplay
- [ ] Pause menu → Save → Confirmation → Resume
- [ ] Pause menu → Main Menu → Confirmation → Menu
- [ ] Game state persists across all transitions
- [ ] Fade transitions between major screens
- [ ] No duplicate state instances
- [ ] All registered in main.py correctly
- [ ] Keyboard shortcuts work (I=inventory, R=recipes, D=dragon, ESC=pause)

## Context Files
- src/states/*.py
- src/main.py
- src/state_manager.py

## Outputs
- Created: src/states/pause_menu_state.py (PauseMenuState)
- Created: src/states/save_load_state.py (SaveLoadState)
- Modified: src/main.py (register all states)
- Modified: All states (proper transitions)

---

## Work Log

