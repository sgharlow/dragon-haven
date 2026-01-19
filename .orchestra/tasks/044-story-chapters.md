# Task 044: Additional Story Chapters

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 044 |
| **Status** | blocked |
| **Branch** | |
| **Assigned** | |
| **Depends** | 039 |
| **Blocked-By** | Chapter 4 requires Adolescent stage |
| **Estimated** | 180 min |

## Inputs
- src/systems/story.py (existing chapter system)
- data/events/ (existing story events)

## Description
Add 2 new story chapters: Chapter 4 (Captain Vera - courage theme) and Chapter 5 (The Masked Noble - identity theme). Each chapter includes a new character, dialogue trees, and recipe rewards.

## Acceptance Criteria
- [ ] Chapter 4: Captain Vera
  - Theme: Courage vs. recklessness
  - Unlock: Dragon reaches Adolescent stage
  - Character: Retired ship captain, weathered appearance
  - 5-6 story events with dialogue
  - Conflict: Hesitant to return to sea
  - Resolution: Finds balance, offers seafood recipes
  - Rewards: 2 new recipes, zone hint
- [ ] Chapter 5: The Masked Noble
  - Theme: Identity and authenticity
  - Unlock: Reputation 200+
  - Character: Mysterious visitor hiding identity
  - 5-6 story events with dialogue
  - Conflict: Hiding from responsibilities
  - Resolution: Accepts true self
  - Rewards: 2 premium recipes, gold bonus
- [ ] Create character sprites for both
- [ ] Write dialogue trees (15-20 nodes each)
- [ ] Define story event triggers and conditions
- [ ] Update story manager chapter progression
- [ ] Add characters to data/characters/

## Context Files
- src/systems/story.py
- src/entities/story_character.py
- data/events/
- data/dialogues/
- data/characters/
- src/sprites.py

## Outputs
- Created: data/events/chapter_4_*.json
- Created: data/events/chapter_5_*.json
- Created: data/dialogues/vera_*.json
- Created: data/dialogues/noble_*.json
- Modified: data/characters/story_characters.json
- Modified: src/sprites.py (character sprites)
- Modified: src/constants.py (chapter definitions)

---

## Work Log
