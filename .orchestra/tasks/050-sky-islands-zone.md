# Task 050: Sky Islands Zone

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 050 |
| **Status** | ready |
| **Branch** | task/050 |
| **Depends** | 049 |
| **Blocked-By** | |
| **Estimated** | 90 min |

## Inputs
- Spec: Zone requires Adult dragon (flight-only access)
- Spec: Contains legendary ingredients, endgame content
- src/systems/world.py

## Description
Add the Sky Islands zone, the final exploration area accessible only with an Adult dragon capable of full flight. This endgame zone contains the rarest legendary ingredients and serves as the culmination of the exploration progression.

## Acceptance Criteria
- [ ] Add ZONE_SKY_ISLANDS to constants.py
- [ ] Define zone properties:
  - Required dragon stage: Adult
  - Required ability: Full Flight
  - Primary resources: Legendary/mythical ingredients
- [ ] Add 6-8 legendary ingredients:
  - cloud_essence - Collected from clouds
  - sky_crystal - Crystals forming in high altitude
  - celestial_berry - Berries growing on floating islands
  - wind_flower - Flowers that float on air currents
  - starlight_nectar - Nectar infused with starlight
  - dragon_tear - Rare crystallized dragon tears
  - phoenix_feather - Mythical ingredient
  - sky_honey - Honey from sky bees
- [ ] Add spawn points with low spawn rates (legendary rarity)
- [ ] Add zone to WorldManager
- [ ] Add zone renderer with sky/cloud visuals
- [ ] Add 3-4 legendary recipes using Sky Islands ingredients
- [ ] Add zone to exploration navigation (flight required message)

## Context Files
- src/constants.py
- src/systems/world.py
- src/ui/zone_renderer.py
- src/states/exploration_mode_state.py

## Outputs
- Modified: src/constants.py (zone, legendary ingredients, recipes)
- Modified: src/systems/world.py
- Modified: src/ui/zone_renderer.py
- Modified: src/states/exploration_mode_state.py

---

## Work Log

