# Task 026: Dragon Status Screen

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 026 |
| **Status** | done |
| **Branch** | task/026 |
| **Assigned** | task/026 |
| **Depends** | 004, 008 |
| **Blocked-By** | |
| **Estimated** | 45 min |

## Inputs
- src/sprites.py from 004
- src/entities/dragon.py from 008

## Description
Create the dragon status screen showing detailed dragon information, stats, abilities, and preferences.

## Acceptance Criteria
- [x] DragonStatusState extending BaseScreen (or overlay)
- [x] Large dragon portrait (center):
  - Current appearance with color
  - Stage-appropriate size
  - Idle animation
- [x] Stats panel:
  - Hunger bar with value
  - Stamina bar with value
  - Happiness bar with value
  - Bond level progress bar
- [x] Info panel:
  - Dragon name (editable)
  - Current stage
  - Days alive
  - Days in current stage
  - Days until next stage
- [x] Abilities panel:
  - List of unlocked abilities
  - Stamina cost each
  - Usage hint
  - Locked abilities shown grayed with unlock condition
- [x] Preferences panel:
  - Favorite foods (discovered)
  - Disliked foods (discovered)
  - "?" for undiscovered preferences
- [x] Color breakdown (RGB values shown)
- [x] Feed button (opens food selection)
- [x] Pet button (quick interaction)
- [x] Close with ESC

## Context Files
- src/sprites.py
- src/entities/dragon.py
- src/constants.py

## Outputs
- Created: src/states/dragon_status_state.py (DragonStatusState)

---

## Work Log

[2025-01-18] - Completed task
- Created DragonStatusState with large dragon portrait showing egg/hatchling/juvenile stages
- Added idle bob animation for portrait
- Created stats panel with hunger/happiness/stamina/bond bars
- Created info panel showing name (editable), stage, days alive, mood
- Created abilities panel showing unlocked/locked abilities with costs and hints
- Created preferences panel for favorite/disliked foods
- Added color breakdown panel showing RGB shift values
- Implemented feed and pet buttons
- ESC to close
- All acceptance criteria complete
