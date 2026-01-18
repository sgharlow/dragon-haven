# Task 003: State Machine

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 003 |
| **Status** | done |
| **Branch** | task/003 |
| **Assigned** | task/003 |
| **Depends** | 002 |
| **Blocked-By** | |
| **Estimated** | 45 min |

## Inputs
- src/game.py from 002

## Description
Create the state machine system for managing game screens and transitions. Includes BaseState class, StateManager, and support for screen transitions with fade effects.

## Acceptance Criteria
- [x] BaseState class with enter(), exit(), update(dt), draw(screen), handle_event(event)
- [x] StateManager class that:
  - Registers states by name
  - Handles state transitions
  - Passes events/update/draw to current state
  - Supports optional fade transitions
- [x] Game class integrated with StateManager
- [x] Placeholder test state to verify system works

## Context Files
- src/game.py
- src/constants.py

## Outputs
- Created: src/state_manager.py (StateManager, BaseState)
- Created: src/states/__init__.py
- Created: src/states/base_state.py (BaseState, BaseScreen)
- Modified: src/game.py (integrate StateManager)

---

## Work Log

### 2026-01-17
- Created BaseState class with full lifecycle methods (enter, exit, update, draw, handle_event)
- Created BaseScreen class extending BaseState with fade transitions and title support
- Created StateManager with state registration, transitions, and fade effect overlay
- Created TestState to verify system works (shows transitions counter)
- Updated main.py to use StateManager and TestState
- Verified state machine works with fade transitions
