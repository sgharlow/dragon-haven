# Task 045: Character Affinity System

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 045 |
| **Status** | in_progress |
| **Branch** | task/045 |
| **Assigned** | task/045 |
| **Depends** | |
| **Blocked-By** | |
| **Estimated** | 120 min |

## Inputs
- src/entities/story_character.py (existing character system)
- src/systems/story.py (story events)

## Description
Add per-character affinity tracking (0-100). Affinity increases through cooking their requested dishes, discovering favorite recipes, positive dialogue choices, and gifts. Higher affinity unlocks bonus dialogue and secret recipes.

## Acceptance Criteria
- [x] Add affinity field to Character entity (0-100, default 0)
- [x] Define affinity gains:
  - Cook requested dish: +5 (+10 if high quality)
  - Cook favorite recipe: +15
  - Positive dialogue choice: +5-10
  - Give preferred ingredient: +3-8
- [x] Define affinity thresholds:
  - Acquaintance (0-24): Basic dialogue
  - Friendly (25-49): Personal stories unlock
  - Close (50-74): Secret recipes unlock
  - Best Friend (75-100): Special events unlock
- [x] Add favorite_recipes and preferred_ingredients to characters
- [x] Display affinity level during character interactions
- [x] Add affinity bar to dialogue box UI
- [x] Create affinity-gated dialogue variants
- [x] Add 1 secret recipe per story character (unlocks at Close)
- [x] Save/load affinity values correctly

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

### Implementation Complete

**Constants (src/constants.py):**
- Added CHARACTER AFFINITY SYSTEM section with:
  - AFFINITY_MIN/MAX (0-100 range)
  - AFFINITY_LEVEL_* constants for 4 levels
  - AFFINITY_LEVELS dict with min/max/name for each level
  - AFFINITY_COOK_* constants for cooking interaction bonuses
  - AFFINITY_UNLOCK_* thresholds for unlocks
  - CHARACTER_SECRET_RECIPES mapping character IDs to recipe IDs
  - UNLOCK_TYPE_AFFINITY for affinity-locked recipes
- Added 5 secret recipes (one per story character):
  - mothers_comfort_stew (Mother)
  - wanderers_secret_blend (Marcus)
  - lilys_perfect_souffle (Lily)
  - captains_treasure_catch (Vera)
  - royal_midnight_feast (Noble)

**Story Character Entity (src/entities/story_character.py):**
- Existing affinity infrastructure used imported constants
- Added helper methods: get_affinity_level_name(), can_unlock_personal_story(),
  can_unlock_secret_recipe(), can_unlock_special_event(), get_secret_recipe()
- CharacterManager already had record_cook, record_gift, record_dialogue_choice,
  get_state/load_state for save/load

**Story System (src/systems/story.py):**
- Added 3 new condition types for affinity-gated events:
  - affinity_min: {'character': id, 'amount': min_value}
  - affinity_level: {'character': id, 'level': 'friendly'/'close'/'best_friend'}
  - character_met: character_id

**Dialogue Box UI (src/ui/dialogue_box.py):**
- Added _draw_affinity_bar() method showing:
  - Progress bar filled based on affinity (0-100)
  - Color coded by level (gray-blue/green/gold/pink)
  - Level name displayed below bar
- Bar only shows for met story characters
