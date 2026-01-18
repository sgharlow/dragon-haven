# Task 032: Balance Tuning

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 032 |
| **Status** | ready |
| **Branch** | task/032 |
| **Assigned** | |
| **Depends** | 031 |
| **Blocked-By** | |
| **Estimated** | 60 min |

## Inputs
- Playable game from 031

## Description
Play through the game and tune all balance values for a satisfying experience. Ensure progression feels good and there are no dead ends.

## Acceptance Criteria
- [ ] Time progression feels right (not too fast/slow)
- [ ] Dragon stat decay is manageable but meaningful
- [ ] Dragon growth rate allows progression within play session
- [ ] Cooking minigame difficulty appropriate:
  - Easy mode completable by casual players
  - Normal mode challenging but fair
- [ ] Recipe ingredients achievable with exploration
- [ ] Gold economy balanced:
  - Can afford basic upgrades
  - Not trivially easy to max everything
- [ ] Customer patience not frustrating
- [ ] Reputation gain/loss feels fair
- [ ] Story triggers at appropriate points
- [ ] No game-breaking exploits found
- [ ] All values documented in constants.py with comments
- [ ] DECISIONS.md updated with balance rationale (DEC-003)

## Context Files
- src/constants.py
- All system files
- .orchestra/DECISIONS.md

## Outputs
- Modified: src/constants.py (tuned values)
- Modified: .orchestra/DECISIONS.md (DEC-003: Balance decisions)

---

## Work Log

