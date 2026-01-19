# Task 037: Autumn & Winter Seasons

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 037 |
| **Status** | ready |
| **Branch** | |
| **Assigned** | |
| **Depends** | |
| **Blocked-By** | |
| **Estimated** | 90 min |

## Inputs
- src/systems/time_system.py (existing time system)
- src/constants.py (current season config)

## Description
Add Autumn and Winter seasons to the existing Spring/Summer cycle. Each season affects weather probabilities, resource availability, ingredient quality bonuses, and visual atmosphere.

## Acceptance Criteria
- [ ] Add 'autumn' and 'winter' to SEASONS list in constants.py
- [ ] Define weather probabilities for new seasons:
  - Autumn: 35% sunny, 40% cloudy, 25% rainy
  - Winter: 25% sunny, 50% cloudy, 25% rainy
- [ ] Add seasonal quality bonuses:
  - Autumn: mushroom +1, root vegetables +1
  - Winter: preserved items bonus, warm dishes popular
- [ ] Update time system season cycling (4 seasons)
- [ ] Add autumn color palette (orange, brown, gold)
- [ ] Add winter color palette (white, blue, gray)
- [ ] Update zone_renderer for seasonal visuals
- [ ] Test full year cycle (28 days = 4 seasons × 7 days)

## Context Files
- src/constants.py
- src/systems/time_system.py
- src/sprites.py
- src/ui/zone_renderer.py

## Outputs
- Modified: src/constants.py (season definitions, colors)
- Modified: src/systems/time_system.py (4-season cycle)
- Modified: src/sprites.py (seasonal palettes)
- Modified: src/ui/zone_renderer.py (seasonal rendering)

---

## Work Log
