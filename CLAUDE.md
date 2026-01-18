# Project: Dragon Haven Cafe

## Overview
A dragon-raising cafe management simulation game built with Python and Pygame. Players raise a baby dragon while operating a family cafe, gathering ingredients from an explorable world.

## Tech Stack
- Python 3.8+
- Pygame 2.0+
- JSON for data persistence

## Development Commands
```bash
pip install pygame    # Install dependencies
python src/main.py    # Run the game
```

## Orchestra Lite - Multi-Agent Coordination

This project uses Orchestra Lite for coordinated parallel development.

### Quick Start
```
/orchestra plan    - Break down the goal into tasks
/orchestra work    - Claim and complete next task
/orchestra status  - Check progress
/orchestra done ID - Mark task complete
```

### Key Files
| File | Purpose |
|------|---------|
| `.orchestra/GOAL.md` | What we are building |
| `.orchestra/PLAN.md` | High-level phases |
| `.orchestra/TASKS.md` | Task board (Ready/In Progress/Done/Blocked) |
| `.orchestra/DECISIONS.md` | Architectural decisions log |
| `.orchestra/tasks/*.md` | Individual task details |
| `.orchestra/done/*.md` | Completed task files |

### Workflow Rules

1. **Always work on a branch**: `git checkout -b task/XXX`
2. **Load context first**: Read DECISIONS.md and dependency outputs before starting
3. **One task at a time**: Finish or drop before claiming another
4. **Update both files**: Task file AND TASKS.md stay in sync
5. **Log decisions**: Any non-trivial technical choice goes in DECISIONS.md
6. **Verify before done**: Check acceptance criteria and run tests

### Task Lifecycle
```
ready ──→ in_progress ──→ done
              │
              ↓
          blocked ──→ ready (when unblocked)
```

### Important Conventions

**Task IDs**: Three-digit numbers (001, 002, etc.)

**Branch naming**: `task/XXX` where XXX is the task ID

**Commit messages**: `[XXX] Description of change`

**Decision IDs**: `DEC-XXX` sequential numbering

### Context Loading (MANDATORY before work)

Before starting any task, you MUST read:
1. `.orchestra/DECISIONS.md` - All architectural decisions
2. `.orchestra/done/[dependency-ids].md` - Output from dependency tasks
3. The task's Context Files section

This prevents context-blind mistakes and maintains consistency.

## Key Architecture Decisions

### Sprite Generation
All sprites are procedurally generated using pygame.draw functions. No external image files.

### Singleton Pattern
Use singleton pattern for global managers:
- `get_game_manager()` - Central game state
- `get_sound_manager()` - Audio system
- `get_save_manager()` - Save/Load system

### State Machine
Game uses a state machine for screen management:
- BaseState → BaseScreen → Specific screens
- StateManager handles transitions with optional fade effects

### Data-Driven Design
All balance values in `constants.py` for easy tuning:
- Dragon stats and growth rates
- Recipe definitions
- Customer behavior
- Economy values
