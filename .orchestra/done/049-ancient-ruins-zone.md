# Task 049: Ancient Ruins Zone

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 049 |
| **Status** | done |
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
- [x] Add ZONE_ANCIENT_RUINS to constants.py
- [x] Define zone properties:
  - Required dragon stage: Adolescent
  - Primary resources: Ancient ingredients, rare herbs, crystal formations
  - Special features: Connected to Forest Depths
- [x] Add 8 unique ingredients for Ancient Ruins:
  - ancient_spice - Preserved spices from old storage
  - ruin_moss - Moss with magical properties
  - crystal_flower - Flowers growing from crystal
  - dragon_scale_herb - Herb resembling dragon scales
  - forgotten_grain - Ancient grain variety
  - mystic_mushroom - Glowing underground mushroom
  - ancient_honey - Crystallized ancient honey
  - ruin_berry - Wild berries in ruins
- [x] Add spawn points for the zone (11 regular + 4 weather)
- [x] Add zone to WorldManager with tile map generator
- [x] Add zone renderer colors/visuals in zone_renderer.py
- [x] Add 3 recipes using Ancient Ruins ingredients:
  - ancient_elixir - Mystical beverage
  - dragon_scale_stew - Hearty stew with dragon scale herbs
  - ruins_mystery_bread - Bread with ancient grains
- [x] Add zone to exploration mode navigation via ZONE_CONNECTIONS

## Context Files
- src/constants.py (ZONES, INGREDIENTS, RECIPES)
- src/systems/world.py
- src/ui/zone_renderer.py
- src/states/exploration_mode_state.py

## Outputs
- Modified: src/constants.py (zone, ingredients, recipes, spawn points)
- Modified: src/systems/world.py (zone registration, tile types, map generator)
- Modified: src/ui/zone_renderer.py (zone visuals, tile colors)

---

## Work Log

### Session 1
- Added ZONE_ANCIENT_RUINS constant to constants.py
- Added zone to ALL_ZONES, ZONE_UNLOCK_REQUIREMENTS (adolescent), ZONE_CONNECTIONS
- Added 8 new ingredients specific to Ancient Ruins
- Added 11 spawn points and 4 weather-conditional spawn points
- Added 3 new recipes: ancient_elixir, dragon_scale_stew, ruins_mystery_bread
- Added 5 new TileTypes for ruins (RUIN_FLOOR, RUIN_WALL, CRYSTAL_CLUSTER, OVERGROWN, ANCIENT_PATH)
- Created _generate_ruins_map() method in WorldManager
- Added zone registration with resource points in WorldManager
- Added tile colors and zone theme in ZoneRenderer
