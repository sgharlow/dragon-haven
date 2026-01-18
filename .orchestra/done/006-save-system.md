# Task 006: Save System Foundation

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 006 |
| **Status** | done |
| **Branch** | task/006 |
| **Assigned** | task/006 |
| **Depends** | 001 |
| **Blocked-By** | |
| **Estimated** | 45 min |

## Inputs
- src/constants.py from 001

## Description
Create the foundation for save/load system. Defines save data structure, serialization, and file handling. Actual game data will be added as systems are built.

## Acceptance Criteria
- [x] SaveManager class with singleton get_save_manager()
- [x] 3 save slots supported
- [x] SaveData dataclass with:
  - Meta: slot, version, playtime, last_saved
  - Placeholder sections for: player, dragon, cafe, world, story, inventory
- [x] save(slot) method - writes JSON to saves/slot_N.json
- [x] load(slot) method - reads and validates
- [x] list_saves() - returns info about existing saves
- [x] delete_save(slot) method
- [x] Version compatibility checking

## Context Files
- src/constants.py

## Outputs
- Created: src/save_manager.py (SaveManager, SaveData, get_save_manager)
- Created: saves/ directory (gitignored)

---

## Work Log

### 2026-01-17
- Created SaveManager class with singleton pattern
- Defined SaveData dataclass with nested dataclasses for each section:
  - SaveMeta: slot, version, playtime_seconds, timestamps
  - PlayerData: name, stats
  - DragonData: name, stage, age, color, stats, abilities
  - CafeData: gold, reputation, level, recipes, staff
  - WorldData: zone, day, time, weather, discoveries
  - StoryData: chapter, events, relationships, flags
  - InventoryData: items dict, max slots
- Implemented save() with JSON serialization and metadata auto-update
- Implemented load() with version compatibility checking
- Implemented list_saves() returning SaveSlotInfo for UI
- Implemented delete_save() for slot deletion
- Added has_any_saves() and get_most_recent_slot() helpers
- All tests pass
