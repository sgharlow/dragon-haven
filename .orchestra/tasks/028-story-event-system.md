# Task 028: Story Event System

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 028 |
| **Status** | ready |
| **Branch** | task/028 |
| **Assigned** | |
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
- [ ] StoryEvent dataclass:
  - id, chapter, sequence_order
  - Trigger conditions (time, reputation, dragon stage, completed events)
  - Dialogue tree ID
  - Outcomes (reputation change, unlocks, next event)
- [ ] StoryManager class with singleton get_story_manager()
- [ ] check_triggers() - evaluates all pending events
- [ ] Condition types:
  - Time of day, day range
  - Reputation minimum
  - Dragon stage minimum
  - Previous events completed
  - Location
- [ ] Event queue (multiple events can be pending)
- [ ] trigger_event() - starts event, plays dialogue
- [ ] complete_event() - applies outcomes
- [ ] Chapter tracking (Prologue, Chapter 1, Chapter 2)
- [ ] Event flags for conditional branching
- [ ] Serialization for save/load

## Context Files
- src/systems/time_system.py
- src/systems/cafe.py
- src/systems/dialogue.py
- src/constants.py
- Dragon_Haven_Cafe_Software_Specification.docx.md (Section 6.2)

## Outputs
- Created: src/systems/story.py (StoryEvent, StoryManager, get_story_manager)
- Created: data/events/ directory for event definitions

---

## Work Log

