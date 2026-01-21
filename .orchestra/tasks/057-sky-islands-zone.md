# Task 057: Sky Islands Zone

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 057 |
| **Status** | blocked |
| **Branch** | task/057 |
| **Assigned** | |
| **Depends** | 054, 056 |
| **Blocked-By** | Creature System, Ancient Ruins Zone |
| **Estimated** | 4-6 hours |

## Inputs
- Zone system in `src/systems/world.py`
- Dragon flight ability
- Creature system from task 054

## Description
Add the Sky Islands zone - the final end-game area requiring an Adult dragon with Full Flight ability.

### Zone Details
- **Name:** Sky Islands
- **Unlock Requirement:** Adult dragon + Full Flight ability
- **Theme:** Floating islands above the clouds
- **Size:** Multi-island layout (4-5 islands)
- **Connections:** Special access from any outdoor zone (flight)

### Unique Features
1. **Flight-Based Traversal:**
   - Islands connected by flight paths
   - Cannot walk between islands
   - Flight stamina management

2. **Special Resources (Legendary tier):**
   - Sky Berries (rare fruit)
   - Cloud Essence (magical ingredient)
   - Starlight Crystals (ultimate rare)
   - Phoenix Feathers (legendary)

3. **Creatures:**
   - Sky Serpents (majestic, non-hostile)
   - Cloud Wisps (guide to resources)
   - Storm Hawks (challenge for rewards)

4. **Weather:**
   - Always clear/special (above storm clouds)
   - Unique sky visuals

5. **End-Game Content:**
   - Legendary ingredient farming
   - Final story revelation location
   - Ultimate recipes require Sky Island ingredients

### Implementation Tasks
1. Add ZONE_SKY_ISLANDS constant
2. Create multi-island zone layout
3. Implement island-to-island flight mechanics
4. Define legendary spawn points
5. Create sky-themed procedural tiles (clouds, sky, islands)
6. Add flight-based zone entry (not walking)
7. Add zone-specific creatures
8. Create unique weather/atmosphere

## Acceptance Criteria
- [ ] Zone constant and data defined
- [ ] Zone renders with sky/cloud theme
- [ ] Zone only accessible with Adult dragon + Flight
- [ ] Flight traversal between islands works
- [ ] Legendary resources spawn correctly
- [ ] Zone creatures present
- [ ] Unique atmosphere/visuals
- [ ] Save/load preserves zone state
- [ ] Performance maintained (60 FPS)

## Context Files
- `src/constants.py` - Zone constants
- `src/systems/world.py` - Zone data
- `src/sprites.py` - Tile generation
- `src/entities/dragon.py` - Flight ability

## Outputs
<!-- Filled when complete -->

---
## Work Log
<!-- Appended during work -->
