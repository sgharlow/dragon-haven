# Task 054: Creature System

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 054 |
| **Status** | blocked |
| **Branch** | task/054 |
| **Assigned** | |
| **Depends** | 052, 053 |
| **Blocked-By** | |
| **Estimated** | 6-8 hours |

## Inputs
- Exploration mode state in `src/states/exploration_mode_state.py`
- Dragon abilities system
- Zone/world system

## Description
Add wildlife creatures to exploration zones that interact with dragon abilities, bringing the world to life.

### Creature Types
| Creature | Zones | Behavior | Dragon Interaction |
|----------|-------|----------|-------------------|
| Forest Sprites | Forest, Meadow | Friendly, give hints | Feed for bonus items |
| Wild Boars | Forest, Mountain | Aggressive, block paths | Creature Scare to clear |
| Cliff Birds | Mountain, Coastal | Neutral, carry items | Flight to reach nests |
| Shore Crabs | Coastal | Defensive, guard resources | Rock Smash to reveal |
| Cave Bats | Crystal Cave | Skittish, flee from light | Ember Breath reveals hidden areas |

### Implementation Tasks
1. Create `Creature` entity class with:
   - Position, behavior state, sprite
   - AI patterns (patrol, flee, guard, follow)
   - Interaction methods
2. Create `CreatureManager` singleton for:
   - Spawning creatures per zone
   - Updating creature AI
   - Handling interactions
3. Add creature spawn points to zone data
4. Implement creature AI behaviors:
   - Patrol: Move between waypoints
   - Flee: Run from player/dragon
   - Guard: Block access until cleared
   - Follow: Accompany player temporarily
5. Connect dragon abilities to creature interactions
6. Add creature sprites to procedural generation
7. Update exploration state to render and update creatures

## Acceptance Criteria
- [ ] Creature entity class created
- [ ] CreatureManager singleton implemented
- [ ] At least 5 creature types defined
- [ ] Creatures spawn in appropriate zones
- [ ] Creatures have basic AI behaviors
- [ ] Dragon abilities affect creatures (Creature Scare, etc.)
- [ ] Creatures render with procedural sprites
- [ ] Creature state persists in save/load
- [ ] Performance: 60 FPS with 10+ creatures on screen

## Context Files
- `src/entities/` - Entity patterns
- `src/systems/world.py` - Zone data
- `src/states/exploration_mode_state.py` - Exploration rendering
- `src/sprites.py` - Procedural sprite generation

## Outputs
<!-- Filled when complete -->

---
## Work Log
<!-- Appended during work -->
