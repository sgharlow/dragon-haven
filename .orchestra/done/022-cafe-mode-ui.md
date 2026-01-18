# Task 022: Cafe Mode UI

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 022 |
| **Status** | done |
| **Branch** | task/022 |
| **Assigned** | task/022 |
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
- [x] CafeModeState extending BaseScreen
- [x] Two main areas:
  - Kitchen (left): cooking station, ingredient access
  - Serving area (right): tables, customers, staff
- [x] Customer visualization:
  - Tables with seats
  - Customers sitting, waiting, eating, leaving
  - Order bubbles showing what they want
  - Patience meter above head
- [x] Staff visualization:
  - Staff moving around
  - Morale indicator
  - Current task indicator
- [x] Interaction system:
  - Click customer to take order
  - Click kitchen to start cooking
  - Click staff to talk/assign
- [x] Cooking triggers minigame overlay
- [x] Serve dish by clicking ready food then customer
- [x] Service timer and customer count display
- [x] End of service summary
- [x] Menu management popup

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

### 2026-01-17
- Created src/ui/order_bubble.py with OrderBubble and PatienceMeter classes
  - OrderBubble shows customer orders with category icons and bobbing animation
  - PatienceMeter displays customer patience with color-coded progress bar
- Created src/ui/table.py with Table, TableSeat, CustomerSprite, and CafeFloor classes
  - Table component with configurable seats and visual representation
  - CustomerSprite for visual representation of seated customers with mood/state
  - CafeFloor manages all tables and customer seating with default 5-table layout
- Created src/states/cafe_mode_state.py with CafeModeState
  - Integrates CafeManager, CustomerManager, StaffManager
  - Kitchen area (left) and serving area (right) layout
  - Cooking minigame integration
  - Staff and customer visualization
  - Interaction system for orders, cooking, and serving
  - Service timer, customer count, and end-of-service summary
- Updated src/ui/__init__.py to export new components
- All tests passed

