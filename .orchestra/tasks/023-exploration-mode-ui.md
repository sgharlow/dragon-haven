# Task 023: Exploration Mode UI

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 023 |
| **Status** | ready |
| **Branch** | task/023 |
| **Assigned** | |
| **Depends** | 008, 010, 011, 021 |
| **Blocked-By** | |
| **Estimated** | 90 min |

## Inputs
- src/entities/dragon.py from 008
- src/systems/world.py from 010
- src/systems/resources.py from 011
- src/ui/hud.py from 021

## Description
Create the exploration mode screen where players explore zones, gather ingredients, and interact with their dragon.

## Acceptance Criteria
- [ ] ExplorationModeState extending BaseScreen
- [ ] Zone visualization:
  - Tile-based background for current zone
  - Resource spawn points visible (with icons)
  - Zone boundaries and exits
- [ ] Player character:
  - Simple sprite
  - Movement with WASD or arrow keys
  - Walk animation (2-3 frames)
- [ ] Dragon companion:
  - Follows player
  - Size based on stage
  - Color reflects current RGB values
  - Idle animations
- [ ] Resource gathering:
  - Approach resource point
  - Press interact key (E or Space)
  - Gathering animation
  - Item added notification
- [ ] Dragon abilities:
  - Press ability key (1, 2, 3)
  - Ability effects (visual + functional)
  - Stamina cost display
- [ ] Zone transitions:
  - Walk to exit area
  - Confirmation if zone requires dragon stage
  - Loading transition
- [ ] Dragon interaction:
  - Press key to pet/interact
  - Happiness feedback

## Context Files
- src/entities/dragon.py
- src/systems/world.py
- src/systems/resources.py
- src/ui/hud.py
- Dragon_Haven_Cafe_Software_Specification.docx.md (Section 5, 8)

## Outputs
- Created: src/states/exploration_mode_state.py (ExplorationModeState)
- Created: src/entities/player.py (Player class)
- Created: src/ui/zone_renderer.py (zone background rendering)

---

## Work Log

