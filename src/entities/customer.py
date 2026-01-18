"""
Customer System for Dragon Haven Cafe.
Handles customers, orders, patience, satisfaction, and tips.
"""

import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
from uuid import uuid4

from constants import (
    CUSTOMER_TYPE_REGULAR, CUSTOMER_TYPE_STORY,
    CUSTOMER_STATE_WAITING, CUSTOMER_STATE_SEATED, CUSTOMER_STATE_ORDERING,
    CUSTOMER_STATE_WAITING_FOOD, CUSTOMER_STATE_EATING, CUSTOMER_STATE_LEAVING,
    CUSTOMER_PATIENCE_BASE, CUSTOMER_PATIENCE_VARIATION, CUSTOMER_EATING_TIME,
    CUSTOMER_SPAWN_BASE, CUSTOMER_SPAWN_REP_BONUS,
    CUSTOMER_QUALITY_LOW, CUSTOMER_QUALITY_MEDIUM, CUSTOMER_QUALITY_HIGH,
    CUSTOMER_SATISFACTION_ANGRY, CUSTOMER_SATISFACTION_NEUTRAL, CUSTOMER_SATISFACTION_HAPPY,
    SATISFACTION_QUALITY_WEIGHT, SATISFACTION_SPEED_WEIGHT, SATISFACTION_STAFF_WEIGHT,
    REP_CHANGE_ANGRY, REP_CHANGE_NEUTRAL, REP_CHANGE_HAPPY, REP_CHANGE_DELIGHTED,
    ORDER_CATEGORY_APPETIZER, ORDER_CATEGORY_MAIN, ORDER_CATEGORY_DESSERT, ORDER_CATEGORY_DRINK,
    TIP_BASE_PERCENT, TIP_SATISFACTION_BONUS, TIP_MAX_PERCENT
)


@dataclass
class Order:
    """A customer's order."""
    category: str                    # appetizer, main, dessert, drink
    recipe_id: Optional[str] = None  # Specific recipe if they know what they want
    quality_received: float = 0.0    # Quality of dish received (1-5)
    is_fulfilled: bool = False


