# Task 029: Character Relationship System

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 029 |
| **Status** | ready |
| **Branch** | task/029 |
| **Assigned** | |
| **Depends** | 028 |
| **Blocked-By** | |
| **Estimated** | 45 min |

## Inputs
- src/systems/story.py from 028

## Description
Create the character relationship system that tracks affinity with story characters. Affinity affects dialogue options and unlocks bonus content.

## Acceptance Criteria
- [ ] StoryCharacter class:
  - id, name, portrait_id
  - affinity (0-100)
  - favorite_recipes
  - gift_preferences
  - unlocked_dialogues
- [ ] 3 story characters defined:
  - Marcus the Wanderer (Chapter 1)
  - Lily the Perfectionist (Chapter 2)
  - Mother (Prologue + later)
- [ ] Affinity gain methods:
  - Cook requested dish (+5 base, +10 if high quality)
  - Cook favorite recipe (+15)
  - Positive dialogue choice (+5-10)
  - Give preferred gift (+3-8)
- [ ] get_affinity_level() - Low/Medium/High/Max
- [ ] Affinity unlocks:
  - Medium: Additional dialogue options
  - High: Backstory revelations
  - Max: Post-chapter bonus scene
- [ ] Integration with recipe cooking
- [ ] Serialization for save/load

## Context Files
- src/systems/story.py
- src/systems/recipes.py
- src/constants.py
- Dragon_Haven_Cafe_Software_Specification.docx.md (Section 6.3)

## Outputs
- Created: src/entities/story_character.py (StoryCharacter class)
- Modified: src/systems/story.py (character integration)
- Created: data/characters/ directory for character definitions

---

## Work Log

