# Task 037: Autumn & Winter Seasons

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 037 |
| **Status** | done |
| **Branch** | task/037 |
| **Assigned** | task/037 |
| **Depends** | |
| **Blocked-By** | |
| **Estimated** | 90 min |

## Inputs
- src/systems/time_system.py (existing time system)
- src/constants.py (current season config)

## Description
Add Autumn and Winter seasons to the existing Spring/Summer cycle. Each season affects weather probabilities, resource availability, ingredient quality bonuses, and visual atmosphere.

## Acceptance Criteria
- [x] Add 'autumn' and 'winter' to SEASONS list in constants.py
- [x] Define weather probabilities for new seasons:
  - Autumn: 35% sunny, 40% cloudy, 25% rainy
  - Winter: 25% sunny, 50% cloudy, 25% rainy
- [x] Add seasonal quality bonuses:
  - Autumn: mushroom +1, root vegetables +1
  - Winter: preserved items bonus, warm dishes popular
- [x] Update time system season cycling (4 seasons)
- [x] Add autumn color palette (orange, brown, gold)
- [x] Add winter color palette (white, blue, gray)
- [x] Update zone_renderer for seasonal visuals
- [x] Test full year cycle (28 days = 4 seasons × 7 days)

## Context Files
- src/constants.py
- src/systems/time_system.py
- src/sprites.py
- src/ui/zone_renderer.py

## Outputs
- Modified: src/constants.py (season definitions, colors, weather, quality bonuses)
- Modified: src/ui/zone_renderer.py (seasonal rendering with color blending)
- Note: time_system.py already supported arbitrary SEASONS list length

---

## Work Log

### 2026-01-18
- Added 'autumn' and 'winter' to SEASONS list in constants.py
- Added WEATHER_PROBABILITIES entries for autumn and winter
- Added QUALITY_SEASON_BONUS with seasonal ingredient bonuses
- Added SEASON_POPULAR_DISHES for customer preferences by season
- Added SEASON_ICONS (leaf for autumn, snowflake for winter)
- Added SEASON_COLORS palettes:
  - Autumn: faded grass, orange-brown leaves, deep red accents
  - Winter: frost-touched grass, gray-brown leaves, snow white accents
- Added SEASON_OVERLAY tints for atmospheric effects
- Updated zone_renderer.py:
  - Imports SEASON_COLORS, SEASON_OVERLAY from constants
  - Tracks current season via _current_season and _season_colors
  - update() method detects season changes from time_manager
  - _draw_seasonal_overlay() applies subtle tint per season
  - Grass tiles blend 60% zone theme / 40% seasonal color
  - Tree foliage uses 50% blend of zone + seasonal leaf colors
  - Bush tiles use seasonal leaf colors
  - Flower tiles use seasonal grass background + accent colors
  - Grass tuft decorations use seasonal grass colors
  - Flower decorations use seasonal accent colors
- Verified 28-day year cycle (4 seasons × 7 days each)
