# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Dragon Haven Cafe is a dragon-raising cafe management simulation game built with Python and Pygame. Players raise a baby dragon while operating a family cafe, gathering ingredients from an explorable world.

## Development Commands

```bash
pip install pygame        # Install dependencies
cd src && python main.py  # Run the game (must run from src/)
```

No test framework or build commands - this is a pure Python project that runs directly.

## Architecture

### Entry Point & Game Loop

- `src/main.py` - Entry point that initializes all systems and starts the game
- `src/game.py` - Main Game class with pygame initialization, event handling, and 60 FPS game loop with delta time

### Singleton Pattern (Global Managers)

All managers use lazy-initialized singletons accessed via `get_*()` functions:

| Function | Module | Purpose |
|----------|--------|---------|
| `get_time_manager()` | systems/time_system.py | Day/night cycle, seasons, time callbacks |
| `get_inventory()` | systems/inventory.py | Items, storage, spoilage tracking |
| `get_world_manager()` | systems/world.py | Zones, tile maps, resource points |
| `get_resource_manager()` | systems/resources.py | Ingredient spawning/harvesting |
| `get_recipe_manager()` | systems/recipes.py | Recipe definitions, unlocks, mastery |
| `get_cafe_manager()` | systems/cafe.py | Cafe operations, service, reputation |
| `get_economy()` | systems/economy.py | Pricing, transactions, earnings |
| `get_dialogue_manager()` | systems/dialogue.py | Dialogue tree loading/playback |
| `get_story_manager()` | systems/story.py | Story events and chapter progression |
| `get_character_manager()` | entities/story_character.py | NPCs and relationships |
| `get_customer_manager()` | entities/customer.py | Customer generation and preferences |
| `get_staff_manager()` | entities/staff.py | Staff workers and morale |
| `get_save_manager()` | save_manager.py | Save/Load with 3 slots |
| `get_sound_manager()` | sound_manager.py | Procedural audio synthesis |
| `get_game_state_manager()` | game_state.py | Aggregates state for save/load |
| `get_sprite_generator()` | sprites.py | Procedural sprite generation |

### State Machine (Screen Management)

All screens extend `BaseScreen` (which extends `BaseState`) in `states/base_state.py`:

```python
class MyScreen(BaseScreen):
    def enter(self, previous_state=None): ...  # Called on screen entry
    def handle_event(self, event): ...         # Process pygame events
    def update(self, dt): ...                  # Update logic (dt in seconds)
    def draw(self, screen): ...                # Render to screen
    def exit(self): ...                        # Cleanup on exit
```

`StateManager` in `state_manager.py` handles transitions with optional fade effects. States request transitions via `self.transition_to('state_name')`.

**Registered states**: main_menu, exploration, cafe, inventory, recipe_book, dragon_status, pause_menu, save_load, settings

### Procedural Asset Generation

All visual and audio assets are generated at runtime (no external files):
- **Sprites** (`sprites.py`): All graphics via `pygame.draw` functions
- **Sound** (`sound_manager.py`): Audio via waveform synthesis

### Data Serialization Pattern

All entities use `@dataclass` with `to_dict()`/`from_dict()` methods for save/load:

```python
@dataclass
class EntityData:
    def to_dict(self): return asdict(self)
    @classmethod
    def from_dict(cls, data): return cls(**data)
```

### Key Configuration

`src/constants.py` contains all tunable values:
- Display: 1280x720, 60 FPS
- Time scale: 30 real seconds = 1 game hour
- Dragon: 3 stages, stat decay rates, abilities
- Recipes: ~15 dishes with ingredients/difficulty
- Economy: pricing, tips, reputation effects

### Directory Structure

```
src/
├── main.py, game.py     # Entry point and game loop
├── constants.py         # All configuration values
├── state_manager.py     # State machine
├── game_state.py        # Save state aggregation
├── save_manager.py      # File persistence
├── sound_manager.py     # Procedural audio
├── sprites.py           # Procedural graphics
├── entities/            # Dragon, Player, Customer, Staff, Characters
├── systems/             # Time, Inventory, World, Recipes, Cafe, Economy, Dialogue, Story
├── states/              # Screen implementations (BaseState → BaseScreen → Specific)
└── ui/                  # UI components (HUD, buttons, tooltips, minigame)
data/                    # JSON content (dialogues/, events/, characters/)
saves/                   # Runtime save files (slot_1.json, slot_2.json, slot_3.json)
```

## Orchestra Lite (Task Coordination)

This project uses Orchestra Lite for multi-agent coordination:

```
/orchestra plan    - Break down goals into tasks
/orchestra work    - Claim and complete next task
/orchestra status  - Check progress
/orchestra done ID - Mark task complete
```

**Key files**: `.orchestra/GOAL.md`, `PLAN.md`, `TASKS.md`, `DECISIONS.md`

**Conventions**:
- Task IDs: Three-digit (001, 002, etc.)
- Branch naming: `task/XXX`
- Commit messages: `[XXX] Description`
- Decisions: `DEC-XXX` in DECISIONS.md

**Before starting any task**: Read `DECISIONS.md` and dependency task outputs in `.orchestra/done/`.
