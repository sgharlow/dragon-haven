# Task 015: Customer System

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 015 |
| **Status** | done |
| **Branch** | task/015 |
| **Assigned** | task/015 |
| **Depends** | 013 |
| **Blocked-By** | |
| **Estimated** | 75 min |

## Inputs
- src/systems/cafe.py from 013

## Description
Create the customer system that spawns customers during service, handles orders, patience, satisfaction, and tips. Customers are the core of cafe revenue.

## Acceptance Criteria
- [x] Customer class: type, patience, order_preferences, quality_expectation, satisfaction
- [x] Customer types: REGULAR (generic), STORY_CHARACTER (named NPCs)
- [x] Patience timer (seconds before leaving unhappy)
- [x] Spawn rate based on reputation level
- [x] Customer enters, sits, waits for service
- [x] take_order() - customer reveals what they want
- [x] Order preferences based on category (appetizer, main, dessert)
- [x] serve_dish(recipe, quality) - customer evaluates
- [x] Satisfaction calculation:
  - Base from quality vs expectation
  - Speed bonus/penalty
  - Staff efficiency factor
- [x] Tip calculation from satisfaction
- [x] Customer leaves (happy, neutral, or angry)
- [x] Reputation change from customer satisfaction
- [x] Visual states: waiting, eating, leaving

## Context Files
- src/systems/cafe.py
- src/systems/economy.py
- src/constants.py
- Dragon_Haven_Cafe_Software_Specification.docx.md (Section 4.4)

## Outputs
- Created: src/entities/customer.py (Customer class)
- Modified: src/systems/cafe.py (customer spawning, service flow)
- Modified: src/constants.py (customer configs, spawn rates)

---

## Work Log

### 2026-01-17
- Added customer constants to constants.py (states, patience, spawn rates, satisfaction)
- Created Customer class with patience, quality expectations, state machine
- Implemented Order dataclass for order tracking
- Created service flow: seat_at_table, take_order, serve_dish, finish_eating
- Implemented weighted satisfaction calculation (quality, speed, staff efficiency)
- Added tip calculation based on satisfaction
- Implemented reputation change based on customer mood
- Added patience depletion and angry leave mechanism
- Created CustomerManager with singleton pattern
- Implemented reputation-based spawn rate system
- Added full serialization (to_dict/from_dict)
- Updated entities/__init__.py
- All tests pass

