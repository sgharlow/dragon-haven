# Task 044: Additional Story Chapters

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 044 |
| **Status** | done |
| **Branch** | task/044 |
| **Assigned** | task/044 |
| **Depends** | 039 |
| **Blocked-By** | Chapter 4 requires Adolescent stage |
| **Estimated** | 180 min |

## Inputs
- src/systems/story.py (existing chapter system)
- data/events/ (existing story events)

## Description
Add 2 new story chapters: Chapter 4 (Captain Vera - courage theme) and Chapter 5 (The Masked Noble - identity theme). Each chapter includes a new character, dialogue trees, and recipe rewards.

## Acceptance Criteria
- [x] Chapter 4: Captain Vera
  - Theme: Courage vs. recklessness
  - Unlock: Dragon reaches Adolescent stage
  - Character: Retired ship captain, weathered appearance
  - 5-6 story events with dialogue (6 events)
  - Conflict: Hesitant to return to sea
  - Resolution: Finds balance, offers seafood recipes
  - Rewards: 2 new recipes (coastal_chowder, crab_cakes)
- [x] Chapter 5: The Masked Noble
  - Theme: Identity and authenticity
  - Unlock: Reputation 200+
  - Character: Mysterious visitor hiding identity
  - 5-6 story events with dialogue (7 events)
  - Conflict: Hiding from responsibilities
  - Resolution: Accepts true self
  - Rewards: 2 recipes (crystal_infused_dessert, honey_glazed_game), 500 gold
- [x] Create character sprites for both
- [x] Write dialogue trees (15-20 nodes each)
- [x] Define story event triggers and conditions
- [x] Update story manager chapter progression
- [x] Add characters to data/characters/

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

### Session 1
- Updated StoryManager.CHAPTERS to include chapter4 and chapter5
- Fixed dragon_stage condition checker to use DRAGON_STAGES for all 5 stages
- Added two new characters to story_characters.json:
  - Captain Vera (chapter4): Retired sea captain, seafood recipes
  - The Masked Noble (chapter5): Mysterious aristocrat, premium recipes
- Created chapter4 events (6 events):
  - ch4_vera_arrives, ch4_vera_memories, ch4_vera_storm
  - ch4_vera_courage, ch4_vera_resolution, ch4_complete
- Created chapter5 events (7 events):
  - ch5_noble_arrives, ch5_noble_tastes, ch5_noble_slip
  - ch5_noble_confession, ch5_noble_choice, ch5_noble_resolution, ch5_complete
- Created 11 dialogue files:
  - Chapter 4: vera_arrival, vera_memories, vera_storm, vera_courage, vera_resolution, chapter4_end
  - Chapter 5: noble_arrival, noble_tastes, noble_slip, noble_confession, noble_choice, noble_resolution, chapter5_end
- Added character portrait drawing methods in dialogue_box.py:
  - _draw_vera_portrait: Weathered captain with salt-streaked gray hair
  - _draw_noble_portrait: Mysterious figure with ornate half-mask
  - _draw_marcus_portrait, _draw_lily_portrait, _draw_mother_portrait (existing characters)
- Recipe unlocks: coastal_chowder, crab_cakes (Ch4), crystal_infused_dessert, honey_glazed_game (Ch5)
- Chapter unlock conditions: Ch4 requires adolescent dragon, Ch5 requires 200+ reputation
