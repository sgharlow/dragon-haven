# Task 053: Recipe Completion (80+ Total)

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 053 |
| **Status** | done |
| **Branch** | task/053 |
| **Assigned** | |
| **Depends** | none |
| **Blocked-By** | |
| **Estimated** | 2-3 hours |

## Inputs
- Current recipes in `src/constants.py` (76 recipes)
- Existing ingredient definitions

## Description
Add 4-6 new recipes to exceed the 80 recipe target from the original specification.

### Proposed New Recipes
| Recipe | Category | Difficulty | Key Ingredients |
|--------|----------|------------|-----------------|
| Legendary Dragon Feast | Main | 5 | dragon_scale_herb, premium_meat, exotic_spice |
| Mythic Tea Ceremony | Beverage | 4 | premium_tea, rare_flower, honey |
| Ancient Relic Cake | Dessert | 4 | flour, exotic_spice, honey |
| Cloud Puffs | Dessert | 3 | cream, egg, flour |
| Storm Brew | Beverage | 3 | herb, honey, berry |
| Founders' Original | Main | 5 | Secret combination - unlocks via story |

### Implementation Tasks
1. Add 4-6 new recipe definitions to RECIPES dict
2. Ensure all required ingredients exist
3. Set appropriate difficulty levels (3-5 for end-game)
4. Add color influence for dragon feeding
5. Balance pricing based on difficulty

## Acceptance Criteria
- [x] At least 80 recipes total in RECIPES dict (82 total)
- [x] All new recipes have valid ingredients
- [x] New recipes appear in recipe book
- [x] New recipes can be cooked in cafe mode
- [x] Dragon color system works with new recipes
- [x] Game runs without errors

## Context Files
- `src/constants.py` - Recipe and ingredient definitions
- `src/systems/recipes.py` - Recipe manager

## Outputs
Added 6 new legendary tier recipes:
1. `legendary_dragon_feast` - Main, Diff 5, 500g, unlocks at Legendary rep (500)
2. `mythic_tea_ceremony` - Beverage, Diff 4, 300g, unlocks at Legendary rep (500)
3. `ancient_relic_cake` - Dessert, Diff 4, 250g, discovery unlock
4. `cloud_puffs` - Dessert, Diff 3, 85g, default unlock (added to DEFAULT_UNLOCKED_RECIPES)
5. `storm_brew` - Beverage, Diff 3, 75g, discovery unlock
6. `founders_original` - Special, Diff 5, 400g, story unlock (Chapter 8)

Total recipes: 76 -> 82 (+6)

---
## Work Log
- 2026-01-20: Added 6 new legendary tier recipes, validated all ingredients
