# Task 042: Additional Recipes

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 042 |
| **Status** | blocked |
| **Branch** | |
| **Assigned** | |
| **Depends** | 041 |
| **Blocked-By** | Requires new ingredients from zones |
| **Estimated** | 120 min |

## Inputs
- src/constants.py (new ingredients from 041)
- src/systems/recipes.py (existing recipe system)

## Description
Add 15-20 new recipes using ingredients from new zones and seasons. Focus on seafood dishes (Coastal), mountain cuisine (Mountain Pass), and seasonal specialties (Autumn/Winter comfort foods).

## Acceptance Criteria
- [ ] Add 15-20 new recipes (target: 30-35 total)
- [ ] Seafood recipes (5-6):
  - Coastal Chowder (Main, 3-star)
  - Seaweed Salad (Appetizer, 1-star)
  - Grilled Oysters (Appetizer, 2-star)
  - Crab Cakes (Main, 3-star)
  - Ocean Medley (Main, 4-star)
  - Salt-Crusted Fish (Main, 3-star)
- [ ] Mountain recipes (4-5):
  - Mountain Stew (Main, 3-star)
  - Alpine Tea (Beverage, 1-star)
  - Honey Glazed Game (Main, 4-star)
  - Crystal-Infused Dessert (Dessert, 4-star)
  - Rock Honey Pastry (Dessert, 2-star)
- [ ] Seasonal recipes (5-6):
  - Autumn Harvest Soup (Main, 2-star)
  - Mushroom Medley (Main, 3-star)
  - Winter Warmer (Beverage, 2-star)
  - Hearty Root Stew (Main, 3-star)
  - Spiced Berry Cider (Beverage, 2-star)
  - Comfort Casserole (Main, 3-star)
- [ ] Define unlock conditions for each recipe
- [ ] Add dragon color influences for new recipes
- [ ] Update recipe book categories

## Context Files
- src/constants.py
- src/systems/recipes.py
- src/states/recipe_book_state.py

## Outputs
- Modified: src/constants.py (recipe definitions)
- Modified: src/systems/recipes.py (recipe manager)
- Modified: src/states/recipe_book_state.py (display updates)

---

## Work Log
