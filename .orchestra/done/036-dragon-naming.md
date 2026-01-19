# Task 036: Dragon Naming System

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 036 |
| **Status** | done |
| **Branch** | task/036 |
| **Assigned** | task/036 |
| **Depends** | |
| **Blocked-By** | |
| **Estimated** | 60 min |

## Inputs
- src/entities/dragon.py (existing dragon system)
- src/systems/story.py (for hatch event)

## Description
Add the ability for players to name their dragon. The naming prompt appears when the egg hatches. Dragon name is displayed in HUD and all references. Players can also rename from the dragon status screen.

## Acceptance Criteria
- [x] Add `name` field to Dragon entity (default: "Dragon")
- [x] Add name validation (max 20 chars, no empty)
- [x] Create naming prompt UI component
- [x] Trigger naming prompt during egg hatch story event
- [x] Update HUD to show dragon name instead of generic "Dragon"
- [x] Add rename option to dragon status screen
- [x] Save/load dragon name correctly
- [x] Update all dragon references in UI to use name

## Context Files
- src/entities/dragon.py
- src/systems/story.py
- src/states/dragon_status_state.py
- src/ui/hud.py
- src/constants.py

## Outputs
- Modified: src/constants.py (DRAGON_NAME_MAX_LENGTH, DRAGON_NAME_DEFAULT)
- Modified: src/entities/dragon.py (get_name, set_name, validate_name methods)
- Modified: src/ui/hud.py (dragon name display - already supported)
- Modified: src/states/dragon_status_state.py (rename via dragon manager)
- Created: src/systems/dragon_manager.py (centralized dragon management)
- Created: src/states/dragon_naming_state.py (naming popup)
- Modified: src/main.py (register naming state and dialogue callback)
- Modified: src/game_state.py (dragon state save/load integration)
- Modified: src/states/exploration_mode_state.py (dragon from manager, naming check)
- Modified: data/dialogues/dragon_hatches.json (already had trigger_event)

---

## Work Log

### 2026-01-18
- Analyzed existing codebase - discovered Dragon class already had name field
- DragonStatusState already had name editing UI
- dragon_hatches.json already had `trigger_event: "name_dragon_popup"` but callback wasn't implemented
- Added DRAGON_NAME_MAX_LENGTH=20 and DRAGON_NAME_DEFAULT="Dragon" constants
- Added get_name(), set_name(), validate_name() methods to Dragon class
- Created DragonManager singleton for centralized dragon access across states
- Created DragonNamingState popup for naming during hatch event
- Registered `name_dragon_popup` callback with dialogue manager
- Integrated dragon manager with game state save/load system
- Updated exploration and dragon status states to use dragon manager
