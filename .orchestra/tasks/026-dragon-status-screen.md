# Task 026: Dragon Status Screen

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 026 |
| **Status** | ready |
| **Branch** | task/026 |
| **Assigned** | |
| **Depends** | 004, 008 |
| **Blocked-By** | |
| **Estimated** | 45 min |

## Inputs
- src/sprites.py from 004
- src/entities/dragon.py from 008

## Description
Create the dragon status screen showing detailed dragon information, stats, abilities, and preferences.

## Acceptance Criteria
- [ ] DragonStatusState extending BaseScreen (or overlay)
- [ ] Large dragon portrait (center):
  - Current appearance with color
  - Stage-appropriate size
  - Idle animation
- [ ] Stats panel:
  - Hunger bar with value
  - Stamina bar with value
  - Happiness bar with value
  - Bond level progress bar
- [ ] Info panel:
  - Dragon name (editable)
  - Current stage
  - Days alive
  - Days in current stage
  - Days until next stage
- [ ] Abilities panel:
  - List of unlocked abilities
  - Stamina cost each
  - Usage hint
  - Locked abilities shown grayed with unlock condition
- [ ] Preferences panel:
  - Favorite foods (discovered)
  - Disliked foods (discovered)
  - "?" for undiscovered preferences
- [ ] Color breakdown (RGB values shown)
- [ ] Feed button (opens food selection)
- [ ] Pet button (quick interaction)
- [ ] Close with ESC

## Context Files
- src/sprites.py
- src/entities/dragon.py
- src/constants.py

## Outputs
- Created: src/states/dragon_status_state.py (DragonStatusState)
- Modified: src/entities/dragon.py (any needed getters)

---

## Work Log

