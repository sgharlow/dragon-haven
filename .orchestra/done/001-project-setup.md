# Task 001: Project Setup

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 001 |
| **Status** | done |
| **Branch** | task/001 |
| **Assigned** | task/001 |
| **Depends** | |
| **Blocked-By** | |
| **Estimated** | 30 min |

## Inputs
- None (first task)

## Description
Set up the project structure for Dragon Haven Cafe. Create the directory hierarchy, initialize pygame, and create placeholder files for all major modules.

## Acceptance Criteria
- [x] src/ directory with __init__.py files
- [x] src/main.py entry point that opens a pygame window
- [x] src/constants.py with basic game constants
- [x] Directory structure:
  ```
  src/
    main.py
    game.py
    constants.py
    states/
    entities/
    systems/
    ui/
  ```
- [x] Window opens at 1280x720 with title "Dragon Haven Cafe"
- [x] Game exits cleanly on window close
- [x] requirements.txt with pygame dependency

## Context Files
- .orchestra/GOAL.md
- .orchestra/DECISIONS.md

## Outputs
- Created: src/ directory structure
- Created: src/main.py (entry point)
- Created: src/constants.py (game constants)
- Created: requirements.txt

---

## Work Log

### 2026-01-17
- Created src/ directory with subdirectories: states/, entities/, systems/, ui/
- Added __init__.py files to all packages
- Created constants.py with display settings, colors, and game version
- Created main.py with pygame initialization and basic game loop
- Created placeholder game.py (full implementation in Task 002)
- Created requirements.txt with pygame>=2.0.0
- Verified game window opens at 1280x720 with correct title
- Verified clean exit on ESC key or window close
