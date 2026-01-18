# Task 027: Dialogue System

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 027 |
| **Status** | ready |
| **Branch** | task/027 |
| **Assigned** | |
| **Depends** | 003, 004 |
| **Blocked-By** | |
| **Estimated** | 60 min |

## Inputs
- src/state_manager.py from 003
- src/sprites.py from 004

## Description
Create the dialogue system for character conversations. Supports branching dialogue, choices, and character portraits.

## Acceptance Criteria
- [ ] DialogueManager class
- [ ] Dialogue data structure:
  - Speaker name
  - Portrait ID
  - Text content
  - Choices (optional)
  - Next dialogue ID
- [ ] Dialogue box UI:
  - Semi-transparent background
  - Character portrait (left)
  - Speaker name
  - Text with typewriter effect
  - Choice buttons when applicable
- [ ] Typewriter text effect (configurable speed)
- [ ] Click/key to skip to full text
- [ ] Click/key to advance dialogue
- [ ] Choice selection with keyboard/mouse
- [ ] Choices can lead to different dialogue branches
- [ ] Dialogue can trigger events (via callbacks)
- [ ] Dialogue file format (JSON-based)
- [ ] Support for dialogue flags (set/check conditions)

## Context Files
- src/state_manager.py
- src/sprites.py
- src/constants.py

## Outputs
- Created: src/systems/dialogue.py (DialogueManager)
- Created: src/ui/dialogue_box.py (DialogueBox UI)
- Created: data/dialogues/ directory for dialogue files

---

## Work Log

