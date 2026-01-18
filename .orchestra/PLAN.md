# High-Level Plan: Dragon Haven Cafe

## Phase 1: Foundation (Tasks 001-006)
Core infrastructure and engine setup.

- Project structure and pygame initialization
- Game loop with delta time
- State machine for screen management
- Asset generation system (procedural sprites)
- Sound manager with procedural audio
- Save/Load system foundation

## Phase 2: Core Systems (Tasks 007-012)
The fundamental game mechanics.

- Time system (day/night cycle, seasons)
- Dragon entity system (stats, stages, colors)
- Inventory system (items, storage, recipes)
- World/Zone system (exploration, resources)
- Ingredient and resource spawning
- Economy system (gold, pricing)

## Phase 3: Cafe Operations (Tasks 013-018)
The cafe management gameplay.

- Cafe state and operations flow
- Staff system (NPC workers, morale)
- Customer system (orders, satisfaction)
- Recipe system (definitions, unlocks)
- Cooking minigame (rhythm-based)
- Reputation and progression

## Phase 4: UI Screens (Tasks 019-026)
All game screens and menus.

- Main menu and title screen
- Settings screen
- Gameplay HUD
- Cafe mode UI (kitchen, serving)
- Exploration mode UI
- Inventory screen
- Recipe book screen
- Dragon status screen

## Phase 5: Story & Content (Tasks 027-030)
Narrative and content.

- Dialogue system
- Story event system
- Character relationships
- Prologue and Chapter 1 content

## Phase 6: Integration & Polish (Tasks 031-035)
Final integration and polish.

- Screen integration and flow
- Balance tuning
- Save/Load full implementation
- Final polish and testing
- README and documentation

## Dependencies Flow
```
Phase 1 (Foundation)
    ↓
Phase 2 (Core Systems) ←→ Phase 3 (Cafe Operations)
    ↓                           ↓
         Phase 4 (UI Screens)
              ↓
    Phase 5 (Story & Content)
              ↓
    Phase 6 (Integration & Polish)
```

## Estimated Tasks: ~35
