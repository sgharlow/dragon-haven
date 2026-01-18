# Task 025: Recipe Book Screen

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 025 |
| **Status** | done |
| **Branch** | task/025 |
| **Assigned** | task/025 |
| **Depends** | 004, 016 |
| **Blocked-By** | |
| **Estimated** | 45 min |

## Inputs
- src/sprites.py from 004
- src/systems/recipes.py from 016

## Description
Create the recipe book screen that shows all discovered recipes, their ingredients, and cooking status.

## Acceptance Criteria
- [x] RecipeBookState extending BaseScreen (or overlay)
- [x] Category tabs: All, Appetizers, Mains, Desserts, Beverages
- [x] Recipe list with icons
- [x] Locked recipes show as ??? with unlock hint
- [x] Selected recipe shows details:
  - Name and description
  - Difficulty stars
  - Required ingredients (with owned count)
  - Dragon color effect preview
  - Times cooked / Mastery progress
- [x] "Can Cook" indicator based on inventory
- [x] Filter: All / Can Cook Now / Mastered
- [x] Mastered recipes have special badge
- [x] Dragon color preview (small dragon silhouette showing color shift)
- [x] Close with ESC

## Context Files
- src/sprites.py
- src/systems/recipes.py
- src/systems/inventory.py
- src/constants.py

## Outputs
- Created: src/states/recipe_book_state.py (RecipeBookState)
- Created: src/ui/recipe_card.py (RecipeCard, RecipeDetailPanel)
- Updated: src/ui/__init__.py (exports new components)

---

## Work Log

[2025-01-18] - Completed task
- Created RecipeCard with category icons, difficulty stars, can_cook indicator, mastered badge
- Created RecipeDetailPanel showing full recipe info with ingredients, dragon color preview, mastery progress
- Created RecipeBookState with category tabs (All/Appetizer/Main/Dessert/Beverage)
- Implemented filters (All/Can Cook/Mastered)
- Added scroll support, keyboard navigation, ESC to close
- All acceptance criteria complete
