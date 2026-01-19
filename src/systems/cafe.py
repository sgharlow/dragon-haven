"""
Cafe Management System for Dragon Haven Cafe.
Handles cafe operations, service periods, menu management, and daily tracking.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Callable

from constants import (
    CAFE_STATE_CLOSED, CAFE_STATE_PREP, CAFE_STATE_SERVICE, CAFE_STATE_CLEANUP,
    CAFE_SERVICE_START, CAFE_SERVICE_END,
    CAFE_PREP_DURATION, CAFE_CLEANUP_DURATION,
    CAFE_MAX_MENU_ITEMS, CAFE_SKIP_REP_PENALTY,
    CAFE_SKIP_SERVICE_PENALTY, CAFE_SKIP_DAY_PENALTY,
    SERVICE_PERIOD_MORNING, SERVICE_PERIOD_EVENING,
    CAFE_MORNING_SERVICE_START, CAFE_MORNING_SERVICE_END,
    CAFE_MORNING_PREP_START, CAFE_MORNING_CLEANUP_END,
    CAFE_EVENING_SERVICE_START, CAFE_EVENING_SERVICE_END,
    CAFE_EVENING_PREP_START, CAFE_EVENING_CLEANUP_END,
    SERVICE_VOLUME_MULTIPLIER, SERVICE_CATEGORY_PREFERENCE,
    REPUTATION_MIN, REPUTATION_MAX,
    REPUTATION_LEVEL_UNKNOWN, REPUTATION_LEVEL_LOCAL,
    REPUTATION_LEVEL_TOWN, REPUTATION_LEVEL_REGIONAL,
    REPUTATION_LEVELS, REPUTATION_CUSTOMER_RANGE, REPUTATION_UNLOCKS,
    REPUTATION_DAILY_DECAY,
)
from systems.time_system import get_time_manager
from systems.economy import get_economy


@dataclass
class ServiceStats:
    """Statistics for a service period."""
    customers_served: int = 0
    dishes_sold: int = 0
    revenue: int = 0
    tips: int = 0
    satisfaction_sum: float = 0.0
    satisfaction_count: int = 0

    @property
    def average_satisfaction(self) -> float:
        if self.satisfaction_count == 0:
            return 0.0
        return self.satisfaction_sum / self.satisfaction_count

    def to_dict(self) -> Dict[str, Any]:
        return {
            'customers_served': self.customers_served,
            'dishes_sold': self.dishes_sold,
            'revenue': self.revenue,
            'tips': self.tips,
            'satisfaction_sum': self.satisfaction_sum,
            'satisfaction_count': self.satisfaction_count
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ServiceStats':
        return cls(
            customers_served=data.get('customers_served', 0),
            dishes_sold=data.get('dishes_sold', 0),
            revenue=data.get('revenue', 0),
            tips=data.get('tips', 0),
            satisfaction_sum=data.get('satisfaction_sum', 0.0),
            satisfaction_count=data.get('satisfaction_count', 0)
        )


class CafeManager:
    """
    Manages the cafe's operations and service periods.

    Usage:
        cafe = get_cafe_manager()
        cafe.set_menu(['berry_tart', 'herb_soup'])

        # Update each frame
        cafe.update(time_manager.current_hour)

        # Service callbacks
        cafe.on_service_start(callback)
        cafe.on_service_end(callback)
    """

    def __init__(self):
        """Initialize the cafe manager."""
        self._state: str = CAFE_STATE_CLOSED
        self._current_menu: List[str] = []  # Recipe IDs
        self._reputation: int = 0

        # Service period tracking
        self._current_service_period: Optional[str] = None
        self._morning_stats: ServiceStats = ServiceStats()
        self._evening_stats: ServiceStats = ServiceStats()
        self._morning_completed: bool = False
        self._evening_completed: bool = False
        self._morning_skipped: bool = False
        self._evening_skipped: bool = False

        # Backwards compatibility
        self._today_stats: ServiceStats = ServiceStats()  # Combined stats
        self._day_skipped: bool = False
        self._service_completed: bool = False

        # Callbacks
        self._on_prep_start: List[Callable] = []
        self._on_service_start: List[Callable] = []
        self._on_service_end: List[Callable] = []
        self._on_cleanup_end: List[Callable] = []

    # =========================================================================
    # STATE MANAGEMENT
    # =========================================================================

    def get_state(self) -> str:
        """Get current cafe state."""
        return self._state

    def is_open(self) -> bool:
        """Check if cafe is in service."""
        return self._state == CAFE_STATE_SERVICE

    def is_prep(self) -> bool:
        """Check if in prep phase."""
        return self._state == CAFE_STATE_PREP

    def is_closed(self) -> bool:
        """Check if cafe is closed."""
        return self._state == CAFE_STATE_CLOSED

    def update(self, current_hour: float):
        """
        Update cafe state based on current time.

        Args:
            current_hour: Current game hour (0-24)
        """
        old_state = self._state
        old_period = self._current_service_period

        # Determine which service period we're in (or between)
        new_state = CAFE_STATE_CLOSED
        new_period = None

        # Check morning service
        if not self._morning_skipped and not self._morning_completed:
            if CAFE_MORNING_PREP_START <= current_hour < CAFE_MORNING_SERVICE_START:
                new_state = CAFE_STATE_PREP
                new_period = SERVICE_PERIOD_MORNING
            elif CAFE_MORNING_SERVICE_START <= current_hour < CAFE_MORNING_SERVICE_END:
                new_state = CAFE_STATE_SERVICE
                new_period = SERVICE_PERIOD_MORNING
            elif CAFE_MORNING_SERVICE_END <= current_hour < CAFE_MORNING_CLEANUP_END:
                new_state = CAFE_STATE_CLEANUP
                new_period = SERVICE_PERIOD_MORNING

        # Check evening service (only if not in morning service)
        if new_state == CAFE_STATE_CLOSED and not self._evening_skipped and not self._evening_completed:
            if CAFE_EVENING_PREP_START <= current_hour < CAFE_EVENING_SERVICE_START:
                new_state = CAFE_STATE_PREP
                new_period = SERVICE_PERIOD_EVENING
            elif CAFE_EVENING_SERVICE_START <= current_hour < CAFE_EVENING_SERVICE_END:
                new_state = CAFE_STATE_SERVICE
                new_period = SERVICE_PERIOD_EVENING
            elif CAFE_EVENING_SERVICE_END <= current_hour < CAFE_EVENING_CLEANUP_END:
                new_state = CAFE_STATE_CLEANUP
                new_period = SERVICE_PERIOD_EVENING

        self._state = new_state
        self._current_service_period = new_period

        # Update backwards compatibility flags
        self._service_completed = self._morning_completed or self._evening_completed
        self._day_skipped = self._morning_skipped and self._evening_skipped

        # Fire callbacks on state changes
        if old_state != self._state or old_period != new_period:
            self._on_state_change(old_state, self._state, old_period, new_period)

    def _on_state_change(self, old_state: str, new_state: str,
                         old_period: Optional[str] = None, new_period: Optional[str] = None):
        """Handle state transitions."""
        if new_state == CAFE_STATE_PREP:
            for cb in self._on_prep_start:
                cb()

        elif new_state == CAFE_STATE_SERVICE and old_state == CAFE_STATE_PREP:
            for cb in self._on_service_start:
                cb()

        elif new_state == CAFE_STATE_CLEANUP and old_state == CAFE_STATE_SERVICE:
            # Mark the appropriate service as completed
            if old_period == SERVICE_PERIOD_MORNING:
                self._morning_completed = True
                stats = self._morning_stats
            elif old_period == SERVICE_PERIOD_EVENING:
                self._evening_completed = True
                stats = self._evening_stats
            else:
                stats = self._today_stats

            self._service_completed = True
            for cb in self._on_service_end:
                cb(stats)

        elif new_state == CAFE_STATE_CLOSED and old_state == CAFE_STATE_CLEANUP:
            for cb in self._on_cleanup_end:
                cb()

    def start_service(self) -> bool:
        """
        Manually start service (if in prep).

        Returns:
            True if service started
        """
        if self._state == CAFE_STATE_PREP:
            self._state = CAFE_STATE_SERVICE
            for cb in self._on_service_start:
                cb()
            return True
        return False

    def end_service(self) -> bool:
        """
        Manually end service.

        Returns:
            True if service ended
        """
        if self._state == CAFE_STATE_SERVICE:
            self._state = CAFE_STATE_CLEANUP
            self._service_completed = True
            for cb in self._on_service_end:
                cb(self._today_stats)
            return True
        return False

    # =========================================================================
    # MENU MANAGEMENT
    # =========================================================================

    def set_menu(self, recipe_ids: List[str]):
        """
        Set today's menu.

        Args:
            recipe_ids: List of recipe IDs to serve
        """
        self._current_menu = recipe_ids[:CAFE_MAX_MENU_ITEMS]

    def get_menu(self) -> List[str]:
        """Get current menu."""
        return self._current_menu.copy()

    def add_to_menu(self, recipe_id: str) -> bool:
        """
        Add a recipe to the menu.

        Returns:
            True if added successfully
        """
        if recipe_id in self._current_menu:
            return False
        if len(self._current_menu) >= CAFE_MAX_MENU_ITEMS:
            return False
        self._current_menu.append(recipe_id)
        return True

    def remove_from_menu(self, recipe_id: str) -> bool:
        """
        Remove a recipe from the menu.

        Returns:
            True if removed
        """
        if recipe_id not in self._current_menu:
            return False
        self._current_menu.remove(recipe_id)
        return True

    def clear_menu(self):
        """Clear the menu."""
        self._current_menu = []

    # =========================================================================
    # SERVICE PERIOD INFO
    # =========================================================================

    def get_current_service_period(self) -> Optional[str]:
        """Get the current service period (morning/evening) or None if closed."""
        return self._current_service_period

    def get_service_volume_multiplier(self) -> float:
        """Get customer volume multiplier for current service period."""
        if self._current_service_period:
            return SERVICE_VOLUME_MULTIPLIER.get(self._current_service_period, 1.0)
        return 1.0

    def get_service_category_preference(self, category: str) -> float:
        """Get category preference multiplier for current service period."""
        if self._current_service_period:
            prefs = SERVICE_CATEGORY_PREFERENCE.get(self._current_service_period, {})
            return prefs.get(category, 1.0)
        return 1.0

    def is_morning_completed(self) -> bool:
        """Check if morning service was completed."""
        return self._morning_completed

    def is_evening_completed(self) -> bool:
        """Check if evening service was completed."""
        return self._evening_completed

    def is_morning_skipped(self) -> bool:
        """Check if morning service was skipped."""
        return self._morning_skipped

    def is_evening_skipped(self) -> bool:
        """Check if evening service was skipped."""
        return self._evening_skipped

    # =========================================================================
    # SERVICE TRACKING
    # =========================================================================

    def _get_current_stats(self) -> ServiceStats:
        """Get the stats object for the current service period."""
        if self._current_service_period == SERVICE_PERIOD_MORNING:
            return self._morning_stats
        elif self._current_service_period == SERVICE_PERIOD_EVENING:
            return self._evening_stats
        return self._today_stats

    def record_sale(self, recipe_id: str, price: int, tip: int = 0,
                    satisfaction: float = 3.0):
        """
        Record a dish sale during service.

        Args:
            recipe_id: ID of recipe sold
            price: Sale price
            tip: Tip received
            satisfaction: Customer satisfaction (1-5)
        """
        stats = self._get_current_stats()
        stats.dishes_sold += 1
        stats.revenue += price
        stats.tips += tip
        stats.satisfaction_sum += satisfaction
        stats.satisfaction_count += 1

        # Also update combined today stats
        self._today_stats.dishes_sold += 1
        self._today_stats.revenue += price
        self._today_stats.tips += tip
        self._today_stats.satisfaction_sum += satisfaction
        self._today_stats.satisfaction_count += 1

        # Add to economy
        economy = get_economy()
        economy.add_gold(price, 'sale', f'Sold {recipe_id}')
        if tip > 0:
            economy.add_gold(tip, 'tip', f'Tip for {recipe_id}')

    def record_customer_served(self):
        """Record a customer was served."""
        stats = self._get_current_stats()
        stats.customers_served += 1
        self._today_stats.customers_served += 1

    def get_today_stats(self) -> ServiceStats:
        """Get today's combined service statistics."""
        return self._today_stats

    def get_morning_stats(self) -> ServiceStats:
        """Get morning service statistics."""
        return self._morning_stats

    def get_evening_stats(self) -> ServiceStats:
        """Get evening service statistics."""
        return self._evening_stats

    def get_today_revenue(self) -> int:
        """Get today's total revenue."""
        return self._today_stats.revenue + self._today_stats.tips

    # =========================================================================
    # REPUTATION SYSTEM
    # =========================================================================

    def get_reputation(self) -> int:
        """Get current reputation."""
        return self._reputation

    def add_reputation(self, amount: int) -> Dict[str, Any]:
        """
        Add or remove reputation.

        Args:
            amount: Amount to add (negative to subtract)

        Returns:
            Dict with 'old_level', 'new_level', 'level_changed', 'unlocks'
        """
        old_level = self.get_reputation_level()
        old_rep = self._reputation

        self._reputation = max(REPUTATION_MIN, min(REPUTATION_MAX, self._reputation + amount))

        new_level = self.get_reputation_level()
        level_changed = old_level != new_level
        unlocks = []

        # Check for level up unlocks
        if level_changed and amount > 0:
            unlocks = REPUTATION_UNLOCKS.get(new_level, [])

        return {
            'old_reputation': old_rep,
            'new_reputation': self._reputation,
            'change': self._reputation - old_rep,
            'old_level': old_level,
            'new_level': new_level,
            'level_changed': level_changed,
            'unlocks': unlocks,
        }

    def get_reputation_level(self) -> str:
        """
        Get the current reputation tier.

        Returns:
            One of REPUTATION_LEVEL_* constants
        """
        for level_id, level_data in REPUTATION_LEVELS.items():
            if level_data['min'] <= self._reputation <= level_data['max']:
                return level_id
        return REPUTATION_LEVEL_REGIONAL  # Max level if above all

    def get_reputation_level_name(self) -> str:
        """Get the display name of current reputation level."""
        level = self.get_reputation_level()
        return REPUTATION_LEVELS.get(level, {}).get('name', 'Unknown')

    def get_reputation_progress(self) -> Dict[str, Any]:
        """
        Get reputation progress towards next level.

        Returns:
            Dict with 'current', 'min', 'max', 'progress_percent', 'level_name'
        """
        level = self.get_reputation_level()
        level_data = REPUTATION_LEVELS.get(level, {})
        min_rep = level_data.get('min', 0)
        max_rep = level_data.get('max', REPUTATION_MAX)

        # Progress within current level
        if max_rep > min_rep:
            progress = (self._reputation - min_rep) / (max_rep - min_rep) * 100
        else:
            progress = 100.0

        return {
            'current': self._reputation,
            'level_min': min_rep,
            'level_max': max_rep,
            'progress_percent': min(100.0, progress),
            'level_name': level_data.get('name', 'Unknown'),
            'level_id': level,
        }

    def get_customer_count_range(self) -> tuple:
        """
        Get the customer count range for current reputation level.

        Returns:
            (min_customers, max_customers) tuple
        """
        level = self.get_reputation_level()
        return REPUTATION_CUSTOMER_RANGE.get(level, (1, 2))

    def apply_daily_decay(self, cafe_operated: bool = True) -> Dict[str, Any]:
        """
        Apply daily reputation decay if cafe wasn't operated.

        Args:
            cafe_operated: Whether cafe was operated today

        Returns:
            Result dict from add_reputation
        """
        if cafe_operated:
            return {'change': 0, 'level_changed': False}

        return self.add_reputation(-REPUTATION_DAILY_DECAY)

    # =========================================================================
    # SKIP SERVICE
    # =========================================================================

    def skip_morning_service(self) -> bool:
        """
        Skip morning service (small reputation penalty).

        Returns:
            True if service was skipped
        """
        if self._morning_completed or self._morning_skipped:
            return False  # Already done or skipped

        if self._current_service_period == SERVICE_PERIOD_MORNING and self._state == CAFE_STATE_SERVICE:
            return False  # Can't skip during service

        self._morning_skipped = True
        self.add_reputation(-CAFE_SKIP_SERVICE_PENALTY)
        return True

    def skip_evening_service(self) -> bool:
        """
        Skip evening service (small reputation penalty).

        Returns:
            True if service was skipped
        """
        if self._evening_completed or self._evening_skipped:
            return False  # Already done or skipped

        if self._current_service_period == SERVICE_PERIOD_EVENING and self._state == CAFE_STATE_SERVICE:
            return False  # Can't skip during service

        self._evening_skipped = True
        self.add_reputation(-CAFE_SKIP_SERVICE_PENALTY)
        return True

    def skip_day(self) -> bool:
        """
        Skip entire day's service (larger reputation penalty).

        Returns:
            True if day was skipped
        """
        if self._service_completed:
            return False  # Already completed at least one service

        if self._state == CAFE_STATE_SERVICE:
            return False  # Can't skip during service

        self._morning_skipped = True
        self._evening_skipped = True
        self._day_skipped = True
        self.add_reputation(-CAFE_SKIP_DAY_PENALTY)
        return True

    def was_day_skipped(self) -> bool:
        """Check if entire day was skipped (both services)."""
        return self._morning_skipped and self._evening_skipped

    # =========================================================================
    # DAY MANAGEMENT
    # =========================================================================

    def advance_day(self):
        """Called at the start of a new day."""
        # Reset all daily state
        self._today_stats = ServiceStats()
        self._morning_stats = ServiceStats()
        self._evening_stats = ServiceStats()
        self._morning_completed = False
        self._evening_completed = False
        self._morning_skipped = False
        self._evening_skipped = False
        self._day_skipped = False
        self._service_completed = False
        self._current_service_period = None
        self._state = CAFE_STATE_CLOSED

    def get_next_service_period(self) -> Optional[str]:
        """Get the next upcoming service period."""
        time_mgr = get_time_manager()
        current = time_mgr.current_hour

        # Check if morning service is still available
        if not self._morning_completed and not self._morning_skipped:
            if current < CAFE_MORNING_CLEANUP_END:
                return SERVICE_PERIOD_MORNING

        # Check if evening service is still available
        if not self._evening_completed and not self._evening_skipped:
            if current < CAFE_EVENING_CLEANUP_END:
                return SERVICE_PERIOD_EVENING

        return None  # No more services today

    def get_time_until_service(self) -> float:
        """Get hours until next service starts."""
        time_mgr = get_time_manager()
        current = time_mgr.current_hour

        # Check morning service
        if not self._morning_completed and not self._morning_skipped:
            if current < CAFE_MORNING_SERVICE_START:
                return CAFE_MORNING_SERVICE_START - current
            if current < CAFE_MORNING_SERVICE_END:
                return 0  # In morning service

        # Check evening service
        if not self._evening_completed and not self._evening_skipped:
            if current < CAFE_EVENING_SERVICE_START:
                return CAFE_EVENING_SERVICE_START - current
            if current < CAFE_EVENING_SERVICE_END:
                return 0  # In evening service

        # All services done, time until tomorrow's morning
        return (24 - current) + CAFE_MORNING_SERVICE_START

    def get_time_until_close(self) -> float:
        """Get hours until current service ends (0 if not in service)."""
        time_mgr = get_time_manager()
        current = time_mgr.current_hour

        if self._state != CAFE_STATE_SERVICE:
            return 0

        if self._current_service_period == SERVICE_PERIOD_MORNING:
            return max(0, CAFE_MORNING_SERVICE_END - current)
        elif self._current_service_period == SERVICE_PERIOD_EVENING:
            return max(0, CAFE_EVENING_SERVICE_END - current)

        return 0

    # =========================================================================
    # CALLBACKS
    # =========================================================================

    def on_prep_start(self, callback: Callable):
        """Register callback for prep phase start."""
        self._on_prep_start.append(callback)

    def on_service_start(self, callback: Callable):
        """Register callback for service start."""
        self._on_service_start.append(callback)

    def on_service_end(self, callback: Callable[[ServiceStats], None]):
        """Register callback for service end. Receives ServiceStats."""
        self._on_service_end.append(callback)

    def on_cleanup_end(self, callback: Callable):
        """Register callback for cleanup end."""
        self._on_cleanup_end.append(callback)

    # =========================================================================
    # SERIALIZATION
    # =========================================================================

    def get_save_state(self) -> Dict[str, Any]:
        """Get state for saving."""
        return {
            'state': self._state,
            'current_menu': self._current_menu.copy(),
            'today_stats': self._today_stats.to_dict(),
            'morning_stats': self._morning_stats.to_dict(),
            'evening_stats': self._evening_stats.to_dict(),
            'reputation': self._reputation,
            'day_skipped': self._day_skipped,
            'service_completed': self._service_completed,
            'current_service_period': self._current_service_period,
            'morning_completed': self._morning_completed,
            'evening_completed': self._evening_completed,
            'morning_skipped': self._morning_skipped,
            'evening_skipped': self._evening_skipped,
        }

    def load_state(self, state: Dict[str, Any]):
        """Load state from save data."""
        self._state = state.get('state', CAFE_STATE_CLOSED)
        self._current_menu = state.get('current_menu', [])
        self._reputation = state.get('reputation', 0)
        self._day_skipped = state.get('day_skipped', False)
        self._service_completed = state.get('service_completed', False)

        # Load combined stats
        stats_data = state.get('today_stats', {})
        self._today_stats = ServiceStats.from_dict(stats_data)

        # Load service period stats
        morning_data = state.get('morning_stats', {})
        self._morning_stats = ServiceStats.from_dict(morning_data)
        evening_data = state.get('evening_stats', {})
        self._evening_stats = ServiceStats.from_dict(evening_data)

        # Load service period state
        self._current_service_period = state.get('current_service_period', None)
        self._morning_completed = state.get('morning_completed', False)
        self._evening_completed = state.get('evening_completed', False)
        self._morning_skipped = state.get('morning_skipped', False)
        self._evening_skipped = state.get('evening_skipped', False)


# =============================================================================
# SINGLETON ACCESS
# =============================================================================

_cafe_manager = None


def get_cafe_manager() -> CafeManager:
    """Get the global cafe manager instance."""
    global _cafe_manager
    if _cafe_manager is None:
        _cafe_manager = CafeManager()
    return _cafe_manager


def reset_cafe_manager():
    """Reset the cafe manager (for new game)."""
    global _cafe_manager
    _cafe_manager = CafeManager()