class Customer:
    """
    A cafe customer who orders food and provides feedback.

    Customers:
    - Have patience that decreases while waiting
    - Order food based on preferences
    - Rate dish quality vs expectations
    - Leave tips based on satisfaction
    - Affect reputation when leaving
    """

    def __init__(self, customer_type: str = CUSTOMER_TYPE_REGULAR,
                 name: str = None, quality_expectation: int = None):
        """
        Initialize a customer.

        Args:
            customer_type: REGULAR or STORY
            name: Display name (generated if None for regulars)
            quality_expectation: Expected dish quality (randomized if None)
        """
        self.id = str(uuid4())[:8]
        self.customer_type = customer_type
        self.name = name or self._generate_name()

        # Quality expectations
        if quality_expectation is None:
            roll = random.random()
            if roll < 0.5:
                self.quality_expectation = CUSTOMER_QUALITY_MEDIUM
            elif roll < 0.8:
                self.quality_expectation = CUSTOMER_QUALITY_LOW
            else:
                self.quality_expectation = CUSTOMER_QUALITY_HIGH
        else:
            self.quality_expectation = quality_expectation

        # Patience
        self.patience_max = CUSTOMER_PATIENCE_BASE + random.uniform(
            -CUSTOMER_PATIENCE_VARIATION, CUSTOMER_PATIENCE_VARIATION
        )
        self.patience_remaining = self.patience_max

        # State
        self._state: str = CUSTOMER_STATE_WAITING
        self._order: Optional[Order] = None
        self._satisfaction: float = 3.0  # Neutral starting point
        self._time_waiting: float = 0.0  # Track wait time for speed bonus
        self._time_eating: float = 0.0

        # Table assignment (for UI)
        self.table_id: Optional[int] = None
        self.seat_id: Optional[int] = None

    def _generate_name(self) -> str:
        """Generate a random customer name."""
        first_names = ['Alex', 'Casey', 'Drew', 'Ellis', 'Flynn', 'Gray',
                       'Harper', 'Jade', 'Kay', 'Lake', 'Morgan', 'Noel',
                       'Parker', 'Quinn', 'River', 'Sage', 'Taylor', 'Val']
        return random.choice(first_names)

    # =========================================================================
    # STATE MANAGEMENT
    # =========================================================================

    @property
    def state(self) -> str:
        """Get current customer state."""
        return self._state

    def is_waiting(self) -> bool:
        """Check if customer is waiting for something."""
        return self._state in [CUSTOMER_STATE_WAITING, CUSTOMER_STATE_SEATED,
                               CUSTOMER_STATE_WAITING_FOOD]

    def is_being_served(self) -> bool:
        """Check if customer is currently being served."""
        return self._state in [CUSTOMER_STATE_ORDERING, CUSTOMER_STATE_EATING]

    def has_left(self) -> bool:
        """Check if customer has left."""
        return self._state == CUSTOMER_STATE_LEAVING

    def get_visual_state(self) -> str:
        """Get visual state for UI."""
        if self._state in [CUSTOMER_STATE_WAITING, CUSTOMER_STATE_SEATED]:
            return 'waiting'
        elif self._state in [CUSTOMER_STATE_ORDERING, CUSTOMER_STATE_WAITING_FOOD]:
            return 'waiting'
        elif self._state == CUSTOMER_STATE_EATING:
            return 'eating'
        else:
            return 'leaving'

    def get_mood(self) -> str:
        """Get current mood based on patience/satisfaction."""
        if self._satisfaction >= CUSTOMER_SATISFACTION_HAPPY:
            return 'happy'
        elif self._satisfaction >= CUSTOMER_SATISFACTION_NEUTRAL:
            return 'neutral'
        else:
            return 'unhappy'

    # =========================================================================
    # SERVICE FLOW
    # =========================================================================

    def seat_at_table(self, table_id: int, seat_id: int = 0):
        """Seat the customer at a table."""
        self.table_id = table_id
        self.seat_id = seat_id
        self._state = CUSTOMER_STATE_SEATED
        self._time_waiting = 0

    def take_order(self, available_recipes: List[str] = None) -> Order:
        """
        Customer places their order.

        Args:
            available_recipes: Menu items available

        Returns:
            The order
        """
        self._state = CUSTOMER_STATE_ORDERING

        # Choose order category (weighted towards mains)
        categories = [ORDER_CATEGORY_MAIN, ORDER_CATEGORY_APPETIZER,
                      ORDER_CATEGORY_DESSERT, ORDER_CATEGORY_DRINK]
        weights = [0.5, 0.2, 0.2, 0.1]
        category = random.choices(categories, weights=weights)[0]

        # Pick a specific recipe if menu is available
        recipe_id = None
        if available_recipes:
            # In a real implementation, would filter by category
            recipe_id = random.choice(available_recipes)

        self._order = Order(category=category, recipe_id=recipe_id)
        self._state = CUSTOMER_STATE_WAITING_FOOD

        return self._order

    def get_order(self) -> Optional[Order]:
        """Get the customer's current order."""
        return self._order

    def serve_dish(self, recipe_id: str, quality: float,
                   staff_efficiency: float = 1.0) -> Dict[str, Any]:
        """
        Serve a dish to the customer.

        Args:
            recipe_id: ID of dish served
            quality: Quality of the dish (1-5)
            staff_efficiency: Efficiency of serving staff

        Returns:
            Result dict with satisfaction, will_tip, etc.
        """
        if self._state != CUSTOMER_STATE_WAITING_FOOD:
            return {'success': False, 'error': 'Customer not waiting for food'}

        if not self._order:
            return {'success': False, 'error': 'No order placed'}

        # Mark order as fulfilled
        self._order.is_fulfilled = True
        self._order.quality_received = quality

        # Calculate satisfaction
        self._satisfaction = self._calculate_satisfaction(
            quality, self._time_waiting, staff_efficiency
        )

        self._state = CUSTOMER_STATE_EATING
        self._time_eating = 0

        return {
            'success': True,
            'satisfaction': self._satisfaction,
            'mood': self.get_mood(),
            'recipe_id': recipe_id
        }

    def _calculate_satisfaction(self, quality: float, wait_time: float,
                                staff_efficiency: float) -> float:
        """
        Calculate customer satisfaction.

        Args:
            quality: Dish quality (1-5)
            wait_time: How long they waited (hours)
            staff_efficiency: Staff service efficiency (0.5-1.2)

        Returns:
            Satisfaction score (1-5)
        """
        # Quality component (how dish compares to expectations)
        quality_diff = quality - self.quality_expectation
        quality_score = 3.0 + quality_diff  # 1-5 based on diff

        # Speed component (faster = better)
        wait_ratio = wait_time / self.patience_max
        if wait_ratio < 0.3:
            speed_score = 5.0  # Fast service
        elif wait_ratio < 0.6:
            speed_score = 4.0  # Good service
        elif wait_ratio < 0.8:
            speed_score = 3.0  # Average
        else:
            speed_score = 2.0  # Slow

        # Staff component
        staff_score = 3.0 + (staff_efficiency - 1.0) * 2  # Normalized around 3

        # Weighted combination
        satisfaction = (
            quality_score * SATISFACTION_QUALITY_WEIGHT +
            speed_score * SATISFACTION_SPEED_WEIGHT +
            staff_score * SATISFACTION_STAFF_WEIGHT
        )

        # Clamp to 1-5
        return max(1.0, min(5.0, satisfaction))

    # =========================================================================
    # LEAVING
    # =========================================================================

    def finish_eating(self) -> Dict[str, Any]:
        """
        Customer finishes eating and prepares to leave.

        Returns:
            Result with tip, reputation change, feedback
        """
        self._state = CUSTOMER_STATE_LEAVING

        # Calculate tip based on satisfaction
        tip = self._calculate_tip()

        # Calculate reputation change
        rep_change = self._get_reputation_change()

        # Generate feedback
        feedback = self._generate_feedback()

        return {
            'tip': tip,
            'reputation_change': rep_change,
            'satisfaction': self._satisfaction,
            'mood': self.get_mood(),
            'feedback': feedback
        }

    def leave_angry(self) -> Dict[str, Any]:
        """
        Customer leaves due to running out of patience.

        Returns:
            Result with no tip, negative reputation
        """
        self._state = CUSTOMER_STATE_LEAVING
        self._satisfaction = 1.0  # Minimum satisfaction

        return {
            'tip': 0,
            'reputation_change': REP_CHANGE_ANGRY,
            'satisfaction': 1.0,
            'mood': 'angry',
            'feedback': f"{self.name} left without being served!"
        }

    def _calculate_tip(self) -> int:
        """Calculate tip amount based on satisfaction."""
        if self._satisfaction < CUSTOMER_SATISFACTION_NEUTRAL:
            return 0

        # Assume a base price for tip calculation
        base_price = 50  # Average dish price

        tip_percent = TIP_BASE_PERCENT
        if self._satisfaction > CUSTOMER_SATISFACTION_NEUTRAL:
            tip_percent += (self._satisfaction - 3) * TIP_SATISFACTION_BONUS

        tip_percent = min(tip_percent, TIP_MAX_PERCENT)

        return int(base_price * tip_percent)

    def _get_reputation_change(self) -> int:
        """Get reputation change based on satisfaction."""
        if self._satisfaction >= 5.0:
            return REP_CHANGE_DELIGHTED
        elif self._satisfaction >= CUSTOMER_SATISFACTION_HAPPY:
            return REP_CHANGE_HAPPY
        elif self._satisfaction >= CUSTOMER_SATISFACTION_NEUTRAL:
            return REP_CHANGE_NEUTRAL
        elif self._satisfaction >= CUSTOMER_SATISFACTION_ANGRY:
            return REP_CHANGE_NEUTRAL
        else:
            return REP_CHANGE_ANGRY

    def _generate_feedback(self) -> str:
        """Generate feedback message based on satisfaction."""
        if self._satisfaction >= 4.5:
            messages = [
                f"{self.name}: 'Absolutely delicious! I'll be back!'",
                f"{self.name}: 'Best meal I've had in ages!'",
                f"{self.name}: 'Simply wonderful!'",
            ]
        elif self._satisfaction >= CUSTOMER_SATISFACTION_HAPPY:
            messages = [
                f"{self.name}: 'Very tasty, thank you!'",
                f"{self.name}: 'That hit the spot!'",
                f"{self.name}: 'Good food, good service.'",
            ]
        elif self._satisfaction >= CUSTOMER_SATISFACTION_NEUTRAL:
            messages = [
                f"{self.name}: 'It was okay.'",
                f"{self.name}: 'Not bad.'",
                f"{self.name}: 'Decent meal.'",
            ]
        else:
            messages = [
                f"{self.name}: 'Not what I expected...'",
                f"{self.name}: 'Could be better.'",
                f"{self.name}: 'Hmm, disappointing.'",
            ]

        return random.choice(messages)

    # =========================================================================
    # UPDATE
    # =========================================================================

    def update(self, dt_hours: float) -> Dict[str, Any]:
        """
        Update customer for time passing.

        Args:
            dt_hours: Time passed in game hours

        Returns:
            Result dict with any events
        """
        result = {
            'patience_depleted': False,
            'finished_eating': False,
        }

        # Update time waiting if in waiting state
        if self._state in [CUSTOMER_STATE_SEATED, CUSTOMER_STATE_WAITING_FOOD]:
            self._time_waiting += dt_hours
            self.patience_remaining -= dt_hours

            # Check if patience ran out
            if self.patience_remaining <= 0:
                result['patience_depleted'] = True
                result['leave_result'] = self.leave_angry()

        # Update eating time
        elif self._state == CUSTOMER_STATE_EATING:
            self._time_eating += dt_hours
            if self._time_eating >= CUSTOMER_EATING_TIME:
                result['finished_eating'] = True
                result['leave_result'] = self.finish_eating()

        return result

    # =========================================================================
    # SERIALIZATION
    # =========================================================================

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            'id': self.id,
            'customer_type': self.customer_type,
            'name': self.name,
            'quality_expectation': self.quality_expectation,
            'patience_max': self.patience_max,
            'patience_remaining': self.patience_remaining,
            'state': self._state,
            'satisfaction': self._satisfaction,
            'time_waiting': self._time_waiting,
            'time_eating': self._time_eating,
            'table_id': self.table_id,
            'seat_id': self.seat_id,
            'order': {
                'category': self._order.category,
                'recipe_id': self._order.recipe_id,
                'quality_received': self._order.quality_received,
                'is_fulfilled': self._order.is_fulfilled
            } if self._order else None
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Customer':
        """Deserialize from dictionary."""
        customer = cls(
            customer_type=data['customer_type'],
            name=data['name'],
            quality_expectation=data['quality_expectation']
        )
        customer.id = data['id']
        customer.patience_max = data['patience_max']
        customer.patience_remaining = data['patience_remaining']
        customer._state = data['state']
        customer._satisfaction = data['satisfaction']
        customer._time_waiting = data['time_waiting']
        customer._time_eating = data['time_eating']
        customer.table_id = data.get('table_id')
        customer.seat_id = data.get('seat_id')

        if data.get('order'):
            customer._order = Order(
                category=data['order']['category'],
                recipe_id=data['order'].get('recipe_id'),
                quality_received=data['order'].get('quality_received', 0),
                is_fulfilled=data['order'].get('is_fulfilled', False)
            )

        return customer


