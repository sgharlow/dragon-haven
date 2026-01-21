# Task 054: Creature System

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 054 |
| **Status** | done |
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
- [x] Creature entity class created
- [x] CreatureManager singleton implemented
- [x] At least 5 creature types defined
- [x] Creatures spawn in appropriate zones
- [x] Creatures have basic AI behaviors
- [x] Dragon abilities affect creatures (Creature Scare, etc.)
- [x] Creatures render with procedural sprites
- [x] Creature state persists in save/load
- [x] Performance: 60 FPS with 10+ creatures on screen

## Context Files
- `src/entities/` - Entity patterns
- `src/systems/world.py` - Zone data
- `src/states/exploration_mode_state.py` - Exploration rendering
- `src/sprites.py` - Procedural sprite generation

## Outputs
Created `src/entities/creature.py` with:
- `Creature` dataclass with position, AI state, behavior patterns
- AI behaviors: patrol, flee, guard, follow, stationary
- `scare()` and `interact()` methods for dragon ability integration
- `draw()` method for procedural creature sprites
- `to_dict()`/`from_dict()` for save/load serialization

Created `CreatureManager` singleton with:
- Zone-based creature spawning from `CREATURE_SPAWN_POINTS`
- Active creature tracking and updates
- `use_ability_on_creatures()` for dragon ability effects
- `get_nearby_creature()` for interaction detection
- Save/load state management

Added to `src/constants.py`:
- 5 creature types: Forest Sprite, Wild Boar, Cliff Bird, Shore Crab, Cave Bat
- Creature behavior constants (patrol, flee, guard, follow, stationary)
- `CREATURE_DATA` with name, behavior, hostile, zones, drops, dragon_ability, color, speed
- `CREATURE_SPAWN_POINTS` for each zone
- Creature interaction reward constants

---
## Work Log
- 2026-01-20: Implemented core creature system with 5 types, AI behaviors, and manager
