# Task 013: Cafe State and Operations

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 013 |
| **Status** | ready |
| **Branch** | task/013 |
| **Assigned** | |
| **Depends** | 007, 012 |
| **Blocked-By** | |
| **Estimated** | 60 min |

## Inputs
- src/systems/time_system.py from 007
- src/systems/economy.py from 012

## Description
Create the cafe management system that handles cafe operations, service periods, and overall cafe state. The core framework for cafe gameplay.

## Acceptance Criteria
- [ ] CafeManager class with singleton get_cafe_manager()
- [ ] Cafe states: CLOSED, PREP, SERVICE, CLEANUP
- [ ] Service period: 10:00-14:00 (single period for prototype)
- [ ] start_service(), end_service() methods
- [ ] Service automatically starts/ends based on time
- [ ] Prep phase (30 min before service) for setup
- [ ] Track customers served today
- [ ] Track revenue today
- [ ] Menu management (which recipes are available today)
- [ ] set_menu(), get_menu()
- [ ] Cafe can be skipped (with reputation penalty)
- [ ] Callbacks for service events
- [ ] Serialization for save/load

## Context Files
- src/systems/time_system.py
- src/systems/economy.py
- src/constants.py
- Dragon_Haven_Cafe_Software_Specification.docx.md (Section 4.1)

## Outputs
- Created: src/systems/cafe.py (CafeManager, get_cafe_manager)
- Modified: src/constants.py (cafe timing, service config)

---

## Work Log

