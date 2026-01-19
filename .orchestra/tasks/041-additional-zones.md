# Task 041: Additional World Zones

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 041 |
| **Status** | done |
| **Branch** | task/041 |
| **Assigned** | task/041 |
| **Depends** | 039 |
| **Blocked-By** | Requires Adolescent stage for zone unlock |
| **Estimated** | 180 min |

## Inputs
- src/systems/world.py (existing zone system)
- src/constants.py (zone definitions from 039)

## Description
Add Coastal Shore and Mountain Pass zones (2 of 4 missing zones). Coastal Shore requires Juvenile stage and provides seafood ingredients. Mountain Pass requires Adolescent stage and provides rare herbs and minerals.

## Acceptance Criteria
- [x] Add ZONE_COASTAL_SHORE and ZONE_MOUNTAIN_PASS constants
- [x] Define zone unlock requirements:
  - Coastal Shore: Requires Juvenile (same as Forest)
  - Mountain Pass: Requires Adolescent
- [x] Update zone connections:
  - Forest Depths ↔ Coastal Shore
  - Meadow Fields ↔ Mountain Pass
- [x] Create Coastal Shore zone:
  - Beach/ocean tile themes
  - Fishing spots
  - Tidal pools
  - 6-8 spawn points
- [x] Create Mountain Pass zone:
  - Rocky terrain tiles
  - Alpine flowers
  - Hot springs feature
  - 6-8 spawn points
- [x] Add new ingredients for zones:
  - Coastal: Sea Salt, Fresh Seaweed, Coastal Crab, Pearl Oyster
  - Mountain: Mountain Herb, Rock Honey, Mineral Crystal, Alpine Flower
- [x] Generate sprites for new zone tiles
- [x] Add zone-specific background colors/atmosphere

## Context Files
- src/constants.py
- src/systems/world.py
- src/systems/resources.py
- src/sprites.py
- src/ui/zone_renderer.py

## Outputs
- Modified: src/constants.py (zones, ingredients, spawn points)
- Modified: src/systems/world.py (zone data, connections)
- Modified: src/systems/resources.py (new spawn points)
- Modified: src/sprites.py (zone tiles, ingredients)
- Modified: src/ui/zone_renderer.py (zone rendering)

---

## Work Log

### Session 1
- Added ZONE_COASTAL_SHORE and ZONE_MOUNTAIN_PASS constants
- Updated ALL_ZONES list with new zones
- Added zone unlock requirements (Coastal: Juvenile, Mountain: Adolescent)
- Updated ZONE_CONNECTIONS for bidirectional navigation
- Added 12 new ingredients:
  - Coastal: sea_salt, fresh_seaweed, coastal_crab, pearl_oyster, tidal_clam, beach_berry
  - Mountain: mountain_herb, rock_honey, mineral_crystal, alpine_flower, mountain_moss, hot_spring_egg
- Added ABILITY_GLIDE and ABILITY_FLIGHT constants for spawn requirements
- Added 8 spawn points per zone in ZONE_SPAWN_POINTS
- Added weather spawn points for both zones
- Created new tile types in world.py:
  - Coastal: SAND, SHALLOW_WATER, SEAWEED, TIDAL_POOL
  - Mountain: ROCK, SNOW, ALPINE_FLOWER, HOT_SPRING
- Added zone creation in WorldManager._create_zones()
- Added _generate_coastal_map() and _generate_mountain_map() methods
- Updated can_enter_zone() with full 5-stage progression
- Added tile sprites in sprites.py for all 8 new tile types
- Added tile colors and zone themes in zone_renderer.py
- Added tile rendering in _draw_tile() for new tile types
- Added zone-specific decorations (shells, driftwood, rocks, lichen, crystals)
- Added decoration rendering for new types
