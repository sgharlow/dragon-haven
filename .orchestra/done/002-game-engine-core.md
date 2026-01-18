# Task 002: Game Engine Core

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 002 |
| **Status** | done |
| **Branch** | task/002 |
| **Assigned** | task/002 |
| **Depends** | 001 |
| **Blocked-By** | |
| **Estimated** | 45 min |

## Inputs
- src/main.py from 001
- src/constants.py from 001

## Description
Create the main Game class with the game loop, delta time calculation, and FPS control. This is the core engine that runs the entire game.

## Acceptance Criteria
- [x] Game class in src/game.py
- [x] Game loop with event handling, update, and draw phases
- [x] Delta time calculation (capped at 0.1s to prevent spiral of death)
- [x] 60 FPS target with pygame.Clock
- [x] Clean quit handling
- [x] Game class accepts and runs a state manager (placeholder for now)

## Context Files
- src/main.py
- src/constants.py

## Outputs
- Created: src/game.py (Game class with main loop)
- Modified: src/main.py (instantiate and run Game)

---

## Work Log

### 2026-01-17
- Created Game class with full game loop (event handling, update, draw)
- Implemented delta time calculation with 0.1s cap to prevent spiral of death
- Added 60 FPS target using pygame.Clock
- Added state_manager integration with register_state_manager(), register_state(), set_initial_state()
- Added placeholder display when no state manager is set
- Updated main.py to use Game class
- Verified game runs correctly with placeholder mode
