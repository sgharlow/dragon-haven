# Task 016: Recipe System

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 016 |
| **Status** | ready |
| **Branch** | task/016 |
| **Assigned** | |
| **Depends** | 009 |
| **Blocked-By** | |
| **Estimated** | 60 min |

## Inputs
- src/systems/inventory.py from 009

## Description
Create the recipe system that defines all recipes, their ingredients, unlock conditions, and effects. Recipes are central to both cafe operation and dragon feeding.

## Acceptance Criteria
- [ ] Recipe dataclass: id, name, description, category, ingredients, difficulty, base_quality, price_range, dragon_color_influence
- [ ] Recipe categories: APPETIZER, MAIN, DESSERT, BEVERAGE
- [ ] 12-15 recipes implemented:
  - 4 Appetizers (1-2 star difficulty)
  - 5 Mains (2-4 star difficulty)
  - 4 Desserts (2-3 star difficulty)
  - 2 Beverages (1 star difficulty)
- [ ] Ingredient requirements: item_id, quantity, quality_min
- [ ] Unlock conditions: reputation level, story progress, discovery
- [ ] can_cook(recipe) - checks inventory has ingredients
- [ ] get_available_recipes() - recipes player can currently make
- [ ] Dragon color influence per recipe (RGB modifiers)
- [ ] Recipe discovery through exploration/story
- [ ] Mastery tracking (cook 10x with perfect = mastered)

## Context Files
- src/systems/inventory.py
- src/constants.py
- Dragon_Haven_Cafe_Software_Specification.docx.md (Section 4.3, 12.1)

## Outputs
- Created: src/systems/recipes.py (Recipe class, recipe definitions)
- Modified: src/constants.py (recipe data)

---

## Work Log

