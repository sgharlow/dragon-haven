# Task 022: Cafe Mode UI

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 022 |
| **Status** | ready |
| **Branch** | task/022 |
| **Assigned** | |
| **Depends** | 013, 014, 015, 017, 021 |
| **Blocked-By** | |
| **Estimated** | 90 min |

## Inputs
- src/systems/cafe.py from 013
- src/entities/staff.py from 014
- src/entities/customer.py from 015
- src/ui/cooking_minigame.py from 017
- src/ui/hud.py from 021

## Description
Create the cafe mode screen where players manage cafe operations. Includes kitchen view, serving area, and staff management.

## Acceptance Criteria
- [ ] CafeModeState extending BaseScreen
- [ ] Two main areas:
  - Kitchen (left): cooking station, ingredient access
  - Serving area (right): tables, customers, staff
- [ ] Customer visualization:
  - Tables with seats
  - Customers sitting, waiting, eating, leaving
  - Order bubbles showing what they want
  - Patience meter above head
- [ ] Staff visualization:
  - Staff moving around
  - Morale indicator
  - Current task indicator
- [ ] Interaction system:
  - Click customer to take order
  - Click kitchen to start cooking
  - Click staff to talk/assign
- [ ] Cooking triggers minigame overlay
- [ ] Serve dish by clicking ready food then customer
- [ ] Service timer and customer count display
- [ ] End of service summary
- [ ] Menu management popup

## Context Files
- src/systems/cafe.py
- src/entities/staff.py
- src/entities/customer.py
- src/ui/cooking_minigame.py
- src/ui/hud.py
- Dragon_Haven_Cafe_Software_Specification.docx.md (Section 8)

## Outputs
- Created: src/states/cafe_mode_state.py (CafeModeState)
- Created: src/ui/order_bubble.py (order display)
- Created: src/ui/table.py (table/seating component)

---

## Work Log

