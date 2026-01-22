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

### Quick Reference Card

```
┌─────────────────────────────────────────────────────────────┐
│  EXPLORATION                    MENUS                       │
│  ───────────                    ─────                       │
│  W/↑ = Up                       ↑/↓ = Navigate              │
│  S/↓ = Down                     Enter/Space = Select        │
│  A/← = Left                     ESC = Back/Close            │
│  D/→ = Right                                                │
│  E/Space = Interact             QUICK ACCESS                │
│  P = Pet Dragon                 ─────────────               │
│  C = Open Cafe (at cafe)        I = Inventory               │
│                                 R = Recipe Book             │
│  ABILITIES                      D = Dragon Status           │
│  ─────────                      ESC = Pause Menu            │
│  1-9, 0 = Dragon Abilities                                  │
└─────────────────────────────────────────────────────────────┘
```

### Exploration Mode (Walking Around)

| Key | Action | Notes |
|-----|--------|-------|
| **W** or **↑** | Move Up | Hold for continuous movement |
| **S** or **↓** | Move Down | Hold for continuous movement |
| **A** or **←** | Move Left | Hold for continuous movement |
| **D** or **→** | Move Right | Hold for continuous movement |
| **E** or **Space** | Interact | Talk to NPCs, gather resources, use objects |
| **P** | Pet Dragon | Increases dragon happiness and bond |
| **C** | Open Cafe | Only works when at cafe grounds |

### Dragon Abilities

| Key | Ability Slot | Notes |
|-----|--------------|-------|
| **1** | Ability 1 | Unlocked abilities vary by dragon stage |
| **2** | Ability 2 | |
| **3** | Ability 3 | |
| **4** | Ability 4 | |
| **5** | Ability 5 | |
| **6** | Ability 6 | |
| **7** | Ability 7 | |
| **8** | Ability 8 | |
| **9** | Ability 9 | |
| **0** | Ability 10 | |

### Menu Navigation

| Key | Action | Where it works |
|-----|--------|----------------|
| **↑** / **↓** | Navigate options | All menus |
| **Enter** or **Space** | Confirm selection | All menus |
| **ESC** | Go back / Close menu | All menus |
| **Delete** | Delete save file | Save/Load screen only |

### Quick Access (Works Anytime During Gameplay)

| Key | Opens | Notes |
|-----|-------|-------|
| **ESC** | Pause Menu | Access settings, save/load, quit |
| **I** | Inventory | View and manage your items |
| **R** | Recipe Book | Browse recipes and mastery levels |
| **D** | Dragon Status | Check dragon stats, feed, and care |

### Cooking Minigame

The cooking minigame uses a **4-lane rhythm system**. Notes fall down 4 lanes - press the matching key when they hit the target line.

| Key | Lane | Alternative Key |
|-----|------|-----------------|
| **A** | Lane 1 (Left) | **←** |
| **S** | Lane 2 (Down) | **↓** |
| **D** | Lane 3 (Up) | **↑** |
| **F** | Lane 4 (Right) | **→** |

**Tips:**
- Hit notes as close to the target line as possible
- Perfect timing = higher dish quality
- Chain successful hits for combo bonuses

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
