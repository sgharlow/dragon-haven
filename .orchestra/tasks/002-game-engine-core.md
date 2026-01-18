# Task 002: Game Engine Core

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 002 |
| **Status** | ready |
| **Branch** | task/002 |
| **Assigned** | |
| **Depends** | 001 |
| **Blocked-By** | |
| **Estimated** | 45 min |

## Inputs
- src/main.py from 001
- src/constants.py from 001

## Description
Create the main Game class with the game loop, delta time calculation, and FPS control. This is the core engine that runs the entire game.

## Acceptance Criteria
- [ ] Game class in src/game.py
- [ ] Game loop with event handling, update, and draw phases
- [ ] Delta time calculation (capped at 0.1s to prevent spiral of death)
- [ ] 60 FPS target with pygame.Clock
- [ ] Clean quit handling
- [ ] Game class accepts and runs a state manager (placeholder for now)

## Context Files
- src/main.py
- src/constants.py

## Outputs
- Created: src/game.py (Game class with main loop)
- Modified: src/main.py (instantiate and run Game)

---

## Work Log

