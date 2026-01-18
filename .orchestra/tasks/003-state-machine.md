# Task 003: State Machine

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 003 |
| **Status** | ready |
| **Branch** | task/003 |
| **Assigned** | |
| **Depends** | 002 |
| **Blocked-By** | |
| **Estimated** | 45 min |

## Inputs
- src/game.py from 002

## Description
Create the state machine system for managing game screens and transitions. Includes BaseState class, StateManager, and support for screen transitions with fade effects.

## Acceptance Criteria
- [ ] BaseState class with enter(), exit(), update(dt), draw(screen), handle_event(event)
- [ ] StateManager class that:
  - Registers states by name
  - Handles state transitions
  - Passes events/update/draw to current state
  - Supports optional fade transitions
- [ ] Game class integrated with StateManager
- [ ] Placeholder test state to verify system works

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

