# Task 029: Character Relationship System

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 029 |
| **Status** | done |
| **Branch** | task/029 |
| **Assigned** | task/029 |
| **Depends** | 028 |
| **Blocked-By** | |
| **Estimated** | 45 min |

## Inputs
- src/systems/story.py from 028

## Description
Create the character relationship system that tracks affinity with story characters. Affinity affects dialogue options and unlocks bonus content.

## Acceptance Criteria
- [x] StoryCharacter class:
  - id, name, portrait_id
  - affinity (0-100)
  - favorite_recipes
  - gift_preferences
  - unlocked_dialogues
- [x] 3 story characters defined:
  - Marcus the Wanderer (Chapter 1)
  - Lily the Perfectionist (Chapter 2)
  - Mother (Prologue + later)
- [x] Affinity gain methods:
  - Cook requested dish (+5 base, +10 if high quality)
  - Cook favorite recipe (+15)
  - Positive dialogue choice (+5-10)
  - Give preferred gift (+3-8)
- [x] get_affinity_level() - Low/Medium/High/Max
- [x] Affinity unlocks:
  - Medium: Additional dialogue options
  - High: Backstory revelations
  - Max: Post-chapter bonus scene
- [x] Integration with recipe cooking
- [x] Serialization for save/load

## Context Files
- src/systems/story.py
- src/systems/recipes.py
- src/constants.py

## Outputs
- Created: src/entities/story_character.py (StoryCharacter, CharacterManager, get_character_manager)
- Created: data/characters/ directory
- Created: data/characters/story_characters.json (Mother, Marcus, Lily)
- Updated: src/entities/__init__.py

---

## Work Log

[2025-01-18] - Completed task
- Created StoryCharacter with affinity tracking, recipe reactions, gift preferences
- Created CharacterManager with loading, affinity interactions, queries
- Implemented get_affinity_level() with Low/Medium/High/Max thresholds
- Created record_cook(), record_gift(), record_dialogue_choice() for affinity changes
- Added unlocked_dialogues system based on affinity levels
- Defined 3 characters: Mother, Marcus, Lily with preferences
- All acceptance criteria complete
