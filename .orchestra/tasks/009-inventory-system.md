# Task 009: Inventory System

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 009 |
| **Status** | ready |
| **Branch** | task/009 |
| **Assigned** | |
| **Depends** | 001 |
| **Blocked-By** | |
| **Estimated** | 60 min |

## Inputs
- src/constants.py from 001

## Description
Create the inventory system for managing items, ingredients, storage, and the recipe book. Includes carried inventory (exploration) and cafe storage.

## Acceptance Criteria
- [ ] Item dataclass: id, name, category, quality, stack_size, spoil_days
- [ ] Item categories: VEGETABLE, FRUIT, GRAIN, MEAT, SEAFOOD, DAIRY, SPICE, SPECIAL
- [ ] Inventory class:
  - Carried slots (20 default, upgradeable)
  - Storage slots (100 default)
  - Fridge slots (30 default, prevents spoilage)
- [ ] add_item(), remove_item(), has_item(), get_count()
- [ ] transfer_to_storage(), transfer_from_storage()
- [ ] Spoilage system (items decay over days unless in fridge)
- [ ] Recipe book: unlocked_recipes, mastered_recipes
- [ ] Gold tracking
- [ ] Singleton get_inventory()
- [ ] Serialization for save/load

## Context Files
- src/constants.py
- Dragon_Haven_Cafe_Software_Specification.docx.md (Section 7)

## Outputs
- Created: src/systems/inventory.py (Item, Inventory, get_inventory)
- Modified: src/constants.py (item definitions, inventory sizes)

---

## Work Log

