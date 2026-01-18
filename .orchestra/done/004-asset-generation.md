# Task 004: Asset Generation System

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 004 |
| **Status** | done |
| **Branch** | task/004 |
| **Assigned** | task/004 |
| **Depends** | 001 |
| **Blocked-By** | |
| **Estimated** | 60 min |

## Inputs
- src/constants.py from 001

## Description
Create a procedural asset generation system that creates all game sprites using pygame.draw functions. No external image files. Includes a sprite cache for performance.

## Acceptance Criteria
- [x] SpriteGenerator class with caching
- [x] Dragon sprite generation (basic shape for each stage)
- [x] UI element generation (buttons, panels, bars)
- [x] Item/ingredient sprite generation (basic shapes)
- [x] Character sprite generation (simple humanoid shapes)
- [x] Tile/terrain sprite generation
- [x] All sprites are surfaces, cached by key
- [x] Color palette defined in constants.py

## Context Files
- src/constants.py
- .orchestra/DECISIONS.md (DEC-001)

## Outputs
- Created: src/sprites.py (SpriteGenerator, sprite functions)
- Modified: src/constants.py (color palette)

---

## Work Log

### 2026-01-17
- Added extended color palette to constants.py (dragon stages, characters, ingredients, terrain)
- Created SpriteGenerator class with _cache dictionary and helper methods
- Implemented dragon sprites: egg (oval with spots), hatchling (cute round), juvenile (detailed with wings)
- Implemented UI elements: buttons (4 states), panels (4 styles), progress bars (4 types), icons (heart, coin, star, clock)
- Implemented ingredient sprites: berry, herb, mushroom, honey, meat, fish
- Implemented character sprites: player, customer, staff (with customizable hair)
- Implemented tile sprites: grass, forest, dirt, stone, water, sand, cafe_floor
- Implemented decoration sprites: flowers (3 colors), rock, bush, tree
- Added singleton get_sprite_generator() function for global access
- All tests pass, caching verified working
