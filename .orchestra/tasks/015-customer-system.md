# Task 015: Customer System

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 015 |
| **Status** | ready |
| **Branch** | task/015 |
| **Assigned** | |
| **Depends** | 013 |
| **Blocked-By** | |
| **Estimated** | 75 min |

## Inputs
- src/systems/cafe.py from 013

## Description
Create the customer system that spawns customers during service, handles orders, patience, satisfaction, and tips. Customers are the core of cafe revenue.

## Acceptance Criteria
- [ ] Customer class: type, patience, order_preferences, quality_expectation, satisfaction
- [ ] Customer types: REGULAR (generic), STORY_CHARACTER (named NPCs)
- [ ] Patience timer (seconds before leaving unhappy)
- [ ] Spawn rate based on reputation level
- [ ] Customer enters, sits, waits for service
- [ ] take_order() - customer reveals what they want
- [ ] Order preferences based on category (appetizer, main, dessert)
- [ ] serve_dish(recipe, quality) - customer evaluates
- [ ] Satisfaction calculation:
  - Base from quality vs expectation
  - Speed bonus/penalty
  - Staff efficiency factor
- [ ] Tip calculation from satisfaction
- [ ] Customer leaves (happy, neutral, or angry)
- [ ] Reputation change from customer satisfaction
- [ ] Visual states: waiting, eating, leaving

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

