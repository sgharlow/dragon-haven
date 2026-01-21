# Task 056: Ancient Ruins Zone

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 056 |
| **Status** | blocked |
| **Branch** | task/056 |
| **Assigned** | |
| **Depends** | 054 |
| **Blocked-By** | Creature System |
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
- [ ] Zone constant and data defined
- [ ] Zone renders with ruins-themed tiles
- [ ] Zone accessible from Mountain Pass
- [ ] Unlock conditions enforced
- [ ] Special resources spawn correctly
- [ ] Zone creatures present (if creature system complete)
- [ ] Zone appears in zone selection UI
- [ ] Save/load preserves zone state
- [ ] Performance maintained (60 FPS)

## Context Files
- `src/constants.py` - Zone constants
- `src/systems/world.py` - Zone data and connections
- `src/sprites.py` - Tile generation
- `src/systems/resources.py` - Spawn points

## Outputs
<!-- Filled when complete -->

---
## Work Log
<!-- Appended during work -->
