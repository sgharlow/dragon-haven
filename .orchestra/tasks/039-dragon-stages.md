# Task 039: Adolescent & Adult Dragon Stages

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 039 |
| **Status** | done |
| **Branch** | task/039 |
| **Assigned** | task/039 |
| **Depends** | |
| **Blocked-By** | |
| **Estimated** | 120 min |

## Inputs
- src/entities/dragon.py (existing 3-stage system)
- src/sprites.py (dragon sprite generation)

## Description
Add Adolescent and Adult dragon stages to complete the 5-stage life cycle. Each stage unlocks new abilities, increases size, and changes appearance. Adjust day timings for prototype pacing.

## Acceptance Criteria
- [x] Add DRAGON_STAGE_ADOLESCENT and DRAGON_STAGE_ADULT constants
- [x] Define stage progression (adjusted for prototype):
  - Egg: Day 1
  - Hatchling: Days 2-3
  - Juvenile: Days 4-5
  - Adolescent: Days 6-9
  - Adult: Day 10+
- [x] Scale max stamina by stage (juvenile: 100, adolescent: 125, adult: 150)
- [x] Create adolescent sprite generation:
  - Horse-sized, longer neck
  - Small wing buds visible
  - More detailed features
- [x] Create adult sprite generation:
  - Full wingspan (4m scale)
  - Majestic appearance
  - Fire breath visual capability
- [x] Update dragon status screen for new stages
- [x] Update HUD dragon icon for new stages
- [x] Verify save/load works with new stages

## Context Files
- src/entities/dragon.py
- src/constants.py
- src/sprites.py
- src/states/dragon_status_state.py
- src/ui/hud.py

## Outputs
- Modified: src/constants.py (stage definitions, stamina scaling, abilities, descriptions)
- Modified: src/entities/dragon.py (5-stage progression, get_max_stamina method)
- Modified: src/sprites.py (adolescent/adult sprites with wing buds, full wings, fire glow)
- Modified: src/states/dragon_status_state.py (stage display, portraits, ability hints)
- Modified: src/ui/status_bars.py (dragon stage icon in HUD)
- Modified: src/ui/hud.py (pass stage to status bars)
- Modified: src/states/exploration_mode_state.py (pass dragon stage to HUD)

---

## Work Log

### Session 1
- Added DRAGON_STAGE_ADOLESCENT and DRAGON_STAGE_ADULT constants
- Defined DRAGON_STAGES list for all 5 stages
- Configured stage progression timing: Egg (Day 1), Hatchling (2-3), Juvenile (4-5), Adolescent (6-9), Adult (10+)
- Added DRAGON_STAGE_STAMINA_MAX with scaled values (100, 100, 100, 125, 150)
- Added new abilities: fire_breath (cost 40), flight_scout (cost 50)
- Updated dragon.py with 5-stage progression logic and get_max_stamina() method
- Created adolescent sprite: horse-sized body, wing buds, spines down neck, larger horns
- Created adult sprite: full wingspan, majestic appearance, fire glow nostrils, crown of horns
- Updated dragon status screen with portraits and ability hints for all 5 stages
- Added dragon stage icon to HUD status bars
- Verified save/load works correctly with new stages
