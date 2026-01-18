# Task 027: Dialogue System

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 027 |
| **Status** | done |
| **Branch** | task/027 |
| **Assigned** | task/027 |
| **Depends** | 003, 004 |
| **Blocked-By** | |
| **Estimated** | 60 min |

## Inputs
- src/state_manager.py from 003
- src/sprites.py from 004

## Description
Create the dialogue system for character conversations. Supports branching dialogue, choices, and character portraits.

## Acceptance Criteria
- [x] DialogueManager class
- [x] Dialogue data structure:
  - Speaker name
  - Portrait ID
  - Text content
  - Choices (optional)
  - Next dialogue ID
- [x] Dialogue box UI:
  - Semi-transparent background
  - Character portrait (left)
  - Speaker name
  - Text with typewriter effect
  - Choice buttons when applicable
- [x] Typewriter text effect (configurable speed)
- [x] Click/key to skip to full text
- [x] Click/key to advance dialogue
- [x] Choice selection with keyboard/mouse
- [x] Choices can lead to different dialogue branches
- [x] Dialogue can trigger events (via callbacks)
- [x] Dialogue file format (JSON-based)
- [x] Support for dialogue flags (set/check conditions)

## Context Files
- src/state_manager.py
- src/sprites.py
- src/constants.py

## Outputs
- Created: src/systems/dialogue.py (DialogueManager, Dialogue, DialogueNode, DialogueChoice)
- Created: src/ui/dialogue_box.py (DialogueBox UI component)
- Created: data/dialogues/ directory
- Created: data/dialogues/intro.json (sample dialogue)
- Updated: src/systems/__init__.py
- Updated: src/ui/__init__.py

---

## Work Log

[2025-01-18] - Completed task
- Created DialogueNode with speaker, portrait, text, choices, next_id, set_flags, trigger_event
- Created DialogueChoice with text, next_id, condition, set_flags
- Created Dialogue class for complete conversations with nodes dict
- Created DialogueManager with load from JSON, start/advance/select_choice, flags, callbacks
- Created DialogueBox UI with typewriter effect, word wrapping, portraits, choice buttons
- Added keyboard (Space/Enter/arrows) and mouse support
- Created sample intro.json dialogue with branching choices
- All acceptance criteria complete
