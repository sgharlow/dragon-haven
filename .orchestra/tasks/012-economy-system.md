# Task 012: Economy System

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 012 |
| **Status** | ready |
| **Branch** | task/012 |
| **Assigned** | |
| **Depends** | 009 |
| **Blocked-By** | |
| **Estimated** | 45 min |

## Inputs
- src/systems/inventory.py from 009

## Description
Create the economy system that manages gold, pricing, purchases, and upgrades. Integrates with inventory for financial tracking.

## Acceptance Criteria
- [ ] EconomyManager class with singleton get_economy()
- [ ] Starting gold: 100
- [ ] add_gold(), spend_gold(), can_afford()
- [ ] Price calculation for dishes based on:
  - Base recipe price
  - Quality multiplier (1-5 stars)
  - Reputation bonus
- [ ] Tip calculation based on customer satisfaction
- [ ] Upgrade system:
  - Inventory expansion (+5 slots, 500g)
  - Storage expansion (+50 slots, 1000g)
  - Fridge expansion (+10 slots, 750g)
- [ ] purchase_upgrade() method
- [ ] get_upgrade_cost(), is_upgrade_available()
- [ ] Daily expense tracking (optional)
- [ ] Serialization for save/load

## Context Files
- src/systems/inventory.py
- src/constants.py
- Dragon_Haven_Cafe_Software_Specification.docx.md (Section 7.2)

## Outputs
- Created: src/systems/economy.py (EconomyManager, get_economy)
- Modified: src/constants.py (prices, upgrade costs)

---

## Work Log

