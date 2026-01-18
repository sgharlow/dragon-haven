# Task 011: Resource Spawning System

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 011 |
| **Status** | ready |
| **Branch** | task/011 |
| **Assigned** | |
| **Depends** | 009, 010 |
| **Blocked-By** | |
| **Estimated** | 60 min |

## Inputs
- src/systems/inventory.py from 009
- src/systems/world.py from 010

## Description
Create the resource spawning system that populates zones with gatherable ingredients. Handles spawn points, respawn timers, quality variation, and dragon-assisted gathering.

## Acceptance Criteria
- [ ] SpawnPoint class: position, item_id, spawn_chance, respawn_days, requires_ability
- [ ] ResourceManager class
- [ ] Spawn points defined per zone
- [ ] Common resources: 100% daily spawn
- [ ] Uncommon resources: 50% daily spawn
- [ ] Rare resources: 25% daily spawn, weather-dependent
- [ ] Quality variation (1-5 stars) based on:
  - Season bonuses
  - Weather conditions
  - Random variance
- [ ] gather(spawn_point) method - adds to inventory
- [ ] Dragon ability requirements (some spots need rock_smash, etc.)
- [ ] Visual indicators for available resources
- [ ] Daily respawn logic tied to time system
- [ ] Serialization for save/load (which points are depleted)

## Context Files
- src/systems/inventory.py
- src/systems/world.py
- src/systems/time_system.py
- src/constants.py

## Outputs
- Created: src/systems/resources.py (SpawnPoint, ResourceManager)
- Modified: src/constants.py (ingredient definitions per zone)

---

## Work Log

