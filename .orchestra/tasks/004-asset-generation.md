# Task 004: Asset Generation System

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 004 |
| **Status** | ready |
| **Branch** | task/004 |
| **Assigned** | |
| **Depends** | 001 |
| **Blocked-By** | |
| **Estimated** | 60 min |

## Inputs
- src/constants.py from 001

## Description
Create a procedural asset generation system that creates all game sprites using pygame.draw functions. No external image files. Includes a sprite cache for performance.

## Acceptance Criteria
- [ ] SpriteGenerator class with caching
- [ ] Dragon sprite generation (basic shape for each stage)
- [ ] UI element generation (buttons, panels, bars)
- [ ] Item/ingredient sprite generation (basic shapes)
- [ ] Character sprite generation (simple humanoid shapes)
- [ ] Tile/terrain sprite generation
- [ ] All sprites are surfaces, cached by key
- [ ] Color palette defined in constants.py

## Context Files
- src/constants.py
- .orchestra/DECISIONS.md (DEC-001)

## Outputs
- Created: src/sprites.py (SpriteGenerator, sprite functions)
- Modified: src/constants.py (color palette)

---

## Work Log

