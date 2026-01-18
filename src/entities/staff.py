"""
Staff System for Dragon Haven Cafe.
NPC workers who help run the cafe with unique traits and morale.
"""

import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Callable

from constants import (
    STAFF_ROLE_SERVER, STAFF_ROLE_CHEF, STAFF_ROLE_BUSSER,
    STAFF_TRAIT_ENTHUSIASTIC, STAFF_TRAIT_SKILLED, STAFF_TRAIT_LAZY,
    STAFF_MORALE_MAX, STAFF_MORALE_START, STAFF_MORALE_DECAY_PER_HOUR,
    STAFF_TALK_MORALE_BOOST, STAFF_TALK_COOLDOWN,
    STAFF_MIN_EFFICIENCY, STAFF_MAX_EFFICIENCY,
    STAFF_MISTAKE_BASE_CHANCE, STAFF_LOW_MORALE_THRESHOLD,
    STAFF_DEFINITIONS
)


@dataclass
class StaffTask:
    """A task assigned to a staff member."""
    task_type: str  # 'serve', 'cook', 'clean', 'idle'
    target: Optional[str] = None  # Recipe ID, customer ID, etc.
    progress: float = 0.0  # 0-1 completion
    duration: float = 1.0  # Base duration in game hours

    def is_complete(self) -> bool:
        return self.progress >= 1.0


