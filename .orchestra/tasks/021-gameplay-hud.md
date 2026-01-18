# Task 021: Gameplay HUD

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 021 |
| **Status** | done |
| **Branch** | task/021 |
| **Assigned** | task/021 |
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
- [x] HUD class (separate from state, drawn on top)
- [x] Top-right: Time/Date display
  - Current time (HH:MM)
  - Day number
  - Season icon
  - Weather icon
- [x] Bottom-left: Dragon status (exploration mode)
  - Hunger bar
  - Stamina bar
  - Happiness indicator (face icon)
- [x] Top-left: Player info
  - Gold amount
  - Current location name
- [x] Bottom-right: Minimap toggle area (placeholder)
- [x] Bottom-center: Quick inventory (8 slots)
- [x] Top-center: Notification area (achievements, warnings)
- [x] HUD elements fade when not relevant
- [x] Toggle visibility with key (Tab)
- [x] Different HUD configurations for cafe vs exploration

## Context Files
- src/sprites.py
- src/systems/time_system.py
- src/entities/dragon.py
- src/systems/economy.py
- Dragon_Haven_Cafe_Software_Specification.docx.md (Section 8.2)

## Outputs
- Created: src/ui/hud.py (HUD class with exploration/cafe modes)
- Created: src/ui/status_bars.py (StatusBar, DragonStatusBars, QuickInventoryBar)
- Modified: src/constants.py (HUD layout positions, colors, notification types)
- Modified: src/ui/__init__.py (export new components)

---

## Work Log

### 2026-01-17
- Added HUD constants to constants.py (layout positions, colors, notification types)
- Created status_bars.py with StatusBar, DragonStatusBars, QuickInventorySlot, QuickInventoryBar
- Created hud.py with full HUD class implementation
- Top-right: Time display with day number, season/weather icons
- Top-left: Player info with gold and location
- Bottom-left: Dragon status bars (hunger, stamina, happiness) with mood display
- Bottom-center: 8-slot quick inventory with keyboard (1-8) and mouse selection
- Top-center: Notification system with fade animations
- Bottom-right: Minimap placeholder (toggle with M key)
- Tab key toggles HUD visibility
- Two modes: exploration (full HUD) and cafe (simplified)
- Updated ui/__init__.py to export all new components
- All tests pass

