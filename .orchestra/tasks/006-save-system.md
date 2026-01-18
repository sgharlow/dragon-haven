# Task 006: Save System Foundation

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 006 |
| **Status** | ready |
| **Branch** | task/006 |
| **Assigned** | |
| **Depends** | 001 |
| **Blocked-By** | |
| **Estimated** | 45 min |

## Inputs
- src/constants.py from 001

## Description
Create the foundation for save/load system. Defines save data structure, serialization, and file handling. Actual game data will be added as systems are built.

## Acceptance Criteria
- [ ] SaveManager class with singleton get_save_manager()
- [ ] 3 save slots supported
- [ ] SaveData dataclass with:
  - Meta: slot, version, playtime, last_saved
  - Placeholder sections for: player, dragon, cafe, world, story
- [ ] save(slot) method - writes JSON to saves/slot_N.json
- [ ] load(slot) method - reads and validates
- [ ] list_saves() - returns info about existing saves
- [ ] delete_save(slot) method
- [ ] Version compatibility checking

## Context Files
- src/constants.py

## Outputs
- Created: src/save_manager.py (SaveManager, SaveData, get_save_manager)
- Created: saves/ directory (gitignored)

---

## Work Log

