# Task 009: Inventory System

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 009 |
| **Status** | done |
| **Branch** | task/009 |
| **Assigned** | task/009 |
| **Depends** | 001 |
| **Blocked-By** | |
| **Estimated** | 60 min |

## Inputs
- src/constants.py from 001

## Description
Create the inventory system for managing items, ingredients, storage, and the recipe book. Includes carried inventory (exploration) and cafe storage.

## Acceptance Criteria
- [x] Item dataclass: id, name, category, quality, stack_size, spoil_days
- [x] Item categories: VEGETABLE, FRUIT, GRAIN, MEAT, SEAFOOD, DAIRY, SPICE, SPECIAL
- [x] Inventory class:
  - Carried slots (20 default)
  - Storage slots (100 default)
  - Fridge slots (30 default, prevents spoilage)
- [x] add_item(), remove_item(), has_item(), get_count()
- [x] transfer_to_storage(), transfer_from_storage()
- [x] Spoilage system (items decay over days unless in fridge)
- [x] Recipe book: unlocked_recipes, mastered_recipes
- [x] Gold tracking
- [x] Singleton get_inventory()
- [x] Serialization for save/load

## Context Files
- src/constants.py
- Dragon_Haven_Cafe_Software_Specification.docx.md (Section 7)

## Outputs
- Created: src/systems/inventory.py (Item, Inventory, get_inventory)
- Modified: src/constants.py (item definitions, inventory sizes)

---

## Work Log

### 2026-01-17
- Added inventory constants to constants.py (categories, capacities, defaults)
- Created Item dataclass with quality, spoilage, pricing, color influence
- Created ItemStack class for stacked items with spoilage tracking
- Created InventoryContainer for slot-based storage with spoilage handling
- Created Inventory class managing carried, storage, and fridge containers
- Implemented item add/remove/transfer operations
- Implemented spoilage system (advance_day removes spoiled items)
- Added gold tracking with add_gold, spend_gold, can_afford
- Added recipe book with unlock_recipe, master_recipe tracking
- Implemented full serialization (get_state/load_state)
- Updated systems/__init__.py
- All tests pass
