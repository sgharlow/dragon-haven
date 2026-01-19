# Task 043: Evening Service Period

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 043 |
| **Status** | ready |
| **Branch** | |
| **Assigned** | |
| **Depends** | |
| **Blocked-By** | |
| **Estimated** | 90 min |

## Inputs
- src/systems/cafe.py (existing single service)
- src/constants.py (service hours)

## Description
Add evening service period (17:00-21:00) in addition to morning service (10:00-14:00). Players can choose to run one or both services each day, with different customer volumes and preferences.

## Acceptance Criteria
- [ ] Add evening service constants:
  - CAFE_EVENING_SERVICE_START = 17
  - CAFE_EVENING_SERVICE_END = 21
  - Evening prep: 16:00-17:00
  - Evening cleanup: 21:00-22:00
- [ ] Update CafeManager state machine:
  - Support dual service periods
  - Track which services were run today
  - Reset service stats between periods
- [ ] Customer volume differences:
  - Morning: 60% of base volume (lighter)
  - Evening: 100% of base volume (busier)
- [ ] Customer preference differences:
  - Morning: Beverages, appetizers popular
  - Evening: Mains, desserts popular
- [ ] Add "skip evening service" option with reputation penalty
- [ ] Update HUD to show:
  - Current/next service period
  - Time until service starts
- [ ] Update day summary to show both service stats
- [ ] Ensure save/load tracks both services

## Context Files
- src/constants.py
- src/systems/cafe.py
- src/states/cafe_mode_state.py
- src/ui/hud.py
- src/game_state.py

## Outputs
- Modified: src/constants.py (evening service constants)
- Modified: src/systems/cafe.py (dual service logic)
- Modified: src/states/cafe_mode_state.py (service selection)
- Modified: src/ui/hud.py (service display)

---

## Work Log
