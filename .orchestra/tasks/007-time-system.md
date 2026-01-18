# Task 007: Time System

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 007 |
| **Status** | ready |
| **Branch** | task/007 |
| **Assigned** | |
| **Depends** | 002 |
| **Blocked-By** | |
| **Estimated** | 45 min |

## Inputs
- src/game.py from 002
- src/constants.py

## Description
Create the time system that manages day/night cycle, time of day, and seasons. Time progresses during gameplay and can be paused. Central to all time-dependent game systems.

## Acceptance Criteria
- [ ] TimeManager class with singleton get_time_manager()
- [ ] Day/night cycle: Morning (6-12), Afternoon (12-18), Evening (18-24), Night (0-6)
- [ ] 1 in-game day = 24 real minutes (configurable)
- [ ] Current time as hour:minute
- [ ] Day counter (starts at 1)
- [ ] 2 seasons: Spring, Summer (10 days each)
- [ ] pause() and resume() methods
- [ ] advance_to_morning() for sleeping
- [ ] get_time_of_day() returns period name
- [ ] Callbacks for time period changes

## Context Files
- src/constants.py
- src/game.py

## Outputs
- Created: src/systems/time_system.py (TimeManager, get_time_manager)
- Created: src/systems/__init__.py
- Modified: src/constants.py (time constants)

---

## Work Log

