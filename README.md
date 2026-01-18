# Dragon Haven Cafe

A cozy dragon-raising cafe management simulation game built with Python and Pygame.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Pygame](https://img.shields.io/badge/Pygame-2.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## Overview

In Dragon Haven Cafe, you inherit a magical cafe with an unusual twist - your business partner is a dragon! Raise your dragon companion from an egg through multiple life stages while running a successful cafe, exploring the surrounding lands for ingredients, and uncovering a heartwarming story about friendship and magic.

### Features

- **Dragon Raising**: Nurture your dragon through 3 life stages (Egg → Hatchling → Juvenile)
- **Cafe Management**: Serve customers, manage staff, build reputation
- **Cooking Minigame**: Rhythm-based cooking system with quality ratings
- **Exploration**: Gather ingredients across 3 unique zones
- **Day/Night Cycle**: Time-based gameplay with morning, afternoon, and evening periods
- **Story System**: Engaging narrative with memorable characters
- **Save/Load**: Full game state persistence with auto-save

## Installation

### Requirements

- Python 3.8 or higher
- Pygame 2.0 or higher

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/dragon-haven.git
cd dragon-haven
```

2. Install dependencies:
```bash
pip install pygame
```

3. Run the game:
```bash
cd src
python main.py
```

## Controls

### Movement & Interaction
| Key | Action |
|-----|--------|
| W/↑ | Move Up |
| S/↓ | Move Down |
| A/← | Move Left |
| D/→ | Move Right |
| E/Space | Interact |

### Dragon Abilities
| Key | Action |
|-----|--------|
| 1 | Primary Ability |
| 2 | Secondary Ability |
| 3 | Special Ability |

### Menu & Navigation
| Key | Action |
|-----|--------|
| ESC | Pause Menu |
| I | Open Inventory |
| R | Open Recipe Book |
| D | Dragon Status |
| Enter | Confirm Selection |
| Tab | Switch between modes |

### Cooking Minigame
| Key | Action |
|-----|--------|
| Space | Hit timing beat |
| Arrow Keys | Direction inputs |

## Gameplay Guide

### Dragon Care

Your dragon grows through stages based on time and care:
- **Egg Stage**: Keep it warm and fed. Hatches after Day 2.
- **Hatchling Stage**: Feed regularly to increase bond. Grows to Juvenile at Day 5.
- **Juvenile Stage**: Your dragon can now help in the cafe!

Dragon stats to monitor:
- **Hunger**: Feed your dragon regularly from your inventory
- **Happiness**: Pet and play with your dragon
- **Bond Level**: Increases through positive interactions

### Cafe Operations

1. **Morning**: Prepare ingredients and check your dragon
2. **Afternoon**: Cafe opens! Serve customers and cook dishes
3. **Evening**: Wrap up service, count earnings, explore

Tips:
- Match dishes to customer preferences for bonus tips
- Keep staff morale high for better service
- Build reputation to unlock new recipes

### Exploration & Gathering

Three zones to explore:
- **Cafe Grounds**: Basic herbs and common ingredients
- **Meadow Fields**: Berries, flowers, and rare herbs
- **Forest Depths**: Mushrooms, rare ingredients, and secrets

Resources respawn over time. Visit different zones each day for variety!

### Cooking Minigame

The cooking minigame is rhythm-based:
1. Ingredients appear on a timeline
2. Press Space when the indicator reaches the target
3. Perfect timing = higher quality dish
4. Chain combos for bonus points

Quality ratings:
- ★★★★★ Perfect (4.5+)
- ★★★★ Excellent (3.5-4.4)
- ★★★ Good (2.5-3.4)
- ★★ Okay (1.5-2.4)
- ★ Poor (<1.5)

## Project Structure

```
dragon-haven/
├── src/
│   ├── main.py              # Entry point
│   ├── game.py              # Main game loop
│   ├── game_state.py        # Save/load state management
│   ├── state_manager.py     # Screen state machine
│   ├── constants.py         # Game configuration
│   ├── save_manager.py      # Save file handling
│   ├── sound_manager.py     # Audio management
│   ├── states/              # Screen states
│   │   ├── main_menu_state.py
│   │   ├── exploration_mode_state.py
│   │   ├── cafe_mode_state.py
│   │   ├── inventory_state.py
│   │   └── ...
│   ├── systems/             # Game systems
│   │   ├── time_system.py
│   │   ├── inventory.py
│   │   ├── recipes.py
│   │   ├── cafe.py
│   │   ├── dialogue.py
│   │   ├── story.py
│   │   └── ...
│   ├── entities/            # Game entities
│   │   ├── dragon.py
│   │   ├── player.py
│   │   └── story_character.py
│   └── ui/                  # UI components
│       ├── components.py
│       └── hud.py
├── data/
│   ├── dialogues/           # Dialogue JSON files
│   ├── events/              # Story event JSON files
│   └── characters/          # Character definition files
├── saves/                   # Save game files (created at runtime)
└── README.md
```

## Save Files

Save files are stored in the `saves/` directory:
- `slot_1.json`, `slot_2.json`, `slot_3.json`
- Auto-save occurs at the end of each in-game day
- Save files include: game progress, dragon state, inventory, reputation, and story progress

## Troubleshooting

### Game won't start
- Ensure Python 3.8+ is installed: `python --version`
- Ensure Pygame is installed: `pip install pygame`
- Run from the `src/` directory

### No sound
- Sound is optional; the game will run silently if audio initialization fails
- Check your system audio settings

### Performance issues
- The game targets 60 FPS
- Close other applications if experiencing slowdown
- Check your Python version (3.8+ recommended)

### Save file issues
- Save files are JSON format in the `saves/` folder
- If a save becomes corrupted, delete it and start a new game
- Version mismatches will show a warning but still attempt to load

## Credits

**Dragon Haven Cafe** is a prototype game developed as a demonstration of Python/Pygame game development with comprehensive systems including:
- State machine architecture
- Singleton pattern for global systems
- JSON-based data loading
- Rhythm game mechanics
- Procedural sprite generation

## License

MIT License - See LICENSE file for details.

---

*Thank you for playing Dragon Haven Cafe! May your dragon grow strong and your cafe flourish.*
