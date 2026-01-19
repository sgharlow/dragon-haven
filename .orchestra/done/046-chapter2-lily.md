# Task 046: Chapter 2 - Lily the Perfectionist

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 046 |
| **Status** | ready |
| **Branch** | task/046 |
| **Depends** | 045 |
| **Blocked-By** | |
| **Estimated** | 90 min |

## Inputs
- data/characters/story_characters.json (Lily already defined)
- src/systems/story.py (story event system)
- Spec: Chapter 2 theme is "Accepting imperfection"

## Description
Add story events and dialogues for Chapter 2 featuring Lily the Perfectionist. Lily is already defined as a character with affinity tracking. This task adds her story arc events and dialogue trees. Per spec, Chapter 2 unlocks at Reputation 100+.

## Acceptance Criteria
- [x] Create data/events/chapter2.json with 6-8 story events
- [x] Create dialogue files for Lily's story arc:
  - [x] chapter2_lily.json - Initial meeting
  - [x] lily_standards.json - Her impossible standards
  - [x] lily_failure.json - A dish doesn't meet expectations
  - [x] lily_acceptance.json - Learning to accept imperfection
  - [x] chapter2_end.json - Resolution
- [x] Events trigger based on reputation (100+) and cooking interactions
- [x] Add Lily portrait to dialogue_box.py (already exists)
- [x] Affinity interactions work correctly
- [x] Chapter completion unlocks next story progression

## Context Files
- data/characters/story_characters.json
- data/events/chapter1.json (reference for format)
- data/dialogues/chapter1_marcus.json (reference)
- src/ui/dialogue_box.py

## Outputs
- New: data/events/chapter2.json
- New: data/dialogues/chapter2_lily.json
- New: data/dialogues/lily_standards.json
- New: data/dialogues/lily_failure.json
- New: data/dialogues/lily_acceptance.json
- New: data/dialogues/chapter2_end.json

---

## Work Log

### Implementation Complete

**Events (data/events/chapter2.json):**
- 7 story events for Lily's arc
- Triggers at reputation 100+
- Progression: Arrives → Standards → Challenge → Failure → Acceptance → Resolution → Complete
- Unlocks gourmet_special recipe during challenge event
- Sets chapter3_unlocked flag on completion

**Dialogues Created:**
- chapter2_lily.json - Lily's arrival, critical first impressions
- lily_standards.json - Reveals her backstory and fear of failure
- lily_challenge.json - Cooking competition proposal
- lily_failure.json - The pivotal moment when her dish goes "wrong"
- lily_acceptance.json - Learning that imperfection has value
- lily_resolution.json - Sharing her secret recipe, newfound joy
- chapter2_end.json - Departure and reputation boost

**Story Arc Theme: "Accepting Imperfection"**
- Lily arrives as harsh critic
- Reveals she fled her career after a mistake
- Dragon accidentally adds too much spice to her dish
- Discovers the "mistake" made the dish better
- Learns to cook with heart instead of rigid precision
- Shares her secret soufflé recipe as parting gift

