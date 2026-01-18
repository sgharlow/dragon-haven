# Task 016: Recipe System

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 016 |
| **Status** | in_progress |
| **Branch** | task/016 |
| **Assigned** | task/016 |
| **Depends** | 009 |
| **Blocked-By** | |
| **Estimated** | 60 min |

## Inputs
- src/systems/inventory.py from 009

## Description
Create the recipe system that defines all recipes, their ingredients, unlock conditions, and effects. Recipes are central to both cafe operation and dragon feeding.

## Acceptance Criteria
- [x] Recipe dataclass: id, name, description, category, ingredients, difficulty, base_quality, price_range, dragon_color_influence
- [x] Recipe categories: APPETIZER, MAIN, DESSERT, BEVERAGE
- [x] 12-15 recipes implemented:
  - 4 Appetizers (1-2 star difficulty)
  - 5 Mains (2-4 star difficulty)
  - 4 Desserts (2-3 star difficulty)
  - 2 Beverages (1 star difficulty)
- [x] Ingredient requirements: item_id, quantity, quality_min
- [x] Unlock conditions: reputation level, story progress, discovery
- [x] can_cook(recipe) - checks inventory has ingredients
- [x] get_available_recipes() - recipes player can currently make
- [x] Dragon color influence per recipe (RGB modifiers)
- [x] Recipe discovery through exploration/story
- [x] Mastery tracking (cook 10x with perfect = mastered)

## Context Files
- src/systems/inventory.py
- src/constants.py
- Dragon_Haven_Cafe_Software_Specification.docx.md (Section 4.3, 12.1)

## Outputs
- Created: src/systems/recipes.py (Recipe class, recipe definitions)
- Modified: src/constants.py (recipe data)

---

## Work Log

### 2026-01-17
- Added recipe constants to constants.py (categories, difficulty, mastery settings, unlock types)
- Defined 15 recipes: 4 appetizers, 5 mains, 4 desserts, 2 beverages
- Created IngredientRequirement dataclass for ingredient needs
- Created Recipe dataclass with all fields including dragon color influence
- Created RecipeMastery class for tracking cook counts and perfect cooks
- Implemented RecipeManager with:
  - Recipe access (by ID, category, unlocked status)
  - Cooking checks (can_cook, get_available_recipes)
  - Unlock system (reputation, story, discovery types)
  - Mastery tracking (cook 10x + 5 perfect for mastery)
  - Full serialization (get_state/load_state)
- Updated systems/__init__.py with exports
- All tests pass

