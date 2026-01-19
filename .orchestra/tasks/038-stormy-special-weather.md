# Task 038: Stormy & Special Weather

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 038 |
| **Status** | ready |
| **Branch** | |
| **Assigned** | |
| **Depends** | 037 |
| **Blocked-By** | |
| **Estimated** | 90 min |

## Inputs
- src/constants.py (weather config from 037)
- src/systems/world.py (weather effects)

## Description
Add Stormy and Special weather states. Stormy weather closes the cafe and makes exploration dangerous but yields rare resources. Special weather triggers unique events with legendary item spawns.

## Acceptance Criteria
- [ ] Add WEATHER_STORMY and WEATHER_SPECIAL constants
- [ ] Update weather probabilities per season (10% stormy, 5% special)
- [ ] Stormy weather effects:
  - Cafe automatically closed
  - Exploration has danger warnings
  - Spawn "storm flowers" and "lightning crystals" resources
  - Visual effects (dark overlay, rain animation)
- [ ] Special weather effects:
  - Unique events (meteor shower, rainbow, etc.)
  - Spawn legendary ingredients
  - Notification/celebration UI
- [ ] Add storm warning notification (1 hour before)
- [ ] Update HUD weather display for new types
- [ ] Add new ingredients: Storm Flower, Lightning Crystal

## Context Files
- src/constants.py
- src/systems/world.py
- src/systems/cafe.py
- src/states/exploration_mode_state.py
- src/ui/hud.py

## Outputs
- Modified: src/constants.py (weather types, ingredients)
- Modified: src/systems/world.py (weather effects)
- Modified: src/systems/cafe.py (storm closure)
- Modified: src/ui/hud.py (weather icons)
- Modified: src/sprites.py (weather visuals)

---

## Work Log
