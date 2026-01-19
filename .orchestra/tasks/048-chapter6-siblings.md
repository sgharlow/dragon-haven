# Task 048: Chapter 6 - The Estranged Siblings

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 048 |
| **Status** | ready |
| **Branch** | task/048 |
| **Depends** | 047 |
| **Blocked-By** | |
| **Estimated** | 120 min |

## Inputs
- Spec: Theme is "Family reconciliation"
- Spec: Two siblings who need to reconcile
- Note: Spec lists as Chapter 4, but Vera/Noble are 4/5 in implementation
  - Adding as Chapter 6 to maintain existing chapter numbers

## Description
Add the Estranged Siblings as story characters with a reconciliation arc. This involves two characters (brother and sister) who visit the cafe separately and must be brought together. Per spec theme: Family reconciliation.

## Acceptance Criteria
- [ ] Add two sibling characters to story_characters.json:
  - Elena (sister) - proud, hurt
  - Thomas (brother) - regretful, stubborn
- [ ] Create data/events/chapter6.json with 8-10 events
  - Events where each sibling visits separately
  - Events requiring player to mediate
  - Final reconciliation event
- [ ] Create dialogue files:
  - [ ] chapter6_elena.json - Meeting Elena
  - [ ] chapter6_thomas.json - Meeting Thomas
  - [ ] siblings_conflict.json - Learning about their rift
  - [ ] siblings_memories.json - Shared childhood memories
  - [ ] siblings_reconciliation.json - Bringing them together
  - [ ] chapter6_end.json - Resolution
- [ ] Add portraits for both siblings to dialogue_box.py
- [ ] Add secret recipes for both siblings
- [ ] Chapter unlocks at Reputation 500+

## Context Files
- data/characters/story_characters.json
- data/events/chapter5.json (reference)
- src/ui/dialogue_box.py
- src/constants.py

## Outputs
- Modified: data/characters/story_characters.json
- Modified: src/ui/dialogue_box.py (2 portraits)
- Modified: src/constants.py (2 secret recipes)
- New: data/events/chapter6.json
- New: data/dialogues/chapter6_elena.json
- New: data/dialogues/chapter6_thomas.json
- New: data/dialogues/siblings_conflict.json
- New: data/dialogues/siblings_memories.json
- New: data/dialogues/siblings_reconciliation.json
- New: data/dialogues/chapter6_end.json

---

## Work Log

