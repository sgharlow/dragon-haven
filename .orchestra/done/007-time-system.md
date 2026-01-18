# Task 007: Time System

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 007 |
| **Status** | done |
| **Branch** | task/007 |
| **Assigned** | task/007 |
| **Depends** | 002 |
| **Blocked-By** | |
| **Estimated** | 45 min |

## Inputs
- src/game.py from 002
- src/constants.py

## Description
Create the time system that manages day/night cycle, time of day, and seasons. Time progresses during gameplay and can be paused. Central to all time-dependent game systems.

## Acceptance Criteria
- [x] TimeManager class with singleton get_time_manager()
- [x] Day/night cycle: Morning (6-12), Afternoon (12-18), Evening (18-24), Night (0-6)
- [x] 1 in-game day = 24 real minutes (configurable via time_scale)
- [x] Current time as hour:minute (get_current_time, get_formatted_time)
- [x] Day counter (starts at 1)
- [x] 2 seasons: Spring, Summer (10 days each)
- [x] pause() and resume() methods
- [x] advance_to_morning() for sleeping
- [x] get_time_of_day() returns period name
- [x] Callbacks for time period changes (on_period_change, on_new_day, on_new_season)

## Context Files
- src/constants.py
- src/game.py

## Outputs
- Created: src/systems/time_system.py (TimeManager, get_time_manager)
- Created: src/systems/__init__.py
- Modified: src/constants.py (time constants)

---

## Work Log

### 2026-01-17
- Added time constants to constants.py (periods, day length, seasons, cafe hours)
- Created TimeManager class with full day/night cycle management
- Implemented time periods: morning (6-12), afternoon (12-18), evening (18-24), night (0-6)
- Added time queries: get_time_of_day, get_formatted_time, is_cafe_open, get_light_level
- Added time control: pause, resume, set_time_scale, advance_to_morning
- Implemented callback system for period changes, new days, and new seasons
- Added scheduled events support
- Implemented state serialization for save/load
- Updated systems/__init__.py
- All tests pass
