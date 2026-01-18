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
    CAFE_MAX_MENU_ITEMS, CAFE_SKIP_REP_PENALTY
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
        self._today_stats: ServiceStats = ServiceStats()
        self._reputation: int = 0

        # Day tracking
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
        # Calculate state transitions based on time
        prep_start = CAFE_SERVICE_START - CAFE_PREP_DURATION
        service_start = CAFE_SERVICE_START
        service_end = CAFE_SERVICE_END
        cleanup_end = CAFE_SERVICE_END + CAFE_CLEANUP_DURATION

        old_state = self._state

        if self._day_skipped:
            # If day was skipped, stay closed
            self._state = CAFE_STATE_CLOSED
        elif prep_start <= current_hour < service_start:
            self._state = CAFE_STATE_PREP
        elif service_start <= current_hour < service_end:
            self._state = CAFE_STATE_SERVICE
        elif service_end <= current_hour < cleanup_end:
            self._state = CAFE_STATE_CLEANUP
        else:
            self._state = CAFE_STATE_CLOSED

        # Fire callbacks on state changes
        if old_state != self._state:
            self._on_state_change(old_state, self._state)

    def _on_state_change(self, old_state: str, new_state: str):
        """Handle state transitions."""
        if new_state == CAFE_STATE_PREP:
            for cb in self._on_prep_start:
                cb()

        elif new_state == CAFE_STATE_SERVICE and old_state == CAFE_STATE_PREP:
            for cb in self._on_service_start:
                cb()

        elif new_state == CAFE_STATE_CLEANUP and old_state == CAFE_STATE_SERVICE:
            self._service_completed = True
            for cb in self._on_service_end:
                cb(self._today_stats)

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
    # SERVICE TRACKING
    # =========================================================================

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
        self._today_stats.customers_served += 1

    def get_today_stats(self) -> ServiceStats:
        """Get today's service statistics."""
        return self._today_stats

    def get_today_revenue(self) -> int:
        """Get today's total revenue."""
        return self._today_stats.revenue + self._today_stats.tips

    # =========================================================================
    # REPUTATION
    # =========================================================================

    def get_reputation(self) -> int:
        """Get current reputation."""
        return self._reputation

    def add_reputation(self, amount: int):
        """Add or remove reputation."""
        self._reputation = max(0, self._reputation + amount)

    # =========================================================================
    # SKIP DAY
    # =========================================================================

    def skip_day(self) -> bool:
        """
        Skip today's service (reputation penalty).

        Returns:
            True if day was skipped
        """
        if self._service_completed:
            return False  # Already completed service

        if self._state == CAFE_STATE_SERVICE:
            return False  # Can't skip during service

        self._day_skipped = True
        self.add_reputation(-CAFE_SKIP_REP_PENALTY)
        return True

    def was_day_skipped(self) -> bool:
        """Check if today was skipped."""
        return self._day_skipped

    # =========================================================================
    # DAY MANAGEMENT
    # =========================================================================

    def advance_day(self):
        """Called at the start of a new day."""
        # Reset daily state
        self._today_stats = ServiceStats()
        self._day_skipped = False
        self._service_completed = False
        self._state = CAFE_STATE_CLOSED

        # Reputation bonus for completing service
        # (handled by end_service callback typically)

    def get_time_until_service(self) -> float:
        """Get hours until service starts."""
        time_mgr = get_time_manager()
        current = time_mgr.current_hour

        if current >= CAFE_SERVICE_END:
            # Service already passed today
            return (24 - current) + CAFE_SERVICE_START

        if current < CAFE_SERVICE_START:
            return CAFE_SERVICE_START - current

        return 0  # Already in or past service

    def get_time_until_close(self) -> float:
        """Get hours until service ends (0 if not in service)."""
        time_mgr = get_time_manager()
        current = time_mgr.current_hour

        if self._state != CAFE_STATE_SERVICE:
            return 0

        return max(0, CAFE_SERVICE_END - current)

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
            'reputation': self._reputation,
            'day_skipped': self._day_skipped,
            'service_completed': self._service_completed
        }

    def load_state(self, state: Dict[str, Any]):
        """Load state from save data."""
        self._state = state.get('state', CAFE_STATE_CLOSED)
        self._current_menu = state.get('current_menu', [])
        self._reputation = state.get('reputation', 0)
        self._day_skipped = state.get('day_skipped', False)
        self._service_completed = state.get('service_completed', False)

        stats_data = state.get('today_stats', {})
        self._today_stats = ServiceStats.from_dict(stats_data)


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
