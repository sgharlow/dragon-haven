# Task 018: Reputation System

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 018 |
| **Status** | in_progress |
| **Branch** | task/018 |
| **Assigned** | task/018 |
| **Depends** | 013, 015 |
| **Blocked-By** | |
| **Estimated** | 45 min |

## Inputs
- src/systems/cafe.py from 013
- src/entities/customer.py from 015

## Description
Create the reputation system that tracks cafe fame and unlocks content. Reputation determines customer volume, available recipes, and story progression.

## Acceptance Criteria
- [x] ReputationManager class (can be part of CafeManager)
- [x] Reputation points: 0-500 (simplified from 0-1000)
- [x] Reputation levels:
  - Unknown (0-49): 1-2 customers, basic recipes
  - Local Favorite (50-149): 2-4 customers, intermediate recipes
  - Town Attraction (150-299): 3-6 customers, advanced recipes
  - Regional Fame (300-500): 5-8 customers, all recipes
- [x] Gain reputation from satisfied customers
- [x] Lose reputation from angry customers or skipped service
- [x] get_reputation_level() returns current tier
- [x] get_customer_count_range() based on level
- [x] Unlock notifications when reaching new levels
- [x] Reputation decay if cafe not operated (small daily loss)
- [x] Serialization for save/load

## Context Files
- src/systems/cafe.py
- src/entities/customer.py
- src/constants.py
- Dragon_Haven_Cafe_Software_Specification.docx.md (Section 4.5)

## Outputs
- Modified: src/systems/cafe.py (add reputation tracking)
- Modified: src/constants.py (reputation thresholds, rewards)

---

## Work Log

### 2026-01-17
- Added reputation constants to constants.py:
  - 4 reputation levels (Unknown, Local Favorite, Town Attraction, Regional Fame)
  - Customer count ranges per level
  - Rep gain/loss values for customer satisfaction
  - Daily decay value
  - Level up unlocks (recipes)
- Expanded CafeManager with full reputation tracking:
  - add_reputation() with level change detection and unlock tracking
  - get_reputation_level() returns current tier
  - get_reputation_level_name() for display
  - get_reputation_progress() for UI progress bars
  - get_customer_count_range() based on current level
  - apply_customer_feedback() converts satisfaction to rep change
  - apply_daily_decay() for days cafe isn't operated
- Full serialization included in get_save_state()/load_state()
- All tests pass

