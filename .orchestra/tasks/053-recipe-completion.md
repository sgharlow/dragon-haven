# Task 053: Recipe Completion (80+ Total)

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 053 |
| **Status** | ready |
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
- [ ] At least 80 recipes total in RECIPES dict
- [ ] All new recipes have valid ingredients
- [ ] New recipes appear in recipe book
- [ ] New recipes can be cooked in cafe mode
- [ ] Dragon color system works with new recipes
- [ ] Game runs without errors

## Context Files
- `src/constants.py` - Recipe and ingredient definitions
- `src/systems/recipes.py` - Recipe manager

## Outputs
<!-- Filled when complete -->

---
## Work Log
<!-- Appended during work -->