class Staff:
    """
    A cafe staff member with morale, traits, and work behavior.

    Staff members have:
    - Unique traits that affect work style
    - Morale that decays during service
    - Efficiency based on morale
    - Chance to make mistakes based on trait/morale
    """

    def __init__(self, staff_id: str, name: str, role: str, trait: str,
                 description: str = '', mistake_type: str = ''):
        """
        Initialize a staff member.

        Args:
            staff_id: Unique identifier
            name: Display name
            role: Role (server, chef, busser)
            trait: Personality trait
            description: Description text
            mistake_type: What kind of mistakes they make
        """
        self.id = staff_id
        self.name = name
        self.role = role
        self.trait = trait
        self.description = description
        self.mistake_type = mistake_type

        # State
        self._morale: float = STAFF_MORALE_START
        self._current_task: Optional[StaffTask] = None
        self._time_since_talk: float = STAFF_TALK_COOLDOWN  # Can talk immediately

        # Statistics
        self._tasks_completed: int = 0
        self._mistakes_made: int = 0

    # =========================================================================
    # MORALE
    # =========================================================================

    @property
    def morale(self) -> float:
        """Get current morale (0-100)."""
        return self._morale

    def set_morale(self, value: float):
        """Set morale, clamped to valid range."""
        self._morale = max(0, min(STAFF_MORALE_MAX, value))

    def get_mood(self) -> str:
        """Get mood string based on morale."""
        if self._morale >= 70:
            return 'happy'
        elif self._morale >= 40:
            return 'neutral'
        else:
            return 'unhappy'

    def decay_morale(self, hours: float):
        """Decay morale over time during service."""
        # Lazy staff decay faster
        decay_mult = 1.5 if self.trait == STAFF_TRAIT_LAZY else 1.0
        self._morale -= hours * STAFF_MORALE_DECAY_PER_HOUR * decay_mult
        self._morale = max(0, self._morale)

    def boost_morale(self, amount: float):
        """Boost morale (e.g., from player interaction)."""
        self._morale = min(STAFF_MORALE_MAX, self._morale + amount)

    # =========================================================================
    # TALKING
    # =========================================================================

    def can_talk(self) -> bool:
        """Check if player can talk to this staff member."""
        return self._time_since_talk >= STAFF_TALK_COOLDOWN

    def talk_to(self) -> Dict[str, Any]:
        """
        Player talks to staff, boosting morale.

        Returns:
            Result dict with morale_gain, new_morale, message
        """
        if not self.can_talk():
            return {
                'success': False,
                'message': f"{self.name} is too busy right now."
            }

        # Calculate morale boost (varies by trait)
        base_boost = STAFF_TALK_MORALE_BOOST

        if self.trait == STAFF_TRAIT_ENTHUSIASTIC:
            boost = base_boost + random.randint(0, 5)
            message = f"{self.name} beams at your encouragement!"
        elif self.trait == STAFF_TRAIT_SKILLED:
            boost = base_boost - random.randint(0, 5)
            message = f"{self.name} nods appreciatively at your feedback."
        else:  # Lazy
            boost = base_boost + random.randint(0, 8)
            message = f"{self.name} seems more motivated after your pep talk."

        self.boost_morale(boost)
        self._time_since_talk = 0

        return {
            'success': True,
            'morale_gain': boost,
            'new_morale': self._morale,
            'message': message
        }

    # =========================================================================
    # EFFICIENCY
    # =========================================================================

    def get_efficiency(self) -> float:
        """
        Get current work efficiency based on morale and trait.

        Returns:
            Efficiency multiplier (0.5-1.2)
        """
        # Base efficiency from morale
        morale_factor = self._morale / STAFF_MORALE_MAX
        efficiency = STAFF_MIN_EFFICIENCY + (1.0 - STAFF_MIN_EFFICIENCY) * morale_factor

        # Trait modifiers
        if self.trait == STAFF_TRAIT_ENTHUSIASTIC:
            efficiency *= 1.1  # Works faster
        elif self.trait == STAFF_TRAIT_SKILLED:
            efficiency *= 1.0  # Normal speed but quality
        else:  # Lazy
            efficiency *= 0.9  # Works slower

        return min(STAFF_MAX_EFFICIENCY, efficiency)

    def get_quality_bonus(self) -> float:
        """
        Get quality bonus for work output.

        Returns:
            Quality multiplier (0.8-1.2)
        """
        base = 1.0

        if self.trait == STAFF_TRAIT_SKILLED:
            base = 1.1 + (self._morale / STAFF_MORALE_MAX) * 0.1
        elif self.trait == STAFF_TRAIT_ENTHUSIASTIC:
            base = 0.95  # Slightly lower quality
        # Lazy trait: normal quality

        return base

    # =========================================================================
    # TASKS
    # =========================================================================

    def assign_task(self, task_type: str, target: str = None, duration: float = 1.0) -> bool:
        """
        Assign a task to this staff member.

        Args:
            task_type: Type of task
            target: Target (recipe ID, etc.)
            duration: Base duration in hours

        Returns:
            True if task was assigned
        """
        # Check if staff can do this task based on role
        if not self._can_do_task(task_type):
            return False

        self._current_task = StaffTask(
            task_type=task_type,
            target=target,
            progress=0.0,
            duration=duration
        )
        return True

    def _can_do_task(self, task_type: str) -> bool:
        """Check if staff can do a task based on role."""
        role_tasks = {
            STAFF_ROLE_SERVER: ['serve', 'idle', 'greet'],
            STAFF_ROLE_CHEF: ['cook', 'prep', 'idle'],
            STAFF_ROLE_BUSSER: ['clean', 'restock', 'idle'],
        }
        allowed = role_tasks.get(self.role, ['idle'])
        return task_type in allowed

    def get_current_task(self) -> Optional[StaffTask]:
        """Get current task."""
        return self._current_task

    def is_busy(self) -> bool:
        """Check if staff is working on a task."""
        return self._current_task is not None and not self._current_task.is_complete()

    def update(self, dt_hours: float) -> Dict[str, Any]:
        """
        Update staff for time passing.

        Args:
            dt_hours: Time passed in game hours

        Returns:
            Result dict with any events (task_complete, mistake, etc.)
        """
        result = {
            'task_complete': False,
            'mistake': False,
            'mistake_message': '',
            'task_result': None,
        }

        self._time_since_talk += dt_hours

        if not self._current_task:
            return result

        # Progress task based on efficiency
        efficiency = self.get_efficiency()
        progress_rate = efficiency / self._current_task.duration
        self._current_task.progress += progress_rate * dt_hours

        # Check for mistakes
        if self._should_make_mistake():
            result['mistake'] = True
            result['mistake_message'] = self._get_mistake_message()
            self._mistakes_made += 1
            # Mistake might reset progress or cause other issues
            self._current_task.progress = max(0, self._current_task.progress - 0.3)

        # Check for completion
        if self._current_task.is_complete():
            result['task_complete'] = True
            result['task_result'] = {
                'task_type': self._current_task.task_type,
                'target': self._current_task.target,
                'quality': self.get_quality_bonus(),
            }
            self._tasks_completed += 1
            self._current_task = None

        return result

    def _should_make_mistake(self) -> bool:
        """Check if staff makes a mistake this update."""
        base_chance = STAFF_MISTAKE_BASE_CHANCE

        # Low morale increases mistakes
        if self._morale < STAFF_LOW_MORALE_THRESHOLD:
            base_chance *= 2

        # Trait modifiers
        if self.trait == STAFF_TRAIT_ENTHUSIASTIC:
            base_chance *= 1.5  # More likely to make mistakes
        elif self.trait == STAFF_TRAIT_SKILLED:
            base_chance *= 0.5  # Less likely
        # Lazy: normal chance

        return random.random() < base_chance

    def _get_mistake_message(self) -> str:
        """Get a message describing the mistake."""
        messages = {
            STAFF_TRAIT_ENTHUSIASTIC: [
                f"{self.name} accidentally knocked something over!",
                f"{self.name} was moving too fast and made an error.",
                f"{self.name}'s enthusiasm led to a small mishap.",
            ],
            STAFF_TRAIT_SKILLED: [
                f"{self.name} refused to make an unfamiliar dish.",
                f"{self.name} insisted on doing it 'the right way' and lost time.",
            ],
            STAFF_TRAIT_LAZY: [
                f"{self.name} was caught slacking off!",
                f"{self.name} took an unscheduled break.",
                f"{self.name} moved too slowly and missed the timing.",
            ],
        }
        options = messages.get(self.trait, [f"{self.name} made a mistake."])
        return random.choice(options)

    # =========================================================================
    # AUTONOMOUS BEHAVIOR
    # =========================================================================

    def get_autonomous_action(self) -> Optional[str]:
        """
        Get what this staff would do autonomously.

        Returns:
            Task type they would choose, or None
        """
        if self.is_busy():
            return None

        # Based on trait
        if self.trait == STAFF_TRAIT_ENTHUSIASTIC:
            # Always ready to work
            if self.role == STAFF_ROLE_SERVER:
                return 'serve' if random.random() < 0.8 else 'greet'
            elif self.role == STAFF_ROLE_CHEF:
                return 'prep'
            else:
                return 'clean'

        elif self.trait == STAFF_TRAIT_SKILLED:
            # Works, but might idle if morale low
            if self._morale < 50:
                return 'idle' if random.random() < 0.3 else self._get_role_task()
            return self._get_role_task()

        else:  # Lazy
            # Often idles unless morale is high
            if self._morale < 70:
                return 'idle' if random.random() < 0.5 else self._get_role_task()
            return self._get_role_task()

    def _get_role_task(self) -> str:
        """Get default task for this role."""
        defaults = {
            STAFF_ROLE_SERVER: 'serve',
            STAFF_ROLE_CHEF: 'cook',
            STAFF_ROLE_BUSSER: 'clean',
        }
        return defaults.get(self.role, 'idle')

    # =========================================================================
    # SERIALIZATION
    # =========================================================================

    def get_state(self) -> Dict[str, Any]:
        """Get state for saving."""
        return {
            'id': self.id,
            'morale': self._morale,
            'time_since_talk': self._time_since_talk,
            'tasks_completed': self._tasks_completed,
            'mistakes_made': self._mistakes_made,
            'current_task': {
                'task_type': self._current_task.task_type,
                'target': self._current_task.target,
                'progress': self._current_task.progress,
                'duration': self._current_task.duration,
            } if self._current_task else None
        }

    def load_state(self, state: Dict[str, Any]):
        """Load state from save data."""
        self._morale = state.get('morale', STAFF_MORALE_START)
        self._time_since_talk = state.get('time_since_talk', STAFF_TALK_COOLDOWN)
        self._tasks_completed = state.get('tasks_completed', 0)
        self._mistakes_made = state.get('mistakes_made', 0)

        task_data = state.get('current_task')
        if task_data:
            self._current_task = StaffTask(
                task_type=task_data['task_type'],
                target=task_data.get('target'),
                progress=task_data.get('progress', 0),
                duration=task_data.get('duration', 1.0)
            )


