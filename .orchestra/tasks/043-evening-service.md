# Task 043: Evening Service Period

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 043 |
| **Status** | done |
| **Branch** | task/043 |
| **Assigned** | task/043 |
| **Depends** | |
| **Blocked-By** | |
| **Estimated** | 90 min |

## Inputs
- src/systems/cafe.py (existing single service)
- src/constants.py (service hours)

## Description
Add evening service period (17:00-21:00) in addition to morning service (10:00-14:00). Players can choose to run one or both services each day, with different customer volumes and preferences.

## Acceptance Criteria
- [x] Add evening service constants:
  - CAFE_EVENING_SERVICE_START = 17
  - CAFE_EVENING_SERVICE_END = 21
  - Evening prep: 16:00-17:00
  - Evening cleanup: 21:00-22:00
- [x] Update CafeManager state machine:
  - Support dual service periods
  - Track which services were run today
  - Reset service stats between periods
- [x] Customer volume differences:
  - Morning: 60% of base volume (lighter)
  - Evening: 100% of base volume (busier)
- [x] Customer preference differences:
  - Morning: Beverages, appetizers popular
  - Evening: Mains, desserts popular
- [x] Add "skip evening service" option with reputation penalty
- [x] Update HUD to show:
  - Current/next service period
  - Time until service starts
- [x] Update day summary to show both service stats
- [x] Ensure save/load tracks both services

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

### Session 1
- Added evening service constants to constants.py:
  - SERVICE_PERIOD_MORNING, SERVICE_PERIOD_EVENING
  - CAFE_EVENING_SERVICE_START = 17, CAFE_EVENING_SERVICE_END = 21
  - CAFE_EVENING_PREP_START = 16, CAFE_EVENING_CLEANUP_END = 22
  - SERVICE_VOLUME_MULTIPLIER (morning: 0.6, evening: 1.0)
  - SERVICE_CATEGORY_PREFERENCE (morning: beverages/appetizers, evening: mains/desserts)
  - CAFE_SKIP_SERVICE_PENALTY = 5, CAFE_SKIP_DAY_PENALTY = 15
- Updated CafeManager (cafe.py):
  - Added dual service period tracking (_morning_stats, _evening_stats)
  - Added service completion flags (_morning_completed, _evening_completed)
  - Added skip flags (_morning_skipped, _evening_skipped)
  - Updated update() to handle both service periods based on time
  - Added skip_morning_service(), skip_evening_service() methods
  - Updated advance_day() to reset all service period state
  - Updated serialization (get_save_state, load_state)
- Updated HUD (hud.py):
  - Enhanced _draw_cafe_info() to show service period status
  - Added service period indicators with colors (completed/skipped/active/pending)
  - Shows time until next service or closes
- Updated CafeModeState (cafe_mode_state.py):
  - Enhanced _draw_service_summary() to show morning/evening/total columns
  - Shows completion/skipped status for each service
  - Passes service_period to customer.take_order()
- Updated Customer system (customer.py):
  - Updated take_order() to accept service_period parameter
  - Adjusts category weights based on SERVICE_CATEGORY_PREFERENCE
