# Task 021: Gameplay HUD

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 021 |
| **Status** | ready |
| **Branch** | task/021 |
| **Assigned** | |
| **Depends** | 004, 007, 008, 012 |
| **Blocked-By** | |
| **Estimated** | 60 min |

## Inputs
- src/sprites.py from 004
- src/systems/time_system.py from 007
- src/entities/dragon.py from 008
- src/systems/economy.py from 012

## Description
Create the heads-up display (HUD) that shows during gameplay. Displays vital information without cluttering the screen.

## Acceptance Criteria
- [ ] HUD class (separate from state, drawn on top)
- [ ] Top-right: Time/Date display
  - Current time (HH:MM)
  - Day number
  - Season icon
  - Weather icon
- [ ] Bottom-left: Dragon status (exploration mode)
  - Hunger bar
  - Stamina bar
  - Happiness indicator (face icon)
- [ ] Top-left: Player info
  - Gold amount
  - Current location name
- [ ] Bottom-right: Minimap toggle area (placeholder)
- [ ] Bottom-center: Quick inventory (8 slots)
- [ ] Top-center: Notification area (achievements, warnings)
- [ ] HUD elements fade when not relevant
- [ ] Toggle visibility with key (Tab)
- [ ] Different HUD configurations for cafe vs exploration

## Context Files
- src/sprites.py
- src/systems/time_system.py
- src/entities/dragon.py
- src/systems/economy.py
- Dragon_Haven_Cafe_Software_Specification.docx.md (Section 8.2)

## Outputs
- Created: src/ui/hud.py (HUD class)
- Created: src/ui/status_bars.py (health/stamina bar components)
- Modified: src/constants.py (HUD positions, sizes)

---

## Work Log

