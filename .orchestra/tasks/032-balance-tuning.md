# Task 032: Balance Tuning

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 032 |
| **Status** | done |
| **Branch** | task/032 |
| **Assigned** | task/032 |
| **Depends** | 031 |
| **Blocked-By** | |
| **Estimated** | 60 min |

## Inputs
- Playable game from 031

## Description
Play through the game and tune all balance values for a satisfying experience. Ensure progression feels good and there are no dead ends.

## Acceptance Criteria
- [x] Time progression feels right (not too fast/slow)
- [x] Dragon stat decay is manageable but meaningful
- [x] Dragon growth rate allows progression within play session
- [x] Cooking minigame difficulty appropriate:
  - Easy mode completable by casual players
  - Normal mode challenging but fair
- [x] Recipe ingredients achievable with exploration
- [x] Gold economy balanced:
  - Can afford basic upgrades
  - Not trivially easy to max everything
- [x] Customer patience not frustrating
- [x] Reputation gain/loss feels fair
- [x] Story triggers at appropriate points
- [x] No game-breaking exploits found
- [x] All values documented in constants.py with comments
- [x] DECISIONS.md updated with balance rationale (DEC-003)

## Context Files
- src/constants.py
- All system files
- .orchestra/DECISIONS.md

## Outputs
- Modified: src/constants.py (tuned values with BALANCE comments)
- Modified: .orchestra/DECISIONS.md (DEC-003: Balance decisions)

---

## Work Log

### Session 1
- Analyzed current balance values against 15-30 min target
- Time system: Doubled speed (30s/hour vs 60s)
- Dragon growth: Hatches Day 2, Juvenile Day 5 (visible progression)
- Dragon stats: Increased decay slightly, earlier warnings, generous rewards
- Cooking minigame:
  - Wider timing windows (PERFECT ±75ms, GOOD ±125ms, OK ±180ms)
  - Lower combo thresholds (3/7/12/20 instead of 5/10/20/30)
  - Slower note speed (250 vs 300 px/s)
  - Easy mode 75% wider windows (was 50%)
  - Shorter duration (12-20s)
  - More forgiving quality thresholds (3-star at 50%)
- Economy: Starting gold 150, reduced ingredient quality impact
- Customer patience: 2 game hours (60 real seconds)
- Documented all rationale in DEC-003
