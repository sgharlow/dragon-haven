# Task 018: Reputation System

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 018 |
| **Status** | ready |
| **Branch** | task/018 |
| **Assigned** | |
| **Depends** | 013, 015 |
| **Blocked-By** | |
| **Estimated** | 45 min |

## Inputs
- src/systems/cafe.py from 013
- src/entities/customer.py from 015

## Description
Create the reputation system that tracks cafe fame and unlocks content. Reputation determines customer volume, available recipes, and story progression.

## Acceptance Criteria
- [ ] ReputationManager class (can be part of CafeManager)
- [ ] Reputation points: 0-500 (simplified from 0-1000)
- [ ] Reputation levels:
  - Unknown (0-49): 1-2 customers, basic recipes
  - Local Favorite (50-149): 2-4 customers, intermediate recipes
  - Town Attraction (150-299): 3-6 customers, advanced recipes
  - Regional Fame (300-500): 5-8 customers, all recipes
- [ ] Gain reputation from satisfied customers
- [ ] Lose reputation from angry customers or skipped service
- [ ] get_reputation_level() returns current tier
- [ ] get_customer_count_range() based on level
- [ ] Unlock notifications when reaching new levels
- [ ] Reputation decay if cafe not operated (small daily loss)
- [ ] Serialization for save/load

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

