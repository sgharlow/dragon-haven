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
- [x] Add Garrett to data/characters/story_characters.json
  - Define favorite_recipes, liked_recipes, disliked_recipes
  - Set chapter to "chapter3"
- [x] Create data/events/chapter3.json with 6-8 story events
- [x] Create dialogue files:
  - [x] chapter3_garrett.json - First meeting
  - [x] garrett_memories.json - Sharing old memories
  - [x] garrett_recipe_mention.json - His wife's special recipe
  - [x] garrett_grief.json - Deep grief moment
  - [x] garrett_letting_go.json - Learning to move forward
  - [x] garrett_resolution.json - Sharing the recipe
  - [x] chapter3_end.json - Resolution
- [x] Add Garrett portrait method to dialogue_box.py
- [x] Events trigger based on dragon stage (Juvenile+)
- [x] Add secret recipe for Garrett in constants.py
- [x] Affinity system integration

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

### Implementation Complete

**Character (story_characters.json):**
- Added Old Man Garrett with chapter3 assignment
- Favorite recipes: herb_stew, honey_cake, herb_tea (comfort foods)
- Disliked recipes: crystal_sorbet, exotic_blend (too "modern")
- Gift preferences include pressed_flower, old_photograph, antique_trinket

**Portrait (dialogue_box.py):**
- Added _draw_garrett_portrait method
- Elderly appearance: balding with wispy white hair
- Bushy white eyebrows, tired but kind eyes
- Wrinkles and age lines showing life lived
- Simple cardigan with buttons

**Secret Recipe (constants.py):**
- garretts_memory_bread - "An old family recipe that Garrett's late wife used to make"
- Simple ingredients (honey, herbs) reflecting humble but meaningful food
- Added to CHARACTER_SECRET_RECIPES mapping

**Events (chapter3.json):**
- 7 story events with dragon_stage_min: juvenile trigger
- Progression: Arrives → Memories → Recipe Mention → Grief → Letting Go → Resolution → Complete

**Dialogues Created:**
- chapter3_garrett.json - First meeting, notices dragon, mentions Eleanor
- garrett_memories.json - Shares 52-year marriage story, shows photograph
- garrett_recipe_mention.json - Reveals wife's Memory Bread, can't bring himself to make it
- garrett_grief.json - Emotional breakdown on Eleanor's birthday, turning point
- garrett_letting_go.json - Sets one place at table, decides to live again
- garrett_resolution.json - Finally makes the bread, shares recipe
- chapter3_end.json - Plans trip to ocean to scatter ashes, finds new home

**Story Arc Theme: "Letting Go of the Past"**
- Garrett is elderly widower clinging to wife's memory
- Carries her recipe but can't use it (fear of finality)
- Dragon and cafe provide comfort and community
- Learns that letting go isn't forgetting - it's honoring
- Shares recipe as act of moving forward while preserving love

