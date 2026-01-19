# Task 038: Stormy & Special Weather

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 038 |
| **Status** | done |
| **Branch** | task/038 |
| **Assigned** | task/038 |
| **Depends** | 037 |
| **Blocked-By** | |
| **Estimated** | 90 min |

## Inputs
- src/constants.py (weather config from 037)
- src/systems/world.py (weather effects)

## Description
Add Stormy and Special weather states. Stormy weather closes the cafe and makes exploration dangerous but yields rare resources. Special weather triggers unique events with legendary item spawns.

## Acceptance Criteria
- [x] Add WEATHER_STORMY and WEATHER_SPECIAL constants
- [x] Update weather probabilities per season (10% stormy, 5% special)
- [x] Stormy weather effects:
  - Cafe automatically closed (via WEATHER_CLOSES_CAFE flag)
  - Exploration has danger warnings (via WEATHER_DANGER_LEVEL)
  - Spawn "storm flowers" and "lightning crystals" resources
  - Visual effects (dark overlay via WEATHER_OVERLAY)
- [x] Special weather effects:
  - Unique events (meteor shower, rainbow, etc.) via SPECIAL_WEATHER_EVENTS
  - Spawn legendary ingredients (stardust_petal, rainbow_essence, moonbeam_honey)
  - Notification/celebration UI (via exploration state notifications)
- [x] Add storm warning notification (1 hour before)
- [x] Update HUD weather display for new types
- [x] Add new ingredients: Storm Flower, Lightning Crystal

## Context Files
- src/constants.py
- src/systems/world.py
- src/states/exploration_mode_state.py
- src/ui/hud.py

## Outputs
- Modified: src/constants.py (weather types, ingredients, overlays, spawn points)
- Modified: src/systems/world.py (weather effects, storm warnings, special events)
- Modified: src/ui/hud.py (weather icons for stormy and special)
- Modified: src/states/exploration_mode_state.py (weather notifications)

---

## Work Log

### 2026-01-18
- Added WEATHER_STORMY and WEATHER_SPECIAL constants to constants.py
- Updated ALL_WEATHER list to include new types
- Added weather probabilities for all 4 seasons (~10% stormy, ~5% special)
- Added WEATHER_CLOSES_CAFE flags (stormy closes cafe)
- Added WEATHER_DANGER_LEVEL (stormy = level 2)
- Added SPECIAL_WEATHER_EVENTS per season:
  - Spring: rainbow, blossom_shower
  - Summer: meteor_shower, golden_hour
  - Autumn: aurora, harvest_moon
  - Winter: northern_lights, diamond_dust
- Added SPECIAL_WEATHER_DESCRIPTIONS for notification text
- Added WEATHER_COLORS and WEATHER_OVERLAY for visual effects
- Added storm-exclusive ingredients: storm_flower, lightning_crystal
- Added special-weather ingredients: stardust_petal, rainbow_essence, moonbeam_honey
- Added WEATHER_SPAWN_POINTS for weather-conditional resource spawns
- Updated WEATHER_ICONS with storm and star icons
- Updated QUALITY_WEATHER_BONUS for storm/special weather
- Updated world.py:
  - Added tracking for special_weather_event, pending_weather, hours_until_weather_change
  - Added is_cafe_closed_by_weather(), get_weather_danger_level()
  - Added is_stormy(), is_special_weather()
  - Added get_special_weather_event(), get_special_weather_description()
  - Added get_pending_storm_warning(), schedule_weather_change()
  - Added tick_weather_countdown(), apply_pending_weather()
  - Updated roll_new_weather() to support storm warnings and special events
  - Updated save/load state to include new weather fields
- Updated hud.py:
  - Added WEATHER_STORMY and WEATHER_SPECIAL imports
  - Added storm icon (dark cloud with lightning bolt)
  - Added special icon (magical star/sparkle)
- Updated exploration_mode_state.py:
  - Added weather notification tracking flags
  - Added _check_weather_notifications() method
  - Shows storm warnings when stormy weather arrives
  - Shows special event celebrations with description
  - Shows advance storm warnings (1 hour before)