class CustomerManager:
    """
    Manages all customers during cafe service.

    Usage:
        customers = get_customer_manager()
        customers.spawn_customer(reputation=100)
        customer = customers.get_customer(customer_id)
    """

    def __init__(self):
        """Initialize the customer manager."""
        self._customers: Dict[str, Customer] = {}
        self._spawn_timer: float = 0.0

    # =========================================================================
    # SPAWNING
    # =========================================================================

    def spawn_customer(self, reputation: int = 0) -> Customer:
        """
        Spawn a new customer.

        Args:
            reputation: Current cafe reputation (affects spawn rate)

        Returns:
            The new customer
        """
        customer = Customer()
        self._customers[customer.id] = customer
        return customer

    def get_spawn_rate(self, reputation: int) -> float:
        """Get spawn rate based on reputation."""
        return CUSTOMER_SPAWN_BASE * (1 + reputation * CUSTOMER_SPAWN_REP_BONUS)

    def should_spawn(self, reputation: int, dt_hours: float) -> bool:
        """
        Check if a customer should spawn.

        Args:
            reputation: Current reputation
            dt_hours: Time since last check

        Returns:
            True if should spawn
        """
        spawn_rate = self.get_spawn_rate(reputation)
        self._spawn_timer += dt_hours

        # Expected spawns in this period
        expected = spawn_rate * self._spawn_timer

        if expected >= 1.0:
            # Definitely spawn at least one
            self._spawn_timer = 0
            return True
        elif random.random() < expected:
            # Probabilistic spawn
            self._spawn_timer = 0
            return True

        return False

    # =========================================================================
    # CUSTOMER ACCESS
    # =========================================================================

    def get_customer(self, customer_id: str) -> Optional[Customer]:
        """Get a customer by ID."""
        return self._customers.get(customer_id)

    def get_all_customers(self) -> List[Customer]:
        """Get all active customers."""
        return list(self._customers.values())

    def get_customers_in_state(self, state: str) -> List[Customer]:
        """Get customers in a specific state."""
        return [c for c in self._customers.values() if c.state == state]

    def get_waiting_customers(self) -> List[Customer]:
        """Get customers waiting for service."""
        return [c for c in self._customers.values() if c.is_waiting()]

    def remove_customer(self, customer_id: str):
        """Remove a customer who has left."""
        if customer_id in self._customers:
            del self._customers[customer_id]

    def clear_all(self):
        """Remove all customers (end of service)."""
        self._customers.clear()
        self._spawn_timer = 0.0

    # =========================================================================
    # UPDATES
    # =========================================================================

    def update(self, dt_hours: float) -> List[Dict[str, Any]]:
        """
        Update all customers.

        Returns:
            List of events from customer updates
        """
        events = []
        customers_to_remove = []

        for customer_id, customer in self._customers.items():
            result = customer.update(dt_hours)

            if result['patience_depleted'] or result['finished_eating']:
                result['customer_id'] = customer_id
                result['customer_name'] = customer.name
                events.append(result)

                if customer.has_left():
                    customers_to_remove.append(customer_id)

        # Remove customers who left
        for cid in customers_to_remove:
            self.remove_customer(cid)

        return events

    # =========================================================================
    # SERIALIZATION
    # =========================================================================

    def get_state(self) -> Dict[str, Any]:
        """Get state for saving."""
        return {
            'customers': {
                cid: c.to_dict()
                for cid, c in self._customers.items()
            },
            'spawn_timer': self._spawn_timer
        }

    def load_state(self, state: Dict[str, Any]):
        """Load state from save data."""
        self._customers.clear()
        self._spawn_timer = state.get('spawn_timer', 0.0)

        for cid, c_data in state.get('customers', {}).items():
            self._customers[cid] = Customer.from_dict(c_data)


# =============================================================================
# SINGLETON ACCESS
# =============================================================================

_customer_manager = None


def get_customer_manager() -> CustomerManager:
    """Get the global customer manager instance."""
    global _customer_manager
    if _customer_manager is None:
        _customer_manager = CustomerManager()
    return _customer_manager


def reset_customer_manager():
    """Reset the customer manager (for new game/service)."""
    global _customer_manager
    _customer_manager = CustomerManager()
