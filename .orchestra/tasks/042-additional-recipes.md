# Task 042: Additional Recipes

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 042 |
| **Status** | done |
| **Branch** | task/042 |
| **Assigned** | task/042 |
| **Depends** | 041 |
| **Blocked-By** | Requires new ingredients from zones |
| **Estimated** | 120 min |

## Inputs
- src/constants.py (new ingredients from 041)
- src/systems/recipes.py (existing recipe system)

## Description
Add 15-20 new recipes using ingredients from new zones and seasons. Focus on seafood dishes (Coastal), mountain cuisine (Mountain Pass), and seasonal specialties (Autumn/Winter comfort foods).

## Acceptance Criteria
- [x] Add 15-20 new recipes (target: 30-35 total) - Added 17 new recipes (32 total)
- [x] Seafood recipes (6):
  - Coastal Chowder (Main, 3-star)
  - Seaweed Salad (Appetizer, 1-star)
  - Grilled Oysters (Appetizer, 2-star)
  - Crab Cakes (Main, 3-star)
  - Ocean Medley (Main, 4-star)
  - Salt-Crusted Fish (Main, 3-star)
- [x] Mountain recipes (5):
  - Mountain Stew (Main, 3-star)
  - Alpine Tea (Beverage, 1-star)
  - Honey Glazed Game (Main, 4-star)
  - Crystal-Infused Dessert (Dessert, 4-star)
  - Rock Honey Pastry (Dessert, 2-star)
- [x] Seasonal recipes (6):
  - Autumn Harvest Soup (Main, 2-star)
  - Mushroom Medley (Main, 3-star)
  - Winter Warmer (Beverage, 2-star)
  - Hearty Root Stew (Main, 3-star)
  - Spiced Berry Cider (Beverage, 2-star)
  - Comfort Casserole (Main, 3-star)
- [x] Define unlock conditions for each recipe
- [x] Add dragon color influences for new recipes
- [x] Update recipe book categories (no changes needed - uses existing categories)

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

### Session 1
- Added 17 new recipes (32 total, up from 15):
  - 6 Seafood recipes using Coastal Shore ingredients
  - 5 Mountain recipes using Mountain Pass ingredients
  - 6 Seasonal recipes for autumn/winter comfort foods
- Unlock conditions:
  - 5 Discovery (found through exploration)
  - 8 Reputation (20-60 reputation requirement)
  - 3 Story (chapter_2 and chapter_3)
  - 1 Default (autumn_harvest_soup)
- Each recipe has unique color_influence for dragon coloring
- Used new ingredients: sea_salt, fresh_seaweed, coastal_crab, pearl_oyster, tidal_clam, beach_berry, mountain_herb, rock_honey, mineral_crystal, alpine_flower, mountain_moss
- Added autumn_harvest_soup to DEFAULT_UNLOCKED_RECIPES
- Recipe difficulties range from 1-4 stars
- Base prices range from 30-160 gold
