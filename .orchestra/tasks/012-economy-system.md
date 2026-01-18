# Task 012: Economy System

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 012 |
| **Status** | done |
| **Branch** | task/012 |
| **Assigned** | task/012 |
| **Depends** | 009 |
| **Blocked-By** | |
| **Estimated** | 45 min |

## Inputs
- src/systems/inventory.py from 009

## Description
Create the economy system that manages gold, pricing, purchases, and upgrades. Integrates with inventory for financial tracking.

## Acceptance Criteria
- [x] EconomyManager class with singleton get_economy()
- [x] Starting gold: 100
- [x] add_gold(), spend_gold(), can_afford()
- [x] Price calculation for dishes based on:
  - Base recipe price
  - Quality multiplier (1-5 stars)
  - Reputation bonus
- [x] Tip calculation based on customer satisfaction
- [x] Upgrade system:
  - Inventory expansion (+5 slots, 500g)
  - Storage expansion (+50 slots, 1000g)
  - Fridge expansion (+10 slots, 750g)
- [x] purchase_upgrade() method
- [x] get_upgrade_cost(), is_upgrade_available()
- [x] Daily expense tracking (optional)
- [x] Serialization for save/load

## Context Files
- src/systems/inventory.py
- src/constants.py
- Dragon_Haven_Cafe_Software_Specification.docx.md (Section 7.2)

## Outputs
- Created: src/systems/economy.py (EconomyManager, get_economy)
- Modified: src/constants.py (prices, upgrade costs)

---

## Work Log

### 2026-01-17
- Added economy constants to constants.py (quality multipliers, tip rates, upgrades)
- Created EconomyManager class with singleton pattern
- Implemented gold management delegating to Inventory
- Implemented price calculation with quality and reputation modifiers
- Implemented tip calculation based on customer satisfaction
- Created upgrade system with 3 upgrade types (backpack, storage, fridge)
- Added transaction tracking and daily/total summaries
- Implemented full serialization (get_state/load_state)
- Updated systems/__init__.py
- All tests pass

