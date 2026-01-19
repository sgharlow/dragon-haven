# Task 048: Chapter 6 - The Estranged Siblings

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 048 |
| **Status** | done |
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
- [x] Add two sibling characters to story_characters.json:
  - Elena (sister) - proud, hurt
  - Thomas (brother) - regretful, stubborn
- [x] Create data/events/chapter6.json with 8 events
  - Events where each sibling visits separately
  - Events requiring player to mediate
  - Final reconciliation event
- [x] Create dialogue files:
  - [x] elena_arrival.json - Meeting Elena
  - [x] thomas_arrival.json - Meeting Thomas
  - [x] siblings_confrontation.json - Learning about their rift
  - [x] elena_confides.json - Elena's side of the story
  - [x] thomas_confides.json - Thomas's side of the story
  - [x] siblings_reconciliation.json - Beginning to heal
  - [x] siblings_forgiveness.json - Full forgiveness
  - [x] chapter6_end.json - Resolution
- [x] Add portraits for both siblings to dialogue_box.py
- [x] Add secret recipes for both siblings
- [x] Chapter unlocks at Reputation 500+

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
- New: data/dialogues/elena_arrival.json
- New: data/dialogues/thomas_arrival.json
- New: data/dialogues/siblings_confrontation.json
- New: data/dialogues/elena_confides.json
- New: data/dialogues/thomas_confides.json
- New: data/dialogues/siblings_reconciliation.json
- New: data/dialogues/siblings_forgiveness.json
- New: data/dialogues/chapter6_end.json

---

## Work Log

### Session 1
- Added Elena and Thomas to story_characters.json as chapter6 characters
- Added _draw_elena_portrait() and _draw_thomas_portrait() methods to dialogue_box.py
- Added secret recipes: elenas_reconciliation_tea and thomas_humble_pie to constants.py
- Created chapter6.json with 8 story events
- Created 8 dialogue files telling the siblings' reconciliation story
- Theme: "Mending What Was Broken" - estranged siblings find their way back
- Story arc: Separate arrivals -> Confrontation -> Each confides -> Reconciliation -> Forgiveness
