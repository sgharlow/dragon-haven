# Task 041: Additional World Zones

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 041 |
| **Status** | blocked |
| **Branch** | |
| **Assigned** | |
| **Depends** | 039 |
| **Blocked-By** | Requires Adolescent stage for zone unlock |
| **Estimated** | 180 min |

## Inputs
- src/systems/world.py (existing zone system)
- src/constants.py (zone definitions from 039)

## Description
Add Coastal Shore and Mountain Pass zones (2 of 4 missing zones). Coastal Shore requires Juvenile stage and provides seafood ingredients. Mountain Pass requires Adolescent stage and provides rare herbs and minerals.

## Acceptance Criteria
- [ ] Add ZONE_COASTAL_SHORE and ZONE_MOUNTAIN_PASS constants
- [ ] Define zone unlock requirements:
  - Coastal Shore: Requires Juvenile (same as Forest)
  - Mountain Pass: Requires Adolescent
- [ ] Update zone connections:
  - Forest Depths ↔ Coastal Shore
  - Meadow Fields ↔ Mountain Pass
- [ ] Create Coastal Shore zone:
  - Beach/ocean tile themes
  - Fishing spots
  - Tidal pools
  - 6-8 spawn points
- [ ] Create Mountain Pass zone:
  - Rocky terrain tiles
  - Alpine flowers
  - Hot springs feature
  - 6-8 spawn points
- [ ] Add new ingredients for zones:
  - Coastal: Sea Salt, Fresh Seaweed, Coastal Crab, Pearl Oyster
  - Mountain: Mountain Herb, Rock Honey, Mineral Crystal, Alpine Flower
- [ ] Generate sprites for new zone tiles
- [ ] Add zone-specific background colors/atmosphere

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
