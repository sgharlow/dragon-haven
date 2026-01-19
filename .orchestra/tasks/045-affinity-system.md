# Task 045: Character Affinity System

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 045 |
| **Status** | ready |
| **Branch** | |
| **Assigned** | |
| **Depends** | |
| **Blocked-By** | |
| **Estimated** | 120 min |

## Inputs
- src/entities/story_character.py (existing character system)
- src/systems/story.py (story events)

## Description
Add per-character affinity tracking (0-100). Affinity increases through cooking their requested dishes, discovering favorite recipes, positive dialogue choices, and gifts. Higher affinity unlocks bonus dialogue and secret recipes.

## Acceptance Criteria
- [ ] Add affinity field to Character entity (0-100, default 0)
- [ ] Define affinity gains:
  - Cook requested dish: +5 (+10 if high quality)
  - Cook favorite recipe: +15
  - Positive dialogue choice: +5-10
  - Give preferred ingredient: +3-8
- [ ] Define affinity thresholds:
  - Acquaintance (0-24): Basic dialogue
  - Friendly (25-49): Personal stories unlock
  - Close (50-74): Secret recipes unlock
  - Best Friend (75-100): Special events unlock
- [ ] Add favorite_recipes and preferred_ingredients to characters
- [ ] Display affinity level during character interactions
- [ ] Add affinity bar to dialogue box UI
- [ ] Create affinity-gated dialogue variants
- [ ] Add 1 secret recipe per story character (unlocks at Close)
- [ ] Save/load affinity values correctly

## Context Files
- src/entities/story_character.py
- src/systems/story.py
- src/ui/dialogue_box.py
- src/constants.py
- data/characters/story_characters.json

## Outputs
- Modified: src/entities/story_character.py (affinity tracking)
- Modified: src/constants.py (affinity constants)
- Modified: src/ui/dialogue_box.py (affinity display)
- Modified: src/systems/story.py (affinity conditions)
- Modified: data/characters/story_characters.json (favorites)

---

## Work Log
