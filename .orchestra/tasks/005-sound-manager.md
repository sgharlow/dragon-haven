# Task 005: Sound Manager

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 005 |
| **Status** | ready |
| **Branch** | task/005 |
| **Assigned** | |
| **Depends** | 001 |
| **Blocked-By** | |
| **Estimated** | 45 min |

## Inputs
- src/constants.py from 001

## Description
Create a sound manager with procedurally generated sound effects. Uses pygame.mixer and numpy for synthesis. Singleton pattern for global access.

## Acceptance Criteria
- [ ] SoundManager class with singleton get_sound_manager()
- [ ] initialize() method for pygame mixer setup
- [ ] Procedural sound generation using sine waves, noise
- [ ] Sound categories: UI, cooking, dragon, ambient
- [ ] play(sound_name) method
- [ ] set_volume(category, level) method
- [ ] At least 10 distinct procedural sounds
- [ ] Graceful fallback if mixer fails

## Context Files
- src/constants.py

## Outputs
- Created: src/sound_manager.py (SoundManager, get_sound_manager)
- Sound effects: ui_click, ui_confirm, ui_cancel, dragon_chirp, dragon_eat, cooking_chop, cooking_sizzle, coin_collect, customer_happy, customer_angry

---

## Work Log

