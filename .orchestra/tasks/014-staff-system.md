# Task 014: Staff System

## Metadata
| Field | Value |
|-------|-------|
| **ID** | 014 |
| **Status** | done |
| **Branch** | task/014 |
| **Assigned** | task/014 |
| **Depends** | 013 |
| **Blocked-By** | |
| **Estimated** | 60 min |

## Inputs
- src/systems/cafe.py from 013

## Description
Create the staff system with NPC workers who help run the cafe. Each staff member has unique traits, morale that affects performance, and can be directed by the player.

## Acceptance Criteria
- [x] Staff class: name, role, trait, morale (0-100), efficiency
- [x] 3 staff members:
  - Melody (Server): Enthusiastic but clumsy, needs pep talks
  - Bruno (Chef): Skilled but prideful, needs recipe guidance
  - Sage (Busser): Lazy but perceptive, needs frequent motivation
- [x] Morale affects work efficiency (50% morale = 50% efficiency)
- [x] Morale decays slowly over time
- [x] talk_to(staff) increases morale (+10-20)
- [x] assign_task(staff, task) for specific orders
- [x] Autonomous behavior when not directed (with trait quirks)
- [x] Staff can make mistakes based on trait (Melody drops things, etc.)
- [x] Visual feedback for staff morale (happy/neutral/unhappy)
- [x] Serialization for save/load

## Context Files
- src/systems/cafe.py
- src/constants.py
- Dragon_Haven_Cafe_Software_Specification.docx.md (Section 4.2)

## Outputs
- Created: src/entities/staff.py (Staff class, staff definitions)
- Modified: src/systems/cafe.py (integrate staff)
- Modified: src/constants.py (staff configs)

---

## Work Log

### 2026-01-17
- Added staff constants to constants.py (roles, traits, morale settings)
- Defined 3 staff members: Melody, Bruno, Sage with unique traits
- Created Staff class with morale, efficiency, task management
- Implemented trait-based behavior modifiers
- Created StaffTask dataclass for task tracking
- Implemented talk_to() with cooldown and morale boost
- Added efficiency calculation based on morale and trait
- Implemented autonomous behavior with trait quirks
- Added mistake system with trait-specific messages
- Created StaffManager with singleton pattern
- Implemented full serialization
- Updated entities/__init__.py
- All tests pass

