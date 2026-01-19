# Task 051: Finale - Mother's Secret

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 051 |
| **Status** | ready |
| **Branch** | task/051 |
| **Depends** | 048, 050 |
| **Blocked-By** | |
| **Estimated** | 120 min |

## Inputs
- Spec: Finale theme is "Heritage and acceptance"
- Spec: Unlocks when Dragon reaches Adult stage
- Spec: Reveals Mother's secret about family heritage
- All previous chapters should be completable

## Description
Add the Finale chapter that concludes the main story. This chapter reveals Mother's secret about the family's heritage and connection to dragons. It ties together the themes from all previous chapters and provides a satisfying conclusion.

## Acceptance Criteria
- [ ] Create data/events/finale.json with 8-10 culminating events
- [ ] Create dialogue files:
  - [ ] finale_beginning.json - Mother recovers, has something to share
  - [ ] finale_heritage.json - Family history revealed
  - [ ] finale_dragon_bond.json - Special connection to dragons explained
  - [ ] finale_acceptance.json - Player accepts their heritage
  - [ ] finale_celebration.json - All characters gather
  - [ ] finale_end.json - Epilogue and credits trigger
- [ ] Events require Adult dragon stage
- [ ] Events can reference completed chapter flags
- [ ] Add special finale recipes unlocked by completion
- [ ] Trigger ending sequence/credits state
- [ ] Ensure all story characters can appear in finale events

## Context Files
- data/events/prologue.json (mother's illness setup)
- data/characters/story_characters.json
- src/systems/story.py
- All chapter event files for reference

## Outputs
- New: data/events/finale.json
- New: data/dialogues/finale_beginning.json
- New: data/dialogues/finale_heritage.json
- New: data/dialogues/finale_dragon_bond.json
- New: data/dialogues/finale_acceptance.json
- New: data/dialogues/finale_celebration.json
- New: data/dialogues/finale_end.json
- Modified: src/constants.py (finale recipes if any)

---

## Work Log

