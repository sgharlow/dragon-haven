# Task 011: Resource Spawning System

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 011 |
| **Status** | done |
| **Branch** | task/011 |
| **Assigned** | task/011 |
| **Depends** | 009, 010 |
| **Blocked-By** | |
| **Estimated** | 60 min |

## Inputs
- src/systems/inventory.py from 009
- src/systems/world.py from 010

## Description
Create the resource spawning system that populates zones with gatherable ingredients. Handles spawn points, respawn timers, quality variation, and dragon-assisted gathering.

## Acceptance Criteria
- [x] SpawnPoint class: position, item_id, spawn_chance, respawn_days, requires_ability
- [x] ResourceManager class
- [x] Spawn points defined per zone
- [x] Common resources: 100% daily spawn
- [x] Uncommon resources: 50% daily spawn
- [x] Rare resources: 25% daily spawn, weather-dependent
- [x] Quality variation (1-5 stars) based on:
  - Season bonuses
  - Weather conditions
  - Random variance
- [x] gather(spawn_point) method - adds to inventory
- [x] Dragon ability requirements (some spots need rock_smash, etc.)
- [x] Visual indicators for available resources
- [x] Daily respawn logic tied to time system
- [x] Serialization for save/load (which points are depleted)

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

### 2026-01-17
- Added resource spawning constants to constants.py (rarity tiers, quality bonuses)
- Defined 14 ingredient types across 3 zones
- Defined 21 spawn points across all zones with positions, rarities, and ability requirements
- Created SpawnPoint class with spawn chance, respawn timers, quality calculation
- Implemented quality variation based on season, weather, and random variance (1-5 stars)
- Created ResourceManager class with singleton access
- Implemented gathering with inventory integration and ability checking
- Added visual indicator system for UI
- Implemented daily respawn logic with weather influence on rare spawns
- Added full serialization (get_state/load_state)
- Updated systems/__init__.py with new exports
- All tests pass

