# Task 049: Ancient Ruins Zone

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 049 |
| **Status** | ready |
| **Branch** | task/049 |
| **Depends** | |
| **Blocked-By** | |
| **Estimated** | 90 min |

## Inputs
- Spec: Zone requires Adolescent dragon stage
- Spec: Contains special ingredients, recipes, puzzles, lore collectibles
- src/systems/world.py (zone system)
- src/constants.py (zone definitions)

## Description
Add the Ancient Ruins zone, accessible with an Adolescent+ dragon. This mysterious zone contains ancient structures, special ingredients, and lore about dragons and the world's history.

## Acceptance Criteria
- [ ] Add ZONE_ANCIENT_RUINS to constants.py
- [ ] Define zone properties:
  - Required dragon stage: Adolescent
  - Primary resources: Ancient ingredients, rare herbs, crystal formations
  - Special features: Puzzles, lore items
- [ ] Add 6-8 unique ingredients for Ancient Ruins:
  - ancient_spice - Preserved spices from old storage
  - ruin_moss - Moss with magical properties
  - crystal_flower - Flowers growing from crystal
  - dragon_scale_herb - Herb resembling dragon scales
  - forgotten_grain - Ancient grain variety
  - mystic_mushroom - Glowing underground mushroom
- [ ] Add spawn points for the zone
- [ ] Add zone to WorldManager
- [ ] Add zone renderer colors/visuals in zone_renderer.py
- [ ] Add 2-3 recipes using Ancient Ruins ingredients
- [ ] Add zone to exploration mode navigation

## Context Files
- src/constants.py (ZONES, INGREDIENTS, RECIPES)
- src/systems/world.py
- src/ui/zone_renderer.py
- src/states/exploration_mode_state.py

## Outputs
- Modified: src/constants.py (zone, ingredients, recipes, spawn points)
- Modified: src/systems/world.py (zone registration)
- Modified: src/ui/zone_renderer.py (zone visuals)
- Modified: src/states/exploration_mode_state.py (navigation)

---

## Work Log

