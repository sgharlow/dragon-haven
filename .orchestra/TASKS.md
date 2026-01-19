# Tasks

> Last updated: 2026-01-18
> Progress: 43/45 complete (Phase 1 done, Phase 2 in progress)

## Ready
- [ ] `044` Additional story chapters
- [ ] `045` Character affinity system

## In Progress

## Blocked

## Done (Phase 2)
- [x] `043` Evening service period ✓
- [x] `042` Additional recipes ✓
- [x] `041` Additional world zones ✓
- [x] `040` Additional dragon abilities ✓
- [x] `039` Adolescent & Adult dragon stages ✓
- [x] `038` Stormy & Special weather ✓
- [x] `037` Autumn & Winter seasons ✓
- [x] `036` Dragon naming system ✓

## Done (Phase 1)
- [x] `035` Documentation ✓
- [x] `034` Final polish ✓
- [x] `033` Save/load full implementation ✓
- [x] `032` Balance tuning ✓
- [x] `031` Screen integration ✓
- [x] `030` Story content ✓
- [x] `029` Character relationships ✓
- [x] `028` Story event system ✓
- [x] `027` Dialogue system ✓
- [x] `026` Dragon status screen ✓
- [x] `025` Recipe book screen ✓
- [x] `024` Inventory screen ✓
- [x] `023` Exploration mode UI ✓
- [x] `022` Cafe mode UI ✓
- [x] `021` Gameplay HUD ✓
- [x] `020` Settings screen ✓
- [x] `019` Main menu screen ✓
- [x] `018` Reputation system ✓
- [x] `017` Cooking minigame ✓
- [x] `016` Recipe system ✓
- [x] `015` Customer system ✓
- [x] `014` Staff system ✓
- [x] `013` Cafe system ✓
- [x] `012` Economy system ✓
- [x] `011` Resource spawning ✓
- [x] `010` World/zone system ✓
- [x] `009` Inventory system ✓
- [x] `008` Dragon system ✓
- [x] `007` Time system ✓
- [x] `006` Save system foundation ✓
- [x] `005` Sound manager ✓
- [x] `004` Asset generation system ✓
- [x] `003` State machine ✓
- [x] `002` Game engine core ✓
- [x] `001` Project setup ✓

---

## Phase 2: Expansion

Closing gaps between prototype and full specification. See `.orchestra/EXPANSION_PLAN.md` for details.

### Implementation Order
1. **Foundation** (036, 037, 038): Dragon naming, seasons, weather
2. **Dragon Expansion** (039, 040): New stages, abilities
3. **World Expansion** (041, 042): New zones, recipes
4. **Story & Depth** (043, 044, 045): Evening service, chapters, affinity

### Dependencies
```
036 Dragon Naming ────────────────────────────────┐
037 Seasons ──────→ 038 Weather                   │
039 Dragon Stages ──→ 040 Abilities               ├── All independent
                  └─→ 041 Zones ──→ 042 Recipes   │
                  └─→ 044 Story Chapters          │
043 Evening Service ──────────────────────────────┤
045 Affinity System ──────────────────────────────┘
```
