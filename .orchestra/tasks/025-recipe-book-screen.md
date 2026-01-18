# Task 025: Recipe Book Screen

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 025 |
| **Status** | ready |
| **Branch** | task/025 |
| **Assigned** | |
| **Depends** | 004, 016 |
| **Blocked-By** | |
| **Estimated** | 45 min |

## Inputs
- src/sprites.py from 004
- src/systems/recipes.py from 016

## Description
Create the recipe book screen that shows all discovered recipes, their ingredients, and cooking status.

## Acceptance Criteria
- [ ] RecipeBookState extending BaseScreen (or overlay)
- [ ] Category tabs: All, Appetizers, Mains, Desserts, Beverages
- [ ] Recipe list with icons
- [ ] Locked recipes show as ??? with unlock hint
- [ ] Selected recipe shows details:
  - Name and description
  - Difficulty stars
  - Required ingredients (with owned count)
  - Dragon color effect preview
  - Times cooked / Mastery progress
- [ ] "Can Cook" indicator based on inventory
- [ ] Filter: All / Can Cook Now / Mastered
- [ ] Mastered recipes have special badge
- [ ] Dragon color preview (small dragon silhouette showing color shift)
- [ ] Close with ESC

## Context Files
- src/sprites.py
- src/systems/recipes.py
- src/systems/inventory.py
- src/constants.py

## Outputs
- Created: src/states/recipe_book_state.py (RecipeBookState)
- Created: src/ui/recipe_card.py (recipe display component)

---

## Work Log

