# Task 024: Inventory Screen

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 024 |
| **Status** | done |
| **Branch** | task/024 |
| **Assigned** | task/024 |
| **Depends** | 004, 009 |
| **Blocked-By** | |
| **Estimated** | 60 min |

## Inputs
- src/sprites.py from 004
- src/systems/inventory.py from 009

## Description
Create the inventory screen for viewing and managing items. Shows carried inventory, storage, and fridge contents.

## Acceptance Criteria
- [x] InventoryState extending BaseScreen (or overlay)
- [x] Tab navigation:
  - Carried (backpack)
  - Storage (cafe storage)
  - Fridge (cold storage)
- [x] Grid display of items (5 columns)
- [x] Item slots show:
  - Item icon
  - Quantity
  - Quality stars
  - Spoilage indicator (if applicable)
- [x] Click item for details popup:
  - Name, description
  - Category
  - Quality
  - Days until spoil
- [x] Transfer items between inventories (drag or button)
- [x] Sort options (by name, category, quality)
- [x] Discard items (with confirmation)
- [x] Slot count display (used/max)
- [x] Upgrade button if upgrades available
- [x] Close with ESC or click outside

## Context Files
- src/sprites.py
- src/systems/inventory.py
- src/constants.py

## Outputs
- Created: src/states/inventory_state.py (InventoryState)
- Created: src/ui/item_slot.py (ItemSlot, ItemSlotGrid components)
- Created: src/ui/item_tooltip.py (ItemTooltip, ConfirmDialog)
- Updated: src/ui/__init__.py (exports new components)

---

## Work Log

[2025-01-18] - Started task
- Created ItemSlot with category-colored icons, quantity badges, quality stars, spoilage indicators
- Created ItemSlotGrid for grid display with selection and hover
- Created ItemTooltip with fade animation showing item details
- Created ConfirmDialog for discard confirmation
- Created InventoryState with tab navigation (Carried/Storage/Fridge)
- Implemented transfer, sort, discard actions
- All acceptance criteria complete
