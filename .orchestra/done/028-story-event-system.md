# Task 028: Story Event System

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 028 |
| **Status** | done |
| **Branch** | task/028 |
| **Assigned** | task/028 |
| **Depends** | 007, 013, 027 |
| **Blocked-By** | |
| **Estimated** | 60 min |

## Inputs
- src/systems/time_system.py from 007
- src/systems/cafe.py from 013
- src/systems/dialogue.py from 027

## Description
Create the story event system that triggers narrative events based on game conditions. Events drive the story forward and introduce characters.

## Acceptance Criteria
- [x] StoryEvent dataclass:
  - id, chapter, sequence_order
  - Trigger conditions (time, reputation, dragon stage, completed events)
  - Dialogue tree ID
  - Outcomes (reputation change, unlocks, next event)
- [x] StoryManager class with singleton get_story_manager()
- [x] check_triggers() - evaluates all pending events
- [x] Condition types:
  - Time of day, day range
  - Reputation minimum
  - Dragon stage minimum
  - Previous events completed
  - Location
- [x] Event queue (multiple events can be pending)
- [x] trigger_event() - starts event, plays dialogue
- [x] complete_event() - applies outcomes
- [x] Chapter tracking (Prologue, Chapter 1, Chapter 2)
- [x] Event flags for conditional branching
- [x] Serialization for save/load

## Context Files
- src/systems/time_system.py
- src/systems/cafe.py
- src/systems/dialogue.py
- src/constants.py

## Outputs
- Created: src/systems/story.py (StoryEvent, EventCondition, EventOutcome, StoryManager, get_story_manager)
- Created: data/events/ directory
- Created: data/events/prologue.json (sample events)
- Updated: src/systems/__init__.py

---

## Work Log

[2025-01-18] - Completed task
- Created EventCondition supporting time_of_day, day_range, day_min, reputation_min, dragon_stage, events_completed, location, flag, not_flag, chapter
- Created EventOutcome supporting set_flag, clear_flag, next_event, set_chapter, reputation_change, unlock_recipe, unlock_zone, gold_reward
- Created StoryEvent with id, chapter, sequence_order, conditions, dialogue_id, outcomes, repeatable
- Created StoryManager with event loading from JSON, check_triggers(), trigger_event(), complete_current_event()
- Implemented event queue, chapter progression, outcome handlers
- Created prologue.json with 5 sample events
- All acceptance criteria complete
