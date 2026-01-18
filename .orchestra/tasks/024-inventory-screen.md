# Task 024: Inventory Screen

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 024 |
| **Status** | ready |
| **Branch** | task/024 |
| **Assigned** | |
| **Depends** | 004, 009 |
| **Blocked-By** | |
| **Estimated** | 60 min |

## Inputs
- src/sprites.py from 004
- src/systems/inventory.py from 009

## Description
Create the inventory screen for viewing and managing items. Shows carried inventory, storage, and fridge contents.

## Acceptance Criteria
- [ ] InventoryState extending BaseScreen (or overlay)
- [ ] Tab navigation:
  - Carried (backpack)
  - Storage (cafe storage)
  - Fridge (cold storage)
- [ ] Grid display of items (5 columns)
- [ ] Item slots show:
  - Item icon
  - Quantity
  - Quality stars
  - Spoilage indicator (if applicable)
- [ ] Click item for details popup:
  - Name, description
  - Category
  - Quality
  - Days until spoil
- [ ] Transfer items between inventories (drag or button)
- [ ] Sort options (by name, category, quality)
- [ ] Discard items (with confirmation)
- [ ] Slot count display (used/max)
- [ ] Upgrade button if upgrades available
- [ ] Close with ESC or click outside

## Context Files
- src/sprites.py
- src/systems/inventory.py
- src/constants.py

## Outputs
- Created: src/states/inventory_state.py (InventoryState)
- Created: src/ui/item_slot.py (ItemSlot component)
- Created: src/ui/item_tooltip.py (tooltip popup)

---

## Work Log

