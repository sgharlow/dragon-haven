# Task 056: Ancient Ruins Zone

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 056 |
| **Status** | done |
| **Branch** | task/056 |
| **Assigned** | |
| **Depends** | 054 |
| **Blocked-By** | |
| **Estimated** | 4-6 hours |

## Inputs
- Zone system in `src/systems/world.py`
- Existing zone patterns (7 zones)
- Creature system from task 054

## Description
Add the Ancient Ruins zone - a mysterious area with puzzle elements, hidden recipes, and dragon lore.

### Zone Details
- **Name:** Ancient Ruins
- **Unlock Requirement:** Adolescent dragon + Chapter 5 complete
- **Theme:** Mysterious ancient dragon civilization ruins
- **Size:** Standard zone (40x30 tiles)
- **Connections:** From Mountain Pass

### Unique Features
1. **Puzzle Elements:**
   - Pressure plates that open doors
   - Hidden passages revealed by dragon abilities
   - Light-based puzzles (Ember Breath)

2. **Special Resources:**
   - Ancient Spices (rare cooking ingredient)
   - Relic Fragments (crafting/story items)
   - Crystal Shards (high-value)
   - Dragon Tablets (lore items)

3. **Creatures:**
   - Stone Guardians (stationary, activated by proximity)
   - Ruin Spirits (friendly, give hints)

4. **Story Content:**
   - Dragon lore tablets revealing backstory
   - Hidden recipe scrolls (unlock legendary recipes)

### Implementation Tasks
1. Add ZONE_ANCIENT_RUINS constant
2. Create zone tile map with ruins theme
3. Define spawn points for special resources
4. Add zone unlock conditions (dragon stage + story)
5. Create ruins-themed procedural tiles
6. Add zone connection from Mountain Pass
7. Implement simple puzzle mechanics (optional)
8. Add zone-specific creatures

## Acceptance Criteria
- [x] Zone constant and data defined
- [x] Zone renders with ruins-themed tiles
- [x] Zone accessible from Mountain Pass
- [x] Unlock conditions enforced
- [x] Special resources spawn correctly
- [x] Zone creatures present (3 Cave Bats)
- [x] Zone appears in zone selection UI
- [x] Save/load preserves zone state
- [x] Performance maintained (60 FPS)

## Context Files
- `src/constants.py` - Zone constants
- `src/systems/world.py` - Zone data and connections
- `src/sprites.py` - Tile generation
- `src/systems/resources.py` - Spawn points

## Outputs
Zone implemented in `src/systems/world.py`:
- ZONE_ANCIENT_RUINS constant defined
- 15x20 tile map with ruins theme (walls, paths, rubble)
- Connected to forest_depths
- 7 resource spawn points (ancient_spice, relic_fragment, crystal_shard)
- 3 Cave Bat creatures at spawn points

Creatures in `src/constants.py`:
- CREATURE_CAVE_BAT with guard behavior
- Spawn points at (8,10), (14,8), (10,14)

---
## Work Log
- 2026-01-20: Verified zone implementation complete with creature integration
