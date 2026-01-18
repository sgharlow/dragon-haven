# Task 010: World/Zone System

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 010 |
| **Status** | ready |
| **Branch** | task/010 |
| **Assigned** | |
| **Depends** | 007, 008 |
| **Blocked-By** | |
| **Estimated** | 75 min |

## Inputs
- src/systems/time_system.py from 007
- src/entities/dragon.py from 008

## Description
Create the world and zone system for exploration. Defines zones, their unlock requirements, navigation, and basic terrain/collision.

## Acceptance Criteria
- [ ] Zone class: id, name, unlock_condition, resource_points, connections
- [ ] 3 zones implemented:
  - CAFE_GROUNDS: Always unlocked, basic resources
  - MEADOW_FIELDS: Requires Hatchling stage
  - FOREST_DEPTHS: Requires Juvenile stage
- [ ] WorldManager class with singleton get_world_manager()
- [ ] Zone unlock checking based on dragon stage
- [ ] get_current_zone(), set_zone()
- [ ] Zone connections (which zones connect to which)
- [ ] Basic tile map system for zone layout (simple grid)
- [ ] Collision detection for boundaries
- [ ] Weather states: Sunny, Cloudy, Rainy (affects resources)
- [ ] Weather probability per day
- [ ] Serialization for save/load

## Context Files
- src/systems/time_system.py
- src/entities/dragon.py
- src/constants.py
- Dragon_Haven_Cafe_Software_Specification.docx.md (Section 5)

## Outputs
- Created: src/systems/world.py (Zone, WorldManager, get_world_manager)
- Modified: src/constants.py (zone definitions, weather config)

---

## Work Log

