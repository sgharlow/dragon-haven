# Task 047: Chapter 3 - Old Man Garrett

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 047 |
| **Status** | ready |
| **Branch** | task/047 |
| **Depends** | 046 |
| **Blocked-By** | |
| **Estimated** | 120 min |

## Inputs
- Spec: Chapter 3 theme is "Letting go of the past"
- Spec: Unlocks when Dragon reaches Juvenile stage
- src/systems/story.py

## Description
Add Old Man Garrett as a new story character with full story arc. Garrett is an elderly man struggling to let go of memories from the past. Per spec, Chapter 3 unlocks when dragon reaches Juvenile stage.

## Acceptance Criteria
- [ ] Add Garrett to data/characters/story_characters.json
  - Define favorite_recipes, liked_recipes, disliked_recipes
  - Set chapter to "chapter3"
- [ ] Create data/events/chapter3.json with 6-8 story events
- [ ] Create dialogue files:
  - [ ] chapter3_garrett.json - First meeting
  - [ ] garrett_memories.json - Sharing old memories
  - [ ] garrett_loss.json - Revealing what he lost
  - [ ] garrett_letting_go.json - Learning to move forward
  - [ ] chapter3_end.json - Resolution
- [ ] Add Garrett portrait method to dialogue_box.py
- [ ] Events trigger based on dragon stage (Juvenile+)
- [ ] Add secret recipe for Garrett in constants.py
- [ ] Affinity system integration

## Context Files
- data/characters/story_characters.json
- data/events/chapter1.json (reference)
- src/ui/dialogue_box.py
- src/constants.py

## Outputs
- Modified: data/characters/story_characters.json
- Modified: src/ui/dialogue_box.py (portrait)
- Modified: src/constants.py (secret recipe)
- New: data/events/chapter3.json
- New: data/dialogues/chapter3_garrett.json
- New: data/dialogues/garrett_memories.json
- New: data/dialogues/garrett_loss.json
- New: data/dialogues/garrett_letting_go.json
- New: data/dialogues/chapter3_end.json

---

## Work Log