class StaffManager:
    """
    Manages all staff members.

    Usage:
        staff_mgr = get_staff_manager()
        staff_mgr.initialize()

        melody = staff_mgr.get_staff('melody')
        melody.talk_to()
    """

    def __init__(self):
        """Initialize the staff manager."""
        self._staff: Dict[str, Staff] = {}
        self._initialized = False

    def initialize(self):
        """Initialize all staff from definitions."""
        if self._initialized:
            return

        for staff_id, data in STAFF_DEFINITIONS.items():
            staff = Staff(
                staff_id=staff_id,
                name=data['name'],
                role=data['role'],
                trait=data['trait'],
                description=data.get('description', ''),
                mistake_type=data.get('mistake_type', '')
            )
            self._staff[staff_id] = staff

        self._initialized = True

    # =========================================================================
    # STAFF ACCESS
    # =========================================================================

    def get_staff(self, staff_id: str) -> Optional[Staff]:
        """Get a staff member by ID."""
        return self._staff.get(staff_id)

    def get_all_staff(self) -> List[Staff]:
        """Get all staff members."""
        return list(self._staff.values())

    def get_staff_by_role(self, role: str) -> List[Staff]:
        """Get staff members with a specific role."""
        return [s for s in self._staff.values() if s.role == role]

    # =========================================================================
    # UPDATES
    # =========================================================================

    def update(self, dt_hours: float) -> List[Dict[str, Any]]:
        """
        Update all staff members.

        Returns:
            List of events from staff updates
        """
        events = []
        for staff in self._staff.values():
            result = staff.update(dt_hours)
            if result['task_complete'] or result['mistake']:
                result['staff_id'] = staff.id
                result['staff_name'] = staff.name
                events.append(result)
        return events

    def decay_all_morale(self, hours: float):
        """Decay morale for all staff during service."""
        for staff in self._staff.values():
            staff.decay_morale(hours)

    def reset_morale_for_new_day(self):
        """Reset morale at start of new day (slight recovery)."""
        for staff in self._staff.values():
            # Recover 10-20 morale overnight
            recovery = 10 + (staff.morale / STAFF_MORALE_MAX) * 10
            staff.boost_morale(recovery)

    # =========================================================================
    # SERIALIZATION
    # =========================================================================

    def get_state(self) -> Dict[str, Any]:
        """Get state for saving."""
        return {
            'staff': {
                staff_id: staff.get_state()
                for staff_id, staff in self._staff.items()
            }
        }

    def load_state(self, state: Dict[str, Any]):
        """Load state from save data."""
        if not self._initialized:
            self.initialize()

        staff_states = state.get('staff', {})
        for staff_id, staff_state in staff_states.items():
            if staff_id in self._staff:
                self._staff[staff_id].load_state(staff_state)


# =============================================================================
# SINGLETON ACCESS
# =============================================================================

_staff_manager = None


def get_staff_manager() -> StaffManager:
    """Get the global staff manager instance."""
    global _staff_manager
    if _staff_manager is None:
        _staff_manager = StaffManager()
    return _staff_manager


def reset_staff_manager():
    """Reset the staff manager (for new game)."""
    global _staff_manager
    _staff_manager = StaffManager()
