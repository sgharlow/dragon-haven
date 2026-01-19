# Task 036: Dragon Naming System

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 036 |
| **Status** | ready |
| **Branch** | |
| **Assigned** | |
| **Depends** | |
| **Blocked-By** | |
| **Estimated** | 60 min |

## Inputs
- src/entities/dragon.py (existing dragon system)
- src/systems/story.py (for hatch event)

## Description
Add the ability for players to name their dragon. The naming prompt appears when the egg hatches. Dragon name is displayed in HUD and all references. Players can also rename from the dragon status screen.

## Acceptance Criteria
- [ ] Add `name` field to Dragon entity (default: "Dragon")
- [ ] Add name validation (max 20 chars, no empty)
- [ ] Create naming prompt UI component
- [ ] Trigger naming prompt during egg hatch story event
- [ ] Update HUD to show dragon name instead of generic "Dragon"
- [ ] Add rename option to dragon status screen
- [ ] Save/load dragon name correctly
- [ ] Update all dragon references in UI to use name

## Context Files
- src/entities/dragon.py
- src/systems/story.py
- src/states/dragon_status_state.py
- src/ui/hud.py
- src/constants.py

## Outputs
- Modified: src/entities/dragon.py (name field)
- Modified: src/ui/hud.py (dragon name display)
- Modified: src/states/dragon_status_state.py (rename option)
- Modified: data/events/ (hatch event with naming)

---

## Work Log
