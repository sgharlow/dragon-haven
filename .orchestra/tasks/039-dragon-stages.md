# Task 039: Adolescent & Adult Dragon Stages

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 039 |
| **Status** | ready |
| **Branch** | |
| **Assigned** | |
| **Depends** | |
| **Blocked-By** | |
| **Estimated** | 120 min |

## Inputs
- src/entities/dragon.py (existing 3-stage system)
- src/sprites.py (dragon sprite generation)

## Description
Add Adolescent and Adult dragon stages to complete the 5-stage life cycle. Each stage unlocks new abilities, increases size, and changes appearance. Adjust day timings for prototype pacing.

## Acceptance Criteria
- [ ] Add DRAGON_STAGE_ADOLESCENT and DRAGON_STAGE_ADULT constants
- [ ] Define stage progression (adjusted for prototype):
  - Egg: Day 1
  - Hatchling: Days 2-3
  - Juvenile: Days 4-5
  - Adolescent: Days 6-9
  - Adult: Day 10+
- [ ] Scale max stamina by stage (juvenile: 100, adolescent: 125, adult: 150)
- [ ] Create adolescent sprite generation:
  - Horse-sized, longer neck
  - Small wing buds visible
  - More detailed features
- [ ] Create adult sprite generation:
  - Full wingspan (4m scale)
  - Majestic appearance
  - Fire breath visual capability
- [ ] Update dragon status screen for new stages
- [ ] Update HUD dragon icon for new stages
- [ ] Verify save/load works with new stages

## Context Files
- src/entities/dragon.py
- src/constants.py
- src/sprites.py
- src/states/dragon_status_state.py
- src/ui/hud.py

## Outputs
- Modified: src/constants.py (stage definitions)
- Modified: src/entities/dragon.py (5-stage progression)
- Modified: src/sprites.py (adolescent/adult sprites)
- Modified: src/states/dragon_status_state.py (stage display)

---

## Work Log
